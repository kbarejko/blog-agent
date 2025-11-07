"""
Step 9: Multimedia Suggestions

AI suggests 4-9 multimedia elements (images, charts, infographics).
"""
from typing import Dict, Any
import json

from ...domain.article import Article
from ...domain.value_objects import MultimediaSuggestion


def execute_multimedia(
    article: Article,
    deps: Dict[str, Any],
    config: Dict[str, Any]
) -> Article:
    """
    Generate multimedia suggestions

    AI suggests:
    - Hero image
    - 3-8 section-specific media (images, charts, infographics)
    - DALL-E/Midjourney prompts for each

    Args:
        article: Article (must have final content)
        deps: Dependencies (ai, prompts, storage)
        config: Step configuration

    Returns:
        Article with multimedia suggestions set
    """
    if not article.final_content:
        raise ValueError("Final content must exist before multimedia suggestions")

    ai = deps['ai']
    prompts = deps['prompts']
    storage = deps['storage']

    print("🔄 Generating multimedia suggestions...")

    # Load outline content
    outline_path = article.get_outline_path()
    outline_content = ""
    if outline_path.exists():
        outline_content = storage.read_file(outline_path)

    # Load and render prompt
    prompt = prompts.load_and_render(
        "articles/prompt_multimedia_suggestions.md",
        {
            'TYTUL_ARTYKULU': article.config.title,
            'ARTICLE_CONTENT': article.final_content,
            'KONSPEKT_TRESC': outline_content,
            'TARGET_AUDIENCE': article.config.target_audience,
        }
    )

    # Generate suggestions
    response = ai.generate(prompt, max_tokens=2000)

    # Parse multimedia suggestions from JSON response
    try:
        # Extract JSON from response (may have markdown or text wrapper)
        response_clean = response.strip()

        # Remove markdown code blocks if present
        if response_clean.startswith('```'):
            lines = response_clean.split('\n')
            # Remove first line (```json or ```)
            lines = lines[1:]
            # Remove last line if it's ```
            if lines and lines[-1].strip() == '```':
                lines = lines[:-1]
            response_clean = '\n'.join(lines)

        # Parse JSON
        data = json.loads(response_clean)

        # Extract multimedia_suggestions array
        suggestions = data.get('multimedia_suggestions', [])

        if not suggestions:
            print("   ⚠️  No suggestions in AI response, using fallback")
            raise ValueError("Empty suggestions")

        # Find hero image (subtype='hero')
        hero = None
        section_media = []

        for item in suggestions:
            if item.get('subtype') == 'hero':
                hero = {
                    'type': item.get('type', 'photo'),
                    'title': item.get('title', ''),
                    'description': item.get('description', ''),
                    'alt_text': item.get('alt_text', ''),
                    'prompt': item.get('image_prompt', ''),
                    'keywords': item.get('keywords', []),
                }
            else:
                section_media.append({
                    'type': item.get('type', 'image'),
                    'subtype': item.get('subtype', ''),
                    'section': item.get('section', ''),
                    'title': item.get('title', ''),
                    'description': item.get('description', ''),
                    'alt_text': item.get('alt_text', ''),
                    'prompt': item.get('image_prompt', ''),
                    'placement': item.get('placement', ''),
                    'keywords': item.get('keywords', []),
                })

        # Fallback hero if not found
        if not hero:
            print("   ⚠️  No hero image found, creating fallback")
            hero = {
                'type': 'photo',
                'title': f'Hero image - {article.config.title}',
                'description': 'Professional illustration related to article topic',
                'alt_text': article.config.title,
                'prompt': f'Professional illustration for article about {article.config.title}',
                'keywords': [],
            }

        multimedia = MultimediaSuggestion(
            hero_image=hero,
            section_media=section_media
        )

        print(f"   ✓ Parsed {len(suggestions)} multimedia suggestions")
        print(f"   - Hero image: {hero.get('title', 'Untitled')}")
        print(f"   - Section media: {len(section_media)} items")

    except (json.JSONDecodeError, ValueError) as e:
        print(f"   ⚠️  Failed to parse AI response: {str(e)}")
        print(f"   Using fallback placeholder")

        # Fallback to placeholder
        multimedia = MultimediaSuggestion(
            hero_image={
                'type': 'photo',
                'title': f'Hero image - {article.config.title}',
                'description': 'Professional illustration related to article topic',
                'alt_text': article.config.title,
                'prompt': f'Professional modern illustration for {article.config.title}',
                'keywords': [],
            },
            section_media=[]
        )

    article.set_multimedia(multimedia)

    # Save to multimedia.json
    multimedia_path = article.get_multimedia_path()
    multimedia_data = {
        'hero_image': multimedia.hero_image,
        'section_media': multimedia.section_media,
        'total_count': multimedia.get_total_count()
    }
    storage.write_json(multimedia_path, multimedia_data)

    print(f"✅ Multimedia suggestions: {multimedia.get_total_count()} elements")

    return article
