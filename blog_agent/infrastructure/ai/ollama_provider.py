"""
Ollama AI Provider

Implementation using Ollama local models.
"""
from typing import Dict, Any, Optional
import ollama

from .base_provider import BaseAIProvider


class OllamaProvider(BaseAIProvider):
    """Ollama AI provider for local models"""

    def __init__(self, config: Dict[str, Any]):
        """
        Initialize Ollama provider

        Config:
            model: Model name (e.g., "llama3:latest", "mistral:latest", "codellama:13b")
            host: Ollama server URL (default: "http://localhost:11434")
            max_tokens: Default max tokens (default: 4000)
            temperature: Default temperature (default: 0.7)
        """
        super().__init__(config)

        # Ollama doesn't require API key, so override validation
        if 'model' not in self.config:
            raise ValueError(f"Ollama requires 'model' in config")

        self.model = config['model']
        self.host = config.get('host', 'http://localhost:11434')
        self.default_max_tokens = config.get('max_tokens', 4000)
        self.default_temperature = config.get('temperature', 0.7)

        # Configure Ollama client with custom host if specified
        if self.host != 'http://localhost:11434':
            self.client = ollama.Client(host=self.host)
        else:
            self.client = ollama.Client()

    def generate(
        self,
        prompt: str,
        max_tokens: Optional[int] = None,
        temperature: Optional[float] = None,
        **kwargs
    ) -> str:
        """
        Generate text using Ollama

        Args:
            prompt: Input prompt
            max_tokens: Maximum tokens (default from config)
            temperature: Temperature (default from config)
            **kwargs: Additional Ollama parameters

        Returns:
            Generated text
        """
        try:
            # Prepare options
            options = {
                'num_predict': max_tokens or self.default_max_tokens,
                'temperature': temperature if temperature is not None else self.default_temperature,
            }

            # Add any additional options from kwargs
            if 'options' in kwargs:
                options.update(kwargs.pop('options'))

            response = self.client.generate(
                model=self.model,
                prompt=prompt,
                options=options,
                **kwargs
            )

            # Extract text from response
            return response['response']

        except ollama.ResponseError as e:
            # Handle Ollama-specific errors
            error_msg = f"Ollama API error: {str(e)}"
            if hasattr(e, 'status_code'):
                error_msg += f" (status: {e.status_code})"
            raise RuntimeError(error_msg) from e
        except Exception as e:
            # Wrap other exceptions
            raise RuntimeError(f"Error generating text with Ollama: {str(e)}") from e

    def get_provider_name(self) -> str:
        """Get provider name"""
        return "ollama"

    def get_model_name(self) -> str:
        """Get model name"""
        return self.model

    def validate_config(self) -> None:
        """Validate provider configuration (override to skip api_key check)"""
        if 'model' not in self.config:
            raise ValueError(f"{self.get_provider_name()} requires 'model' in config")

    def count_tokens(self, text: str) -> int:
        """
        Count tokens using rough estimate

        For more accurate counting, could use model-specific tokenizers.
        """
        # Rough estimate: ~4 chars per token for most models
        return len(text) // 4
