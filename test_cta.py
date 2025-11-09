#!/usr/bin/env python3
"""
Quick test script for CTA step
"""
from pathlib import Path
from blog_agent.core.domain.article import Article
from blog_agent.core.domain.config import ArticleConfig
from blog_agent.core.workflow.engine import WorkflowEngine
from blog_agent.core.factory import DependencyFactory

# Paths
project_root = Path.cwd()
config_path = project_root / "artykuly/test/final/complete-workflow/config.yaml"
article_path = config_path.parent

# Load article config
article_config = ArticleConfig.from_yaml(config_path)

# Create article
article = Article(path=article_path, config=article_config)

print(f"🧪 Testing CTA step for: {article.config.title}")
print(f"   Path: {article_path}\n")

# Load existing data
article_md = article.get_article_path()
if article_md.exists():
    with open(article_md, 'r', encoding='utf-8') as f:
        article.final_content = f.read()
    print(f"✅ Loaded article.md ({len(article.final_content)} chars)")
else:
    print(f"❌ article.md not found!")
    exit(1)

# Load business metadata if exists
business_metadata_path = article_path / "business_metadata.yaml"
if business_metadata_path.exists():
    import yaml
    with open(business_metadata_path, 'r', encoding='utf-8') as f:
        metadata_dict = yaml.safe_load(f)
        # You would normally deserialize this properly, but for testing we'll skip
        print(f"✅ Found business_metadata.yaml")

# Create factory and deps
factory = DependencyFactory(project_root)
deps = factory.create_deps('claude')

# Create workflow engine
workflow_config_path = factory.get_workflow_config_path()
engine = WorkflowEngine(workflow_config_path)

# Execute ONLY CTA step
print("\n" + "="*60)
print("🚀 Running CTA step...")
print("="*60 + "\n")

try:
    article = engine.execute_single_step('cta', article, deps)
    print("\n" + "="*60)
    print("✅ CTA step completed successfully!")
    print("="*60)
    print(f"\nCTA section added to: {article.get_article_path()}")

except Exception as e:
    print("\n" + "="*60)
    print(f"❌ CTA step failed: {str(e)}")
    print("="*60)
    import traceback
    traceback.print_exc()
    exit(1)
