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

    # Generate meta title and description
    # Limit content length to avoid API errors - use first 30000 chars for context
    content_for_seo = article.draft_content[:30000] if len(article.draft_content) > 30000 else article.draft_content
    
    try:
        prompt = prompts.load_and_render(
            "audyt/prompt_sprawdz_naglowki.md",
            {
                'ARTICLE_CONTENT': content_for_seo,
                'TYTUL_ARTYKULU': article.config.title,
            }
        )

        response = ai.generate(prompt, max_tokens=300)
    except Exception as e:
        print(f"   ⚠️  Could not generate SEO data: {str(e)}")
        print("   Using fallback SEO data")
        # Use fallback SEO data
        seo_data = SEOData(
            meta_title=article.config.title[:60],
            meta_description=f"Dowiedz się więcej o: {article.config.title}"[:160]
        )
        article.set_seo_data(seo_data)
        article.config.save(article.get_config_path())
        return article

    # Parse SEO data from response
    seo_data = _parse_seo_data(response, article.config.title)

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

    for line in lines:
        line = line.strip()

        if line.lower().startswith('meta title:') or line.lower().startswith('meta-title:'):
            meta_title = line.split(':', 1)[1].strip()

        if line.lower().startswith('meta description:') or line.lower().startswith('meta-description:'):
            meta_description = line.split(':', 1)[1].strip()

    # Fallbacks
    if not meta_title:
        meta_title = fallback_title[:60]  # Truncate to 60 chars

    if not meta_description:
        meta_description = f"Dowiedz się więcej o: {fallback_title}"[:160]

    return SEOData(
        meta_title=meta_title,
        meta_description=meta_description
    )
