"""
Step 18: Generate Checklist

Generates checklist section with humanization.
Pipeline: generate → humanize as a whole → save
"""
from typing import Dict, Any

from ...domain.article import Article


def execute_checklist(
    article: Article,
    deps: Dict[str, Any],
    config: Dict[str, Any]
) -> Article:
    """
    Generate and humanize Checklist section

    Pipeline:
    1. Generate checklist from outline
    2. Humanize entire checklist
    3. Save to checklist.md

    Args:
        article: Article (must have outline)
        deps: Dependencies (ai, prompts, storage)
        config: Step configuration

    Returns:
        Article with checklist generated
    """
    if not article.outline:
        raise ValueError("Outline must exist before generating Checklist")

    ai = deps['ai']
    prompts = deps['prompts']
    storage = deps['storage']

    # Step 1: Generate checklist
    print("🔄 Generating Checklist...")
    prompt = prompts.load_and_render(
        "checklist/prompt_checklist.md",
        {
            'TYTUL_ARTYKULU': article.config.title,
            'KONSPEKT_TRESC': article.outline.to_markdown(),
            'TARGET_AUDIENCE': article.config.target_audience,
        }
    )
    checklist_draft = ai.generate(prompt, max_tokens=1500)

    # Count items
    checklist_lines = checklist_draft.strip().split('\n')
    item_count = sum(1 for line in checklist_lines if line.strip().startswith('- [ ]'))

    if item_count == 0:
        print("   ⚠️  No checklist items found - saving draft as-is")
        checklist_path = article.path / 'checklist.md'
        storage.write_file(checklist_path, checklist_draft)
        return article

    print(f"   📊 Generated {item_count} items")

    # Step 2: Humanize checklist
    print(f"🔄 Humanizing checklist...")
    humanize_prompt = prompts.load_and_render(
        "audyt/prompt_sprawdz_styl.md",
        {
            'ARTICLE_CONTENT': checklist_draft,
            'TARGET_AUDIENCE': article.config.target_audience,
        }
    )
    humanized_checklist = ai.generate(humanize_prompt, max_tokens=2000)

    # Step 3: Save final checklist
    checklist_path = article.path / 'checklist.md'
    storage.write_file(checklist_path, humanized_checklist)

    print(f"✅ Checklist saved to checklist.md ({item_count} items, humanized)")

    # Publish recommendation
    if item_count >= 8:
        print(f"   📊 {item_count} pozycji - REKOMENDACJA: Opublikuj checklist")
    elif item_count >= 5:
        print(f"   📊 {item_count} pozycji - REKOMENDACJA: Rozważ publikację")
    else:
        print(f"   📊 {item_count} pozycji - REKOMENDACJA: Dodaj więcej pozycji przed publikacją")

    return article
