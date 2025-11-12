"""
Stability AI Image Provider

Generates images using Stability AI API (Stable Diffusion, SDXL, SD3).
"""
import os
import base64
import requests
from pathlib import Path
from typing import Optional, Dict, Any

from .base_provider import BaseImageProvider


class StabilityProvider(BaseImageProvider):
    """
    Image generator using Stability AI API

    Supports Stable Diffusion models (SDXL, SD3, etc.)
    """

    # API endpoints
    API_HOST = "https://api.stability.ai"

    # Available models
    MODELS = {
        'sdxl': 'stable-diffusion-xl-1024-v1-0',  # SDXL 1.0 - $0.011/image
        'sd3': 'sd3-large',  # SD3 Large - $0.037/image
        'sd3-medium': 'sd3-medium',  # SD3 Medium
        'sd3-large-turbo': 'sd3-large-turbo',  # SD3 Large Turbo
    }

    def __init__(self, api_key: Optional[str] = None):
        """
        Initialize Stability AI provider

        Args:
            api_key: Stability AI API key (defaults to STABILITY_API_KEY env var)
        """
        self.api_key = api_key or os.getenv('STABILITY_API_KEY')
        if not self.api_key:
            raise ValueError("STABILITY_API_KEY must be set for image generation")

    def generate_image(
        self,
        prompt: str,
        output_path: Path,
        model: str = "sdxl",
        width: int = 1024,
        height: int = 1024,
        steps: int = 40,
        cfg_scale: float = 7.0,
        **kwargs
    ) -> Dict[str, Any]:
        """
        Generate image from prompt and save to file

        Args:
            prompt: Text prompt for image generation
            output_path: Where to save the generated image
            model: Model name ("sdxl", "sd3", "sd3-medium", "sd3-large-turbo")
            width: Image width (must be multiple of 64)
            height: Image height (must be multiple of 64)
            steps: Number of diffusion steps (more = better quality, slower)
            cfg_scale: Classifier-free guidance scale (how closely to follow prompt)
            **kwargs: Additional parameters

        Returns:
            Dict with generation info (path, model, etc.)
        """
        print(f"   🎨 Generating image with Stability AI: {prompt[:60]}...", flush=True)

        # Get model ID
        model_id = self.MODELS.get(model, model)

        # Determine API endpoint based on model
        if model.startswith('sd3'):
            # SD3 uses v2beta endpoint
            endpoint = f"{self.API_HOST}/v2beta/stable-image/generate/sd3"
            payload = {
                "prompt": prompt,
                "model": model_id,
                "mode": "text-to-image",
                "output_format": "png",
            }
            # SD3 uses form data, not JSON
            use_form_data = True
        else:
            # SDXL uses v1 generation endpoint
            endpoint = f"{self.API_HOST}/v1/generation/{model_id}/text-to-image"
            payload = {
                "text_prompts": [{"text": prompt, "weight": 1.0}],
                "cfg_scale": cfg_scale,
                "height": height,
                "width": width,
                "steps": steps,
                "samples": 1,
            }
            use_form_data = False

        # Headers
        headers = {
            "Authorization": f"Bearer {self.api_key}",
        }

        try:
            # Make request
            if use_form_data:
                headers["Accept"] = "image/*"
                response = requests.post(endpoint, headers=headers, data=payload)
            else:
                headers["Content-Type"] = "application/json"
                headers["Accept"] = "application/json"
                response = requests.post(endpoint, headers=headers, json=payload)

            # Check response
            if response.status_code != 200:
                error_msg = f"API error {response.status_code}: {response.text}"
                print(f"   ❌ {error_msg}")
                raise Exception(error_msg)

            # Extract image data
            if use_form_data:
                # SD3 returns raw image bytes
                image_data = response.content
            else:
                # SDXL returns base64-encoded images in JSON
                response_data = response.json()
                if 'artifacts' not in response_data or not response_data['artifacts']:
                    raise Exception("No images in response")

                # Get first artifact (image)
                artifact = response_data['artifacts'][0]
                image_base64 = artifact['base64']
                image_data = base64.b64decode(image_base64)

            # Ensure directory exists
            output_path.parent.mkdir(parents=True, exist_ok=True)

            # Save image
            with open(output_path, 'wb') as f:
                f.write(image_data)

            print(f"   ✅ Image saved: {output_path.name}")

            return {
                'path': str(output_path),
                'model': model_id,
                'width': width,
                'height': height,
                'steps': steps,
                'cfg_scale': cfg_scale
            }

        except Exception as e:
            print(f"   ❌ Image generation failed: {str(e)}")
            raise
