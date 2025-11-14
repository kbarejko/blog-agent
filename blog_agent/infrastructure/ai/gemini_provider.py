"""
Google Gemini Provider

Implementation using Google Generative AI API.
"""
from typing import Dict, Any, Optional
import google.generativeai as genai
from google.generativeai.types import HarmCategory, HarmBlockThreshold

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
        # Retry logic for SAFETY false positives and rate limits
        max_safety_retries = 3  # Max retries for SAFETY false positives
        max_total_attempts = 10  # Hard limit to prevent infinite loops
        retry_delay = 1  # seconds

        import time
        import re

        attempt = 0
        while attempt < max_total_attempts:
            try:
                return self._generate_with_safety_check(prompt, max_tokens, temperature, **kwargs)
            except RuntimeError as e:
                error_msg = str(e)
                attempt += 1

                # Handle rate limit errors (429) - retry with suggested delay
                if '429' in error_msg and 'retry in' in error_msg:
                    if attempt >= max_total_attempts:
                        print(f"   ❌ Max total attempts ({max_total_attempts}) reached")
                        raise

                    # Extract retry delay from error message
                    match = re.search(r'retry in ([\d.]+)s', error_msg)
                    if match:
                        retry_seconds = float(match.group(1))
                        print(f"   ⏳ Rate limit exceeded - waiting {retry_seconds:.0f}s...")
                        print(f"   🔄 Retrying... (attempt {attempt + 1}/{max_total_attempts})")
                        time.sleep(retry_seconds + 1)  # +1s buffer
                        continue
                    else:
                        # Fallback if we can't extract delay
                        print(f"   ⏳ Rate limit exceeded - waiting 20s...")
                        time.sleep(20)
                        continue

                # Handle SAFETY blocks with NEGLIGIBLE ratings (false positives)
                if 'finish_reason=SAFETY' in error_msg and 'NEGLIGIBLE' in error_msg:
                    if attempt < max_safety_retries:
                        wait_time = retry_delay * attempt  # Linear backoff
                        print(f"   ⚠️  SAFETY false positive detected (all ratings NEGLIGIBLE)")
                        print(f"   🔄 Retrying in {wait_time}s... (attempt {attempt + 1}/{max_total_attempts})")
                        time.sleep(wait_time)
                        continue

                # Not a retry-able error, or max retries reached
                raise

        # Max attempts reached
        raise RuntimeError(f"Max total attempts ({max_total_attempts}) reached for Gemini generation")

    def _generate_with_safety_check(
        self,
        prompt: str,
        max_tokens: Optional[int] = None,
        temperature: Optional[float] = None,
        **kwargs
    ) -> str:
        """
        Internal generation method with safety checks

        Returns:
            Generated text
        """
        try:
            # Prepare generation config
            generation_config = genai.GenerationConfig(
                max_output_tokens=max_tokens or self.default_max_tokens,
                temperature=temperature if temperature is not None else self.default_temperature,
            )

            # Configure safety settings (permissive for content generation)
            # Set to BLOCK_NONE to minimize false positives
            safety_settings = {
                HarmCategory.HARM_CATEGORY_HARASSMENT: HarmBlockThreshold.BLOCK_NONE,
                HarmCategory.HARM_CATEGORY_HATE_SPEECH: HarmBlockThreshold.BLOCK_NONE,
                HarmCategory.HARM_CATEGORY_SEXUALLY_EXPLICIT: HarmBlockThreshold.BLOCK_NONE,
                HarmCategory.HARM_CATEGORY_DANGEROUS_CONTENT: HarmBlockThreshold.BLOCK_NONE,
            }

            # Generate content
            response = self.model.generate_content(
                prompt,
                generation_config=generation_config,
                safety_settings=safety_settings,
                **kwargs
            )

            # Check if response was blocked
            if not response.candidates:
                # Response blocked at prompt level
                feedback = response.prompt_feedback

                print(f"\n⚠️  Gemini blocked at PROMPT level")
                print(f"   Block reason: {feedback.block_reason if hasattr(feedback, 'block_reason') else 'Unknown'}")

                if hasattr(feedback, 'safety_ratings') and feedback.safety_ratings:
                    print(f"\n⚠️  Prompt Safety Ratings:")
                    for rating in feedback.safety_ratings:
                        print(f"   - {rating.category.name}: {rating.probability.name}")

                raise RuntimeError(
                    f"Gemini blocked prompt. "
                    f"Block reason: {feedback.block_reason if hasattr(feedback, 'block_reason') else 'Unknown'}. "
                    f"Safety ratings: {feedback.safety_ratings if hasattr(feedback, 'safety_ratings') else 'N/A'}"
                )

            # Check finish reason
            candidate = response.candidates[0]
            finish_reasons = {
                1: 'STOP',           # Success
                2: 'SAFETY',         # Blocked by safety filters
                3: 'MAX_TOKENS',     # Reached token limit
                4: 'RECITATION',     # Blocked due to recitation
                5: 'OTHER'           # Other reason
            }

            if candidate.finish_reason != 1:  # 1 = STOP (success)
                reason = finish_reasons.get(candidate.finish_reason, f'UNKNOWN({candidate.finish_reason})')

                # Build detailed error message
                error_parts = [f"Gemini generation failed: finish_reason={reason}"]

                # Always show candidate info for debugging
                print(f"\n⚠️  Gemini Response Debug:")
                print(f"   Finish reason: {reason} ({candidate.finish_reason})")
                print(f"   Has safety_ratings attr: {hasattr(candidate, 'safety_ratings')}")

                # Get safety ratings value
                safety_ratings = getattr(candidate, 'safety_ratings', None)
                print(f"   safety_ratings value: {safety_ratings}")
                print(f"   safety_ratings type: {type(safety_ratings)}")

                if safety_ratings:
                    print(f"   safety_ratings length: {len(safety_ratings)}")

                    ratings_str = ', '.join([
                        f"{rating.category.name}={rating.probability.name}"
                        for rating in safety_ratings
                    ])
                    error_parts.append(f"Safety ratings: {ratings_str}")

                    # Print to console for debugging
                    print(f"\n⚠️  Candidate Safety Ratings:")
                    for rating in safety_ratings:
                        print(f"   - {rating.category.name}: {rating.probability.name}")
                else:
                    print(f"   safety_ratings is None or empty - Gemini didn't provide details")

                if candidate.finish_reason == 2:  # SAFETY
                    error_parts.append(
                        "Content was blocked by safety filters. "
                        "This may be a false positive. Try rephrasing the prompt or using a different model."
                    )

                    # Show FULL prompt for debugging SAFETY false positives
                    print(f"\n⚠️  FULL PROMPT that triggered SAFETY block:")
                    print(f"{'='*80}")
                    print(prompt)
                    print(f"{'='*80}\n")

                raise RuntimeError(' '.join(error_parts))

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
