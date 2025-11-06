"""
Step 1: Initialize Article Structure

Creates folder structure and config.yaml.
"""
from typing import Dict, Any
from pathlib import Path

from ...domain.article import Article
from ...domain.config import ArticleConfig


def execute_init(
    article: Article,
    deps: Dict[str, Any],
    config: Dict[str, Any]
) -> Article:
    """
    Initialize article structure

    Creates:
    - Article directory
    - config.yaml
    - sections/ subdirectory

    Args:
        article: Article (with path and config)
        deps: Dependencies (storage, etc.)
        config: Step configuration

    Returns:
        Article (unchanged, just creates structure)
    """
    storage = deps['storage']

    # Create article directory
    storage.create_dir(article.path)

    # Create sections directory
    storage.create_dir(article.get_sections_dir())

    # Save config.yaml
    article.config.save(article.get_config_path())

    print(f"✅ Initialized article structure at: {article.path}")
    print(f"   - config.yaml")
    print(f"   - sections/")

    return article
