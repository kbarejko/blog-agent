#!/usr/bin/env python3
"""
Test Stability AI Hero Generation
"""
import os
import sys
import time
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

# Article path
article_path = project_root / "artykuly/ecommerce/ux-ui/checkout-ux-konwersja"

print(f"🧪 Testing Stability AI (SDXL)")
print(f"Article: {article_path.name}")

# Load article
config_path = article_path / "config.yaml"
article_config = ArticleConfig.from_yaml(config_path)
article = Article(path=article_path, config=article_config)

# Create deps
factory = DependencyFactory(project_root)
deps = factory.create_deps(provider_name='claude')

# Check API key
if not os.getenv('STABILITY_API_KEY'):
    print(f"❌ STABILITY_API_KEY not set!")
    sys.exit(1)

print(f"✅ Stability key loaded")

# Generate
from blog_agent.core.workflow.steps.step_15_generate_images import execute_generate_images

config = {
    'provider': 'stability',
    'model': 'sdxl',
    'width': 1024,
    'height': 1024,
    'skip_existing': False
}

start = time.time()
article = execute_generate_images(article, deps, config)
duration = time.time() - start

print(f"\n⏱️  Time: {duration:.1f}s")
print(f"💰 Cost: $0.011")
