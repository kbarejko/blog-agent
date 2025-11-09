"""
Step 11: CTA/Next Steps

Generates "Co dalej?" section with actionable next steps.
"""
from typing import Dict, Any

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
            'RELATED_ARTICLES': '',  # Placeholder - will be populated by internal linking step
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

    # Determine variant (simplified - AI should specify in response)
    variant = 'practical'  # Default

    # Create CTA section
    cta_section = CTASection(
        variant=variant,
        content=response
    )

    article.set_cta_section(cta_section)

    # Add CTA to final content
    article.add_cta_to_final()

    # Save updated article.md
    article_path = article.get_article_path()
    storage.write_file(article_path, article.final_content)

    print(f"✅ CTA section added (variant: {variant})")

    return article
