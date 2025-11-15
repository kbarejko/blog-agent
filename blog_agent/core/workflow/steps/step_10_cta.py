"""
Step 11: CTA/Next Steps

Generates "Co dalej?" section with actionable next steps.
"""
from typing import Dict, Any, List
from pathlib import Path
import yaml

from ...domain.article import Article
from ...domain.value_objects import CTASection


def execute_cta(
    article: Article,
    deps: Dict[str, Any],
    config: Dict[str, Any]
) -> Article:
    """
    Generate CTA/Next Steps section

    Creates "Co dalej?" section with:
    - First steps
    - Useful tools
    - Self-assessment (for theoretical articles)
    - CTA for consultation

    Variant selected by AI:
    - practical: Implementation-focused
    - theoretical: Strategic/educational
    - optimization: Improvement-focused

    Args:
        article: Article (must have final content and business metadata)
        deps: Dependencies (ai, prompts, storage)
        config: Step configuration

    Returns:
        Article with CTA section added to final content
    """
    if not article.final_content:
        raise ValueError("Final content must exist before CTA")

    ai = deps['ai']
    prompts = deps['prompts']
    storage = deps['storage']

    print("🔄 Generating CTA/Next Steps...")

    # Prepare business metadata context
    business_context = ""
    investment_range = ""
    timeframe = ""
    optional_warning = ""
    optional_note = ""

    if article.business_metadata:
        business_context = f"""Investment: {article.business_metadata.investment_level} ({article.business_metadata.investment_range})
Timeline: {article.business_metadata.timeline_estimate}
Team: {article.business_metadata.team_size}"""
        investment_range = article.business_metadata.investment_range
        timeframe = article.business_metadata.timeline_estimate

        # Generate optional warning for high complexity
        if article.business_metadata.complexity_technical == "high" or article.business_metadata.investment_level == "high":
            optional_warning = f"⚠️ **Ważne:** {article.config.title} to złożone wdrożenie wymagające doświadczonego zespołu. Zalecamy konsultację z ekspertem przed podjęciem decyzji."

        # Generate optional note for high organizational complexity
        if article.business_metadata.complexity_organizational == "high":
            optional_note = f"💡 **Wskazówka:** Sukces wdrożenia to w 70% change management, a w 30% technologia. Zadbaj o komunikację i szkolenia od pierwszego dnia."

    # Extract series and silo from article path
    # Path structure: artykuly/[series]/[silo]/[slug]/
    path_parts = article.path.parts
    series = path_parts[1] if len(path_parts) > 1 else "unknown"
    silo = path_parts[2] if len(path_parts) > 2 else "unknown"

    # Find related articles in the same silo
    current_slug = path_parts[-1] if len(path_parts) > 0 else "unknown"
    silo_articles = _find_silo_articles(article.path, current_slug)

    # Format silo articles for prompt (prioritize silo articles)
    related_articles_text = ""
    if silo_articles:
        related_articles_text = "**Artykuły z tego samego silosu tematycznego:**\n"
        for art in silo_articles[:5]:  # Limit to 5 articles
            related_articles_text += f"- [{art['title']}]({art['url']})\n"

    # Generate checklist name from article title
    checklist_name = f"{article.config.title} - Checklist"

    # Topic is the article title
    topic = article.config.title

    # Load and render prompt
    prompt = prompts.load_and_render(
        "articles/prompt_cta_next_steps.md",
        {
            # INPUT variables (provided by system)
            'TYTUL_ARTYKULU': article.config.title,
            'ARTICLE_CONTENT': article.final_content,
            'BUSINESS_METADATA': business_context,
            'SERIA': series,
            'SILOS': silo,
            'CHECKLIST_NAME': checklist_name,
            'RELATED_ARTICLES': related_articles_text,
            'INVESTMENT_RANGE': investment_range,
            'TIMEFRAME': timeframe,
            'TOPIC': topic,
            'OPTIONAL_WARNING': optional_warning,
            'OPTIONAL_NOTE': optional_note,

            # OUTPUT variables (placeholders for AI to fill in response)
            'AUDIT_LINK': '{{LINK}}',
            'AUDIT_PRICE': '{{PRICE}}',
            'AUDIT_TOOL_LINK': '{{LINK}}',
            'AUDIT_TOOL_NAME': '',
            'CHECKLIST_LINK': '{{LINK}}',
            'CONSULTATION_LINK': '{{LINK}}',
            'IMPLEMENTATION_LINK': '{{LINK}}',
            'LINK': '{{LINK}}',
            'NEWSLETTER_LINK': '{{LINK}}',
            'RECOMMENDATION': '',
            'RELATED_ARTICLES_LIST': '',
            'RFP_TEMPLATE_LINK': '{{LINK}}',
            'SURVEY_LINK': '{{LINK}}',
            'WEBINAR_LINK': '{{LINK}}',
        }
    )

    # Generate CTA
    response = ai.generate(prompt, max_tokens=3000)

    # Clean response - remove ```markdown wrapper if present
    cleaned_response = response.strip()
    if cleaned_response.startswith('```markdown'):
        # Remove opening ```markdown
        cleaned_response = cleaned_response[len('```markdown'):].lstrip()
    if cleaned_response.startswith('```'):
        # Remove opening ``` (without markdown keyword)
        cleaned_response = cleaned_response[3:].lstrip()
    if cleaned_response.endswith('```'):
        # Remove closing ```
        cleaned_response = cleaned_response[:-3].rstrip()

    cleaned_response = cleaned_response.strip()

    # Determine variant (simplified - AI should specify in response)
    variant = 'practical'  # Default

    # Create CTA section
    cta_section = CTASection(
        variant=variant,
        content=cleaned_response
    )

    article.set_cta_section(cta_section)

    # Save CTA to separate file (cta.md)
    cta_path = article.path / 'cta.md'
    storage.write_file(cta_path, cleaned_response)

    print(f"✅ CTA section saved to cta.md (variant: {variant})")

    return article


def _find_silo_articles(article_path: Path, current_slug: str) -> List[Dict[str, str]]:
    """
    Find all published articles in the same silo

    Args:
        article_path: Path to current article directory
        current_slug: Current article slug to exclude

    Returns:
        List of article metadata dicts with title and url
    """
    articles = []

    # Get silo path (parent directory)
    silo_path = article_path.parent

    # Scan all subdirectories in the silo
    for article_dir in silo_path.iterdir():
        if not article_dir.is_dir():
            continue

        slug = article_dir.name
        if slug == current_slug:
            continue  # Skip current article

        # Check if article is published
        article_md = article_dir / "article.md"
        if not article_md.exists():
            continue  # Not published yet

        # Load config to get title
        config_path = article_dir / "config.yaml"
        if not config_path.exists():
            continue

        with open(config_path, 'r', encoding='utf-8') as f:
            config = yaml.safe_load(f)

        # Build full URL path from "artykuly/" onwards
        parts = article_dir.parts
        try:
            artykuly_idx = parts.index('artykuly')
            relative_parts = parts[artykuly_idx:]
            url = '/' + '/'.join(relative_parts)
        except ValueError:
            # Fallback if "artykuly" not found in path
            url = f"/{'/'.join(article_dir.parts[-3:])}"

        articles.append({
            'slug': slug,
            'title': config.get('title', slug),
            'url': url
        })

    return articles
