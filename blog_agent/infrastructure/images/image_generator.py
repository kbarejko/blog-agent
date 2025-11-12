"""
Image Generator Factory

Creates appropriate image provider based on configuration.
Maintains backward compatibility with original ImageGenerator class.
"""
import os
from typing import Optional

from .dalle_provider import DalleProvider
from .stability_provider import StabilityProvider
from .base_provider import BaseImageProvider


# Backward compatibility: ImageGenerator is now DalleProvider
ImageGenerator = DalleProvider


class ImageProviderFactory:
    """
    Factory for creating image providers

    Supports multiple providers: DALL-E, Stability AI, etc.
    """

    @staticmethod
    def create(provider: str = "dalle", api_key: Optional[str] = None) -> BaseImageProvider:
        """
        Create image provider instance

        Args:
            provider: Provider name ("dalle" or "stability")
            api_key: API key for the provider (optional, reads from env)

        Returns:
            Image provider instance

        Raises:
            ValueError: If provider is not supported
        """
        provider = provider.lower()

        if provider == "dalle":
            return DalleProvider(api_key=api_key)
        elif provider == "stability":
            return StabilityProvider(api_key=api_key)
        else:
            raise ValueError(f"Unsupported image provider: {provider}")

    @staticmethod
    def auto_detect() -> Optional[BaseImageProvider]:
        """
        Auto-detect available provider based on environment variables

        Checks for API keys in this order:
        1. OPENAI_API_KEY -> DALL-E
        2. STABILITY_API_KEY -> Stability AI

        Returns:
            Image provider instance or None if no API keys found
        """
        # Check for OpenAI API key
        if os.getenv('OPENAI_API_KEY'):
            try:
                return DalleProvider()
            except:
                pass

        # Check for Stability API key
        if os.getenv('STABILITY_API_KEY'):
            try:
                return StabilityProvider()
            except:
                pass

        return None
