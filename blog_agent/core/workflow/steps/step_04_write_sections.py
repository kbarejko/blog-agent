"""
Step 4-5: Write Article Sections

Writes all sections with AI review on each section.
Combines steps 4 (first section) and 5 (remaining sections) into one step.
"""
from typing import Dict, Any

from ...domain.article import Article
from ._section_writer import write_section_with_review


def execute_write_sections(
    article: Article,
    deps: Dict[str, Any],
    config: Dict[str, Any]
) -> Article:
    """
    Write all article sections

    Each section is:
    1. Generated with AI
    2. Reviewed (word count, Flesch score)
    3. Auto-fixed if needed (max 2 retries)
    4. Saved to sections/NN-section.md

    Args:
        article: Article (must have outline and summary)
        deps: Dependencies (ai, prompts, storage, review)
        config: Step configuration

    Returns:
        Article with all sections written
    """
    if not article.outline:
        raise ValueError("Outline must be created before writing sections")
    if not article.summary:
        raise ValueError("Summary must be created before writing sections")

    storage = deps['storage']

    num_sections = len(article.outline.sections)
    print(f"🔄 Writing {num_sections} sections...")

    # Write each section
    for i in range(num_sections):
        section = article.outline.sections[i]
        print(f"\n📝 Section {i + 1}/{num_sections}: {section['title']}")

        # Write section with review
        content = write_section_with_review(article, i, deps)

        # Add section to article
        article.add_section(content)

        # Save to file
        section_path = article.get_section_path(i + 1)  # 1-indexed filenames
        storage.write_file(section_path, content)

    print(f"\n✅ All {num_sections} sections written")

    # FAQ and Checklist are always included in outline
    print("   📋 Checklist section included")
    print("   ❓ FAQ section included")

    return article
