"""
Base Image Provider Interface

Defines common interface for image generation providers.
"""
from abc import ABC, abstractmethod
from pathlib import Path
from typing import Dict, Any


class BaseImageProvider(ABC):
    """
    Abstract base class for image generation providers

    Providers (DALL-E, Stability AI, etc.) implement this interface.
    """

    @abstractmethod
    def generate_image(
        self,
        prompt: str,
        output_path: Path,
        **kwargs
    ) -> Dict[str, Any]:
        """
        Generate single image from prompt

        Args:
            prompt: Text prompt for image generation
            output_path: Where to save the generated image
            **kwargs: Provider-specific parameters

        Returns:
            Dict with generation info (url, path, model, etc.)
        """
        pass

    def generate_batch(
        self,
        prompts: list[Dict[str, Any]],
        output_dir: Path,
        skip_existing: bool = True,
        **kwargs
    ) -> list[Dict[str, Any]]:
        """
        Generate multiple images from prompts

        Default implementation calls generate_image for each prompt.
        Providers can override for optimized batch processing.

        Args:
            prompts: List of dicts with 'prompt' and 'filename'
            output_dir: Directory to save images
            skip_existing: Skip if image file already exists
            **kwargs: Provider-specific parameters

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
                    **kwargs
                )
                results.append(result)

            except Exception as e:
                print(f"   ⚠️  Failed to generate {filename}: {str(e)}")
                results.append({
                    'path': str(output_path),
                    'error': str(e)
                })

        return results
