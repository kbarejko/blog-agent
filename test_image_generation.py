"""
Test Image Generation (Step 15)

Tests DALL-E image generation from multimedia prompts.
"""
import sys
import os
from pathlib import Path

# Add project to path
sys.path.insert(0, str(Path(__file__).parent))

from blog_agent.core.domain.article import Article
from blog_agent.core.domain.config import ArticleConfig
from blog_agent.core.factory import DependencyFactory
from blog_agent.core.workflow.engine import WorkflowEngine


def test_image_generation():
    """Test image generation step on an existing article"""
    print("🧪 Testing Step 15: Image Generation\n")

    # Check for OPENAI_API_KEY
    api_key = os.getenv('OPENAI_API_KEY')
    if not api_key:
        print("❌ OPENAI_API_KEY not set in environment")
        print("\nTo test image generation:")
        print("1. Get API key from https://platform.openai.com/api-keys")
        print("2. Set environment variable:")
        print("   export OPENAI_API_KEY='sk-...'")
        print("3. Enable step in workflow.yaml (set enabled: true)")
        print("\nNote: DALL-E 3 costs $0.04-0.12 per image")
        return False

    print(f"✅ API key found: {api_key[:10]}...{api_key[-4:]}\n")

    # Paths
    project_root = Path.cwd()
    config_path = project_root / "artykuly/test/final/complete-workflow/config.yaml"
    article_path = config_path.parent

    if not article_path.exists():
        print("❌ Test article not found")
        print(f"   Looking for: {article_path}")
        return False

    # Check if multimedia.json exists
    multimedia_path = article_path / "multimedia.json"
    if not multimedia_path.exists():
        print("❌ multimedia.json not found")
        print("   Run the workflow up to step 8 (multimedia) first:")
        print("   blog-agent create --config path.yaml --only outline,summary,write_sections,create_draft,seo_review,humanize,multimedia")
        return False

    print(f"📂 Testing article: {article_path}")
    print(f"✅ multimedia.json found\n")

    # Load article config and create article
    try:
        article_config = ArticleConfig.from_yaml(config_path)
        article = Article(path=article_path, config=article_config)

        print(f"✅ Article loaded: {article.config.title}")
        print(f"   Path: {article.path}\n")
    except Exception as e:
        print(f"❌ Failed to load article: {str(e)}")
        import traceback
        traceback.print_exc()
        return False

    # Setup dependencies
    try:
        factory = DependencyFactory(project_root)
        deps = factory.create_deps('claude')  # Provider doesn't matter for image generation

        if not deps.get('image_generator'):
            print("❌ Image generator not available in dependencies")
            print("   Check OPENAI_API_KEY is set correctly")
            return False

        print("✅ Dependencies loaded")
        print(f"   Image generator: Available\n")
    except Exception as e:
        print(f"❌ Failed to setup dependencies: {str(e)}")
        import traceback
        traceback.print_exc()
        return False

    # Execute image generation step
    print("=" * 60)
    print("Executing Image Generation Step")
    print("=" * 60 + "\n")

    try:
        # Create workflow engine
        workflow_config_path = factory.get_workflow_config_path()
        engine = WorkflowEngine(workflow_config_path)

        # Execute generate_images step
        updated_article = engine.execute_single_step('generate_images', article, deps)

        # Check results
        images_dir = article_path / "images"
        if images_dir.exists():
            image_files = list(images_dir.glob("*.png"))
            print(f"\n✅ Images directory created: {len(image_files)} images")
            for img in image_files:
                size_kb = img.stat().st_size / 1024
                print(f"   → {img.name} ({size_kb:.1f} KB)")
        else:
            print(f"\nℹ️  No images directory created (may have been skipped)")

        return True

    except Exception as e:
        print(f"\n❌ Image generation failed: {str(e)}")
        import traceback
        traceback.print_exc()
        return False


def show_cost_info():
    """Show DALL-E pricing information"""
    print("\n" + "=" * 60)
    print("DALL-E 3 Pricing")
    print("=" * 60 + "\n")

    print("Standard Quality (1024x1024): $0.040 per image")
    print("Standard Quality (1792x1024): $0.080 per image")
    print("HD Quality (1024x1024):       $0.080 per image")
    print("HD Quality (1792x1024):       $0.120 per image")

    print("\nFor typical blog article:")
    print("  Hero image + 4-6 section images = 5-7 images")
    print("  Cost (standard 1792x1024): ~$0.40-0.56 per article")
    print("  Cost (HD 1792x1024):       ~$0.60-0.84 per article")

    print("\nDALL-E 2 (cheaper alternative):")
    print("  1024x1024: $0.020 per image")
    print("  Cost per article: ~$0.10-0.14")
    print("\nTo use DALL-E 2, set model: 'dall-e-2' in workflow.yaml")


if __name__ == '__main__':
    # Show cost info first
    show_cost_info()

    print("\n" + "=" * 60)
    print("Testing Image Generation")
    print("=" * 60 + "\n")

    success = test_image_generation()

    if success:
        print("\n✅ Image generation test completed successfully!")
        print("\nNext steps:")
        print("  - Review generated images in images/ folder")
        print("  - Check updated multimedia.json for local_path fields")
        print("  - Enable step in workflow.yaml if satisfied with results")
        print("  - Run: blog-agent create --config path.yaml --only generate_images")
    else:
        print("\n❌ Image generation test failed!")
        print("\nTroubleshooting:")
        print("  - Ensure OPENAI_API_KEY is set correctly")
        print("  - Ensure multimedia.json exists (run step 8 first)")
        print("  - Check API key has billing enabled")
        print("  - See cost info above for pricing")

    sys.exit(0 if success else 1)
