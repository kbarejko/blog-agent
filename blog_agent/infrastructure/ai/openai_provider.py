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

    def _is_gpt5_model(self) -> bool:
        """
        Check if model is GPT-5 series

        GPT-5 models don't support custom temperature (only default 1.0)

        Returns:
            True if model is GPT-5
        """
        model_lower = self.model.lower()
        return model_lower.startswith('gpt-5') or model_lower.startswith('gpt5')

    def _adjust_tokens_for_gpt5(self, requested_tokens: int) -> int:
        """
        Adjust token limit for GPT-5 reasoning models

        GPT-5 uses reasoning tokens before output. If the limit is too low,
        all tokens are consumed by reasoning and output is empty.

        Strategy: Multiply requested tokens by 5-10x for GPT-5 to leave room
        for both reasoning and output.

        Args:
            requested_tokens: Original token limit from step

        Returns:
            Adjusted token limit for GPT-5 (or original if not GPT-5)
        """
        if not self._is_gpt5_model():
            return requested_tokens

        # Multipliers based on requested amount
        if requested_tokens < 1000:
            # Small requests (200-800): multiply by 10x
            # e.g., 800 → 8000
            return requested_tokens * 10
        elif requested_tokens < 3000:
            # Medium requests (1000-3000): multiply by 6x
            # e.g., 2500 → 15000
            return requested_tokens * 6
        elif requested_tokens < 6000:
            # Large requests (3000-6000): multiply by 4x
            # e.g., 4000 → 16000
            return requested_tokens * 4
        else:
            # Very large requests (6000+): multiply by 2x
            # e.g., 8000 → 16000
            return requested_tokens * 2

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
            requested_limit = max_tokens or self.default_max_tokens

            # Auto-adjust for GPT-5 reasoning models
            token_limit = self._adjust_tokens_for_gpt5(requested_limit)

            # Build request parameters
            request_params = {
                "model": self.model,
                "messages": [{"role": "user", "content": prompt}],
                **kwargs
            }

            # GPT-5 doesn't support temperature parameter at all (uses default 1.0)
            # Other models support custom temperature
            if not self._is_gpt5_model():
                temp_value = temperature if temperature is not None else self.default_temperature
                request_params["temperature"] = temp_value

            # Use appropriate token limit parameter based on model
            if self._uses_max_completion_tokens():
                request_params["max_completion_tokens"] = token_limit
            else:
                request_params["max_tokens"] = token_limit

            response = self.client.chat.completions.create(**request_params)

            # Debug logging for GPT-5 models
            if self._is_gpt5_model():
                print(f"   🐛 GPT-5 Debug:")
                print(f"      Model: {self.model}")
                print(f"      Requested tokens: {requested_limit}")
                print(f"      Adjusted tokens: {token_limit} (x{token_limit/requested_limit:.1f})")
                print(f"      Request params: {list(request_params.keys())}")
                if 'max_completion_tokens' in request_params:
                    print(f"      max_completion_tokens: {request_params['max_completion_tokens']}")
                print(f"      Response ID: {response.id}")
                print(f"      Finish reason: {response.choices[0].finish_reason}")
                print(f"      Has content: {response.choices[0].message.content is not None}")
                if response.choices[0].message.content:
                    print(f"      Content length: {len(response.choices[0].message.content)} chars")

            # Extract text from response
            content = response.choices[0].message.content

            # Handle None content (some models might return refusal or empty response)
            if content is None:
                # Check if there's a refusal reason
                if hasattr(response.choices[0].message, 'refusal') and response.choices[0].message.refusal:
                    raise RuntimeError(f"OpenAI API refused to generate: {response.choices[0].message.refusal}")
                raise RuntimeError(f"OpenAI API returned empty response. Model: {self.model}, Finish reason: {response.choices[0].finish_reason}, Response ID: {response.id}")

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
