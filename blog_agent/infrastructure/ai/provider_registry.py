"""
AI Provider Registry

Factory for creating AI providers from configuration.
"""
from typing import Dict, Any, Type
from .base_provider import BaseAIProvider
from .claude_provider import ClaudeProvider
from .openai_provider import OpenAIProvider
from .ollama_provider import OllamaProvider
from .gemini_provider import GeminiProvider


class ProviderRegistry:
    """Registry for AI providers"""

    _providers: Dict[str, Type[BaseAIProvider]] = {
        'claude': ClaudeProvider,
        'openai': OpenAIProvider,
        'ollama': OllamaProvider,
        'gemini': GeminiProvider,
    }

    @classmethod
    def register(cls, name: str, provider_class: Type[BaseAIProvider]) -> None:
        """
        Register a new provider

        Args:
            name: Provider name (e.g., 'claude', 'openai')
            provider_class: Provider class
        """
        cls._providers[name] = provider_class

    @classmethod
    def create(cls, name: str, config: Dict[str, Any]) -> BaseAIProvider:
        """
        Create provider instance

        Args:
            name: Provider name
            config: Provider configuration

        Returns:
            Provider instance

        Raises:
            ValueError: If provider not registered
        """
        if name not in cls._providers:
            available = ', '.join(cls._providers.keys())
            raise ValueError(f"Unknown provider '{name}'. Available: {available}")

        provider_class = cls._providers[name]
        return provider_class(config)

    @classmethod
    def list_providers(cls) -> list[str]:
        """List available provider names"""
        return list(cls._providers.keys())
