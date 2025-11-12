"""
Step 15: Generate Images

Generates images using DALL-E based on multimedia suggestions.
Creates images/ folder and downloads generated images.
"""
from pathlib import Path
from typing import Dict, Any
import json

from ...domain.article import Article


def execute_generate_images(article: Any, deps: Dict[str, Any], config: Dict[str, Any]) -> Any:
    """
    Generate images from multimedia suggestions

    Reads multimedia.json, generates images using DALL-E,
    saves them to images/ folder, and updates multimedia.json
    with local paths.

    Args:
        article: Article domain object
        deps: Dependencies (image_generator, storage, etc.)
        config: Step configuration

    Returns:
        Updated article with generated images
    """
    print(f"🎨 Generating images with DALL-E...")

    # Check if multimedia.json exists
    multimedia_path = article.path / "multimedia.json"
    if not multimedia_path.exists():
        print("   ⚠️  No multimedia.json found, skipping image generation")
        return article

    # Load multimedia suggestions
    with open(multimedia_path, 'r', encoding='utf-8') as f:
        multimedia_data = json.load(f)

    # Get image generator from deps
    image_generator = deps.get('image_generator')
    if not image_generator:
        print("   ⚠️  Image generator not available in dependencies")
        print("   💡 Set OPENAI_API_KEY to enable image generation")
        return article

    # Create images directory
    images_dir = article.path / "images"
    images_dir.mkdir(exist_ok=True)

    # Collect prompts to generate
    prompts_to_generate = []

    # Hero image
    hero = multimedia_data.get('hero_image', {})
    if hero and hero.get('prompt'):
        prompts_to_generate.append({
            'prompt': hero['prompt'],
            'filename': 'hero.png',
            'type': 'hero',
            'title': hero.get('title', 'Hero image')
        })

    # Section media
    section_media = multimedia_data.get('section_media', [])
    for i, media in enumerate(section_media):
        if media.get('prompt'):
            # Generate filename from section or index
            section_name = media.get('section', f'section-{i+1}')
            filename = f"{section_name.lower().replace(' ', '-')}.png"

            prompts_to_generate.append({
                'prompt': media['prompt'],
                'filename': filename,
                'type': 'section_media',
                'index': i,
                'title': media.get('title', f'Image {i+1}')
            })

    if not prompts_to_generate:
        print("   ℹ️  No image prompts found in multimedia.json")
        return article

    print(f"   Found {len(prompts_to_generate)} images to generate")
    print(f"   Output: {images_dir.relative_to(article.path.parent.parent)}\n")

    # Generate images
    try:
        results = image_generator.generate_batch(
            prompts=prompts_to_generate,
            output_dir=images_dir,
            model=config.get('model', 'dall-e-3'),
            size=config.get('size', '1792x1024'),
            quality=config.get('quality', 'standard'),
            skip_existing=config.get('skip_existing', True)
        )

        # Update multimedia.json with generated paths
        generated_count = 0
        skipped_count = 0

        for i, (prompt_info, result) in enumerate(zip(prompts_to_generate, results)):
            if result.get('skipped'):
                skipped_count += 1
                continue

            if result.get('error'):
                continue

            generated_count += 1

            # Update multimedia data with local path
            relative_path = f"images/{prompt_info['filename']}"

            if prompt_info['type'] == 'hero':
                multimedia_data['hero_image']['local_path'] = relative_path
                multimedia_data['hero_image']['generated'] = True
                if result.get('revised_prompt'):
                    multimedia_data['hero_image']['revised_prompt'] = result['revised_prompt']

            elif prompt_info['type'] == 'section_media':
                idx = prompt_info['index']
                multimedia_data['section_media'][idx]['local_path'] = relative_path
                multimedia_data['section_media'][idx]['generated'] = True
                if result.get('revised_prompt'):
                    multimedia_data['section_media'][idx]['revised_prompt'] = result['revised_prompt']

        # Save updated multimedia.json
        with open(multimedia_path, 'w', encoding='utf-8') as f:
            json.dump(multimedia_data, f, indent=2, ensure_ascii=False)

        print(f"\n✅ Image generation complete:")
        print(f"   Generated: {generated_count} images")
        if skipped_count > 0:
            print(f"   Skipped: {skipped_count} (already exist)")
        print(f"   Updated: multimedia.json with local paths")

    except Exception as e:
        print(f"\n❌ Image generation failed: {str(e)}")
        print(f"   Continuing without images")

    return article
