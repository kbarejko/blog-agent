"""
Category Reader

Reads categories from YAML file.
"""
from pathlib import Path
from typing import List, Dict, Any, Optional
import yaml


class CategoryReader:
    """Read and search categories from YAML"""

    def __init__(self, yaml_path: Path):
        """
        Initialize category reader

        Args:
            yaml_path: Path to categories.yaml
        """
        self.yaml_path = yaml_path
        self._categories: Optional[List[Dict[str, Any]]] = None
        self._flat_categories: Optional[Dict[str, Dict[str, Any]]] = None

    def load(self) -> None:
        """Load categories from YAML file"""
        with open(self.yaml_path, 'r', encoding='utf-8') as f:
            data = yaml.safe_load(f)

        self._categories = data.get('categories', [])
        self._flat_categories = self._flatten_categories(self._categories)

    def _flatten_categories(self, categories: List[Dict[str, Any]], parent_path: str = "") -> Dict[str, Dict[str, Any]]:
        """
        Flatten hierarchical categories to dict

        Args:
            categories: List of category dicts
            parent_path: Parent category path (for building full path)

        Returns:
            Dict[slug, category_data]
        """
        flat = {}

        for cat in categories:
            slug = cat['slug']
            title = cat['title']

            # Build full path for nested categories
            full_path = f"{parent_path}/{slug}" if parent_path else slug

            # Store category with metadata
            flat[slug] = {
                'slug': slug,
                'title': title,
                'path': full_path,
                'description': cat.get('description', ''),
                'article_count': cat.get('article_count', 0),
                'url': cat.get('url', slug),
                'keywords': cat.get('keywords', [])
            }

            # Recursively flatten children
            if 'children' in cat:
                children_flat = self._flatten_categories(cat['children'], full_path)
                flat.update(children_flat)

        return flat

    def get_all_categories(self) -> Dict[str, Dict[str, Any]]:
        """
        Get all categories as flat dict

        Returns:
            Dict[slug, category_data]
        """
        if self._flat_categories is None:
            self.load()
        return self._flat_categories or {}

    def get_category(self, slug: str) -> Optional[Dict[str, Any]]:
        """
        Get category by slug

        Args:
            slug: Category slug

        Returns:
            Category data or None if not found
        """
        categories = self.get_all_categories()
        return categories.get(slug)

    def search_categories(self, query: str, limit: int = 10) -> List[Dict[str, Any]]:
        """
        Search categories by title or keywords

        Args:
            query: Search query
            limit: Maximum results

        Returns:
            List of matching categories
        """
        categories = self.get_all_categories()
        query_lower = query.lower()

        results = []
        for cat in categories.values():
            # Check title
            if query_lower in cat['title'].lower():
                results.append(cat)
                continue

            # Check keywords
            keywords = cat.get('keywords', [])
            if any(query_lower in kw.lower() for kw in keywords):
                results.append(cat)
                continue

            # Check description
            if query_lower in cat.get('description', '').lower():
                results.append(cat)

        return results[:limit]

    def get_categories_for_ai(self) -> str:
        """
        Get categories formatted for AI prompt

        Returns:
            Formatted string with all categories
        """
        categories = self.get_all_categories()

        lines = ["# Dostępne kategorie\n"]

        for slug, cat in sorted(categories.items(), key=lambda x: x[1]['path']):
            path = cat['path']
            title = cat['title']
            desc = cat.get('description', '')
            count = cat.get('article_count', 0)

            lines.append(f"- **{title}** (`{slug}`)")
            lines.append(f"  - Ścieżka: {path}")
            if desc:
                lines.append(f"  - Opis: {desc}")
            lines.append(f"  - Liczba artykułów: {count}")
            lines.append("")

        return "\n".join(lines)

    def get_category_count(self) -> int:
        """Get total number of categories"""
        return len(self.get_all_categories())

    def validate_categories(self, category_slugs: List[str]) -> tuple[List[str], List[str]]:
        """
        Validate category slugs

        Args:
            category_slugs: List of category slugs to validate

        Returns:
            (valid_slugs, invalid_slugs)
        """
        categories = self.get_all_categories()

        valid = []
        invalid = []

        for slug in category_slugs:
            if slug in categories:
                valid.append(slug)
            else:
                invalid.append(slug)

        return valid, invalid
