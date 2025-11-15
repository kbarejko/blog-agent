#!/usr/bin/env python3
"""
Generate SEO headers alternatives for all articles in the tree

Usage:
    python generate_headers_alternatives_all.py [directory]

Examples:
    python generate_headers_alternatives_all.py                    # Process all articles
    python generate_headers_alternatives_all.py artykuly/ecommerce # Process only ecommerce series
"""
import subprocess
import sys
from pathlib import Path


def find_articles(search_dir: Path):
    """Find all articles with config.yaml"""
    return sorted(search_dir.rglob("config.yaml"))


def get_article_title(config_path: Path) -> str:
    """Extract article title from config.yaml"""
    try:
        with open(config_path, 'r', encoding='utf-8') as f:
            for line in f:
                if line.startswith('title:'):
                    return line.replace('title:', '').strip().strip('"')
    except Exception:
        pass
    return "Unknown"


def generate_headers_alternatives(config_path: Path) -> bool:
    """
    Run headers_alternatives step for a single article

    Args:
        config_path: Path to article's config.yaml

    Returns:
        True if successful, False otherwise
    """
    try:
        result = subprocess.run(
            [
                sys.executable, '-m', 'blog_agent',
                'create',
                '--config', str(config_path),
                '--only', 'headers_alternatives'
            ],
            capture_output=True,
            text=True,
            timeout=120
        )

        # Check if successful
        return "✅ Headers alternatives saved" in result.stdout

    except subprocess.TimeoutExpired:
        return False
    except Exception:
        return False


def main():
    # Get search directory from args or default to 'artykuly'
    search_dir = Path(sys.argv[1]) if len(sys.argv) > 1 else Path('artykuly')

    print(f"🔍 Searching for articles in: {search_dir}\n")

    # Find all articles
    configs = find_articles(search_dir)
    total = len(configs)

    print(f"📊 Found {total} articles\n")

    success = 0
    failed = 0
    skipped = 0

    # Process each article
    for idx, config_path in enumerate(configs, 1):
        article_dir = config_path.parent
        article_name = get_article_title(config_path)

        print(f"[{idx}/{total}] Processing: {article_name}")
        print(f"   Path: {article_dir}")

        # Check if article.md exists
        article_md = article_dir / "article.md"
        if not article_md.exists():
            print(f"   ⚠️  Skipping - article.md not found\n")
            skipped += 1
            continue

        # Generate alternatives
        if generate_headers_alternatives(config_path):
            success += 1
            print(f"   ✅ Generated headers_alternatives.md\n")
        else:
            failed += 1
            print(f"   ❌ Failed to generate alternatives\n")

    # Summary
    print("\n" + "=" * 40)
    print("📊 Summary")
    print("=" * 40)
    print(f"Total articles:    {total}")
    print(f"Successful:        {success}")
    if skipped > 0:
        print(f"Skipped (no article.md): {skipped}")
    if failed > 0:
        print(f"Failed:            {failed}")
    print("=" * 40)


if __name__ == "__main__":
    main()
