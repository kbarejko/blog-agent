"""
Step 8: Humanize Content

Makes content more natural and conversational while keeping expertise.
"""
from typing import Dict, Any

from ...domain.article import Article


def execute_humanize(
    article: Article,
    deps: Dict[str, Any],
    config: Dict[str, Any]
) -> Article:
    """
    Humanize article content

    Makes language more natural and conversational while maintaining
    expert tone. Creates final article.md.

    Args:
        article: Article (must have draft)
        deps: Dependencies (ai, prompts, storage)
        config: Step configuration

    Returns:
        Article with final_content set
    """
    if not article.draft_content:
        raise ValueError("Draft must exist before humanization")

    ai = deps['ai']
    prompts = deps['prompts']
    storage = deps['storage']

    print("🔄 Humanizing content...")

    # Load and render prompt
    prompt = prompts.load_and_render(
        "audyt/prompt_sprawdz_styl.md",
        {
            'ARTICLE_CONTENT': article.draft_content,
            'TARGET_AUDIENCE': article.config.target_audience,
        }
    )

    # Generate humanized version
    humanized_content = ai.generate(prompt, max_tokens=4000)

    # Set final content
    article.set_final_content(humanized_content)

    # Save article.md
    article_path = article.get_article_path()
    storage.write_file(article_path, humanized_content)

    print(f"✅ Content humanized and saved to article.md")

    return article
