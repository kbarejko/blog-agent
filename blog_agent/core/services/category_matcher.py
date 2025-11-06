"""
Category Matcher

Helps AI select appropriate categories for articles.
"""
from typing import List, Dict, Any
from pathlib import Path

from ...infrastructure.yaml.category_reader import CategoryReader


class CategoryMatcher:
    """Match articles to categories"""

    def __init__(self, category_reader: CategoryReader):
        """
        Initialize category matcher

        Args:
            category_reader: CategoryReader instance
        """
        self.reader = category_reader

    def get_categories_for_prompt(self) -> str:
        """
        Get formatted category list for AI prompt

        Returns:
            Formatted string with all categories
        """
        return self.reader.get_categories_for_ai()

    def validate_category_selection(
        self,
        selected_slugs: List[str],
        min_categories: int = 1,
        max_categories: int = 5
    ) -> Dict[str, Any]:
        """
        Validate category selection

        Args:
            selected_slugs: List of selected category slugs
            min_categories: Minimum required categories
            max_categories: Maximum allowed categories

        Returns:
            Validation result
        """
        issues = []

        # Check count
        if len(selected_slugs) < min_categories:
            issues.append(f"Too few categories: {len(selected_slugs)} (min {min_categories})")

        if len(selected_slugs) > max_categories:
            issues.append(f"Too many categories: {len(selected_slugs)} (max {max_categories})")

        # Validate slugs exist
        valid_slugs, invalid_slugs = self.reader.validate_categories(selected_slugs)

        if invalid_slugs:
            issues.append(f"Invalid category slugs: {', '.join(invalid_slugs)}")

        return {
            'valid': len(issues) == 0,
            'issues': issues,
            'valid_slugs': valid_slugs,
            'invalid_slugs': invalid_slugs
        }

    def get_category_details(self, slugs: List[str]) -> List[Dict[str, Any]]:
        """
        Get detailed info for category slugs

        Args:
            slugs: List of category slugs

        Returns:
            List of category details
        """
        details = []

        for slug in slugs:
            cat = self.reader.get_category(slug)
            if cat:
                details.append(cat)

        return details

    def suggest_similar_categories(self, keywords: List[str], limit: int = 5) -> List[Dict[str, Any]]:
        """
        Suggest categories based on keywords

        Args:
            keywords: List of keywords to search
            limit: Maximum suggestions per keyword

        Returns:
            List of suggested categories
        """
        suggestions = []
        seen_slugs = set()

        for keyword in keywords:
            results = self.reader.search_categories(keyword, limit=limit)

            for cat in results:
                if cat['slug'] not in seen_slugs:
                    suggestions.append(cat)
                    seen_slugs.add(cat['slug'])

        return suggestions[:limit * 2]  # Return up to limit*2 total suggestions

    def format_categories_for_yaml(self, slugs: List[str]) -> Dict[str, Any]:
        """
        Format categories for saving to article's categories.yaml

        Args:
            slugs: Category slugs

        Returns:
            Dict ready for YAML serialization
        """
        categories_data = []

        for slug in slugs:
            cat = self.reader.get_category(slug)
            if cat:
                categories_data.append({
                    'slug': slug,
                    'title': cat['title'],
                    'path': cat['path']
                })

        return {
            'categories': categories_data,
            'count': len(categories_data)
        }
