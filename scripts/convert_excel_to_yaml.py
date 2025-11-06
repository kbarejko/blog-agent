#!/usr/bin/env python3
"""
Convert kategoria-artykulow.xlsx to categories.yaml

Reads Excel with hierarchical categories and converts to YAML format
that is git-friendly and human-readable.
"""

import openpyxl
import yaml
from pathlib import Path
from typing import Dict, List, Optional


def load_categories_from_excel(excel_path: Path) -> Dict[str, Dict]:
    """
    Load categories from Excel into flat dict

    Returns:
        Dict[slug, category_data]
    """
    wb = openpyxl.load_workbook(excel_path)
    sheet = wb.active

    categories = {}
    title_to_slug = {}  # Map title -> slug for parent lookup

    # First pass: load all categories and build title->slug mapping
    for row in sheet.iter_rows(min_row=2, values_only=True):
        title, slug, parent_title, article_count, url_path = row

        # Skip empty rows
        if not title or not slug:
            continue

        title_to_slug[title] = slug

        # Store parent title temporarily
        categories[slug] = {
            'slug': slug,
            'title': title,
            'description': f'Kategoria: {title}',  # Generic description
            'parent_title': parent_title,  # Temporary - will convert to slug
            'article_count': article_count or 0,
            'url': url_path,
            'keywords': []  # Placeholder for future
        }

    # Second pass: convert parent titles to slugs
    for slug, cat in categories.items():
        parent_title = cat['parent_title']

        # Handle parent (Excel uses "<Bez Element nadrzedny>" for root)
        if parent_title and parent_title != "<Bez Element nadrzedny>":
            parent_slug = title_to_slug.get(parent_title)
            cat['parent'] = parent_slug
        else:
            cat['parent'] = None

        # Remove temporary field
        del cat['parent_title']

    return categories


def build_hierarchy(categories: Dict[str, Dict]) -> List[Dict]:
    """
    Build hierarchical structure from flat category dict

    Returns:
        List of root categories with nested children
    """
    # Create a mapping of slug -> category (with children list)
    cat_map = {}
    for slug, cat in categories.items():
        cat_copy = cat.copy()
        cat_copy['children'] = []
        cat_map[slug] = cat_copy

    # Build parent-child relationships
    root_categories = []

    for slug, cat in cat_map.items():
        parent_slug = categories[slug]['parent']

        if parent_slug is None:
            # Root category
            root_categories.append(cat)
        else:
            # Child category - attach to parent
            parent = cat_map.get(parent_slug)
            if parent:
                parent['children'].append(cat)
            else:
                # Parent not found - treat as root
                root_categories.append(cat)

    # Remove empty children arrays and parent field
    def clean_categories(cats):
        for cat in cats:
            # Remove parent field (not needed in hierarchy)
            if 'parent' in cat:
                del cat['parent']

            # Clean children recursively
            if cat['children']:
                clean_categories(cat['children'])
            else:
                # Remove empty children list
                del cat['children']

    clean_categories(root_categories)

    return root_categories


def save_to_yaml(categories: List[Dict], yaml_path: Path):
    """Save hierarchical categories to YAML"""

    # Custom representer for better YAML formatting
    def represent_dict_order(dumper, data):
        return dumper.represent_mapping('tag:yaml.org,2002:map', data.items())

    yaml.add_representer(dict, represent_dict_order)

    # Prepare output structure
    output = {
        'categories': categories,
        'metadata': {
            'total_count': sum(count_categories(categories)),
            'version': '1.0',
            'source': 'Converted from kategoria-artykulow.xlsx'
        }
    }

    with open(yaml_path, 'w', encoding='utf-8') as f:
        f.write("# Categories for Digital Vantage Blog\n")
        f.write("# Auto-generated from kategoria-artykulow.xlsx\n")
        f.write("# Edit this file to add descriptions and keywords\n\n")

        yaml.dump(
            output,
            f,
            allow_unicode=True,
            default_flow_style=False,
            sort_keys=False,
            indent=2,
            width=120
        )

    print(f"✅ Saved to: {yaml_path}")


def count_categories(categories: List[Dict]) -> List[int]:
    """Count total categories recursively"""
    counts = []
    for cat in categories:
        counts.append(1)
        if 'children' in cat:
            counts.extend(count_categories(cat['children']))
    return counts


def main():
    """Main conversion function"""
    excel_path = Path("kategoria-artykulow.xlsx")
    yaml_path = Path("categories.yaml")

    print(f"📖 Reading: {excel_path}")

    # Load from Excel
    flat_categories = load_categories_from_excel(excel_path)
    print(f"   Loaded {len(flat_categories)} categories")

    # Build hierarchy
    print(f"🔄 Building hierarchy...")
    hierarchical_categories = build_hierarchy(flat_categories)
    print(f"   Found {len(hierarchical_categories)} root categories")

    # Save to YAML
    print(f"💾 Saving to YAML...")
    save_to_yaml(hierarchical_categories, yaml_path)

    # Stats
    total = sum(count_categories(hierarchical_categories))
    print(f"\n📊 Statistics:")
    print(f"   Total categories: {total}")
    print(f"   Root categories: {len(hierarchical_categories)}")
    print(f"   YAML size: {yaml_path.stat().st_size / 1024:.1f} KB")
    print(f"\n✅ Conversion complete!")


if __name__ == "__main__":
    main()
