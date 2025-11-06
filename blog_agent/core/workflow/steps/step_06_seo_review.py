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
    prompt = prompts.load_and_render(
        "audyt/prompt_sprawdz_naglowki.md",
        {
            'ARTICLE_CONTENT': article.draft_content,
            'TYTUL_ARTYKULU': article.config.title,
        }
    )

    response = ai.generate(prompt, max_tokens=300)

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

    prompt = f"""Popraw hierarchię nagłówków w poniższym artykule.

PROBLEMY DO NAPRAWIENIA:
{issues_text}

ZASADY:
- Pierwszy nagłówek musi być H1 (#)
- Nie przeskakuj poziomów (np. H2 -> H4)
- Zachowaj treść bez zmian, popraw tylko nagłówki

ARTYKUŁ:

{article.draft_content}

POPRAWIONY ARTYKUŁ:
"""

    fixed_content = ai.generate(prompt, max_tokens=4000)
    return fixed_content


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
