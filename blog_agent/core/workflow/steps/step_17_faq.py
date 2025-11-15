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

    # Step 3: Get related articles for linking
    related_articles = _find_related_articles(article, storage)

    # Step 4: Humanize each question + add contextual links
    print(f"🔄 Humanizing {len(questions)} questions + adding contextual links...")
    humanized_and_linked = []
    for i, (question, answer) in enumerate(questions, 1):
        print(f"   📝 Question {i}/{len(questions)}...", end=" ", flush=True)

        # Humanize first
        qa_text = f"### {question}\n\n{answer}"
        humanized = _humanize_question(qa_text, article.config.target_audience, ai, prompts)

        # Then add contextual link if relevant (AI-powered)
        if related_articles:
            linked = _insert_contextual_link_if_relevant(
                humanized,
                related_articles,
                ai,
                prompts
            )
            humanized_and_linked.append(linked)
        else:
            humanized_and_linked.append(humanized)

        print("✓")

    # Join all Q&As
    linked_faq = "\n\n".join(humanized_and_linked)

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


def _find_related_articles(article: Article, storage) -> List[Dict[str, str]]:
    """
    Find related articles in the same silo

    Args:
        article: Article object
        storage: Storage service

    Returns:
        List of related article metadata: [{'title': str, 'slug': str, 'url': str}, ...]
    """
    # Get silo directory - articles in same silo are subdirectories of current article
    silo_path = article.path

    if not silo_path.exists():
        return []

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

    return related_articles


def _insert_contextual_link_if_relevant(
    qa_text: str,
    related_articles: List[Dict[str, str]],
    ai,
    prompts
) -> str:
    """
    Use AI to determine if a link is relevant and insert it naturally into the answer

    AI analyzes semantic relevance and rewrites answer with natural link if appropriate.
    If no strong match, returns original answer unchanged.

    Args:
        qa_text: Question and answer markdown (### Question\n\nAnswer)
        related_articles: List of available articles
        ai: AI provider
        prompts: Prompts service

    Returns:
        Q&A with natural link inserted (or unchanged if no relevant match)
    """
    if not related_articles:
        return qa_text

    # Build list of available articles for AI
    articles_list = "\n".join([
        f"- **{art['title']}** (slug: {art['slug']}, link: [{art['title']}]({art['url']}))"
        for art in related_articles
    ])

    # AI prompt for contextual linking
    prompt = f"""Masz pytanie i odpowiedź z FAQ oraz listę powiązanych artykułów.

# Pytanie i odpowiedź:
{qa_text}

# Dostępne artykuły w silosie:
{articles_list}

# Zadanie:
1. **Oceń tematyczną relevantność:** Czy KTÓRYKOLWIEK z dostępnych artykułów jest silnie powiązany tematycznie z tym pytaniem? (nie kieruj się tylko podobnymi słowami, ale semantycznym związkiem)

2. **Jeśli TAK (silny związek tematyczny):**
   - Wybierz JEDEN najbardziej relevantny artykuł
   - Przepisz odpowiedź, naturalnie wplatając link w tekst
   - Przykłady naturalnego wplecenia:
     * "Więcej szczegółów znajdziesz w artykule [Tytuł](/slug)"
     * "Zagadnienie to szerzej opisujemy w [Tytuł](/slug)"
     * "Przeczytaj o tym w [Tytuł](/slug)"
   - Link powinien być częścią zdania, nie osobną linijką na końcu
   - Zachowaj długość odpowiedzi (50-70 słów)

3. **Jeśli NIE (brak silnego związku):**
   - Zwróć dokładnie oryginalną odpowiedź BEZ ZMIAN
   - Lepiej brak linku niż wymuszony, słabo powiązany link

**WAŻNE:**
- Zwróć TYLKO pytanie i odpowiedź (### Question\n\nAnswer), bez komentarzy
- NIE dodawaj "Więcej:" na końcu - link MUSI być w tekście
- Jeśli nie ma dobrego dopasowania, zwróć oryginał bez linku

Zwróć przepisany Q&A:"""

    # Get AI response
    result = ai.generate(prompt, max_tokens=500)

    return result.strip()
