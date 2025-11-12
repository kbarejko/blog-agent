"""
Image Generator Service

Generates images using DALL-E API based on text prompts.
"""
import os
import requests
from pathlib import Path
from typing import Optional, Dict, Any
from openai import OpenAI


class ImageGenerator:
    """
    Image generator using OpenAI DALL-E

    Generates images from text prompts and saves them locally.
    """

    def __init__(self, api_key: Optional[str] = None):
        """
        Initialize image generator

        Args:
            api_key: OpenAI API key (defaults to OPENAI_API_KEY env var)
        """
        self.api_key = api_key or os.getenv('OPENAI_API_KEY')
        if not self.api_key:
            raise ValueError("OPENAI_API_KEY must be set for image generation")

        self.client = OpenAI(api_key=self.api_key)

    def generate_image(
        self,
        prompt: str,
        output_path: Path,
        model: str = "dall-e-3",
        size: str = "1792x1024",
        quality: str = "standard"
    ) -> Dict[str, Any]:
        """
        Generate image from prompt and save to file

        Args:
            prompt: Text prompt for image generation
            output_path: Where to save the generated image
            model: DALL-E model ("dall-e-2" or "dall-e-3")
            size: Image size (dall-e-3: "1024x1024", "1792x1024", "1024x1792")
            quality: "standard" or "hd" (dall-e-3 only)

        Returns:
            Dict with generation info (url, revised_prompt, etc.)
        """
        print(f"   🎨 Generating image: {prompt[:60]}...", flush=True)

        try:
            # Generate image
            response = self.client.images.generate(
                model=model,
                prompt=prompt,
                size=size,
                quality=quality,
                n=1
            )

            # Get image URL
            image_url = response.data[0].url
            revised_prompt = getattr(response.data[0], 'revised_prompt', prompt)

            # Download and save image
            image_data = requests.get(image_url).content

            # Ensure directory exists
            output_path.parent.mkdir(parents=True, exist_ok=True)

            # Save image
            with open(output_path, 'wb') as f:
                f.write(image_data)

            print(f"   ✅ Image saved: {output_path.name}")

            return {
                'url': image_url,
                'path': str(output_path),
                'revised_prompt': revised_prompt,
                'model': model,
                'size': size,
                'quality': quality
            }

        except Exception as e:
            print(f"   ❌ Image generation failed: {str(e)}")
            raise

    def generate_batch(
        self,
        prompts: list[Dict[str, Any]],
        output_dir: Path,
        model: str = "dall-e-3",
        size: str = "1792x1024",
        quality: str = "standard",
        skip_existing: bool = True
    ) -> list[Dict[str, Any]]:
        """
        Generate multiple images from prompts

        Args:
            prompts: List of dicts with 'prompt' and 'filename'
            output_dir: Directory to save images
            model: DALL-E model
            size: Image size
            quality: Image quality
            skip_existing: Skip if image file already exists

        Returns:
            List of generation results
        """
        results = []

        for i, item in enumerate(prompts):
            prompt_text = item['prompt']
            filename = item['filename']
            output_path = output_dir / filename

            # Skip if exists
            if skip_existing and output_path.exists():
                print(f"   ⏭️  Skipping {filename} (already exists)")
                results.append({
                    'path': str(output_path),
                    'skipped': True
                })
                continue

            print(f"\n   [{i+1}/{len(prompts)}] Generating: {filename}")

            try:
                result = self.generate_image(
                    prompt=prompt_text,
                    output_path=output_path,
                    model=model,
                    size=size,
                    quality=quality
                )
                results.append(result)

            except Exception as e:
                print(f"   ⚠️  Failed to generate {filename}: {str(e)}")
                results.append({
                    'path': str(output_path),
                    'error': str(e)
                })

        return results
