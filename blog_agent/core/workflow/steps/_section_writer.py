"""
Section Writer Helper

Shared logic for writing sections with AI review and auto-fix.
"""
from typing import Dict, Any, Optional, List, Tuple
import re


def _inject_headers_structure(content: str, expected_structure: str) -> str:
    """
    Inject H3 and H4 headers from outline into generated content

    Args:
        content: Generated content (may be missing H3/H4)
        expected_structure: Structure from outline with H3 and H4 headers

    Returns:
        Content with H3/H4 headers injected
    """
    # Parse header structure from outline (H3 and H4 with hierarchy)
    # Returns list of dicts: [{'level': 3, 'title': 'Header', 'h4_children': [...]}, ...]
    header_structure = []
    current_h3 = None

    for line in expected_structure.split('\n'):
        line = line.strip()

        # Match H3 header
        h3_match = re.match(r'^### (.+)$', line)
        if h3_match:
            # Save previous H3 if any
            if current_h3:
                header_structure.append(current_h3)
            # Start new H3
            current_h3 = {
                'level': 3,
                'title': h3_match.group(1).strip(),
                'h4_children': []
            }
            continue

        # Match H4 header (only if we're inside an H3)
        h4_match = re.match(r'^#### (.+)$', line)
        if h4_match and current_h3:
            current_h3['h4_children'].append(h4_match.group(1).strip())
            continue

    # Save last H3
    if current_h3:
        header_structure.append(current_h3)

    # If no headers in outline, return as-is
    if not header_structure:
        return content

    # Count total headers in structure (H3 + H4)
    total_headers_expected = sum(1 + len(h3['h4_children']) for h3 in header_structure)

    # Check if content already has all headers
    h3_count = content.count('\n### ') + (1 if content.startswith('### ') else 0)
    h4_count = content.count('\n#### ') + (1 if content.startswith('#### ') else 0)
    total_headers_present = h3_count + h4_count

    if total_headers_present >= total_headers_expected:
        # Already has headers, return as-is
        return content

    # Split content into paragraphs
    lines = content.strip().split('\n')
    paragraphs = []
    current_para = []

    for line in lines:
        line_stripped = line.strip()
        if line_stripped == '' and current_para:
            # Empty line - end of paragraph
            paragraphs.append('\n'.join(current_para))
            current_para = []
        elif line_stripped:
            current_para.append(line)

    if current_para:
        paragraphs.append('\n'.join(current_para))

    # Skip H2 header if present
    start_idx = 0
    if paragraphs and paragraphs[0].startswith('##') and not paragraphs[0].startswith('###'):
        start_idx = 1

    # Get content paragraphs (excluding H2)
    content_paragraphs = paragraphs[start_idx:]
    if len(content_paragraphs) == 0:
        return content

    # Calculate how to distribute paragraphs among headers
    # Each H3 gets equal share, then H4s split that share
    paragraphs_per_h3 = max(1, len(content_paragraphs) // len(header_structure))

    # Inject headers
    result = []
    if start_idx == 1:
        result.append(paragraphs[0])  # Keep H2 header
        result.append('')

    para_idx = 0

    for h3_idx, h3_info in enumerate(header_structure):
        # Add H3 header
        result.append(f"### {h3_info['title']}")
        result.append('')

        # Calculate paragraphs for this H3 section
        is_last_h3 = (h3_idx == len(header_structure) - 1)
        if is_last_h3:
            # Last H3 gets all remaining paragraphs
            h3_para_count = len(content_paragraphs) - para_idx
        else:
            h3_para_count = paragraphs_per_h3

        # If this H3 has H4 children, distribute paragraphs among them
        h4_children = h3_info['h4_children']

        if h4_children:
            # Distribute paragraphs: some before first H4, then split among H4s
            paras_before_h4 = max(1, h3_para_count // (len(h4_children) + 1))
            paras_per_h4 = max(1, (h3_para_count - paras_before_h4) // len(h4_children))

            # Add paragraphs before first H4
            for _ in range(paras_before_h4):
                if para_idx < len(content_paragraphs):
                    result.append(content_paragraphs[para_idx])
                    result.append('')
                    para_idx += 1

            # Add H4 sections
            for h4_idx, h4_title in enumerate(h4_children):
                result.append(f"#### {h4_title}")
                result.append('')

                # Add paragraphs for this H4
                is_last_h4 = (h4_idx == len(h4_children) - 1)
                if is_last_h4:
                    # Last H4 in this H3 gets remaining paragraphs for this H3
                    h4_end = para_idx + (h3_para_count - (para_idx - (para_idx - paras_before_h4)))
                else:
                    h4_end = para_idx + paras_per_h4

                while para_idx < h4_end and para_idx < len(content_paragraphs):
                    result.append(content_paragraphs[para_idx])
                    result.append('')
                    para_idx += 1
        else:
            # No H4 children - add all paragraphs directly under H3
            for _ in range(h3_para_count):
                if para_idx < len(content_paragraphs):
                    result.append(content_paragraphs[para_idx])
                    result.append('')
                    para_idx += 1

    return '\n'.join(result).strip()


def _ensure_section_header(content: str, section_title: str) -> str:
    """
    Ensure section starts with H2 header from outline

    Args:
        content: Generated section content
        section_title: Section title from outline (e.g., "1. Introduction" or "Introduction")

    Returns:
        Content with H2 header prepended
    """
    # Normalize title - remove number prefix if present (e.g., "1. Title" -> "Title")
    title_normalized = re.sub(r'^\d+\.\s*', '', section_title).strip()

    # Check if content already starts with H2 header (## Title)
    lines = content.strip().split('\n')
    if lines and lines[0].startswith('## '):
        # Already has H2, return as-is
        return content

    # Check if content starts with H3 header (### Title) - upgrade to H2
    if lines and lines[0].startswith('### '):
        # Check if it's our title
        h3_title = lines[0][4:].strip()  # Remove "### " prefix
        if h3_title.lower() == title_normalized.lower():
            # Replace H3 with H2
            lines[0] = f"## {title_normalized}"
            return '\n'.join(lines)
        # Different title in H3 - prepend our H2
        return f"## {title_normalized}\n\n{content}"

    # No header found - prepend H2
    return f"## {title_normalized}\n\n{content}"


def _select_best_attempt(
    attempts: List[Tuple[str, Dict[str, Any]]],
    target_words: Optional[int] = None
) -> Tuple[str, Dict[str, Any]]:
    """
    Select the attempt closest to requirements

    Args:
        attempts: List of (content, review_result) tuples
        target_words: Optional target word count for this section

    Returns:
        Best (content, review_result) tuple
    """
    if not attempts:
        raise ValueError("No attempts to select from")

    if len(attempts) == 1:
        return attempts[0]

    # Calculate penalty score for each attempt (lower is better)
    scored_attempts = []
    for content, review_result in attempts:
        penalty = 0

        # Word count penalty
        word_count = review_result.get('word_count', 0)
        min_words = review_result.get('min_words', 300)
        max_words = review_result.get('max_words', 400)

        if word_count < min_words:
            penalty += (min_words - word_count) ** 2  # Squared penalty for being too short
        elif word_count > max_words:
            penalty += (word_count - max_words) ** 2  # Squared penalty for being too long

        # Flesch score penalty (if checked)
        flesch = review_result.get('flesch', None)
        if flesch is not None:
            min_flesch = review_result.get('min_flesch', 40)
            max_flesch = review_result.get('max_flesch', 60)
            target_flesch = (min_flesch + max_flesch) / 2

            if flesch < min_flesch:
                penalty += (min_flesch - flesch) ** 2
            elif flesch > max_flesch:
                penalty += (flesch - max_flesch) ** 2
            else:
                # Within range - add small penalty for distance from center
                penalty += abs(flesch - target_flesch) * 0.5

        scored_attempts.append((penalty, content, review_result))

    # Sort by penalty (ascending) and return the best
    scored_attempts.sort(key=lambda x: x[0])
    _, best_content, best_result = scored_attempts[0]

    return best_content, best_result


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
    # POPRZEDNIE_SEKCJE = all previous sections for better consistency
    previous_context = ""
    if section_index > 0:
        previous_sections = article.sections[:section_index]
        previous_context = "\n\n---\n\n".join(previous_sections)

    # Get target words from section (parsed from outline description)
    words_per_section_guidance = ""
    if 'target_words' in section and section['target_words']:
        # Use specific target from outline (e.g., "(~200 słów)")
        target_words = section['target_words']
        words_per_section_guidance = f" Docelowa długość tej sekcji: ~{target_words} słów (z konspektu)."
    elif article.config.target_word_count:
        # Fallback: calculate average from total target
        num_sections = len(article.outline.sections)
        overhead = 0  # Don't subtract overhead - total includes all sections
        content_words = article.config.target_word_count - overhead
        words_per_section = round(content_words / num_sections)
        words_per_section_guidance = f" Docelowa długość tej sekcji: ~{words_per_section} słów (szacunkowa)."

    # Render prompt
    variables = {
        'TYTUL_ARTYKULU': article.config.title,
        'KONSPEKT_TRESC': article.outline.to_markdown(),
        'WYTYCZNE_WSPOLNE': common_prompt + words_per_section_guidance,
        'TARGET_AUDIENCE': article.config.target_audience,
        'SECTION_TITLE': section['title'],
        'SECTION_DESCRIPTION': section.get('description', ''),
    }

    if not is_first_section:
        variables['POPRZEDNIE_SEKCJE'] = previous_context

    prompt = prompts.load_and_render(prompt_path, variables)

    # Get expected structure for H3 injection
    expected_structure = section.get('description', '')
    target_words = section.get('target_words')

    # Track all attempts to select the best one
    attempts = []  # List of (content, review_result) tuples

    # Generate and review with retries
    for attempt in range(max_retries + 1):
        print(f"   Generating section {section_index + 1}: {section['title']} (attempt {attempt + 1})", flush=True)

        # Generate content
        content = ai.generate(prompt, max_tokens=1500)

        # Review with section-specific target words (no structure validation - we inject H3 anyway)
        review_result = review.review_section(content, target_words=target_words)

        # Store this attempt
        attempts.append((content, review_result))

        if review_result['valid']:
            print(f"   ✅ Section passed review")
            # Inject H3/H4 structure if missing
            content = _inject_headers_structure(content, expected_structure)
            # Add H2 header from outline (if not already present)
            content = _ensure_section_header(content, section['title'])
            return content

        # Not valid - provide feedback for retry
        if attempt < max_retries:
            print(f"   ⚠️  Section needs improvement: {', '.join(review_result['issues'])}")
            feedback = review.generate_review_feedback(review_result)

            # Add feedback to prompt for retry
            prompt = f"{prompt}\n\n---\n\n## FEEDBACK NA POPRZEDNIĄ WERSJĘ\n\n{feedback}\n\n**Przepisz sekcję uwzględniając powyższe uwagi:**"

    # Max retries reached - select the attempt closest to requirements
    best_content, best_result = _select_best_attempt(attempts, target_words)
    print(f"   ⚠️  Max retries reached. Selected attempt closest to requirements: {', '.join(best_result['issues'])}")

    # Inject H3/H4 structure if missing
    content = _inject_headers_structure(best_content, expected_structure)
    # Add H2 header from outline (if not already present)
    content = _ensure_section_header(content, section['title'])
    return content
