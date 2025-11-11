"""
Google Gemini Provider

Implementation using Google Generative AI API.
"""
from typing import Dict, Any, Optional
import google.generativeai as genai

from .base_provider import BaseAIProvider


class GeminiProvider(BaseAIProvider):
    """Google Gemini provider using Google Generative AI SDK"""

    def __init__(self, config: Dict[str, Any]):
        """
        Initialize Gemini provider

        Config:
            api_key: Google API key
            model: Model name (e.g., "gemini-pro", "gemini-1.5-pro", "gemini-1.5-flash")
            max_tokens: Default max tokens (default: 8000)
            temperature: Default temperature (default: 0.9)
        """
        super().__init__(config)
        self.validate_config()

        genai.configure(api_key=config['api_key'])
        self.model_name = config['model']
        self.model = genai.GenerativeModel(self.model_name)
        self.default_max_tokens = config.get('max_tokens', 8000)
        self.default_temperature = config.get('temperature', 0.9)

    def generate(
        self,
        prompt: str,
        max_tokens: Optional[int] = None,
        temperature: Optional[float] = None,
        **kwargs
    ) -> str:
        """
        Generate text using Gemini

        Args:
            prompt: Input prompt
            max_tokens: Maximum tokens (default from config)
            temperature: Temperature (default from config)
            **kwargs: Additional Gemini parameters

        Returns:
            Generated text
        """
        try:
            # Prepare generation config
            generation_config = genai.GenerationConfig(
                max_output_tokens=max_tokens or self.default_max_tokens,
                temperature=temperature if temperature is not None else self.default_temperature,
            )

            # Generate content
            response = self.model.generate_content(
                prompt,
                generation_config=generation_config,
                **kwargs
            )

            # Extract text from response
            return response.text

        except Exception as e:
            # Wrap exceptions with more context
            raise RuntimeError(f"Gemini API error: {str(e)}") from e

    def get_provider_name(self) -> str:
        """Get provider name"""
        return "gemini"

    def get_model_name(self) -> str:
        """Get model name"""
        return self.model_name

    def count_tokens(self, text: str) -> int:
        """
        Count tokens using rough estimate

        Gemini has different tokenization than GPT models.
        """
        # Rough estimate: ~4 chars per token
        return len(text) // 4
