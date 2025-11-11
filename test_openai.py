"""
Test OpenAI Provider

Simple test to verify OpenAI integration.
"""
import sys
import os
from pathlib import Path

# Add project to path
sys.path.insert(0, str(Path(__file__).parent))

from blog_agent.infrastructure.ai.openai_provider import OpenAIProvider


def test_openai_connection():
    """Test basic OpenAI connectivity"""
    print("🧪 Testing OpenAI Provider Integration\n")

    # Check for API key
    api_key = os.getenv('OPENAI_API_KEY')
    if not api_key:
        print("❌ OPENAI_API_KEY not set in environment")
        print("\nTo test OpenAI:")
        print("1. Get API key from https://platform.openai.com/api-keys")
        print("2. Set environment variable:")
        print("   export OPENAI_API_KEY='your-api-key-here'\n")
        return False

    print(f"✅ API key found: {api_key[:10]}...{api_key[-4:]}")

    # Test with GPT-3.5 (cheaper for testing)
    config = {
        'api_key': api_key,
        'model': 'gpt-3.5-turbo',
        'max_tokens': 100,
        'temperature': 0.7
    }

    try:
        provider = OpenAIProvider(config)
        print(f"✅ Provider created: {provider.get_provider_name()}")
        print(f"   Model: {provider.get_model_name()}\n")

        # Try simple generation
        print("Generating test response...")
        prompt = "Write a one-sentence summary of what AI is."
        response = provider.generate(prompt, max_tokens=50)

        print(f"✅ Generation successful!")
        print(f"   Prompt: {prompt}")
        print(f"   Response: {response}\n")

        return True

    except Exception as e:
        print(f"❌ Error: {str(e)}\n")

        # Check if it's an auth error
        if "401" in str(e) or "authentication" in str(e).lower():
            print("=" * 60)
            print("AUTHENTICATION ERROR")
            print("=" * 60)
            print("\nYour API key may be invalid or expired.")
            print("Please check:")
            print("1. API key is correct")
            print("2. Account has credits: https://platform.openai.com/account/usage")
            print("3. API key permissions are correct\n")

        return False


def test_openai_models():
    """Test different OpenAI models"""
    print("\n" + "=" * 60)
    print("Available OpenAI Models")
    print("=" * 60 + "\n")

    models = [
        ("gpt-4o", "GPT-4o - Latest and most capable"),
        ("gpt-4-turbo", "GPT-4 Turbo - Fast and powerful"),
        ("gpt-4", "GPT-4 - Original GPT-4"),
        ("gpt-3.5-turbo", "GPT-3.5 Turbo - Fast and cheap"),
    ]

    print("Models you can use with blog-agent:\n")
    for model_name, description in models:
        print(f"  • {model_name}")
        print(f"    {description}\n")

    print("Cost comparison (per 1M tokens):")
    print("  • GPT-4o: $5 input / $15 output")
    print("  • GPT-4 Turbo: $10 input / $30 output")
    print("  • GPT-3.5 Turbo: $0.50 input / $1.50 output\n")

    print("For blog generation (3000-word article):")
    print("  • GPT-4o: ~$0.15 per article")
    print("  • GPT-4 Turbo: ~$0.30 per article")
    print("  • GPT-3.5 Turbo: ~$0.015 per article (cheapest!)\n")


if __name__ == '__main__':
    # Test connection
    success = test_openai_connection()

    # Show available models
    test_openai_models()

    if not success:
        print("\n" + "=" * 60)
        print("NEXT STEPS")
        print("=" * 60)
        print("\n1. Make sure you have an OpenAI account")
        print("2. Get API key: https://platform.openai.com/api-keys")
        print("3. Set environment variable:")
        print("   export OPENAI_API_KEY='sk-...'")
        print("4. Run this test again\n")
        sys.exit(1)

    print("\n✅ All tests passed! OpenAI is ready to use.")
    print("\nUsage:")
    print("  blog-agent create --config path/config.yaml --provider openai")
