"""
Step 3: Generate Article Summary

Generates "Co znajdziesz w artykule?" section with 3-5 concrete value points.
"""
from typing import Dict, Any
import re

from ...domain.article import Article
from ...domain.value_objects import Summary


def execute_summary(
    article: Article,
    deps: Dict[str, Any],
    config: Dict[str, Any]
) -> Article:
    """
    Generate article summary

    Creates "Co znajdziesz w artykule?" with 3-5 concrete points.
    NOT a table of contents - actual value points.

    Args:
        article: Article (must have outline)
        deps: Dependencies (ai, prompts, storage)
        config: Step configuration

    Returns:
        Article with summary set
    """
    if not article.outline:
        raise ValueError("Outline must be created before summary")

    ai = deps['ai']
    prompts = deps['prompts']
    storage = deps['storage']

    # Load and render prompt
    prompt = prompts.load_and_render(
        "articles/prompt_streszczenie_artykulu.md",
        {
            'TYTUL_ARTYKULU': article.config.title,
            'KONSPEKT_TRESC': article.outline.to_markdown(),
            'TARGET_AUDIENCE': article.config.target_audience,
        }
    )

    print("🔄 Generating summary...")

    # Generate summary with AI
    response = ai.generate(prompt, max_tokens=800)

    # Parse summary points
    summary = _parse_summary_from_response(response)

    # Set summary on article
    article.set_summary(summary)

    # Save to sections/00-summary.md
    summary_path = article.get_sections_dir() / "00-summary.md"
    storage.write_file(summary_path, summary.to_markdown())

    print(f"✅ Summary created: {len(summary.points)} points")

    return article


def _parse_summary_from_response(response: str) -> Summary:
    """
    Parse summary from AI response

    Expected format:
    ## Co znajdziesz w artykule?

    - Point 1
    - Point 2
    - Point 3

    Args:
        response: AI response

    Returns:
        Summary value object
    """
    points = []

    lines = response.split('\n')

    for line in lines:
        line = line.strip()

        # Check for bullet point
        if line.startswith('- ') or line.startswith('* '):
            point = line[2:].strip()
            if point:
                points.append(point)

    # If no bullet points found, try numbered list
    if not points:
        for line in lines:
            line = line.strip()
            # Match: 1. Point or 1) Point
            numbered_match = re.match(r'^\d+[\.\)]\s+(.+)$', line)
            if numbered_match:
                point = numbered_match.group(1).strip()
                if point:
                    points.append(point)

    if not points:
        raise ValueError("Could not parse summary points from AI response")

    return Summary(points=points)
