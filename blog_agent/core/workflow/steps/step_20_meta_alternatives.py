"""
Step 20: Meta Alternatives

Generates 2-3 alternative proposals for meta title and meta description.
Uses cheap AI model (gemini-flash or gpt-4o-mini) for cost optimization.
"""
from typing import Dict, Any
from pathlib import Path

from ...domain.article import Article


def execute_meta_alternatives(
    article: Article,
    deps: Dict[str, Any],
    config: Dict[str, Any]
) -> Article:
    """
    Generate 2-3 alternative proposals for meta title and meta description

    This step runs after the article is finalized and provides SEO optimization
    alternatives for the meta tags. It's useful for A/B testing and choosing
    the best meta tags for click-through rate optimization.

    Args:
        article: Article (must have final content and SEO data)
        deps: Dependencies (ai, prompts, storage)
        config: Step configuration

    Returns:
        Article (unchanged, alternatives saved to file)
    """
    if not article.final_content:
        raise ValueError("Article must be finalized before generating meta alternatives")

    if not article.seo_data:
        raise ValueError("SEO data must exist before generating alternatives")

    ai = deps['ai']
    prompts = deps['prompts']
    storage = deps['storage']

    print("🔄 Generating meta alternatives...")

    # Get current meta title and description
    current_meta_title = article.seo_data.meta_title
    current_meta_description = article.seo_data.meta_description

    # Limit content length for context (first 3000 chars is enough)
    content_preview = article.final_content[:3000]

    # Load and render prompt
    prompt = prompts.load_and_render(
        "audyt/prompt_meta_alternatives.md",
        {
            'TYTUL_ARTYKULU': article.config.title,
            'CURRENT_META_TITLE': current_meta_title,
            'CURRENT_META_DESCRIPTION': current_meta_description,
            'ARTICLE_CONTENT': content_preview,
        }
    )

    # Generate alternatives with cheap model (defined in workflow.yaml)
    # Typically gemini-flash or gpt-4o-mini for cost optimization
    try:
        response = ai.generate(prompt, max_tokens=800)

        # Parse and validate alternatives
        alternatives = _parse_alternatives(response)

        if not alternatives or len(alternatives) < 2:
            print(f"   ⚠️  Only generated {len(alternatives)} alternatives (expected 2-3)")
            print("   Using what was generated...")
        else:
            print(f"   ✅ Generated {len(alternatives)} meta alternatives")

        # Format output
        output = _format_output(
            current_meta_title,
            current_meta_description,
            alternatives
        )

        # Save to file
        output_path = article.path / "meta_alternatives.md"
        storage.write_file(output_path, output)

        print(f"   💾 Saved to: meta_alternatives.md")

        # Display summary
        for i, alt in enumerate(alternatives, 1):
            title_len = len(alt.get('meta_title', ''))
            desc_len = len(alt.get('meta_description', ''))
            print(f"   Propozycja {i}: Title={title_len} chars, Desc={desc_len} chars")

    except Exception as e:
        print(f"   ❌ Error generating meta alternatives: {str(e)}")
        print("   Skipping step (not critical)")
        # Don't fail the workflow - this is not a critical step

    return article


def _parse_alternatives(response: str) -> list[dict]:
    """
    Parse AI response into structured alternatives

    Expected format:
    === PROPOZYCJA 1 ===
    Meta Title: ...
    Meta Description: ...
    Approach: ...
    ---
    === PROPOZYCJA 2 ===
    ...

    Args:
        response: AI response text

    Returns:
        List of alternative dicts with meta_title, meta_description, approach
    """
    alternatives = []

    # Split by proposal sections
    sections = response.split('=== PROPOZYCJA')

    for section in sections[1:]:  # Skip first empty section
        lines = section.strip().split('\n')

        meta_title = None
        meta_description = None
        approach = None

        for line in lines:
            line = line.strip()

            if line.lower().startswith('meta title:'):
                meta_title = line.split(':', 1)[1].strip()
            elif line.lower().startswith('meta description:'):
                meta_description = line.split(':', 1)[1].strip()
            elif line.lower().startswith('approach:'):
                approach = line.split(':', 1)[1].strip()

        # Only add if we have at least title and description
        if meta_title and meta_description:
            alternatives.append({
                'meta_title': meta_title,
                'meta_description': meta_description,
                'approach': approach or 'N/A'
            })

    return alternatives


def _format_output(
    current_title: str,
    current_description: str,
    alternatives: list[dict]
) -> str:
    """
    Format alternatives into readable markdown file

    Args:
        current_title: Current meta title
        current_description: Current meta description
        alternatives: List of alternative proposals

    Returns:
        Formatted markdown string
    """
    lines = [
        "# Meta Title & Description - Propozycje Alternatywne",
        "",
        "## Aktualne Meta Tags",
        "",
        f"**Meta Title:** {current_title}",
        f"- Długość: {len(current_title)} znaków",
        "",
        f"**Meta Description:** {current_description}",
        f"- Długość: {len(current_description)} znaków",
        "",
        "---",
        "",
        "## Propozycje Alternatywne",
        ""
    ]

    for i, alt in enumerate(alternatives, 1):
        title = alt['meta_title']
        description = alt['meta_description']
        approach = alt['approach']

        title_len = len(title)
        desc_len = len(description)

        # Validation indicators
        title_valid = "✅" if 50 <= title_len <= 60 else "⚠️"
        desc_valid = "✅" if 140 <= desc_len <= 160 else "⚠️"

        lines.extend([
            f"### Propozycja {i}",
            "",
            f"**Approach:** {approach}",
            "",
            f"**Meta Title:** {title}",
            f"- Długość: {title_len} znaków {title_valid}",
            "",
            f"**Meta Description:** {description}",
            f"- Długość: {desc_len} znaków {desc_valid}",
            "",
            "---",
            ""
        ])

    # Add usage notes
    lines.extend([
        "## Jak użyć tych propozycji?",
        "",
        "1. **Wybierz najlepszą propozycję** - oceń która najlepiej oddaje wartość artykułu",
        "2. **A/B testing** - możesz przetestować różne wersje aby zobaczyć która ma wyższy CTR",
        "3. **Dostosuj do audience** - wybierz wersję która najlepiej przemawia do grupy docelowej",
        "4. **Aktualizuj config.yaml** - skopiuj wybraną wersję do meta_title i meta_description",
        "",
        "## Wskaźniki jakości",
        "",
        "- ✅ = Długość OK (Meta Title: 50-60 chars, Meta Description: 140-160 chars)",
        "- ⚠️ = Długość poza zakresem (może być ucięta w wynikach wyszukiwania)",
    ])

    return '\n'.join(lines)
