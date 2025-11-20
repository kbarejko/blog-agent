#!/usr/bin/env python3
"""
Test multimedia generation with stock_suggestions
"""
import os
import sys
from pathlib import Path

project_root = Path(__file__).parent
sys.path.insert(0, str(project_root))

from blog_agent.core.domain.article import Article
from blog_agent.core.domain.config import ArticleConfig
from blog_agent.core.factory import DependencyFactory

# Load .env
env_file = project_root / ".env"
if env_file.exists():
    with open(env_file) as f:
        for line in f:
            line = line.strip()
            if line and not line.startswith('#') and '=' in line:
                key, value = line.split('=', 1)
                os.environ[key] = value

# Find article with final content but no multimedia.json (or old one)
test_article = project_root / "artykuly/ecommerce/marketing-w-e-commerce/performance-media"

print(f"🧪 Testing multimedia generation with stock_suggestions")
print(f"Article: {test_article.name}\n")

# Load article
config_path = test_article / "config.yaml"
if not config_path.exists():
    print(f"❌ Config not found: {config_path}")
    sys.exit(1)

article_config = ArticleConfig.from_yaml(config_path)
article = Article(path=test_article, config=article_config)

# Check if article has final content
article_md = test_article / "article.md"
if not article_md.exists():
    print(f"❌ Article content not found: {article_md}")
    sys.exit(1)

# Load final content
with open(article_md, 'r', encoding='utf-8') as f:
    article.final_content = f.read()

print(f"✅ Article content loaded: {len(article.final_content)} chars")

# Create deps
factory = DependencyFactory(project_root)
deps = factory.create_deps(provider_name='claude')

print(f"✅ Dependencies created (provider: claude)\n")

# Execute multimedia step
from blog_agent.core.workflow.steps.step_08_multimedia import execute_multimedia

print("=" * 60)
print("Executing multimedia step...")
print("=" * 60 + "\n")

config = {}
article = execute_multimedia(article, deps, config)

# Check multimedia.json
multimedia_path = test_article / "multimedia.json"
if multimedia_path.exists():
    import json
    with open(multimedia_path, 'r', encoding='utf-8') as f:
        multimedia_data = json.load(f)

    print("\n" + "=" * 60)
    print("Checking generated multimedia.json")
    print("=" * 60 + "\n")

    # Check hero_image
    hero = multimedia_data.get('hero_image', {})
    print(f"Hero image:")
    print(f"  title: {hero.get('title', 'N/A')}")
    print(f"  prompt: {hero.get('prompt', 'N/A')[:80]}...")

    stock = hero.get('stock_suggestions', {})
    if stock:
        print(f"  ✅ stock_suggestions present!")
        print(f"     unsplash_query: {stock.get('unsplash_query', 'N/A')}")
        print(f"     pexels_query: {stock.get('pexels_query', 'N/A')}")
        print(f"     keywords: {stock.get('keywords_for_search', [])}")
        print(f"     style_notes: {stock.get('style_notes', 'N/A')[:60]}...")
    else:
        print(f"  ❌ stock_suggestions MISSING or empty!")

    # Check section_media
    section_media = multimedia_data.get('section_media', [])
    print(f"\nSection media: {len(section_media)} items")

    for i, media in enumerate(section_media[:3]):  # Show first 3
        print(f"\n  [{i+1}] {media.get('title', 'Untitled')}")
        print(f"      type: {media.get('type', 'N/A')}")
        print(f"      prompt: {media.get('prompt', 'N/A')[:60]}...")

        stock = media.get('stock_suggestions', {})
        if stock:
            print(f"      ✅ stock_suggestions present!")
            print(f"         unsplash: {stock.get('unsplash_query', 'N/A')[:60]}...")
        else:
            print(f"      ❌ stock_suggestions MISSING or empty!")

    print("\n" + "=" * 60)
    print("Test complete!")
    print("=" * 60)

    # Summary
    has_hero_stock = bool(multimedia_data.get('hero_image', {}).get('stock_suggestions'))
    section_with_stock = sum(1 for m in section_media if m.get('stock_suggestions'))

    print(f"\nSummary:")
    print(f"  Hero stock_suggestions: {'✅ YES' if has_hero_stock else '❌ NO'}")
    print(f"  Section stock_suggestions: {section_with_stock}/{len(section_media)}")

    if has_hero_stock and (len(section_media) == 0 or section_with_stock == len(section_media)):
        print(f"\n✅ SUCCESS - All multimedia have stock_suggestions!")
        sys.exit(0)
    else:
        print(f"\n⚠️  PARTIAL - Some multimedia missing stock_suggestions")
        sys.exit(0)
else:
    print(f"\n❌ multimedia.json not created!")
    sys.exit(1)
