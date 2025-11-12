"""
Step 14: Internal Linking

Adds internal links to related articles within the same silo.
Improves SEO and user engagement by connecting related content.
"""
from pathlib import Path
from typing import Dict, Any, List
import yaml
import re


def execute_internal_linking(article: Any, deps: Dict[str, Any], config: Dict[str, Any]) -> Any:
    """
    Add internal links to related articles in the same silo

    Args:
        article: Article domain object
        deps: Dependencies (ai, storage, prompts, etc.)
        config: Step configuration

    Returns:
        Updated article with internal links
    """
    print(f"🔗 Adding internal links...")

    # Get article path components
    path_parts = article.path.parts
    if len(path_parts) < 3:
        print("   ⚠️  Path too short, skipping internal linking")
        return article

    series = path_parts[-3]  # e.g., "ecommerce"
    silo = path_parts[-2]     # e.g., "operacje"
    current_slug = path_parts[-1]  # e.g., "test-bezpieczenstwo"

    print(f"   Series: {series}")
    print(f"   Silo: {silo}")
    print(f"   Current: {current_slug}\n")

    # Find related articles in the same silo
    related_articles = _find_silo_articles(article.path.parent, current_slug, deps)

    if not related_articles:
        print("   ℹ️  No related articles found in this silo")
        return article

    print(f"   Found {len(related_articles)} related articles in silo")

    # Read current article content
    article_path = article.get_article_path()
    if not article_path.exists():
        print("   ⚠️  Article.md not found, skipping")
        return article

    with open(article_path, 'r', encoding='utf-8') as f:
        content = f.read()

    # Use AI to select best articles and suggest link placements
    selected_links = _select_and_place_links(
        content=content,
        related_articles=related_articles,
        current_title=article.config.title,
        ai_provider=deps['ai'],
        prompts=deps['prompts']
    )

    if not selected_links:
        print("   ℹ️  No suitable link placements found")
        return article

    # Insert links into content
    updated_content, inserted_count = _insert_links(content, selected_links)

    # Save updated article
    with open(article_path, 'w', encoding='utf-8') as f:
        f.write(updated_content)

    if inserted_count > 0:
        print(f"✅ Added {inserted_count} internal links")

        # Git commit
        git = deps.get('git')
        if git:
            git.commit_article_stage(
                article.path,
                "internal_linking",
                f"Add internal links ({inserted_count} links)"
            )
    else:
        print(f"ℹ️  No internal links were added")

    return article


def _find_silo_articles(silo_path: Path, current_slug: str, deps: Dict[str, Any]) -> List[Dict[str, str]]:
    """
    Find all published articles in the same silo

    Args:
        silo_path: Path to the silo directory
        current_slug: Current article slug to exclude
        deps: Dependencies

    Returns:
        List of article metadata dicts
    """
    articles = []

    # Scan all subdirectories in the silo
    for article_dir in silo_path.iterdir():
        if not article_dir.is_dir():
            continue

        slug = article_dir.name
        if slug == current_slug:
            continue  # Skip current article

        # Check if article is published
        article_md = article_dir / "article.md"
        if not article_md.exists():
            continue  # Not published yet

        # Load config to get title
        config_path = article_dir / "config.yaml"
        if not config_path.exists():
            continue

        with open(config_path, 'r', encoding='utf-8') as f:
            config = yaml.safe_load(f)

        # Read first 500 chars of article for context
        with open(article_md, 'r', encoding='utf-8') as f:
            article_content = f.read()

        # Extract excerpt (first paragraph after summary)
        excerpt = _extract_excerpt(article_content)

        articles.append({
            'slug': slug,
            'title': config.get('title', slug),
            'url': f"/{'/'.join(article_dir.parts[-3:])}/",  # /series/silo/slug/
            'excerpt': excerpt
        })

    return articles


def _extract_excerpt(content: str) -> str:
    """Extract a brief excerpt from article content"""
    # Skip "Co znajdziesz w artykule?" section
    parts = content.split('\n## ')
    if len(parts) > 1:
        # Get first section after summary
        section = parts[1]
        lines = section.split('\n')
        # Get first few sentences
        text = '\n'.join(lines[1:6])  # Skip heading
        # Clean and truncate
        text = text.strip()[:300]
        return text
    return content[:300]


def _select_and_place_links(
    content: str,
    related_articles: List[Dict[str, str]],
    current_title: str,
    ai_provider: Any,
    prompts: Any
) -> List[Dict[str, Any]]:
    """
    Use AI to select best related articles and suggest where to place links

    Args:
        content: Current article content
        related_articles: List of related article metadata
        current_title: Current article title
        ai_provider: AI provider
        prompts: Prompt loader

    Returns:
        List of link placements with anchor text and target
    """
    # Prepare related articles context
    articles_context = "\n\n".join([
        f"**{i+1}. {art['title']}**\nURL: {art['url']}\nExcerpt: {art['excerpt']}"
        for i, art in enumerate(related_articles[:10])  # Limit to 10
    ])

    # Build prompt
    prompt = f"""Jesteś ekspertem SEO specjalizującym się w internal linkingu dla blogów.

Masz artykuł "{current_title}" i listę powiązanych artykułów w tym samym silosie tematycznym.

Twoim zadaniem jest:
1. Przeczytać dokładnie treść bieżącego artykułu
2. Znaleźć konkretne frazy/zdania które już istnieją w artykule
3. Dopasować te istniejące frazy do powiązanych artykułów (3-5 linków max)

KRYTYCZNE: Anchor text MUSI być dokładnym fragmentem tekstu z bieżącego artykułu (skopiuj go dosłownie).
NIE wymyślaj nowego tekstu. NIE parafrazuj. Użyj dokładnie tego samego tekstu co w artykule.

ARTYKUŁY POWIĄZANE:
{articles_context}

TREŚĆ BIEŻĄCEGO ARTYKUŁU:
{content[:3000]}

Zwróć odpowiedź w formacie:

LINK 1
Tytuł: [tytuł powiązanego artykułu]
URL: [url]
Anchor: [DOKŁADNA kopia fragmentu tekstu z artykułu powyżej - 2-8 słów]
Context: [dlaczego ten link pasuje tematycznie]

LINK 2
...

Reguły:
- Maksymalnie 5 linków
- Anchor text musi być DOKŁADNIE skopiowany z artykułu (2-8 słów)
- Wybieraj frazy które naturalnie odnoszą się do tematu powiązanego artykułu
- Nie linkuj nagłówków (##)
"""

    try:
        response = ai_provider.generate(
            prompt=prompt,
            max_tokens=2000,
            temperature=0.7
        )

        # Parse AI response
        links = _parse_link_suggestions(response, related_articles)
        return links

    except Exception as e:
        print(f"   ⚠️  AI link selection failed: {str(e)}")
        # Fallback: just link first 3 related articles
        return _fallback_link_selection(related_articles[:3])


def _parse_link_suggestions(response: str, related_articles: List[Dict[str, str]]) -> List[Dict[str, Any]]:
    """Parse AI response to extract link suggestions"""
    links = []

    # Split by "LINK N"
    sections = re.split(r'LINK \d+', response)

    for section in sections[1:]:  # Skip first empty section
        lines = section.strip().split('\n')
        link = {}

        for line in lines:
            line = line.strip()
            if line.startswith('Tytuł:'):
                link['title'] = line.replace('Tytuł:', '').strip()
            elif line.startswith('URL:'):
                link['url'] = line.replace('URL:', '').strip()
            elif line.startswith('Anchor:'):
                link['anchor'] = line.replace('Anchor:', '').strip()
            elif line.startswith('Context:'):
                link['context'] = line.replace('Context:', '').strip()

        if 'url' in link and 'anchor' in link:
            links.append(link)

    return links


def _fallback_link_selection(articles: List[Dict[str, str]]) -> List[Dict[str, Any]]:
    """Fallback: create simple links from first N articles"""
    links = []
    for art in articles:
        links.append({
            'title': art['title'],
            'url': art['url'],
            'anchor': art['title'],  # Use title as anchor
            'context': 'Automatic link'
        })
    return links


def _insert_links(content: str, links: List[Dict[str, Any]]) -> tuple[str, int]:
    """
    Insert links into article content

    Args:
        content: Original article content
        links: List of link placements

    Returns:
        Tuple of (updated content with links inserted, number of links inserted)
    """
    updated_content = content
    inserted_count = 0

    for link in links:
        anchor = link['anchor']
        url = link['url']
        title = link.get('title', '')

        # Check if anchor text exists in content
        if anchor.lower() not in content.lower():
            print(f"   ⚠️  Anchor text not found in article: '{anchor[:50]}...'")
            continue

        # Create markdown link
        markdown_link = f"[{anchor}]({url})"

        # Replace first occurrence of anchor text with link
        # Use word boundaries to avoid partial matches
        pattern = re.compile(re.escape(anchor), re.IGNORECASE)
        before = updated_content
        updated_content = pattern.sub(markdown_link, updated_content, count=1)

        if updated_content != before:
            inserted_count += 1
            print(f"   ✓ Inserted link: '{anchor[:40]}...' → {url}")

    if inserted_count == 0:
        print(f"   ℹ️  No links were inserted (anchor texts not found in content)")

    return updated_content, inserted_count
