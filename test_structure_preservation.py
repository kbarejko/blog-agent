"""
Test structure preservation in section generation

This will generate a test section to verify that H3 headers and bullet points
from the outline are preserved in the generated content.
"""
from pathlib import Path
from blog_agent.core.domain.config import ArticleConfig
from blog_agent.core.domain.article import Article
from blog_agent.core.factory import DependencyFactory
from blog_agent.infrastructure.storage.file_storage import FileStorage


def test_structure_preservation():
    """Test that H3 and structure from outline are preserved"""

    print("=" * 60)
    print("Testing Structure Preservation in Section Generation")
    print("=" * 60)

    # Use UX/UI article as test case
    article_path = Path("artykuly/ecommerce/ux-ui")
    config_path = article_path / "config.yaml"

    if not config_path.exists():
        print(f"❌ Article not found: {article_path}")
        return

    # Load article
    article_config = ArticleConfig.from_yaml(config_path)
    article = Article(path=article_path, config=article_config)

    # Load outline
    storage = FileStorage()
    outline_path = article_path / "outline.md"
    outline_text = storage.read_file(outline_path)

    # Parse outline
    from blog_agent.core.workflow.steps.step_02_outline import _parse_outline_from_response
    outline = _parse_outline_from_response(outline_text)
    article.outline = outline

    # Check section 2 (index 1) - it has H3 headers
    section_index = 1
    section = outline.sections[section_index]

    print(f"\n📋 Outline Structure for Section {section_index + 1}:")
    print(f"Title: {section['title']}")
    print(f"\nDescription from outline:")
    print("-" * 60)
    print(section['description'][:500] + "..." if len(section['description']) > 500 else section['description'])
    print("-" * 60)

    # Check if H3 present in description
    h3_count = section['description'].count('###')
    print(f"\n✓ H3 headers in outline: {h3_count}")

    # Create dependencies
    project_root = Path.cwd()
    factory = DependencyFactory(project_root)

    # Ask user which provider to use
    print(f"\n🤖 This will generate Section {section_index + 1} using AI.")
    print(f"   Current section file: {article_path}/sections/0{section_index + 1}-section.md")
    print(f"\n   ⚠️  This will cost API tokens!")

    response = input("\n   Continue? (yes/no): ")
    if response.lower() not in ['yes', 'y']:
        print("Aborted.")
        return

    print("\n🔄 Generating section with structure enforcement...")

    # Use claude provider
    deps = factory.create_deps('claude')

    # Generate section using updated prompts
    from blog_agent.core.workflow.steps._section_writer import write_section_with_review

    # Mock previous sections if needed
    if section_index > 0:
        # Load existing sections
        article.sections = []
        for i in range(section_index):
            section_file = article_path / "sections" / f"0{i + 1}-section.md"
            if section_file.exists():
                content = storage.read_file(section_file)
                article.sections.append(content)

    # Generate the section
    generated_content = write_section_with_review(article, section_index, deps, max_retries=2)

    print(f"\n✅ Section generated!")
    print(f"\n📄 Generated Content (first 800 chars):")
    print("=" * 60)
    print(generated_content[:800] + "..." if len(generated_content) > 800 else generated_content)
    print("=" * 60)

    # Check if H3 present in generated content
    generated_h3_count = generated_content.count('###')
    print(f"\n📊 Analysis:")
    print(f"   H3 in outline: {h3_count}")
    print(f"   H3 in generated: {generated_h3_count}")

    if generated_h3_count >= h3_count:
        print(f"   ✅ SUCCESS: H3 headers preserved!")
    else:
        print(f"   ❌ FAIL: H3 headers missing ({generated_h3_count}/{h3_count})")
        print(f"\n   Expected H3:")
        import re
        expected_h3 = re.findall(r'### (.+)', section['description'])
        for h3 in expected_h3:
            present = h3 in generated_content or h3.lower() in generated_content.lower()
            status = "✓" if present else "✗"
            print(f"   {status} {h3}")

    # Ask if user wants to save
    print(f"\n💾 Save generated section to {article_path}/sections/0{section_index + 1}-section-NEW.md?")
    response = input("   (yes/no): ")
    if response.lower() in ['yes', 'y']:
        output_path = article_path / "sections" / f"0{section_index + 1}-section-NEW.md"
        storage.write_file(output_path, generated_content)
        print(f"   ✅ Saved to {output_path}")


if __name__ == '__main__':
    test_structure_preservation()
