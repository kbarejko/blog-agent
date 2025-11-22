"""
Step 19: Generate Headers Alternatives

Generates SEO-optimized alternative proposals for all H1, H2, H3 headers.
"""
from typing import Dict, Any, List, Tuple
import re

from ...domain.article import Article


def execute_headers_alternatives(
    article: Article,
    deps: Dict[str, Any],
    config: Dict[str, Any]
) -> Article:
    """
    Generate SEO-optimized alternative headers

    For each H1, H2, H3 header in article.md:
    1. Generate 3-4 alternative proposals
    2. Include SEO optimization aspects
    3. Include at least one long-tail variant
    4. Save to headers_alternatives.md

    Args:
        article: Article (must have published article.md)
        deps: Dependencies (ai, prompts, storage)
        config: Step configuration

    Returns:
        Article unchanged (alternatives saved to separate file)
    """
    ai = deps['ai']
    prompts = deps['prompts']
    storage = deps['storage']

    print("🔄 Generating headers alternatives...")

    # Read article.md
    article_path = article.get_article_path()
    if not article_path.exists():
        print("   ⚠️  article.md not found - skipping headers alternatives")
        return article

    with open(article_path, 'r', encoding='utf-8') as f:
        article_content = f.read()

    # Parse headers
    headers = _parse_headers(article_content)

    if not headers:
        print("   ⚠️  No headers found in article.md")
        return article

    print(f"   📊 Found {len(headers)} headers (H1/H2/H3)")

    # Generate alternatives for all headers
    alternatives_content = _generate_alternatives(
        headers=headers,
        article_title=article.config.title,
        article_content=article_content,
        ai_provider=ai,
        prompts=prompts
    )

    # Save to headers_alternatives.md
    output_path = article.path / 'headers_alternatives.md'
    storage.write_file(output_path, alternatives_content)

    print(f"✅ Headers alternatives saved to headers_alternatives.md")
    print(f"   📊 {len(headers)} headers with 3-4 SEO alternatives each")

    # Git commit
    git = deps.get('git')
    if git:
        git.commit_article_stage(
            article.path,
            "headers_alternatives",
            f"Add SEO header alternatives ({len(headers)} headers)"
        )

    return article


def _parse_headers(content: str) -> List[Tuple[int, str]]:
    """
    Parse all H1, H2, H3 headers from markdown content

    Args:
        content: Markdown article content

    Returns:
        List of tuples (level, header_text)
        Example: [(1, "Main Title"), (2, "Section Title"), (3, "Subsection")]
    """
    headers = []

    # Match H1, H2, H3 headers (# , ## , ### )
    # Pattern: ^(#{1,3})\s+(.+)$
    pattern = re.compile(r'^(#{1,3})\s+(.+)$', re.MULTILINE)

    for match in pattern.finditer(content):
        level = len(match.group(1))  # Number of # symbols
        header_text = match.group(2).strip()
        headers.append((level, header_text))

    return headers


def _generate_alternatives(
    headers: List[Tuple[int, str]],
    article_title: str,
    article_content: str,
    ai_provider: Any,
    prompts: Any
) -> str:
    """
    Generate SEO alternatives for all headers

    Args:
        headers: List of (level, header_text) tuples
        article_title: Article title for context
        article_content: Full article content for context
        ai_provider: AI provider
        prompts: Prompt loader

    Returns:
        Markdown formatted content with all headers and their alternatives
    """
    # Build context for AI
    headers_context = "\n".join([
        f"{'#' * level} {text}"
        for level, text in headers
    ])

    # Load and render prompt
    prompt = prompts.load_and_render(
        "seo/prompt_headers_alternatives.md",
        {
            'ARTICLE_TITLE': article_title,
            'HEADERS_LIST': headers_context,
            'ARTICLE_EXCERPT': article_content[:1500],  # First 1500 chars for context
        }
    )

    # Generate alternatives
    response = ai_provider.generate(prompt, max_tokens=4000)

    # Clean response - remove markdown wrapper if present
    cleaned_response = response.strip()
    if cleaned_response.startswith('```markdown'):
        cleaned_response = cleaned_response[len('```markdown'):].lstrip()
    if cleaned_response.startswith('```'):
        cleaned_response = cleaned_response[3:].lstrip()
    if cleaned_response.endswith('```'):
        cleaned_response = cleaned_response[:-3].rstrip()

    return cleaned_response.strip()
