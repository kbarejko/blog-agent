"""
Test Google Gemini Provider

Simple test to verify Gemini integration.
"""
import sys
import os
from pathlib import Path

# Add project to path
sys.path.insert(0, str(Path(__file__).parent))

from blog_agent.infrastructure.ai.gemini_provider import GeminiProvider


def test_gemini_connection():
    """Test basic Gemini connectivity"""
    print("🧪 Testing Google Gemini Provider Integration\n")

    # Check for API key
    api_key = os.getenv('GOOGLE_API_KEY')
    if not api_key:
        print("❌ GOOGLE_API_KEY not set in environment")
        print("\nTo test Gemini:")
        print("1. Get API key from https://makersuite.google.com/app/apikey")
        print("2. Set environment variable:")
        print("   export GOOGLE_API_KEY='your-api-key-here'\n")
        return False

    print(f"✅ API key found: {api_key[:10]}...{api_key[-4:]}")

    # Test with Gemini 2.5 Flash (cheaper for testing)
    config = {
        'api_key': api_key,
        'model': 'gemini-2.5-flash',
        'max_tokens': 100,
        'temperature': 0.9
    }

    try:
        provider = GeminiProvider(config)
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
        if "401" in str(e) or "authentication" in str(e).lower() or "API_KEY" in str(e):
            print("=" * 60)
            print("AUTHENTICATION ERROR")
            print("=" * 60)
            print("\nYour API key may be invalid or not enabled.")
            print("Please check:")
            print("1. API key is correct")
            print("2. Enable Generative Language API:")
            print("   https://console.cloud.google.com/apis/library/generativelanguage.googleapis.com")
            print("3. Check usage limits: https://makersuite.google.com/\n")

        return False


def test_gemini_models():
    """Test different Gemini models"""
    print("\n" + "=" * 60)
    print("Available Google Gemini Models")
    print("=" * 60 + "\n")

    models = [
        ("gemini-2.5-pro", "Gemini 2.5 Pro - Most capable, advanced reasoning"),
        ("gemini-2.5-flash", "Gemini 2.5 Flash - Fast and efficient"),
        ("gemini-2.0-flash-001", "Gemini 2.0 Flash - Legacy, still supported"),
    ]

    print("Models you can use with blog-agent:\n")
    for model_name, description in models:
        print(f"  • {model_name}")
        print(f"    {description}\n")

    print("⚠️  Gemini 1.x models (gemini-1.5-pro, gemini-1.5-flash, gemini-pro)")
    print("    are deprecated as of April 2025. Use Gemini 2.x models.\n")

    print("Key features:")
    print("  • Up to 2M token context window (2.5 models)")
    print("  • Multimodal support (text, images, video, audio)")
    print("  • Free tier available with rate limits\n")

    print("Cost comparison (per 1M tokens):")
    print("  • Gemini 2.5 Pro: $3.50 input / $10.50 output")
    print("  • Gemini 2.5 Flash: $0.30 input / $1.20 output")
    print("  • Gemini 2.0 Flash: $0.15 input / $0.60 output\n")

    print("For blog generation (3000-word article):")
    print("  • Gemini 2.5 Pro: ~$0.10 per article")
    print("  • Gemini 2.5 Flash: ~$0.01 per article (recommended!)")
    print("  • Gemini 2.0 Flash: ~$0.005 per article (cheapest cloud option!)\n")

    print("Free tier:")
    print("  • 15 requests/minute")
    print("  • 1M tokens/day")
    print("  • Perfect for testing!\n")


if __name__ == '__main__':
    # Test connection
    success = test_gemini_connection()

    # Show available models
    test_gemini_models()

    if not success:
        print("\n" + "=" * 60)
        print("NEXT STEPS")
        print("=" * 60)
        print("\n1. Get Google AI Studio API key:")
        print("   https://makersuite.google.com/app/apikey")
        print("2. Enable Generative Language API (if needed)")
        print("3. Set environment variable:")
        print("   export GOOGLE_API_KEY='...'")
        print("4. Run this test again\n")
        sys.exit(1)

    print("\n✅ All tests passed! Gemini is ready to use.")
    print("\nUsage:")
    print("  blog-agent create --config path/config.yaml --provider gemini")
