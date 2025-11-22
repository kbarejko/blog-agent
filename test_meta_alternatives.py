#!/usr/bin/env python3
"""
Test script for Meta Alternatives step (Step 20)

This script tests the meta alternatives generation step to ensure it works correctly.
"""
import sys
from pathlib import Path

# Add blog_agent to path
sys.path.insert(0, str(Path(__file__).parent))

from blog_agent.core.workflow.steps.step_20_meta_alternatives import execute_meta_alternatives
from blog_agent.core.domain.article import Article, ArticleConfig
from blog_agent.core.domain.value_objects import SEOData
from blog_agent.infrastructure.ai.provider_registry import ProviderRegistry
from blog_agent.core.services.prompt_loader import PromptLoader
from blog_agent.infrastructure.storage.file_storage import FileStorage


def test_meta_alternatives():
    """Test meta alternatives generation"""

    print("=" * 70)
    print("Testing Meta Alternatives Generation (Step 20)")
    print("=" * 70)
    print()

    # Create test article path
    test_path = Path("artykuly/test/meta-test")
    test_path.mkdir(parents=True, exist_ok=True)

    # Create test config
    config = ArticleConfig(
        title="Wybór CMS w 2025 - WordPress vs Headless: Co wybrać dla biznesu?",
        target_audience="Przedsiębiorcy i właściciele firm",
        tone="ekspercki, ale naturalny i rozmowny",
        model="openai-gpt4o-mini"
    )

    # Create test article
    article = Article(path=test_path, config=config)

    # Set test SEO data (simulating existing meta tags)
    article.set_seo_data(SEOData(
        meta_title="CMS 2025: WordPress vs Headless - Praktyczny Przewodnik",
        meta_description="Dowiedz się jak wybrać najlepszy CMS dla swojego biznesu w 2025. Porównanie WordPress i headless CMS z praktycznymi wskazówkami dla przedsiębiorców."
    ))

    # Set test final content (simulating completed article)
    article.set_final_content("""
# Wybór CMS w 2025 - WordPress vs Headless: Co wybrać dla biznesu?

## Co znajdziesz w artykule?

- **WordPress to 43% internetu** - nadal najpopularniejsze rozwiązanie, ale czy najlepsze dla Twojego biznesu?
- **Headless CMS kosztuje 3x więcej** - ale może zaoszczędzić setki godzin w długim terminie
- **5 kryteriów wyboru** - konkretna checklist która pomoże podjąć decyzję
- **Koszty ukryte** - czego dostawcy Ci nie powiedzą

## Wprowadzenie

Wybór systemu CMS to jedna z najważniejszych decyzji technologicznych dla każdego biznesu online.
WordPress dominuje rynek z 43% udziałem, ale headless CMS zyskuje na popularności wśród większych firm.

W tym artykule porównamy oba rozwiązania z perspektywy kosztów, wydajności i skalowalności.

## WordPress - Zalety i Wady

WordPress to sprawdzone rozwiązanie używane przez miliony stron na świecie.

**Zalety:**
- Niskie koszty wdrożenia (5-20k PLN)
- Ogromna społeczność i wtyczki
- Łatwy w obsłudze dla nietechnicznych użytkowników

**Wady:**
- Problemy z wydajnością przy dużym ruchu
- Bezpieczeństwo wymaga ciągłej uwagi
- Trudności ze skalowaniem

## Headless CMS - Przyszłość Content Management

Headless CMS to nowoczesne podejście oddzielające backend od frontendu.

**Zalety:**
- Świetna wydajność i szybkość
- Elastyczność w wyborze technologii frontend
- Łatwość integracji z różnymi kanałami

**Wady:**
- Wyższe koszty wdrożenia (30-100k PLN)
- Wymaga zespołu developerskiego
- Dłuższy czas implementacji

## Koszty - Szczegółowe Porównanie

WordPress:
- Setup: 5-20k PLN
- Hosting: 50-300 PLN/miesiąc
- Utrzymanie: 500-2000 PLN/miesiąc

Headless CMS:
- Setup: 30-100k PLN
- Hosting: 200-1000 PLN/miesiąc
- Utrzymanie: 2000-8000 PLN/miesiąc

## Kiedy Wybrać WordPress?

WordPress to dobry wybór gdy:
- Masz ograniczony budżet (<30k PLN)
- Potrzebujesz szybkiego wdrożenia (1-2 miesiące)
- Zespół nietechniczny będzie zarządzał treścią
- Ruch na stronie <100k wizyt/miesiąc

## Kiedy Wybrać Headless CMS?

Headless CMS sprawdzi się gdy:
- Masz budżet >50k PLN
- Priorytetem jest wydajność i skalowalność
- Planujesz multi-channel publishing
- Masz lub możesz zatrudnić zespół developerski

## Podsumowanie

Wybór między WordPress a headless CMS zależy od wielu czynników.
Dla większości małych i średnich firm WordPress będzie lepszym wyborem ze względu na niższe koszty.
Headless CMS to inwestycja w przyszłość dla firm planujących szybki wzrost.
""")

    # Create dependencies
    registry = ProviderRegistry()
    provider = registry.get_provider("openai-gpt4o-mini")

    deps = {
        'ai': provider,
        'prompts': PromptLoader(Path("prompts")),
        'storage': FileStorage(),
    }

    config_dict = {
        'enabled': True,
    }

    print("📝 Test Configuration:")
    print(f"   Article: {article.config.title}")
    print(f"   Current Meta Title: {article.seo_data.meta_title}")
    print(f"   Current Meta Description: {article.seo_data.meta_description[:60]}...")
    print(f"   Provider: openai-gpt4o-mini")
    print()

    # Execute step
    try:
        print("🚀 Executing meta_alternatives step...")
        print()

        result = execute_meta_alternatives(article, deps, config_dict)

        print()
        print("=" * 70)
        print("✅ Test Completed Successfully!")
        print("=" * 70)
        print()
        print(f"📄 Output file: {test_path / 'meta_alternatives.md'}")
        print()
        print("To view the generated alternatives:")
        print(f"   cat {test_path / 'meta_alternatives.md'}")
        print()

        # Display the generated file
        output_file = test_path / 'meta_alternatives.md'
        if output_file.exists():
            print("=" * 70)
            print("Generated Meta Alternatives:")
            print("=" * 70)
            print()
            content = output_file.read_text()
            print(content)

        return True

    except Exception as e:
        print()
        print("=" * 70)
        print("❌ Test Failed!")
        print("=" * 70)
        print(f"Error: {str(e)}")
        print()
        import traceback
        traceback.print_exc()
        return False


if __name__ == "__main__":
    success = test_meta_alternatives()
    sys.exit(0 if success else 1)
