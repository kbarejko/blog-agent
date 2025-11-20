#!/usr/bin/env python3
"""
Test Hero Image Generation

Tests step_15_generate_images.py with real API call.
Generates hero image for an existing article with multimedia.json.
"""
import os
import sys
from pathlib import Path

# Add project root to path
project_root = Path(__file__).parent
sys.path.insert(0, str(project_root))

from blog_agent.core.domain.article import Article
from blog_agent.core.domain.config import ArticleConfig
from blog_agent.core.factory import DependencyFactory


def test_hero_generation():
    """Test hero image generation on real article"""

    # Article path with existing multimedia.json
    article_path = project_root / "artykuly/ecommerce/marketing-w-e-commerce/performance-media"

    print(f"🧪 Testing Hero Image Generation")
    print(f"=" * 60)
    print(f"Article: {article_path.relative_to(project_root)}")

    # Check multimedia.json exists
    multimedia_path = article_path / "multimedia.json"
    if not multimedia_path.exists():
        print(f"❌ multimedia.json not found!")
        return False

    print(f"✅ multimedia.json exists")

    # Load article config
    config_path = article_path / "config.yaml"
    if not config_path.exists():
        print(f"❌ config.yaml not found!")
        return False

    article_config = ArticleConfig.from_yaml(config_path)
    article = Article(path=article_path, config=article_config)

    print(f"✅ Article loaded: {article.config.title}")

    # Create dependencies
    factory = DependencyFactory(project_root)
    deps = factory.create_deps(provider_name='openai-gpt4o')  # Use OpenAI provider

    print(f"\n{'─' * 60}")
    print(f"🔧 Dependencies:")
    print(f"   Storage: {deps['storage'].__class__.__name__}")
    print(f"   Git: {deps['git'].__class__.__name__}")

    # Check API key
    api_key = os.getenv('OPENAI_API_KEY')
    if not api_key:
        print(f"\n❌ OPENAI_API_KEY not set!")
        print(f"   Run: export OPENAI_API_KEY=sk-...")
        return False

    print(f"   OpenAI API Key: {api_key[:20]}... ✅")

    # Import and execute step
    print(f"\n{'─' * 60}")
    print(f"🎨 Generating Hero Image...\n")

    from blog_agent.core.workflow.steps.step_15_generate_images import execute_generate_images

    # Step config (DALL-E 3 Standard for test)
    step_config = {
        'provider': 'dalle',
        'model': 'dall-e-3',
        'size': '1024x1024',  # Smaller size for faster test
        'quality': 'standard',
        'skip_existing': False  # Force regeneration for test
    }

    try:
        article = execute_generate_images(article, deps, step_config)

        print(f"\n{'─' * 60}")
        print(f"✅ Generation completed!")

        # Check result
        hero_path = article_path / "images/hero.png"
        if hero_path.exists():
            size_kb = hero_path.stat().st_size // 1024
            print(f"✅ Hero image created: {hero_path.name} ({size_kb} KB)")
            print(f"\n📁 Full path: {hero_path}")
            return True
        else:
            print(f"⚠️  Hero image not found at {hero_path}")
            return False

    except Exception as e:
        print(f"\n❌ Generation failed: {str(e)}")
        import traceback
        traceback.print_exc()
        return False


if __name__ == "__main__":
    # Load .env file if exists
    env_file = project_root / ".env"
    if env_file.exists():
        print(f"📄 Loading environment from .env...")
        with open(env_file) as f:
            for line in f:
                line = line.strip()
                if line and not line.startswith('#') and '=' in line:
                    key, value = line.split('=', 1)
                    os.environ[key] = value
        print(f"✅ Environment loaded\n")

    success = test_hero_generation()

    print(f"\n{'=' * 60}")
    if success:
        print(f"✅ TEST PASSED - Hero image generated successfully!")
    else:
        print(f"❌ TEST FAILED - See errors above")
    print(f"{'=' * 60}")

    sys.exit(0 if success else 1)
