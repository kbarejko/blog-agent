"""
Step 8: Humanize Content

Makes content more natural and conversational while keeping expertise.
Humanizes section-by-section to avoid truncation.
"""
from typing import Dict, Any
from pathlib import Path

from ...domain.article import Article


def execute_humanize(
    article: Article,
    deps: Dict[str, Any],
    config: Dict[str, Any]
) -> Article:
    """
    Humanize article content section by section

    Makes language more natural and conversational while maintaining
    expert tone. Processes each section individually to avoid truncation,
    then assembles final article.md.

    Args:
        article: Article (must have sections)
        deps: Dependencies (ai, prompts, storage)
        config: Step configuration

    Returns:
        Article with final_content set
    """
    ai = deps['ai']
    prompts = deps['prompts']
    storage = deps['storage']

    sections_dir = article.get_sections_dir()
    if not sections_dir.exists():
        raise ValueError("Sections directory must exist before humanization")

    print("🔄 Humanizing content section by section...")

    # Get all section files sorted by number
    section_files = sorted(sections_dir.glob("*.md"))
    if not section_files:
        raise ValueError("No sections found to humanize")

    print(f"   Found {len(section_files)} sections to humanize")

    humanized_sections = []
    total_original_words = 0
    total_humanized_words = 0

    # Humanize each section individually
    for section_file in section_files:
        section_num = section_file.stem  # e.g., "00-summary", "01-section"

        # Read section content
        section_content = storage.read_file(section_file)
        section_words = len(section_content.split())
        total_original_words += section_words

        print(f"   📝 Humanizing section {section_num} (~{section_words} words)...", end=" ", flush=True)

        # Prepare prompt for this section
        prompt = prompts.load_and_render(
            "audyt/prompt_sprawdz_styl.md",
            {
                'ARTICLE_CONTENT': section_content,
                'TARGET_AUDIENCE': article.config.target_audience,
            }
        )

        # Calculate max_tokens for this section
        # More generous for small sections, capped for large ones
        estimated_tokens = int((section_words / 0.75) * 1.3)  # 30% buffer
        max_tokens = max(2000, min(estimated_tokens, 8000))

        # Humanize section
        humanized_section = ai.generate(prompt, max_tokens=max_tokens)

        # Validate
        humanized_words = len(humanized_section.split())
        total_humanized_words += humanized_words
        word_ratio = humanized_words / section_words if section_words > 0 else 1.0

        if word_ratio < 0.85:
            print(f"⚠️  ({word_ratio:.0%} preserved)")
        else:
            print(f"✅ ({word_ratio:.0%})")

        humanized_sections.append(humanized_section)

    # Assemble final article
    print(f"\n   📦 Assembling final article from {len(humanized_sections)} sections...")

    # Join sections with double newline
    final_content = "\n\n".join(humanized_sections)

    # Overall statistics
    overall_ratio = total_humanized_words / total_original_words if total_original_words > 0 else 1.0

    print(f"   ✓ Total words: {total_original_words} → {total_humanized_words} ({overall_ratio:.1%})")

    if overall_ratio < 0.85:
        print(f"   ⚠️  Some content may have been truncated in individual sections")

    # Set final content
    article.set_final_content(final_content)

    # Save article.md
    article_path = article.get_article_path()
    storage.write_file(article_path, final_content)

    print(f"✅ Content humanized and saved to article.md")

    return article
