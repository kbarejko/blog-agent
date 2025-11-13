"""
Test Step 16: Social Media Post Generation

Tests social media post generation step in isolation.
"""
from pathlib import Path
from blog_agent.core.domain.article import Article
from blog_agent.core.domain.config import ArticleConfig
from blog_agent.core.factory import DependencyFactory
from blog_agent.core.workflow.steps.step_16_social_media import execute_social_media


def test_social_media_generation():
    """Test social media post generation with existing article"""

    print("=" * 60)
    print("Testing Step 16: Social Media Post Generation")
    print("=" * 60)

    # Find an existing article to test with
    # Let's use the SEO article if it exists
    test_article_path = Path("artykuly/ecommerce/seo")

    if not test_article_path.exists():
        print(f"❌ Test article not found: {test_article_path}")
        print("   Please run a complete article generation first, or specify an existing article path.")
        return

    # Load article config
    config_path = test_article_path / "config.yaml"
    if not config_path.exists():
        print(f"❌ Config not found: {config_path}")
        return

    # Check if article.md exists
    article_md = test_article_path / "article.md"
    if not article_md.exists():
        print(f"❌ article.md not found: {article_md}")
        print("   Social media generation requires a published article.")
        return

    print(f"📄 Using article: {test_article_path}")
    print(f"   Article file: {article_md}")

    # Load article
    article_config = ArticleConfig.from_yaml(config_path)
    article = Article(path=test_article_path, config=article_config)

    # Create dependencies
    project_root = Path.cwd()
    factory = DependencyFactory(project_root)
    deps = factory.create_deps('claude')  # Use Claude for generation

    # Execute social media generation
    try:
        print(f"\n🔄 Generating social media posts...")
        article = execute_social_media(article, deps, {})

        # Read generated markdown file
        social_media_file = test_article_path / "social_media.md"
        if social_media_file.exists():
            with open(social_media_file, 'r', encoding='utf-8') as f:
                content = f.read()

            print(f"\n✅ Social media posts generated successfully!")
            print(f"\n📁 File saved: {social_media_file}")
            print(f"\n" + "=" * 60)
            print("CONTENT PREVIEW:")
            print("=" * 60)
            print(content)
            print("=" * 60)

        else:
            print(f"❌ social_media.md not created")

    except Exception as e:
        print(f"❌ Error: {e}")
        import traceback
        traceback.print_exc()


if __name__ == '__main__':
    test_social_media_generation()
