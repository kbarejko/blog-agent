"""
Step 18: Generate Checklist

Generates checklist section (always included in outline).
Saves to checklist.md with publish recommendation.
"""
from typing import Dict, Any

from ...domain.article import Article


def execute_checklist(
    article: Article,
    deps: Dict[str, Any],
    config: Dict[str, Any]
) -> Article:
    """
    Generate Checklist section

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

    print("🔄 Generating Checklist...")

    # Load and render prompt
    prompt = prompts.load_and_render(
        "checklist/prompt_checklist.md",
        {
            'TYTUL_ARTYKULU': article.config.title,
            'KONSPEKT_TRESC': article.outline.to_markdown(),
            'TARGET_AUDIENCE': article.config.target_audience,
        }
    )

    # Generate checklist
    response = ai.generate(prompt, max_tokens=1500)

    # Save to checklist.md
    checklist_path = article.path / 'checklist.md'
    storage.write_file(checklist_path, response)

    print(f"✅ Checklist saved to checklist.md")

    # Analyze checklist quality and give publish recommendation
    checklist_lines = response.strip().split('\n')
    item_count = sum(1 for line in checklist_lines if line.strip().startswith('- [ ]'))

    if item_count >= 8:
        print(f"   📊 {item_count} pozycji - REKOMENDACJA: Opublikuj checklist")
    elif item_count >= 5:
        print(f"   📊 {item_count} pozycji - REKOMENDACJA: Rozważ publikację")
    else:
        print(f"   📊 {item_count} pozycji - REKOMENDACJA: Dodaj więcej pozycji przed publikacją")

    return article
