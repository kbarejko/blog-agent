#!/usr/bin/env python3
"""
Test script for steps 11-13: publish, schema, categories
"""
from pathlib import Path
import yaml
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

print(f"🧪 Testing steps 11-13 for: {article.config.title}")
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

# Load outline if exists (needed for schema step)
outline_path = article_path / "outline.md"
if outline_path.exists():
    with open(outline_path, 'r', encoding='utf-8') as f:
        outline_content = f.read()
    # Create simple outline
    sections = [{"title": "Section 1", "description": "Test section"}]
    article.outline = Outline(sections=sections, has_faq=False, has_checklist=True, estimated_word_count=3000)
    print(f"✅ Loaded outline.md")

# Create factory and deps
factory = DependencyFactory(project_root)
deps = factory.create_deps('claude')

# Create workflow engine
workflow_config_path = factory.get_workflow_config_path()
engine = WorkflowEngine(workflow_config_path)

# Test each step
steps_to_test = [
    ('publish', '11: Publish Article'),
    ('schema', '12: Schema.org Markup'),
    ('categories', '13: Assign Categories')
]

for step_name, step_desc in steps_to_test:
    print(f"\n{'='*60}")
    print(f"🚀 Running step {step_desc}")
    print(f"{'='*60}\n")

    try:
        article = engine.execute_single_step(step_name, article, deps)
        print(f"\n✅ Step {step_name} completed successfully!\n")

        # Check outputs
        if step_name == 'publish':
            print(f"   Status: {article.status}")
        elif step_name == 'schema':
            schema_path = article.get_schema_path()
            if schema_path.exists():
                print(f"   ✅ Schema file created: {schema_path}")
            else:
                print(f"   ⚠️  Schema file not found")
        elif step_name == 'categories':
            categories_path = article.get_categories_path()
            if categories_path.exists():
                with open(categories_path, 'r') as f:
                    cats = yaml.safe_load(f)
                print(f"   ✅ Categories file created: {len(cats)} categories")
            else:
                print(f"   ⚠️  Categories file not found")

    except Exception as e:
        print(f"\n❌ Step {step_name} failed: {str(e)}")
        import traceback
        traceback.print_exc()
        print(f"\n⏭️  Continuing with next step...\n")
        continue

print(f"\n{'='*60}")
print(f"✅ All steps tested!")
print(f"{'='*60}")
