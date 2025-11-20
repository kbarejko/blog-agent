"""
Step 15: Generate Images (Hero Only)

Generates ONLY hero image using AI (DALL-E or Stability AI).
Other images remain as suggestions with stock photo alternatives.
This is cost-effective ($0.01-0.12 per article) while ensuring
every article has a professional hero image.
"""
from pathlib import Path
from typing import Dict, Any
import json

from ...domain.article import Article


def execute_generate_images(article: Any, deps: Dict[str, Any], config: Dict[str, Any]) -> Any:
    """
    Generate hero image from multimedia suggestions

    Reads multimedia.json, generates ONLY the hero image using AI,
    saves it to images/ folder. Other images remain as suggestions
    for manual implementation (stock photos or custom design).

    Args:
        article: Article domain object
        deps: Dependencies (storage, git)
        config: Step configuration (provider, model settings)

    Returns:
        Updated article with hero image generated
    """
    storage = deps.get('storage')
    git = deps.get('git')

    print(f"🎨 Generating hero image...")

    # Check if multimedia.json exists
    multimedia_path = article.path / "multimedia.json"
    if not multimedia_path.exists():
        print("   ⚠️  No multimedia.json found, skipping image generation")
        return article

    # Load multimedia suggestions
    multimedia_data = storage.read_json(multimedia_path)
    hero = multimedia_data.get('hero_image', {})

    if not hero or not hero.get('prompt'):
        print("   ⚠️  No hero image prompt found, skipping")
        return article

    # Get provider from config (default: stability for cost-effectiveness)
    provider_name = config.get('provider', 'stability')

    # Create images directory
    images_dir = article.path / "images"
    images_dir.mkdir(exist_ok=True)
    output_path = images_dir / "hero.png"

    # Skip if already exists
    if config.get('skip_existing', True) and output_path.exists():
        print(f"   ⏭️  Hero image already exists: {output_path.name}")
        return article

    print(f"   Provider: {provider_name}")
    print(f"   Prompt: {hero.get('prompt', '')[:60]}...")

    try:
        # Import image provider factory
        from ....infrastructure.images.image_generator import ImageProviderFactory

        # Create provider (auto-detects from env vars or uses specified)
        try:
            provider = ImageProviderFactory.create(provider=provider_name)
        except ValueError as e:
            # Try auto-detect if specified provider fails
            print(f"   ⚠️  {str(e)}")
            print(f"   Trying auto-detect...")
            provider = ImageProviderFactory.auto_detect()
            if not provider:
                print(f"   ⚠️  No image provider available")
                print(f"   Set STABILITY_API_KEY or OPENAI_API_KEY to enable")
                return article

        # Generate hero image
        result = provider.generate_image(
            prompt=hero.get('prompt'),
            output_path=output_path,
            model=config.get('model', 'sdxl'),
            **{k: v for k, v in config.items() if k not in ['provider', 'model', 'skip_existing', 'enabled']}
        )

        # Update multimedia.json with generated image info
        hero['generated'] = True
        hero['local_path'] = f"images/{output_path.name}"
        hero['generation_info'] = {
            'provider': provider_name,
            'model': result.get('model', config.get('model')),
        }
        if result.get('revised_prompt'):
            hero['revised_prompt'] = result['revised_prompt']

        multimedia_data['hero_image'] = hero
        storage.write_json(multimedia_path, multimedia_data)

        print(f"✅ Hero image generated: {output_path.name}")
        print(f"   Size: {output_path.stat().st_size // 1024} KB")

        # Show info about other images
        section_media_count = len(multimedia_data.get('section_media', []))
        if section_media_count > 0:
            print(f"\n📋 Other images ({section_media_count} suggestions):")
            print(f"   Check multimedia.json for:")
            print(f"   - AI generation prompts")
            print(f"   - Stock photo suggestions")
            print(f"   - Manual design alternatives")

        # Git commit
        if git:
            git.commit_article_stage(
                article.path,
                "generate_images",
                f"Generate hero image ({provider_name})"
            )

    except ValueError as e:
        error_msg = str(e)
        if 'API_KEY' in error_msg or 'api_key' in error_msg:
            print(f"   ⚠️  {error_msg}")
            print(f"   Skipping image generation")
            print(f"\n   To enable automatic hero generation:")
            print(f"   - Stability AI (cheap): export STABILITY_API_KEY=sk-...")
            print(f"   - DALL-E (quality):     export OPENAI_API_KEY=sk-...")
        else:
            print(f"   ⚠️  Image generation failed: {error_msg}")

    except Exception as e:
        print(f"   ⚠️  Image generation failed: {str(e)}")
        print(f"   Hero image can be added manually to images/hero.png")

    return article
