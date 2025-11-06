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

    # Calculate appropriate max_tokens based on draft length
    # Estimate: 1 token ≈ 0.75 words (Polish text)
    # Add 20% buffer for safety
    draft_words = len(article.draft_content.split())
    estimated_tokens = int((draft_words / 0.75) * 1.2)

    # Ensure minimum and maximum bounds
    max_tokens = max(4000, min(estimated_tokens, 16000))

    print(f"   Draft: ~{draft_words} words, using max_tokens={max_tokens}")

    # Generate humanized version
    humanized_content = ai.generate(prompt, max_tokens=max_tokens)

    # Validate that content wasn't truncated
    humanized_words = len(humanized_content.split())
    word_ratio = humanized_words / draft_words if draft_words > 0 else 1.0

    if word_ratio < 0.85:
        print(f"   ⚠️  Warning: Humanized content may be truncated!")
        print(f"   Draft: {draft_words} words → Humanized: {humanized_words} words ({word_ratio:.1%})")
        print(f"   Consider increasing max_tokens or splitting into chunks.")
    else:
        print(f"   ✓ Content preserved: {humanized_words} words ({word_ratio:.1%} of draft)")

    # Set final content
    article.set_final_content(humanized_content)

    # Save article.md
    article_path = article.get_article_path()
    storage.write_file(article_path, humanized_content)

    print(f"✅ Content humanized and saved to article.md")

    return article
