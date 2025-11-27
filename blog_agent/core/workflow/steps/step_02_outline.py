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

    # Build URL (handle silo articles without slug)
    if slug:
        article_url = f"/artykuly/{series}/{silo}/{slug}"
    else:
        article_url = f"/artykuly/{series}/{silo}"

    # Check if this is a silo article (no slug) to use appropriate prompt
    is_silo_article = not slug

    # Calculate suggested article structure based on target_word_count
    target_info = ""
    if article.config.target_word_count:
        # Calculate number of sections and words per section
        # For SILO articles: FAQ/Checklist are PART of target_word_count, not additional
        # For regular articles: small overhead for intro/summary
        overhead = 0 if is_silo_article else 200  # Intro/summary overhead for regular articles
        content_words = article.config.target_word_count - overhead

        # Optimal section length: 300-400 words
        optimal_section_length = 350
        suggested_sections = max(3, round(content_words / optimal_section_length))
        words_per_section = round(content_words / suggested_sections)

        if is_silo_article:
            target_info = f"\n\n**DŁUGOŚĆ ARTYKUŁU:** Docelowa długość całkowita: {article.config.target_word_count} słów. To sugestia - sam zdecyduj o optymalnej liczbie sekcji i ich długości, aby osiągnąć docelową długość. FAQ i podsumowanie wliczają się w ten limit."
        else:
            target_info = f"\n\n**DŁUGOŚĆ ARTYKUŁU:** Docelowa długość całkowita: {article.config.target_word_count} słów. Sugerowana struktura: {suggested_sections} sekcji × ~{words_per_section} słów/sekcję."

        # Show realistic estimate in console (AI will decide final structure)
        print(f"📏 Target: {article.config.target_word_count} words (AI will determine optimal section count)")

    if is_silo_article:
        # Use silo-specific prompt
        # Get list of existing articles in this silo for context
        silo_articles = _get_silo_articles(article.path)
        silo_articles_text = "\n".join([f"- {art}" for art in silo_articles]) if silo_articles else "Brak istniejących artykułów w silosie."

        prompt = prompts.load_and_render(
            "konspekt/prompt_konspekt_artykulu_silo.md",
            {
                'TEMAT_ARTYKULU': article.config.title,
                'TARGET_AUDIENCE': article.config.target_audience,
                'URL_ARTYKULU': article_url,
                'KONTEKST_TEMATU': f"Artykuł SILO dla {article.config.target_audience.lower()}. Ton: {article.config.tone}{target_info}",
                'SILO_ARTICLES': silo_articles_text,
            }
        )
    else:
        # Use standard article prompt
        prompt = prompts.load_and_render(
            "konspekt/prompt_konspekt_artykulu.md",
            {
                'TEMAT_ARTYKULU': article.config.title,
                'TARGET_AUDIENCE': article.config.target_audience,
                'URL_ARTYKULU': article_url,
                'KONTEKST_TEMATU': f"Artykuł dla {article.config.target_audience.lower()}. Ton: {article.config.tone}{target_info}",
            }
        )
    print("🔄 Generating outline...", flush=True)

    # Generate outline with AI
    # Silo articles need more tokens (more sections, FAQ required, links to articles)
    # Gemini models may need more tokens due to different tokenization
    # Note: GPT-5 token limits are auto-adjusted in OpenAIProvider
    max_tokens = 5000 if is_silo_article else 2500
    response = ai.generate(prompt, max_tokens=max_tokens)

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

    # Save outline.md (main sections only)
    outline_path = article.get_outline_path()
    storage.write_file(outline_path, outline.to_markdown())

    # Extract and save FAQ outline separately
    faq_content = _extract_faq_from_response(response)
    if faq_content:
        faq_outline_path = article.path / 'faq_outline.md'
        storage.write_file(faq_outline_path, faq_content)
        print(f"✅ FAQ outline saved to faq_outline.md")

    # Extract and save Checklist outline separately
    checklist_content = _extract_checklist_from_response(response)
    if checklist_content:
        checklist_outline_path = article.path / 'checklist_outline.md'
        storage.write_file(checklist_outline_path, checklist_content)
        print(f"✅ Checklist outline saved to checklist_outline.md")

    print(f"✅ Outline created: {len(outline.sections)} main sections")

    # Git commit
    series, silo, slug = article.get_series_silo_slug()
    git.commit_article_stage(
        article.path,
        "outline",
        f"Create outline ({len(outline.sections)} sections)"
    )

    return article


def _get_silo_articles(silo_path) -> list[str]:
    """
    Get list of existing articles in the silo

    Args:
        silo_path: Path to the silo directory

    Returns:
        List of article titles with their slugs
    """
    from pathlib import Path
    import yaml

    articles = []

    # Iterate through subdirectories in the silo
    for subdir in silo_path.iterdir():
        if not subdir.is_dir():
            continue

        # Skip special directories
        if subdir.name in ['sections', '__pycache__', '.git']:
            continue

        # Check if this is an article directory
        # An article should have at least one of: config.yaml, article.md, outline.md
        config_path = subdir / 'config.yaml'
        article_path = subdir / 'article.md'
        outline_path = subdir / 'outline.md'

        is_article = config_path.exists() or article_path.exists() or outline_path.exists()

        if not is_article:
            continue

        # Try to get title from config.yaml first
        title = None
        if config_path.exists():
            try:
                with open(config_path, 'r', encoding='utf-8') as f:
                    config = yaml.safe_load(f)
                    title = config.get('title')
            except Exception:
                pass

        # If no title from config, try to extract from article.md H1
        if not title and article_path.exists():
            try:
                with open(article_path, 'r', encoding='utf-8') as f:
                    for line in f:
                        line = line.strip()
                        if line.startswith('# '):
                            title = line[2:].strip()
                            break
            except Exception:
                pass

        # If still no title, use directory name
        if not title:
            title = subdir.name.replace('-', ' ').title()

        # Format: "Title (slug)"
        articles.append(f"{title} (/{subdir.name})")

    return sorted(articles)


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
            # Add to description with proper formatting
            if current_section['description']:
                current_section['description'] += '\n'
            current_section['description'] += original_line.rstrip()
            continue

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

    # Extract target word counts from descriptions (format: "(~200 słów)")
    # and calculate total estimated words
    total_target_words = 0
    for section in sections:
        desc = section.get('description', '')
        # Try to extract target words: (~200 słów), (200 słów), (~200), etc.
        target_match = re.search(r'\(~?(\d+)(?:\s*słów?)?\)', desc)
        if target_match:
            target_words = int(target_match.group(1))
            section['target_words'] = target_words
            total_target_words += target_words
        else:
            # No explicit target - use default 300
            section['target_words'] = 300
            total_target_words += 300

    # Use total_target_words if available, otherwise estimate
    estimated_words = total_target_words if total_target_words > 0 else len(sections) * 350

    return Outline(
        sections=sections,
        estimated_word_count=estimated_words
    )


def _extract_faq_from_response(response: str) -> str:
    """
    Extract FAQ section from outline response

    Looks for FAQ H2 section or series of H3 questions starting with ### 1. ?

    Args:
        response: Full outline response

    Returns:
        FAQ content as markdown (questions with description points) or empty string if not found
    """
    import re

    lines = response.split('\n')
    faq_lines = []
    in_faq = False

    for line in lines:
        line_stripped = line.strip()
        line_lower = line_stripped.lower()

        # Detect FAQ start - either H2 with FAQ keywords or ### 1. with question mark
        if not in_faq:
            # Check for H2 FAQ section
            if line_stripped.startswith('##') and any(keyword in line_lower for keyword in ['faq', 'najczęściej zadawane', 'pytania']):
                in_faq = True
                continue  # Skip the H2 header itself

            # Check for ### 1. Question? (FAQ without H2 header)
            if re.match(r'^###\s*1[\.\)]\s*.*\?', line_stripped):
                in_faq = True

        if in_faq:
            # Stop if we hit another H2 (next main section) - but not H3!
            if line_stripped.startswith('##') and not line_stripped.startswith('###'):
                break

            # Stop if we hit checklist checkbox items
            if line_stripped.startswith('- ['):
                break

            # Add all FAQ content (H3 questions and bullet points)
            faq_lines.append(line)

    if not faq_lines:
        return ""

    # Clean up and return
    faq_content = '\n'.join(faq_lines).strip()

    if not faq_content:
        return ""

    # Add header
    faq_content = "# FAQ Outline\n\n" + faq_content

    return faq_content


def _extract_checklist_from_response(response: str) -> str:
    """
    Extract Checklist section from outline response

    Looks for checklist checkbox items (- [ ] or - [x])

    Args:
        response: Full outline response

    Returns:
        Checklist content as markdown (checkbox list) or empty string if not found
    """
    lines = response.split('\n')
    checklist_lines = []
    in_checklist = False
    checklist_started = False

    for i, line in enumerate(lines):
        line_stripped = line.strip()
        line_lower = line_stripped.lower()

        # Detect Checklist start - H2 with checklist keywords
        if not in_checklist:
            if line_stripped.startswith('##') and any(keyword in line_lower for keyword in ['checklist', 'lista kontrolna', 'check list']):
                in_checklist = True
                checklist_started = True
                continue  # Skip the H2 header

        # Also detect by checkbox pattern (- [ ] or - [x])
        if not in_checklist and (line_stripped.startswith('- [ ]') or line_stripped.startswith('- [x]')):
            in_checklist = True
            checklist_started = True

        if in_checklist:
            # Stop if we hit another H2
            if line_stripped.startswith('##'):
                break

            # Add checklist items (checkboxes and description text)
            # Include checkbox items and any description lines between them
            if line_stripped.startswith('- [') or (checklist_lines and line_stripped and not line_stripped.startswith('#')):
                checklist_lines.append(line)

    if not checklist_started:
        return ""

    # Clean up and return
    checklist_content = '\n'.join(checklist_lines).strip()

    if not checklist_content:
        return ""

    # Add header if not present
    if not checklist_content.startswith('#'):
        checklist_content = "# Checklist Outline\n\n" + checklist_content

    return checklist_content
