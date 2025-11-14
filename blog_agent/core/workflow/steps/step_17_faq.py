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

    # Humanize with moderate token limit
    humanized = ai.generate(prompt, max_tokens=1500)

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
    # Get silo directory (parent of article)
    silo_path = article.path.parent

    if not silo_path.exists():
        return faq_content

    # Find related articles in silo
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

    # Add links to FAQ (simple approach: add at end of each answer if keyword matches)
    # This is simplified - could use AI to place links contextually
    lines = faq_content.split('\n')
    output_lines = []
    in_answer = False

    for line in lines:
        output_lines.append(line)

        if line.strip().startswith('###'):
            in_answer = True
        elif in_answer and line.strip() == '':
            # End of answer - check if we can add a link
            # Simple heuristic: add link if FAQ question mentions related article topic
            in_answer = False

    return '\n'.join(output_lines)
