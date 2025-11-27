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

    def _uses_max_completion_tokens(self) -> bool:
        """
        Check if model uses max_completion_tokens parameter

        GPT-5.x, GPT-4o and newer models use max_completion_tokens.
        Older models (GPT-4, GPT-3.5) use max_tokens.

        Returns:
            True if model uses max_completion_tokens
        """
        model_lower = self.model.lower()
        # GPT-5.x models
        if model_lower.startswith('gpt-5') or model_lower.startswith('gpt5'):
            return True
        # GPT-4o models
        if 'gpt-4o' in model_lower or 'gpt4o' in model_lower:
            return True
        # Default to max_tokens for older models
        return False

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
            # Determine which token limit parameter to use
            token_limit = max_tokens or self.default_max_tokens

            # Build request parameters
            request_params = {
                "model": self.model,
                "messages": [{"role": "user", "content": prompt}],
                "temperature": temperature if temperature is not None else self.default_temperature,
                **kwargs
            }

            # Use appropriate token limit parameter based on model
            if self._uses_max_completion_tokens():
                request_params["max_completion_tokens"] = token_limit
            else:
                request_params["max_tokens"] = token_limit

            response = self.client.chat.completions.create(**request_params)

            # Extract text from response
            content = response.choices[0].message.content

            # Handle None content (some models might return refusal or empty response)
            if content is None:
                # Check if there's a refusal reason
                if hasattr(response.choices[0].message, 'refusal') and response.choices[0].message.refusal:
                    raise RuntimeError(f"OpenAI API refused to generate: {response.choices[0].message.refusal}")
                raise RuntimeError(f"OpenAI API returned empty response. Model: {self.model}, Finish reason: {response.choices[0].finish_reason}")

            return content

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
