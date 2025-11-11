"""
OpenAI Provider

Implementation using OpenAI API.
"""
from typing import Dict, Any, Optional
from openai import OpenAI

from .base_provider import BaseAIProvider


class OpenAIProvider(BaseAIProvider):
    """OpenAI provider using OpenAI SDK"""

    def __init__(self, config: Dict[str, Any]):
        """
        Initialize OpenAI provider

        Config:
            api_key: OpenAI API key
            model: Model name (e.g., "gpt-4", "gpt-4-turbo", "gpt-3.5-turbo")
            max_tokens: Default max tokens (default: 4000)
            temperature: Default temperature (default: 0.7)
        """
        super().__init__(config)
        self.validate_config()

        self.client = OpenAI(api_key=config['api_key'])
        self.model = config['model']
        self.default_max_tokens = config.get('max_tokens', 4000)
        self.default_temperature = config.get('temperature', 0.7)

    def generate(
        self,
        prompt: str,
        max_tokens: Optional[int] = None,
        temperature: Optional[float] = None,
        **kwargs
    ) -> str:
        """
        Generate text using OpenAI

        Args:
            prompt: Input prompt
            max_tokens: Maximum tokens (default from config)
            temperature: Temperature (default from config)
            **kwargs: Additional OpenAI parameters

        Returns:
            Generated text
        """
        try:
            response = self.client.chat.completions.create(
                model=self.model,
                messages=[
                    {"role": "user", "content": prompt}
                ],
                max_tokens=max_tokens or self.default_max_tokens,
                temperature=temperature if temperature is not None else self.default_temperature,
                **kwargs
            )

            # Extract text from response
            return response.choices[0].message.content

        except Exception as e:
            # Wrap exceptions with more context
            raise RuntimeError(f"OpenAI API error: {str(e)}") from e

    def get_provider_name(self) -> str:
        """Get provider name"""
        return "openai"

    def get_model_name(self) -> str:
        """Get model name"""
        return self.model

    def count_tokens(self, text: str) -> int:
        """
        Count tokens using rough estimate

        For accurate counting, could use tiktoken library.
        """
        # Rough estimate: ~4 chars per token for GPT models
        return len(text) // 4
