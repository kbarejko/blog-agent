"""
Base AI Provider

Abstract interface for AI providers.
"""
from abc import ABC, abstractmethod
from typing import Dict, Any, Optional


class BaseAIProvider(ABC):
    """Abstract base class for AI providers"""

    def __init__(self, config: Dict[str, Any]):
        """
        Initialize provider with configuration

        Args:
            config: Provider configuration (api_key, model, etc.)
        """
        self.config = config

    @abstractmethod
    def generate(
        self,
        prompt: str,
        max_tokens: Optional[int] = None,
        temperature: Optional[float] = None,
        **kwargs
    ) -> str:
        """
        Generate text from prompt

        Args:
            prompt: Input prompt
            max_tokens: Maximum tokens to generate
            temperature: Sampling temperature (0.0-1.0)
            **kwargs: Additional provider-specific parameters

        Returns:
            Generated text
        """
        pass

    @abstractmethod
    def get_provider_name(self) -> str:
        """Get provider name (claude, openai, etc.)"""
        pass

    @abstractmethod
    def get_model_name(self) -> str:
        """Get model name"""
        pass

    def count_tokens(self, text: str) -> int:
        """
        Estimate token count (rough approximation)

        Override in subclass for accurate counting.
        """
        # Rough estimate: 1 token ≈ 4 characters
        return len(text) // 4

    def validate_config(self) -> None:
        """Validate provider configuration"""
        if 'api_key' not in self.config:
            raise ValueError(f"{self.get_provider_name()} requires 'api_key' in config")
        if 'model' not in self.config:
            raise ValueError(f"{self.get_provider_name()} requires 'model' in config")
