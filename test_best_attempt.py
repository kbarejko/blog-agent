"""
Test _select_best_attempt logic
"""
from blog_agent.core.workflow.steps._section_writer import _select_best_attempt


def test_select_best_attempt():
    """Test that the best attempt (closest to requirements) is selected"""

    # Simulate the user's example:
    # Attempt 1: 450 words (too long by 230)
    # Attempt 2: 259 words (too long by 39) <- SHOULD WIN
    # Attempt 3: 301 words (too long by 81)
    # Target: 200 words, max 220 (with 10% tolerance)

    attempts = [
        # Attempt 1: 450 words
        (
            "content1" * 100,
            {
                'valid': False,
                'word_count': 450,
                'min_words': 180,  # 200 - 10%
                'max_words': 220,  # 200 + 10%
                'flesch': 50,
                'min_flesch': 40,
                'max_flesch': 60,
                'issues': ['Too long: 450 words']
            }
        ),
        # Attempt 2: 259 words (closest to max 220)
        (
            "content2" * 100,
            {
                'valid': False,
                'word_count': 259,
                'min_words': 180,
                'max_words': 220,
                'flesch': 48,
                'min_flesch': 40,
                'max_flesch': 60,
                'issues': ['Too long: 259 words']
            }
        ),
        # Attempt 3: 301 words
        (
            "content3" * 100,
            {
                'valid': False,
                'word_count': 301,
                'min_words': 180,
                'max_words': 220,
                'flesch': 52,
                'min_flesch': 40,
                'max_flesch': 60,
                'issues': ['Too long: 301 words']
            }
        ),
    ]

    best_content, best_result = _select_best_attempt(attempts, target_words=200)

    print("Test Results:")
    print("=" * 60)

    # Calculate penalties for each attempt
    for i, (content, result) in enumerate(attempts, 1):
        word_count = result['word_count']
        max_words = result['max_words']
        penalty = (word_count - max_words) ** 2 if word_count > max_words else 0

        is_selected = (content == best_content)
        marker = "✅ SELECTED" if is_selected else ""

        print(f"Attempt {i}: {word_count} words (max: {max_words}) - Penalty: {penalty} {marker}")

    print("=" * 60)

    # Verify that attempt 2 was selected (259 words is closest to 220)
    assert best_result['word_count'] == 259, f"Expected 259 words, got {best_result['word_count']}"
    print("\n✅ Test PASSED: Selected attempt 2 (259 words) - closest to requirements!")
    print(f"   Penalty scores:")
    print(f"   - Attempt 1 (450): {(450-220)**2} = {(450-220)**2}")
    print(f"   - Attempt 2 (259): {(259-220)**2} = {(259-220)**2} <- BEST")
    print(f"   - Attempt 3 (301): {(301-220)**2} = {(301-220)**2}")


if __name__ == '__main__':
    test_select_best_attempt()
