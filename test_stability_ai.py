"""
Test Stability AI Integration

Tests Stability AI image generation with various models.
"""
import sys
import os
from pathlib import Path

# Add project to path
sys.path.insert(0, str(Path(__file__).parent))

from blog_agent.infrastructure.images.stability_provider import StabilityProvider


def test_stability_ai():
    """Test Stability AI image generation"""
    print("🧪 Testing Stability AI Integration\n")

    # Check for STABILITY_API_KEY
    api_key = os.getenv('STABILITY_API_KEY')
    if not api_key:
        print("❌ STABILITY_API_KEY not set in environment")
        print("\nTo test Stability AI:")
        print("1. Get API key from https://platform.stability.ai/")
        print("2. Set environment variable:")
        print("   export STABILITY_API_KEY='sk-...'")
        print("\nPricing:")
        print("  SDXL: $0.011 per image (cheapest!)")
        print("  SD3: $0.037 per image")
        print("  SD3.5 Large: $0.065 per image")
        return False

    print(f"✅ API key found: {api_key[:10]}...{api_key[-4:]}\n")

    # Create test directory
    test_dir = Path("test_images_stability")
    test_dir.mkdir(exist_ok=True)
    print(f"📂 Test directory: {test_dir}\n")

    # Initialize provider
    try:
        provider = StabilityProvider(api_key=api_key)
        print("✅ Stability AI provider initialized\n")
    except Exception as e:
        print(f"❌ Failed to initialize provider: {str(e)}")
        return False

    # Test prompts
    tests = [
        {
            'name': 'SDXL Test',
            'model': 'sdxl',
            'prompt': 'A professional office workspace with a modern laptop, natural lighting, minimalist design',
            'filename': 'sdxl_test.png',
            'width': 1024,
            'height': 1024,
        },
        # Uncomment to test SD3 (costs more)
        # {
        #     'name': 'SD3 Test',
        #     'model': 'sd3',
        #     'prompt': 'A stunning landscape with mountains and a lake at sunset, photorealistic',
        #     'filename': 'sd3_test.png',
        #     'width': 1024,
        #     'height': 1024,
        # },
    ]

    # Run tests
    print("=" * 60)
    print("Generating Test Images")
    print("=" * 60 + "\n")

    results = []
    for test in tests:
        print(f"📝 Test: {test['name']}")
        print(f"   Model: {test['model']}")
        print(f"   Prompt: {test['prompt'][:60]}...")

        output_path = test_dir / test['filename']

        try:
            result = provider.generate_image(
                prompt=test['prompt'],
                output_path=output_path,
                model=test['model'],
                width=test.get('width', 1024),
                height=test.get('height', 1024),
                steps=test.get('steps', 40),
                cfg_scale=test.get('cfg_scale', 7.0),
            )

            # Check file size
            size_kb = output_path.stat().st_size / 1024
            print(f"   📊 File size: {size_kb:.1f} KB\n")

            results.append({
                'test': test['name'],
                'success': True,
                'path': str(output_path),
                'size_kb': size_kb
            })

        except Exception as e:
            print(f"   ❌ Failed: {str(e)}\n")
            results.append({
                'test': test['name'],
                'success': False,
                'error': str(e)
            })

    # Summary
    print("=" * 60)
    print("Test Summary")
    print("=" * 60 + "\n")

    successful = sum(1 for r in results if r['success'])
    total = len(results)

    for result in results:
        status = "✅" if result['success'] else "❌"
        print(f"{status} {result['test']}")
        if result['success']:
            print(f"   Path: {result['path']}")
            print(f"   Size: {result['size_kb']:.1f} KB")
        else:
            print(f"   Error: {result['error']}")
        print()

    print(f"Results: {successful}/{total} tests passed")

    return successful == total


def show_pricing():
    """Show Stability AI pricing information"""
    print("\n" + "=" * 60)
    print("Stability AI Pricing (2025)")
    print("=" * 60 + "\n")

    print("Model Pricing:")
    print("  SDXL:          $0.011 per image  (Best value!)")
    print("  SD3:           $0.037 per image")
    print("  SD3 Medium:    ~$0.025 per image")
    print("  SD3.5 Large:   $0.065 per image")

    print("\nCompare to DALL-E:")
    print("  DALL-E 2:      $0.020 per image")
    print("  DALL-E 3 Std:  $0.040-0.080 per image")
    print("  DALL-E 3 HD:   $0.080-0.120 per image")

    print("\nFor typical blog article (6 images):")
    print("  SDXL:       ~$0.07 per article  (55% cheaper than DALL-E 2!)")
    print("  SD3:        ~$0.22 per article")
    print("  DALL-E 2:   ~$0.12 per article")
    print("  DALL-E 3:   ~$0.48 per article")

    print("\nRecommendation:")
    print("  • Best quality: SD3 or DALL-E 3")
    print("  • Best value: SDXL (great quality, lowest cost)")
    print("  • Production: SDXL for cost-effective generation")


if __name__ == '__main__':
    # Show pricing first
    show_pricing()

    print("\n" + "=" * 60)
    print("Testing Stability AI")
    print("=" * 60 + "\n")

    success = test_stability_ai()

    if success:
        print("\n✅ Stability AI test completed successfully!")
        print("\nNext steps:")
        print("  - Review generated images in test_images_stability/ folder")
        print("  - Set STABILITY_API_KEY in your environment")
        print("  - Enable step in workflow.yaml if satisfied")
        print("  - Workflow will auto-detect and use Stability AI")
    else:
        print("\n❌ Stability AI test failed!")
        print("\nTroubleshooting:")
        print("  - Ensure STABILITY_API_KEY is set correctly")
        print("  - Check API key has billing enabled")
        print("  - Verify network connectivity")
        print("  - See pricing info above")

    sys.exit(0 if success else 1)
