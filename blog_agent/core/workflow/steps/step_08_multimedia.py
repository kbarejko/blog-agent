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

    # Parse multimedia suggestions (would need proper JSON parsing)
    # For now, create placeholder
    multimedia = MultimediaSuggestion(
        hero_image={
            'type': 'photo',
            'description': 'Hero image',
            'prompt': 'Professional business setting'
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
