"""
Step 2: Generate Article Outline

Generates outline.md with AI deciding on optional sections (Checklist, FAQ).
"""
from typing import Dict, Any
import re

from ...domain.article import Article
from ...domain.value_objects import Outline


def execute_outline(
    article: Article,
    deps: Dict[str, Any],
    config: Dict[str, Any]
) -> Article:
    """
    Generate article outline

    Uses prompt_konspekt_artykulu.md to generate outline.
    AI decides whether to include Checklist and/or FAQ sections.

    Args:
        article: Article
        deps: Dependencies (ai, prompts, storage, git)
        config: Step configuration

    Returns:
        Article with outline set
    """
    ai = deps['ai']
    prompts = deps['prompts']
    storage = deps['storage']
    git = deps['git']

    # Load and render prompt
    series, silo, slug = article.get_series_silo_slug()
    prompt = prompts.load_and_render(
        "konspekt/prompt_konspekt_artykulu.md",
        {
            'TEMAT_ARTYKULU': article.config.title,
            'TARGET_AUDIENCE': article.config.target_audience,
            'URL_ARTYKULU': f"/artykuly/{series}/{silo}/{slug}",
            'KONTEKST_TEMATU': f"Artykuł dla {article.config.target_audience.lower()}. Ton: {article.config.tone}",
        }
    )
    print("🔄 Generating outline...")

    # Generate outline with AI
    response = ai.generate(prompt, max_tokens=2000)

    # Parse outline from response
    outline = _parse_outline_from_response(response)

    # Set outline on article
    article.set_outline(outline)

    # Save outline.md
    outline_path = article.get_outline_path()
    storage.write_file(outline_path, outline.to_markdown())

    print(f"✅ Outline created: {len(outline.sections)} sections")
    if outline.has_checklist:
        print("   - Includes: Checklist")
    if outline.has_faq:
        print("   - Includes: FAQ")

    # Git commit
    series, silo, slug = article.get_series_silo_slug()
    git.commit_article_stage(
        article.path,
        "outline",
        f"Create outline ({len(outline.sections)} sections)"
    )

    return article


def _parse_outline_from_response(response: str) -> Outline:
    """
    Parse outline from AI response

    Expected format:
    ## 1. Section Title
    Description...

    ## 2. Another Section
    Description...

    OPCJONALNE SEKCJE:
    - Checklist: TAK/NIE
    - FAQ: TAK/NIE

    Args:
        response: AI response

    Returns:
        Outline value object
    """
    sections = []
    has_checklist = False
    has_faq = False

    lines = response.split('\n')
    current_section = None

    for line in lines:
        line = line.strip()

        # Check for section heading (## N. Title)
        section_match = re.match(r'^##\s+(\d+)\.\s+(.+)$', line)
        if section_match:
            # Save previous section
            if current_section:
                sections.append(current_section)

            # Start new section
            section_num = section_match.group(1)
            section_title = section_match.group(2).strip()
            current_section = {
                'title': section_title,
                'description': ''
            }
            continue

        # Check for optional sections markers
        if 'Checklist:' in line and ('TAK' in line.upper() or 'YES' in line.upper()):
            has_checklist = True
        if 'FAQ:' in line and ('TAK' in line.upper() or 'YES' in line.upper()):
            has_faq = True

        # Add to current section description
        if current_section and line and not line.startswith('#'):
            if current_section['description']:
                current_section['description'] += ' '
            current_section['description'] += line

    # Save last section
    if current_section:
        sections.append(current_section)

    # Estimate word count (300-400 per section)
    estimated_words = len(sections) * 350

    return Outline(
        sections=sections,
        has_checklist=has_checklist,
        has_faq=has_faq,
        estimated_word_count=estimated_words
    )
