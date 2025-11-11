"""
Test Ollama Provider

Simple test to verify Ollama integration.
"""
import sys
from pathlib import Path

# Add project to path
sys.path.insert(0, str(Path(__file__).parent))

from blog_agent.infrastructure.ai.ollama_provider import OllamaProvider


def test_ollama_connection():
    """Test basic Ollama connectivity"""
    print("🧪 Testing Ollama Provider Integration\n")

    # Test with Windows host IP
    print("Testing 192.168.0.136:11434...")
    config = {
        'model': 'llama3:latest',
        'host': 'http://192.168.0.136:11434',
        'max_tokens': 100,
        'temperature': 0.7
    }

    try:
        provider = OllamaProvider(config)
        print(f"✅ Provider created: {provider.get_provider_name()}")
        print(f"   Model: {provider.get_model_name()}")
        print(f"   Host: {provider.host}\n")

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

        # Print troubleshooting guide
        print("=" * 60)
        print("TROUBLESHOOTING: Ollama not accessible from WSL")
        print("=" * 60)
        print("\nIf you're running Ollama on Windows and trying to access")
        print("from WSL, you need to configure Ollama to accept external")
        print("connections:\n")
        print("1. Set environment variable on Windows:")
        print("   OLLAMA_HOST=0.0.0.0:11434\n")
        print("2. Restart Ollama service\n")
        print("3. Update providers.yaml to use Windows host IP:")

        # Try to get Windows host IP
        try:
            with open('/etc/resolv.conf', 'r') as f:
                for line in f:
                    if 'nameserver' in line:
                        ip = line.split()[1]
                        print(f"   host: http://{ip}:11434\n")
                        break
        except:
            print("   host: http://<WINDOWS_IP>:11434\n")

        print("Alternative: Run this script directly on Windows where")
        print("Ollama is installed.\n")

        return False


def test_ollama_with_windows_host():
    """Test connection to Ollama on Windows host"""
    print("\n" + "=" * 60)
    print("Testing Ollama on Windows host from WSL...")
    print("=" * 60 + "\n")

    # Get Windows host IP
    windows_ip = None
    try:
        with open('/etc/resolv.conf', 'r') as f:
            for line in f:
                if 'nameserver' in line:
                    windows_ip = line.split()[1]
                    break
    except:
        pass

    if not windows_ip:
        print("❌ Could not determine Windows host IP")
        return False

    print(f"Windows host IP: {windows_ip}")

    config = {
        'model': 'llama3:latest',
        'host': f'http://{windows_ip}:11434',
        'max_tokens': 100,
        'temperature': 0.7
    }

    try:
        provider = OllamaProvider(config)
        print(f"✅ Provider created")
        print(f"   Model: {provider.get_model_name()}")
        print(f"   Host: {provider.host}\n")

        # Try simple generation
        print("Generating test response...")
        prompt = "Write one sentence about Python."
        response = provider.generate(prompt, max_tokens=50)

        print(f"✅ Generation successful!")
        print(f"   Response: {response}\n")

        return True

    except Exception as e:
        print(f"❌ Connection failed: {str(e)}\n")
        return False


if __name__ == '__main__':
    # Test localhost
    success_local = test_ollama_connection()

    # If localhost fails, try Windows host
    if not success_local:
        success_windows = test_ollama_with_windows_host()

        if not success_windows:
            print("\n" + "=" * 60)
            print("NEXT STEPS")
            print("=" * 60)
            print("\n1. Make sure Ollama is running on Windows")
            print("2. Configure OLLAMA_HOST=0.0.0.0:11434")
            print("3. Restart Ollama")
            print("4. Run this test again\n")
            sys.exit(1)

    print("\n✅ All tests passed! Ollama is ready to use.")
