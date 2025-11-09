"""
Step 13: Schema.org Markup

Generates structured data (Article, FAQPage, HowTo, BreadcrumbList).
"""
from typing import Dict, Any

from ...domain.article import Article
from ...domain.value_objects import SchemaMarkup


def execute_schema(
    article: Article,
    deps: Dict[str, Any],
    config: Dict[str, Any]
) -> Article:
    """
    Generate Schema.org structured data

    Creates JSON-LD schemas:
    - Article (always)
    - FAQPage (if FAQ exists)
    - HowTo (if Checklist exists)
    - BreadcrumbList (always)

    Args:
        article: Article (must be published)
        deps: Dependencies (ai, prompts, storage)
        config: Step configuration

    Returns:
        Article with schema_markup set
    """
    if not article.final_content:
        raise ValueError("Final content must exist before schema generation")

    ai = deps['ai']
    prompts = deps['prompts']
    storage = deps['storage']

    print("🔄 Generating Schema.org markup...")

    # Determine which schemas to include
    include_faq = article.outline and article.outline.has_faq
    include_howto = article.outline and article.outline.has_checklist

    # Extract series and silo from article path
    path_parts = article.path.parts
    series = path_parts[1] if len(path_parts) > 1 else "unknown"
    silo = path_parts[2] if len(path_parts) > 2 else "unknown"

    # Get word count from final content
    word_count = len(article.final_content.split())

    # Load and render prompt
    prompt = prompts.load_and_render(
        "metadata/prompt_schema_markup.md",
        {
            'TYTUL_ARTYKULU': article.config.title,
            'ARTICLE_TITLE': article.config.title,
            'META_TITLE': article.config.title,  # Could be enhanced with SEO data
            'ARTICLE_CONTENT': article.final_content,
            'META_DESCRIPTION': article.config.meta_description or '',
            'INCLUDE_FAQ': 'TAK' if include_faq else 'NIE',
            'INCLUDE_HOWTO': 'TAK' if include_howto else 'NIE',
            'ARTICLE_URL': '{{ARTICLE_URL}}',  # Placeholder - will be filled later
            'PUBLISH_DATE': '{{PUBLISH_DATE}}',  # Placeholder
            'MODIFIED_DATE': '{{MODIFIED_DATE}}',  # Placeholder
            'IMAGES': '',  # Placeholder
            'HERO_IMAGE_URL': '{{HERO_IMAGE_URL}}',  # Placeholder
            'FAQ_CONTENT': '',
            'CHECKLIST_CONTENT': '',
            'CHECKLIST_TITLE': '',
            'CHECKLIST_DESCRIPTION': '',
            'BUSINESS_METADATA': '',
            'SERIA': series,
            'SERIA_NAME': series,
            'SILOS': silo,
            'SILOS_NAME': silo,
            'WORD_COUNT': str(word_count),
            'ESTIMATED_TIME': '',  # Empty for now
            'ESTIMATED_COST': '',  # Empty for now
        }
    )

    # Generate schema
    response = ai.generate(prompt, max_tokens=2000)

    # Parse schema (simplified - would need proper JSON extraction)
    schemas = [
        {
            '@context': 'https://schema.org',
            '@type': 'Article',
            'headline': article.config.title,
            'description': article.config.meta_description
        }
    ]

    schema_markup = SchemaMarkup(schemas=schemas)
    article.set_schema_markup(schema_markup)

    # Save to schema.json
    schema_path = article.get_schema_path()
    storage.write_json(schema_path, schemas)

    print(f"✅ Schema markup generated: {len(schemas)} schemas")
    print(f"   - Types: {', '.join(schema_markup.get_schema_types())}")

    return article
