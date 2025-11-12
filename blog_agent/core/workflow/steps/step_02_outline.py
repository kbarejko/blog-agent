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
    print("🔄 Generating outline...", flush=True)

    # Generate outline with AI
    response = ai.generate(prompt, max_tokens=2000)

    # Parse outline from response
    outline = _parse_outline_from_response(response)

    # If no sections found, save raw response for debugging
    if len(outline.sections) == 0:
        print("⚠️  Warning: No sections parsed from AI response")
        print(f"   Response length: {len(response)} chars")
        print(f"   First 500 chars: {response[:500]}")
        # Save raw response to outline.md as fallback
        outline_path = article.get_outline_path()
        storage.write_file(outline_path, f"# Konspekt artykułu\n\n{response}")
        raise ValueError("Could not parse outline sections from AI response. Raw response saved to outline.md for debugging.")

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
        original_line = line
        line = line.strip()

        # Check for H2 section heading - multiple formats:
        # 1. ## N. Title (numbered with dot)
        # 2. ## N Title (numbered without dot)
        # 3. ## Title (no number)
        section_match = None
        section_title = None
        
        # Try numbered with dot: ## 1. Title
        match = re.match(r'^##\s+(\d+)\.\s+(.+)$', line)
        if match:
            section_match = match
            section_title = match.group(2).strip()
        else:
            # Try numbered without dot: ## 1 Title
            match = re.match(r'^##\s+(\d+)\s+(.+)$', line)
            if match:
                section_match = match
                section_title = match.group(2).strip()
            else:
                # Try unnumbered H2: ## Title (but skip if it's FAQ/Checklist)
                match = re.match(r'^##\s+(.+)$', line)
                if match:
                    title_candidate = match.group(1).strip()
                    title_lower = title_candidate.lower()
                    # Skip meta sections
                    if not any(keyword in title_lower for keyword in ['checklist', 'faq', 'opcjonalne', 'optional', 'zawiera', 'contains', 'najczęściej zadawane']):
                        section_match = match
                        section_title = title_candidate
        
        if section_match and section_title:
            # Save previous section
            if current_section:
                sections.append(current_section)

            # Start new section
            current_section = {
                'title': section_title,
                'description': ''
            }
            continue

        # H3 and H4 are part of the description, not new sections
        # Check if line is H3 or H4 and add to current section description
        if current_section:
            if line.startswith('###') or line.startswith('####'):
                # H3/H4 as part of description - keep formatting
                if current_section['description']:
                    current_section['description'] += '\n\n'
                current_section['description'] += original_line.rstrip()
                continue

        # Check for checklist items (lines starting with [ ] or - [ ])
        if current_section and (line.startswith('[ ]') or line.startswith('- [ ]')):
            has_checklist = True
            # Add to description with proper formatting
            if current_section['description']:
                current_section['description'] += '\n'
            current_section['description'] += original_line.rstrip()
            continue

        # Check for FAQ markers (sections with question format or FAQ keyword)
        if 'FAQ' in line.upper() or re.match(r'^\d+\.\s+.*\?', line):
            has_faq = True

        # Check for optional sections markers in text
        if 'Checklist:' in line and ('TAK' in line.upper() or 'YES' in line.upper()):
            has_checklist = True
        if 'FAQ:' in line and ('TAK' in line.upper() or 'YES' in line.upper()):
            has_faq = True

        # Add to current section description
        # Preserve line breaks for lists and formatting
        if current_section and line and not line.startswith('#'):
            # If line starts with - or * (list item), preserve newline
            if line.startswith('- ') or line.startswith('* ') or line.startswith('1.') or line.startswith('1)'):
                if current_section['description']:
                    current_section['description'] += '\n'
                current_section['description'] += original_line.rstrip()
            else:
                # Regular text - add space if description exists
                if current_section['description'] and not current_section['description'].endswith('\n'):
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
