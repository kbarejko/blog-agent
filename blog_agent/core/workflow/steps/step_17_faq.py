"""
Step 17: Generate FAQ

Generates FAQ section (always included in outline).
Saves to faq.md with publish recommendation.
"""
from typing import Dict, Any

from ...domain.article import Article


def execute_faq(
    article: Article,
    deps: Dict[str, Any],
    config: Dict[str, Any]
) -> Article:
    """
    Generate FAQ section

    Args:
        article: Article (must have outline)
        deps: Dependencies (ai, prompts, storage)
        config: Step configuration

    Returns:
        Article with FAQ generated
    """
    if not article.outline:
        raise ValueError("Outline must exist before generating FAQ")

    ai = deps['ai']
    prompts = deps['prompts']
    storage = deps['storage']

    print("🔄 Generating FAQ...")

    # Load and render prompt
    prompt = prompts.load_and_render(
        "faq/prompt_faq.md",
        {
            'TYTUL_ARTYKULU': article.config.title,
            'KONSPEKT_TRESC': article.outline.to_markdown(),
            'TARGET_AUDIENCE': article.config.target_audience,
        }
    )

    # Generate FAQ
    response = ai.generate(prompt, max_tokens=2000)

    # Save to faq.md
    faq_path = article.path / 'faq.md'
    storage.write_file(faq_path, response)

    print(f"✅ FAQ saved to faq.md")

    # Analyze FAQ quality and give publish recommendation
    faq_lines = response.strip().split('\n')
    question_count = sum(1 for line in faq_lines if line.strip().startswith('###'))

    if question_count >= 5:
        print(f"   📊 {question_count} pytań - REKOMENDACJA: Opublikuj FAQ")
    elif question_count >= 3:
        print(f"   📊 {question_count} pytań - REKOMENDACJA: Rozważ publikację")
    else:
        print(f"   📊 {question_count} pytań - REKOMENDACJA: Dodaj więcej pytań przed publikacją")

    return article
