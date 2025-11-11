"""
Test Internal Linking Step (Step 14)

Tests automatic internal linking between articles in the same silo.
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


def test_internal_linking():
    """Test internal linking step on an existing article"""
    print("🧪 Testing Step 14: Internal Linking\n")

    # Paths
    project_root = Path.cwd()
    config_path = project_root / "artykuly/test/final/complete-workflow/config.yaml"
    article_path = config_path.parent

    if not article_path.exists():
        print("❌ Test article not found")
        print(f"   Looking for: {article_path}")
        print("\nPlease create a test article first or adjust the path.")
        return False

    print(f"📂 Testing article: {article_path}")

    # Check if article.md exists
    article_md = article_path / "article.md"
    if not article_md.exists():
        print("❌ article.md not found (article not published yet)")
        print("   Internal linking requires a published article.")
        return False

    # Count articles in the same silo
    silo_path = article_path.parent
    published_count = 0
    for item in silo_path.iterdir():
        if item.is_dir() and (item / "article.md").exists():
            published_count += 1

    print(f"   Found {published_count} published articles in silo '{silo_path.name}'")

    if published_count < 2:
        print("   ⚠️  Not enough articles in silo for testing (need at least 2)")
        print("   Will test the step anyway to verify it doesn't crash.\n")
    else:
        print(f"   ✅ Sufficient articles for internal linking\n")

    # Load article config and create article
    try:
        article_config = ArticleConfig.from_yaml(config_path)
        article = Article(path=article_path, config=article_config)

        # Load article.md content
        with open(article_md, 'r', encoding='utf-8') as f:
            article.final_content = f.read()

        print(f"✅ Article loaded: {article.config.title}")
        print(f"   Path: {article.path}")
        print(f"   Series: {article.path.parts[-3]}")
        print(f"   Silo: {article.path.parts[-2]}")
        print(f"   Slug: {article.path.parts[-1]}\n")
    except Exception as e:
        print(f"❌ Failed to load article: {str(e)}")
        import traceback
        traceback.print_exc()
        return False

    # Setup dependencies
    try:
        factory = DependencyFactory(project_root)
        deps = factory.create_deps('claude')
        print("✅ Dependencies loaded\n")
    except Exception as e:
        print(f"❌ Failed to setup dependencies: {str(e)}")
        import traceback
        traceback.print_exc()
        return False

    # Read current article to check for existing links
    with open(article_md, 'r', encoding='utf-8') as f:
        original_content = f.read()

    original_link_count = original_content.count('](/')
    print(f"   Original internal links: {original_link_count}\n")

    # Execute internal linking step using WorkflowEngine
    print("=" * 60)
    print("Executing Internal Linking Step")
    print("=" * 60 + "\n")

    try:
        # Create workflow engine
        workflow_config_path = factory.get_workflow_config_path()
        engine = WorkflowEngine(workflow_config_path)

        # Execute internal_linking step
        updated_article = engine.execute_single_step('internal_linking', article, deps)

        # Read updated article
        with open(article_md, 'r', encoding='utf-8') as f:
            updated_content = f.read()

        new_link_count = updated_content.count('](/')
        added_links = new_link_count - original_link_count

        print("\n" + "=" * 60)
        print("Internal Linking Results")
        print("=" * 60)
        print(f"✅ Step completed successfully")
        print(f"   Original links: {original_link_count}")
        print(f"   New links: {new_link_count}")
        print(f"   Added: {added_links} internal links\n")

        if added_links > 0:
            print("Sample of added links:")
            # Find new links (simple approach - look for markdown links)
            import re
            links = re.findall(r'\[([^\]]+)\]\((/[^\)]+)\)', updated_content)
            for anchor, url in links[:5]:
                print(f"   → [{anchor}]({url})")

        return True

    except Exception as e:
        print(f"\n❌ Internal linking failed: {str(e)}")
        import traceback
        traceback.print_exc()
        return False


if __name__ == '__main__':
    success = test_internal_linking()

    if success:
        print("\n✅ Internal linking test completed successfully!")
        print("\nNext steps:")
        print("  - Review the updated article.md")
        print("  - Check if links are natural and contextual")
        print("  - Run full workflow test with internal linking enabled")
    else:
        print("\n❌ Internal linking test failed!")
        print("\nTroubleshooting:")
        print("  - Ensure article.md exists")
        print("  - Ensure silo has multiple published articles")
        print("  - Check ANTHROPIC_API_KEY is set")

    sys.exit(0 if success else 1)
