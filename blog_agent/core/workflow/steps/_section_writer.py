"""
Section Writer Helper

Shared logic for writing sections with AI review and auto-fix.
"""
from typing import Dict, Any, Optional


def write_section_with_review(
    article: Any,
    section_index: int,
    deps: Dict[str, Any],
    max_retries: int = 2
) -> str:
    """
    Write a section with automatic review and fixing

    Args:
        article: Article object
        section_index: Section index (0-based)
        deps: Dependencies (ai, prompts, storage, review)
        max_retries: Maximum retry attempts

    Returns:
        Section content (validated)
    """
    ai = deps['ai']
    prompts = deps['prompts']
    review = deps['review']

    section = article.outline.sections[section_index]
    is_first_section = (section_index == 0)

    # Determine which prompt to use
    if is_first_section:
        prompt_path = "articles/prompt_artykul_start.md"
    else:
        prompt_path = "articles/prompt_artykul_kontynuacja.md"

    # Get common guidelines
    common_prompt = prompts.get_common_prompt()

    # Build context from previous sections
    previous_context = ""
    if section_index > 0:
        previous_sections = article.sections[:section_index]
        previous_context = "\n\n---\n\n".join(previous_sections)

    # Render prompt
    variables = {
        'TEMAT_ARTYKULU': article.config.title,
        'KONSPEKT_TRESC': article.outline.to_markdown(),
        'WYTYCZNE_WSPOLNE': common_prompt,
        'TARGET_AUDIENCE': article.config.target_audience,
        'SECTION_TITLE': section['title'],
        'SECTION_DESCRIPTION': section.get('description', ''),
    }

    if not is_first_section:
        variables['POPRZEDNIE_SEKCJE'] = previous_context

    prompt = prompts.load_and_render(prompt_path, variables)

    # Generate and review with retries
    for attempt in range(max_retries + 1):
        print(f"   Generating section {section_index + 1}: {section['title']} (attempt {attempt + 1})")

        # Generate content
        content = ai.generate(prompt, max_tokens=1500)

        # Review
        review_result = review.review_section(content)

        if review_result['valid']:
            print(f"   ✅ Section passed review")
            return content

        # Not valid - provide feedback for retry
        if attempt < max_retries:
            print(f"   ⚠️  Section needs improvement: {', '.join(review_result['issues'])}")
            feedback = review.generate_review_feedback(review_result)

            # Add feedback to prompt for retry
            prompt = f"{prompt}\n\n---\n\n## FEEDBACK NA POPRZEDNIĄ WERSJĘ\n\n{feedback}\n\n**Przepisz sekcję uwzględniając powyższe uwagi:**"
        else:
            # Max retries reached - accept with warning
            print(f"   ⚠️  Max retries reached. Accepting with issues: {', '.join(review_result['issues'])}")
            return content

    return content  # Should never reach here, but for type checker
