"""
Step 17: Generate FAQ

Generates FAQ section with humanization and internal linking.
Pipeline: generate → humanize question-by-question → add internal links → save
"""
from typing import Dict, Any, List, Tuple
import re

from ...domain.article import Article


def execute_faq(
    article: Article,
    deps: Dict[str, Any],
    config: Dict[str, Any]
) -> Article:
    """
    Generate, humanize, and link FAQ section

    Pipeline:
    1. Generate FAQ from outline
    2. Humanize each question+answer
    3. Add internal links to related articles
    4. Save to faq.md

    Args:
        article: Article (must have outline)
        deps: Dependencies (ai, prompts, storage)
        config: Step configuration

    Returns:
        Article with FAQ generated
    """
    if not article.outline:
        raise ValueError("Outline must exist before generating FAQ")

    ai = deps['ai']
    prompts = deps['prompts']
    storage = deps['storage']

    # Step 1: Generate FAQ
    print("🔄 Generating FAQ...")
    prompt = prompts.load_and_render(
        "faq/prompt_faq.md",
        {
            'TYTUL_ARTYKULU': article.config.title,
            'KONSPEKT_TRESC': article.outline.to_markdown(),
            'TARGET_AUDIENCE': article.config.target_audience,
        }
    )
    faq_draft = ai.generate(prompt, max_tokens=2000)

    # Step 2: Parse FAQ into questions
    questions = _parse_faq_questions(faq_draft)
    print(f"   📊 Parsed {len(questions)} questions")

    if len(questions) == 0:
        print("   ⚠️  No questions found in FAQ - saving draft as-is")
        faq_path = article.path / 'faq.md'
        storage.write_file(faq_path, faq_draft)
        return article

    # Step 3: Humanize each question
    print(f"🔄 Humanizing {len(questions)} questions...")
    humanized_questions = []
    for i, (question, answer) in enumerate(questions, 1):
        print(f"   📝 Question {i}/{len(questions)}...", end=" ", flush=True)

        qa_text = f"### {question}\n\n{answer}"
        humanized = _humanize_question(qa_text, article.config.target_audience, ai, prompts)

        humanized_questions.append(humanized)
        print("✓")

    # Step 4: Add internal links
    print("🔄 Adding internal links...")
    linked_faq = _add_internal_links_to_faq(
        "\n\n".join(humanized_questions),
        article,
        storage
    )

    # Step 5: Save final FAQ
    faq_path = article.path / 'faq.md'
    storage.write_file(faq_path, linked_faq)

    print(f"✅ FAQ saved to faq.md ({len(questions)} questions, humanized + linked)")

    # Publish recommendation
    if len(questions) >= 5:
        print(f"   📊 {len(questions)} pytań - REKOMENDACJA: Opublikuj FAQ")
    elif len(questions) >= 3:
        print(f"   📊 {len(questions)} pytań - REKOMENDACJA: Rozważ publikację")
    else:
        print(f"   📊 {len(questions)} pytań - REKOMENDACJA: Dodaj więcej pytań przed publikacją")

    return article


def _parse_faq_questions(faq_content: str) -> List[Tuple[str, str]]:
    """
    Parse FAQ into list of (question, answer) tuples

    Expects format:
    ### 1. Question?
    Answer text...

    Args:
        faq_content: FAQ markdown content

    Returns:
        List of (question, answer) tuples
    """
    questions = []
    lines = faq_content.split('\n')
    current_question = None
    current_answer = []

    for line in lines:
        line_stripped = line.strip()

        # Detect question (### with ?)
        if line_stripped.startswith('###') and '?' in line_stripped:
            # Save previous Q&A
            if current_question:
                questions.append((current_question, '\n'.join(current_answer).strip()))

            # Start new question
            # Remove ### and numbering (e.g., "### 1. Question?" → "Question?")
            current_question = re.sub(r'^###\s*\d+[\.\)]\s*', '', line_stripped)
            current_answer = []
        elif current_question:
            # Add to current answer
            current_answer.append(line)

    # Save last Q&A
    if current_question:
        questions.append((current_question, '\n'.join(current_answer).strip()))

    return questions


def _humanize_question(qa_text: str, target_audience: str, ai, prompts) -> str:
    """
    Humanize a single FAQ question+answer

    Keeps answer concise (50-70 words)

    Args:
        qa_text: Question and answer markdown (### Question\n\nAnswer)
        target_audience: Target audience for tone
        ai: AI provider
        prompts: Prompts service

    Returns:
        Humanized question+answer markdown
    """
    prompt = prompts.load_and_render(
        "audyt/prompt_sprawdz_styl.md",
        {
            'ARTICLE_CONTENT': qa_text,
            'TARGET_AUDIENCE': target_audience,
        }
    )

    # Add instruction to keep answers short
    prompt += "\n\n**WAŻNE:** Odpowiedź MUSI mieć maksymalnie 50-70 słów (2-3 zdania). Nie rozwijaj zbyt szczegółowo."

    # Humanize with limited tokens to enforce brevity
    humanized = ai.generate(prompt, max_tokens=400)

    return humanized.strip()


def _add_internal_links_to_faq(faq_content: str, article: Article, storage) -> str:
    """
    Add internal links to FAQ content

    Finds related articles in the same silo and adds contextual links

    Args:
        faq_content: FAQ content
        article: Article object
        storage: Storage service

    Returns:
        FAQ content with internal links added
    """
    # Get silo directory - articles in same silo are subdirectories of current article
    silo_path = article.path

    if not silo_path.exists():
        return faq_content

    # Find related articles in silo (subdirectories)
    related_articles = []
    for subdir in silo_path.iterdir():
        if not subdir.is_dir() or subdir == article.path:
            continue

        # Skip special directories
        if subdir.name in ['sections', '__pycache__', '.git']:
            continue

        # Check if article exists
        article_md = subdir / 'article.md'
        config_yaml = subdir / 'config.yaml'

        if article_md.exists() or config_yaml.exists():
            # Get title
            title = None
            if config_yaml.exists():
                try:
                    import yaml
                    with open(config_yaml, 'r', encoding='utf-8') as f:
                        config = yaml.safe_load(f)
                        title = config.get('title')
                except:
                    pass

            if not title:
                title = subdir.name.replace('-', ' ').title()

            related_articles.append({
                'title': title,
                'slug': subdir.name,
                'url': f"/{subdir.name}"
            })

    if not related_articles:
        return faq_content

    # Parse FAQ into questions and add relevant links
    lines = faq_content.split('\n')
    output_lines = []
    current_question = None
    current_answer_lines = []

    print(f"   📝 Processing {len(lines)} lines, {len(related_articles)} related articles")

    for line in lines:
        line_stripped = line.strip()

        # Detect question
        if line_stripped.startswith('###') and '?' in line_stripped:
            print(f"   🔍 Found question: {line_stripped[:60]}...")
            # Save previous Q&A with link
            if current_question:
                # Find best matching article for this Q&A
                qa_text = current_question + '\n' + '\n'.join(current_answer_lines)
                best_match = _find_best_article_match(qa_text, related_articles)

                # Add Q&A to output
                output_lines.append(current_question)
                output_lines.extend(current_answer_lines)

                # Add link if found
                if best_match:
                    print(f"      → Adding link to: {best_match['slug']}")
                    output_lines.append('')
                    output_lines.append(f"**Więcej:** [{best_match['title']}]({best_match['url']})")
                else:
                    print(f"      → No match found")

                output_lines.append('')  # Empty line between Q&As

            # Start new question
            current_question = line
            current_answer_lines = []
        else:
            # Add to current answer
            if current_question:
                current_answer_lines.append(line)

    # Save last Q&A
    if current_question:
        qa_text = current_question + '\n' + '\n'.join(current_answer_lines)
        best_match = _find_best_article_match(qa_text, related_articles)

        output_lines.append(current_question)
        output_lines.extend(current_answer_lines)

        if best_match:
            output_lines.append('')
            output_lines.append(f"**Więcej:** [{best_match['title']}]({best_match['url']})")

    return '\n'.join(output_lines)


def _find_best_article_match(qa_text: str, related_articles: list) -> dict:
    """
    Find best matching article for Q&A using keyword matching

    Args:
        qa_text: Question and answer text
        related_articles: List of related articles

    Returns:
        Best matching article dict or None
    """
    if not related_articles:
        return None

    qa_lower = qa_text.lower()
    best_match = None
    best_score = 0

    for article in related_articles:
        # Simple keyword matching from slug
        keywords = article['slug'].split('-')
        score = sum(1 for keyword in keywords if keyword in qa_lower)

        if score > best_score:
            best_score = score
            best_match = article

    # Only return if at least one keyword matched
    return best_match if best_score > 0 else None
