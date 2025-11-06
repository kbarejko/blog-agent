"""
Step 14: Assign Categories

AI analyzes article and selects 1-5 categories from categories.yaml.
"""
from typing import Dict, Any

from ...domain.article import Article


def execute_categories(
    article: Article,
    deps: Dict[str, Any],
    config: Dict[str, Any]
) -> Article:
    """
    Assign categories to article

    AI analyzes article content and selects 1-5 best matching categories
    from categories.yaml (146 categories).

    Args:
        article: Article (must be published)
        deps: Dependencies (ai, prompts, storage, git, category_matcher)
        config: Step configuration

    Returns:
        Article with categories assigned
    """
    if not article.final_content:
        raise ValueError("Final content must exist before category assignment")

    ai = deps['ai']
    prompts = deps['prompts']
    storage = deps['storage']
    git = deps['git']
    category_matcher = deps['category_matcher']

    print("🔄 Assigning categories...")

    # Get categories formatted for AI
    categories_list = category_matcher.get_categories_for_prompt()

    # Load and render prompt
    # Note: We'd need to create a categories prompt or use existing audyt prompt
    prompt = f"""Przeanalizuj poniższy artykuł i wybierz 1-5 najbardziej pasujących kategorii.

ARTYKUŁ:
Tytuł: {article.config.title}

{article.final_content[:2000]}  # First 2000 chars for context

{categories_list}

INSTRUKCJA:
Wybierz 1-5 kategorii, które najlepiej pasują do tematu artykułu.
Zwróć tylko slugi kategorii, po jednym w linii, np:
ecommerce-platform
bezpieczenstwo-it
rodo

WYBRANE KATEGORIE:
"""

    # Generate category selection
    response = ai.generate(prompt, max_tokens=200)

    # Parse category slugs
    selected_slugs = []
    for line in response.strip().split('\n'):
        line = line.strip()
        if line and not line.startswith('#') and not line.startswith('-'):
            # Clean up (remove bullets, numbers)
            slug = line.replace('-', '-').replace('*', '').replace('•', '').strip()
            if slug:
                selected_slugs.append(slug)

    # Validate categories
    validation = category_matcher.validate_category_selection(selected_slugs)

    if not validation['valid']:
        print(f"   ⚠️  Category validation issues:")
        for issue in validation['issues']:
            print(f"      - {issue}")

        # Use only valid slugs
        selected_slugs = validation['valid_slugs'][:5]  # Max 5

    if not selected_slugs:
        raise ValueError("No valid categories selected")

    # Set categories on article
    article.set_categories(selected_slugs)

    # Get category details for saving
    categories_data = category_matcher.format_categories_for_yaml(selected_slugs)

    # Save to categories.yaml
    categories_path = article.get_categories_path()
    storage.write_yaml(categories_path, categories_data)

    print(f"✅ Categories assigned: {len(selected_slugs)}")
    for slug in selected_slugs:
        cat = category_matcher.get_category_details([slug])[0]
        print(f"   - {cat['title']} ({slug})")

    # Git commit
    series, silo, slug_path = article.get_series_silo_slug()
    git.commit_article_stage(
        article.path,
        "categories",
        f"Assign categories ({len(selected_slugs)} categories)"
    )

    return article
