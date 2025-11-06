"""
Step 7: SEO Review

Reviews heading structure and fixes issues automatically.
"""
from typing import Dict, Any

from ...domain.article import Article
from ...domain.value_objects import SEOData


def execute_seo_review(
    article: Article,
    deps: Dict[str, Any],
    config: Dict[str, Any]
) -> Article:
    """
    SEO review of article

    Checks:
    - Heading hierarchy (H1 -> H2 -> H3, no jumps)
    - Meta title and description
    - Auto-fixes heading issues if found

    Args:
        article: Article (must have draft)
        deps: Dependencies (ai, prompts, storage, review)
        config: Step configuration

    Returns:
        Article with SEO data set
    """
    if not article.draft_content:
        raise ValueError("Draft must exist before SEO review")

    ai = deps['ai']
    prompts = deps['prompts']
    storage = deps['storage']
    review = deps['review']

    print("🔄 SEO review...")

    # Check heading structure
    headings = review.check_headings(article.draft_content)
    heading_issues = review.validate_heading_structure(headings)

    if heading_issues:
        print(f"   ⚠️  Heading issues found: {len(heading_issues)}")
        for issue in heading_issues:
            print(f"      - {issue}")

        # Auto-fix headings with AI
        print("   🔧 Auto-fixing headings...")
        fixed_content = _fix_headings_with_ai(article, deps, heading_issues)

        # Update draft
        article.draft_content = fixed_content
        storage.write_file(article.get_draft_path(), fixed_content)

        print("   ✅ Headings fixed")
    else:
        print("   ✅ Heading structure valid")

    # Generate meta title and description with retry logic
    # Limit content length to avoid API errors - use first 30000 chars for context
    content_for_seo = article.draft_content[:30000] if len(article.draft_content) > 30000 else article.draft_content
    
    seo_data = None
    max_retries = 3
    
    for attempt in range(max_retries):
        try:
            prompt = prompts.load_and_render(
                "audyt/prompt_sprawdz_naglowki.md",
                {
                    'ARTICLE_CONTENT': content_for_seo,
                    'TYTUL_ARTYKULU': article.config.title,
                }
            )
            
            # Add explicit instructions for retry
            if attempt > 0:
                prompt += f"\n\nUWAGA: Meta description musi mieć MINIMUM 120 znaków i MAKSIMUM 160 znaków. Poprzednia próba zwróciła za krótki opis."

            response = ai.generate(prompt, max_tokens=300)
            
            # Parse SEO data from response
            seo_data = _parse_seo_data(response, article.config.title)
            
            # Validate SEO data
            issues = seo_data.validate()
            if not issues:
                # Valid SEO data
                break
            else:
                if attempt < max_retries - 1:
                    print(f"   ⚠️  SEO data validation failed (attempt {attempt + 1}/{max_retries}): {', '.join(issues)}")
                    print("   Retrying with improved prompt...")
                else:
                    print(f"   ⚠️  Max retries reached. SEO data has issues: {', '.join(issues)}")
                    # Use fallback if last attempt
                    seo_data = _create_fallback_seo_data(article.config.title, content_for_seo)
                    
        except Exception as e:
            if attempt < max_retries - 1:
                print(f"   ⚠️  Error generating SEO data (attempt {attempt + 1}/{max_retries}): {str(e)}")
                print("   Retrying...")
            else:
                print(f"   ⚠️  Could not generate SEO data after {max_retries} attempts: {str(e)}")
                print("   Using fallback SEO data")
                seo_data = _create_fallback_seo_data(article.config.title, content_for_seo)
                break

    # Set SEO data on article
    article.set_seo_data(seo_data)

    print(f"✅ SEO data generated:")
    print(f"   - Meta title: {seo_data.meta_title}")
    print(f"   - Meta description: {seo_data.meta_description[:50]}...")

    # Update config.yaml with SEO data
    article.config.save(article.get_config_path())

    return article


def _fix_headings_with_ai(
    article: Article,
    deps: Dict[str, Any],
    issues: list[str]
) -> str:
    """
    Fix heading issues with AI

    Args:
        article: Article
        deps: Dependencies
        issues: List of heading issues

    Returns:
        Fixed content
    """
    ai = deps['ai']
    prompts = deps['prompts']

    issues_text = "\n".join([f"- {issue}" for issue in issues])

    # Limit content length to avoid API errors (max ~200K tokens for Claude)
    # Keep first 50000 chars to ensure we have enough context
    content_preview = article.draft_content[:50000] if len(article.draft_content) > 50000 else article.draft_content
    
    prompt = f"""Popraw hierarchię nagłówków w poniższym artykule.

PROBLEMY DO NAPRAWIENIA:
{issues_text}

ZASADY:
- Pierwszy nagłówek musi być H1 (#)
- Nie przeskakuj poziomów (np. H2 -> H4)
- Zachowaj treść bez zmian, popraw tylko nagłówki
- Zachowaj całą strukturę i formatowanie markdown

ARTYKUŁ:

{content_preview}

POPRAWIONY ARTYKUŁ (zachowaj całą treść, popraw tylko nagłówki):
"""

    try:
        # Use larger max_tokens for full article, but cap at reasonable limit
        content_length = len(article.draft_content)
        estimated_tokens = content_length // 4  # Rough estimate
        max_output_tokens = min(estimated_tokens + 1000, 8000)  # Cap at 8K tokens
        
        fixed_content = ai.generate(prompt, max_tokens=max_output_tokens)
        return fixed_content
    except Exception as e:
        # If AI fix fails, return original content with warning
        print(f"   ⚠️  Could not auto-fix headings: {str(e)}")
        print("   Returning original content")
        return article.draft_content


def _parse_seo_data(response: str, fallback_title: str) -> SEOData:
    """
    Parse SEO data from AI response

    Expected format:
    Meta title: ...
    Meta description: ...

    Args:
        response: AI response
        fallback_title: Fallback title if parsing fails

    Returns:
        SEOData value object
    """
    lines = response.split('\n')

    meta_title = None
    meta_description = None
    collecting_description = False
    description_lines = []

    for line in lines:
        line_stripped = line.strip()

        # Check for meta title
        if line_stripped.lower().startswith('meta title:') or line_stripped.lower().startswith('meta-title:'):
            meta_title = line_stripped.split(':', 1)[1].strip()
            collecting_description = False
            continue

        # Check for meta description start
        if line_stripped.lower().startswith('meta description:') or line_stripped.lower().startswith('meta-description:'):
            # Get text after colon
            desc_part = line_stripped.split(':', 1)[1].strip()
            if desc_part:
                description_lines = [desc_part]
            collecting_description = True
            continue

        # Collect multi-line description
        if collecting_description:
            if line_stripped and not line_stripped.lower().startswith('meta'):
                description_lines.append(line_stripped)
            else:
                collecting_description = False

    # Join description lines
    if description_lines:
        meta_description = ' '.join(description_lines).strip()

    # Fallbacks
    if not meta_title:
        meta_title = fallback_title[:60]  # Truncate to 60 chars

    if not meta_description or len(meta_description) < 120:
        # Generate longer fallback description
        meta_description = _create_fallback_seo_data(fallback_title, "").meta_description

    return SEOData(
        meta_title=meta_title,
        meta_description=meta_description
    )


def _create_fallback_seo_data(title: str, content: str) -> SEOData:
    """
    Create fallback SEO data with proper length
    
    Args:
        title: Article title
        content: Article content (optional, for better description)
    
    Returns:
        SEOData with valid meta description (120-160 chars)
    """
    # Create a longer, more descriptive fallback
    base_desc = f"Dowiedz się więcej o {title}. Praktyczny przewodnik z konkretnymi wskazówkami i przykładami."
    
    # If content available, try to extract first sentence or key phrase
    if content:
        # Try to find first meaningful sentence (skip headers)
        lines = content.split('\n')
        for line in lines[:20]:  # Check first 20 lines
            line = line.strip()
            if line and not line.startswith('#') and len(line) > 50:
                # Use first sentence or first 100 chars
                sentence = line.split('.')[0] if '.' in line else line[:100]
                if len(sentence) > 50:
                    base_desc = f"{sentence}. {title} - praktyczny przewodnik."
                    break
    
    # Ensure proper length (120-160 chars)
    if len(base_desc) < 120:
        # Pad with more descriptive text
        base_desc = f"{base_desc} Poznaj najlepsze praktyki i unikaj typowych błędów."
    
    # Truncate to max 160
    meta_description = base_desc[:160]
    
    # If still too short, add more
    if len(meta_description) < 120:
        meta_description = f"{meta_description} Sprawdź nasz kompleksowy przewodnik."[:160]
    
    return SEOData(
        meta_title=title[:60],
        meta_description=meta_description
    )
