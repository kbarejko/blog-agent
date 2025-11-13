"""
Step 16: Generate Social Media Posts

Creates social media post package (Facebook/LinkedIn/Instagram) based on article.
"""
from typing import Dict, Any
import json
import yaml
from pathlib import Path


def execute_social_media(
    article: Any,
    deps: Dict[str, Any],
    config: Dict[str, Any]
) -> Any:
    """
    Generate social media posts for article

    Args:
        article: Article object
        deps: Dependencies (ai, prompts, storage)
        config: Step config

    Returns:
        Updated article
    """
    ai = deps['ai']
    prompts = deps['prompts']
    storage = deps['storage']

    # Load article content (final version)
    article_path = article.get_article_path()
    if not article_path.exists():
        raise FileNotFoundError(f"Article not found: {article_path}")

    article_content = storage.read_file(article_path)

    # Generate article URL from path
    # artykuly/ecommerce/seo/config.yaml → https://www.digitalvantage.pl/artykuly/ecommerce/seo/
    article_url = _generate_article_url(article.path)

    # Load and render prompt
    prompt_path = "social_media/prompt_social_media.md"
    variables = {
        'ARTICLE_TITLE': article.config.title,
        'ARTICLE_URL': article_url,
        'ARTICLE_CONTENT': article_content,
        'TARGET_AUDIENCE': article.config.target_audience,
    }

    prompt = prompts.load_and_render(prompt_path, variables)

    print(f"🔄 Generating social media posts...")

    # Generate with AI (higher max_tokens for comprehensive response)
    response = ai.generate(prompt, max_tokens=2000)

    # Parse JSON response
    try:
        social_data = _parse_social_media_response(response)
    except Exception as e:
        print(f"   ⚠️  Failed to parse JSON, attempting graceful extraction: {e}")
        social_data = _extract_social_data_fallback(response, article_url)

    # Ensure URL is included
    social_data['article_url'] = article_url

    # Convert hashtags from list to space-separated string
    if 'first_comment' in social_data and 'hashtags' in social_data['first_comment']:
        hashtags = social_data['first_comment']['hashtags']
        if isinstance(hashtags, list):
            social_data['first_comment']['hashtags'] = ' '.join(hashtags)

    # Save to Markdown file
    output_path = article.path / 'social_media.md'
    markdown_content = _format_as_markdown(social_data)

    output_path.parent.mkdir(parents=True, exist_ok=True)
    with open(output_path, 'w', encoding='utf-8') as f:
        f.write(markdown_content)

    print(f"   ✅ Social media posts generated")
    print(f"      Post length: {len(social_data.get('post', ''))} chars")
    print(f"      Alternative titles: {len(social_data.get('alternative_titles', []))}")
    print(f"      Hashtags: {len(social_data.get('first_comment', {}).get('hashtags', []))}")

    return article


def _format_as_markdown(social_data: Dict[str, Any]) -> str:
    """
    Format social media data as Markdown

    Args:
        social_data: Social media data dict

    Returns:
        Formatted markdown string
    """
    lines = []

    # Post
    lines.append("# Post")
    lines.append("")
    lines.append(social_data.get('post', ''))
    lines.append("")

    # Alternative titles
    lines.append("## Alternatywne tytuły")
    lines.append("")
    for i, title in enumerate(social_data.get('alternative_titles', []), 1):
        lines.append(f"{i}. {title}")
    lines.append("")

    # First comment
    first_comment = social_data.get('first_comment', {})
    lines.append("## Pierwszy komentarz")
    lines.append("")

    # Intro + bullets
    intro = first_comment.get('intro', 'Co znajdziesz w artykule?')
    lines.append(f"**{intro}**")
    lines.append("")
    for bullet in first_comment.get('bullets', []):
        lines.append(f"- {bullet}")
    lines.append("")

    # Link
    link = first_comment.get('link', social_data.get('article_url', ''))
    lines.append(f"**Link:** {link}")
    lines.append("")

    # Acronym explanations
    acronyms = first_comment.get('acronym_explanations', {})
    if acronyms:
        lines.append("### Wyjaśnienia skrótów")
        lines.append("")
        for acronym, explanation in acronyms.items():
            lines.append(f"- **{acronym}**: {explanation}")
        lines.append("")

    # Hashtags
    hashtags = first_comment.get('hashtags', '')
    if hashtags:
        lines.append("### Hashtags")
        lines.append("")
        lines.append(hashtags)
        lines.append("")

    return '\n'.join(lines)


def _generate_article_url(article_path: Path) -> str:
    """
    Generate article URL from filesystem path

    Args:
        article_path: Path to article directory (e.g., artykuly/ecommerce/seo/)

    Returns:
        Full article URL
    """
    # Convert path to URL parts
    # Path: artykuly/ecommerce/seo → URL: /artykuly/ecommerce/seo/
    path_parts = article_path.parts

    # Find 'artykuly' index
    try:
        artykuly_index = path_parts.index('artykuly')
        url_parts = path_parts[artykuly_index:]
        url_path = '/'.join(url_parts)
        return f"https://www.digitalvantage.pl/{url_path}/"
    except ValueError:
        # Fallback if 'artykuly' not in path
        return f"https://www.digitalvantage.pl/{'/'.join(path_parts)}/"


def _parse_social_media_response(response: str) -> Dict[str, Any]:
    """
    Parse AI response as JSON

    Args:
        response: AI response (expected to be JSON)

    Returns:
        Parsed social media data

    Raises:
        ValueError: If response is not valid JSON
    """
    # Remove markdown code blocks if present
    response = response.strip()
    if response.startswith('```json'):
        response = response[7:]
    if response.startswith('```'):
        response = response[3:]
    if response.endswith('```'):
        response = response[:-3]
    response = response.strip()

    # Parse JSON
    data = json.loads(response)

    # Validate structure
    required_keys = ['post', 'alternative_titles', 'first_comment']
    for key in required_keys:
        if key not in data:
            raise ValueError(f"Missing required key: {key}")

    return data


def _extract_social_data_fallback(response: str, article_url: str) -> Dict[str, Any]:
    """
    Extract social media data from non-JSON response (fallback)

    Args:
        response: AI response (plain text)
        article_url: Article URL

    Returns:
        Best-effort social media data structure
    """
    import re

    lines = response.split('\n')

    # Try to extract post (usually first line or after "POST:")
    post = ""
    for line in lines:
        if line.strip() and not line.startswith('#') and not line.startswith('**'):
            post = line.strip()
            break

    # Try to extract alternative titles
    alt_titles = []
    in_titles_section = False
    for line in lines:
        if 'alternatywne' in line.lower() or 'tytuły' in line.lower():
            in_titles_section = True
            continue
        if in_titles_section and line.strip().startswith(('-', '*', '1', '2', '3', '4')):
            title = re.sub(r'^[-*\d.)\s]+', '', line).strip()
            if title:
                alt_titles.append(title)
            if len(alt_titles) >= 4:
                break

    # Try to extract hashtags
    hashtags = re.findall(r'#\w+', response)[:10]

    return {
        'post': post or "Sprawdź najnowszy artykuł na naszym blogu!",
        'alternative_titles': alt_titles or [
            "Nowy artykuł na blogu",
            "Praktyczny przewodnik",
            "Dowiedz się więcej",
            "Sprawdź nasz artykuł"
        ],
        'first_comment': {
            'intro': 'Co znajdziesz w artykule?',
            'bullets': ['Praktyczne wskazówki', 'Konkretne przykłady', 'Sprawdzone rozwiązania'],
            'link': article_url,
            'acronym_explanations': {},
            'hashtags': hashtags or ['#biznes', '#marketing', '#ecommerce']
        }
    }
