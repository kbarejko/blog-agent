"""
Claude AI Provider

Implementation using Anthropic API.
"""
from typing import Dict, Any, Optional
import anthropic

from .base_provider import BaseAIProvider


class ClaudeProvider(BaseAIProvider):
    """Claude AI provider using Anthropic SDK"""

    def __init__(self, config: Dict[str, Any]):
        """
        Initialize Claude provider

        Config:
            api_key: Anthropic API key
            model: Model name (e.g., "claude-sonnet-4-20250514")
            max_tokens: Default max tokens (default: 4000)
            temperature: Default temperature (default: 1.0)
        """
        super().__init__(config)
        self.validate_config()

        self.client = anthropic.Anthropic(api_key=config['api_key'])
        self.model = config['model']
        self.default_max_tokens = config.get('max_tokens', 4000)
        self.default_temperature = config.get('temperature', 1.0)

    def generate(
        self,
        prompt: str,
        max_tokens: Optional[int] = None,
        temperature: Optional[float] = None,
        **kwargs
    ) -> str:
        """
        Generate text using Claude

        Args:
            prompt: Input prompt
            max_tokens: Maximum tokens (default from config)
            temperature: Temperature (default from config)
            **kwargs: Additional Anthropic parameters

        Returns:
            Generated text
        """
        response = self.client.messages.create(
            model=self.model,
            max_tokens=max_tokens or self.default_max_tokens,
            temperature=temperature if temperature is not None else self.default_temperature,
            messages=[
                {"role": "user", "content": prompt}
            ],
            **kwargs
        )

        # Extract text from response
        return response.content[0].text

    def get_provider_name(self) -> str:
        """Get provider name"""
        return "claude"

    def get_model_name(self) -> str:
        """Get model name"""
        return self.model

    def count_tokens(self, text: str) -> int:
        """
        Count tokens using Anthropic's tokenizer

        For now, use rough estimate. Can be improved with proper tokenizer.
        """
        # Anthropic: ~4 chars per token for English
        return len(text) // 4
