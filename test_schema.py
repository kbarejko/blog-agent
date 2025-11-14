#!/usr/bin/env python3
"""
Quick test for schema step
"""
from pathlib import Path
from blog_agent.core.domain.article import Article
from blog_agent.core.domain.config import ArticleConfig
from blog_agent.core.domain.value_objects import Outline
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

print(f"🧪 Testing schema step for: {article.config.title}\n")

# Load article.md
article_md = article.get_article_path()
with open(article_md, 'r', encoding='utf-8') as f:
    article.final_content = f.read()
print(f"✅ Loaded article.md ({len(article.final_content)} chars)")

# Create outline
sections = [{"title": "Section 1", "description": "Test"}]
article.outline = Outline(sections=sections, estimated_word_count=3000)
print(f"✅ Created outline")

# Create factory and deps
factory = DependencyFactory(project_root)
deps = factory.create_deps('claude')

# Create workflow engine
workflow_config_path = factory.get_workflow_config_path()
engine = WorkflowEngine(workflow_config_path)

# Execute schema step
print(f"\n{'='*60}")
print(f"🚀 Running schema step...")
print(f"{'='*60}\n")

try:
    article = engine.execute_single_step('schema', article, deps)
    print(f"\n✅ Schema step completed!")

    # Check output
    schema_path = article.get_schema_path()
    if schema_path.exists():
        print(f"   ✅ Schema file created: {schema_path}")
    else:
        print(f"   ⚠️  Schema file not found")

except Exception as e:
    print(f"\n❌ Schema step failed: {str(e)}")
    import traceback
    traceback.print_exc()
    exit(1)
