"""
Test section header preservation from outline
"""
from blog_agent.core.workflow.steps._section_writer import _ensure_section_header


def test_header_scenarios():
    """Test various scenarios of header handling"""

    print("=" * 60)
    print("Testing Section Header Preservation")
    print("=" * 60)

    # Test 1: Content with H3 header (should upgrade to H2)
    content1 = """### Optymalizacja techniczna SEO

To jest treść sekcji..."""

    result1 = _ensure_section_header(content1, "1. Optymalizacja techniczna SEO")
    print("\nTest 1: Content with H3 header")
    print("Input H3:", content1.split('\n')[0])
    print("Output H2:", result1.split('\n')[0])
    assert result1.startswith("## Optymalizacja techniczna SEO"), "Should upgrade H3 to H2"
    print("✅ PASS")

    # Test 2: Content without header (should prepend H2)
    content2 = """To jest treść sekcji bez nagłówka..."""

    result2 = _ensure_section_header(content2, "2. Tworzenie treści produktowych")
    print("\nTest 2: Content without header")
    print("Input:", content2[:50] + "...")
    print("Output:", result2.split('\n')[0])
    assert result2.startswith("## Tworzenie treści produktowych"), "Should prepend H2"
    print("✅ PASS")

    # Test 3: Content with correct H2 already (should keep as-is)
    content3 = """## Linkowanie wewnętrzne

To jest treść sekcji..."""

    result3 = _ensure_section_header(content3, "3. Linkowanie wewnętrzne")
    print("\nTest 3: Content with H2 header already")
    print("Input:", content3.split('\n')[0])
    print("Output:", result3.split('\n')[0])
    assert result3.startswith("## Linkowanie wewnętrzne"), "Should keep H2 as-is"
    print("✅ PASS")

    # Test 4: Title with number prefix (should normalize)
    content4 = """### Wprowadzenie

To jest treść..."""

    result4 = _ensure_section_header(content4, "1. Wprowadzenie")
    print("\nTest 4: Title normalization (remove number)")
    print("Section title from outline: '1. Wprowadzenie'")
    print("Output H2:", result4.split('\n')[0])
    assert result4.startswith("## Wprowadzenie"), "Should remove number prefix"
    assert "1." not in result4.split('\n')[0], "Should not include number in H2"
    print("✅ PASS")

    # Test 5: Content with different H3 title (should prepend our H2)
    content5 = """### Różny tytuł

To jest treść..."""

    result5 = _ensure_section_header(content5, "Właściwy tytuł")
    print("\nTest 5: Different H3 title (should prepend)")
    print("Input H3:", content5.split('\n')[0])
    print("Output first line:", result5.split('\n')[0])
    print("Output second line:", result5.split('\n')[2])
    assert result5.startswith("## Właściwy tytuł"), "Should prepend our H2"
    assert "### Różny tytuł" in result5, "Should keep original H3"
    print("✅ PASS")

    print("\n" + "=" * 60)
    print("All tests passed! ✅")
    print("=" * 60)


if __name__ == '__main__':
    test_header_scenarios()
