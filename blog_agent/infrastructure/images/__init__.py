"""
Image infrastructure module
"""
from .image_generator import ImageGenerator, ImageProviderFactory
from .base_provider import BaseImageProvider
from .dalle_provider import DalleProvider
from .stability_provider import StabilityProvider

__all__ = [
    'ImageGenerator',  # Backward compatibility (alias for DalleProvider)
    'ImageProviderFactory',
    'BaseImageProvider',
    'DalleProvider',
    'StabilityProvider',
]
