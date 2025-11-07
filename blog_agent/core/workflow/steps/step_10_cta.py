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
    if article.business_metadata:
        business_context = f"""Investment: {article.business_metadata.investment_level} ({article.business_metadata.investment_range})
Timeline: {article.business_metadata.timeline_estimate}
Team: {article.business_metadata.team_size}"""

    # Extract series and silo from article path
    # Path structure: artykuly/[series]/[silo]/[slug]/
    path_parts = article.path.parts
    series = path_parts[1] if len(path_parts) > 1 else "unknown"
    silo = path_parts[2] if len(path_parts) > 2 else "unknown"

    # Load and render prompt
    prompt = prompts.load_and_render(
        "articles/prompt_cta_next_steps.md",
        {
            'TYTUL_ARTYKULU': article.config.title,
            'ARTICLE_CONTENT': article.final_content,
            'BUSINESS_METADATA': business_context,
            'SERIA': series,
            'SILOS': silo,
        }
    )

    # Generate CTA
    response = ai.generate(prompt, max_tokens=1000)

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
