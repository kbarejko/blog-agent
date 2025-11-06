#!/usr/bin/env python3
"""
Przykład użycia Blog Agent - szybki start
"""

from blog_agent import BlogAgent
import os

def example_1_basic():
    """Przykład 1: Podstawowe użycie"""
    print("\n" + "="*60)
    print("PRZYKŁAD 1: Podstawowe użycie")
    print("="*60)
    
    agent = BlogAgent()
    
    article = agent.create_article(
        topic="5 sposobów na poprawę produktywności podczas pracy zdalnej"
    )
    
    agent.save_article(article, "przyklad_1_podstawowy.md")


def example_2_with_context():
    """Przykład 2: Z dodatkowym kontekstem"""
    print("\n" + "="*60)
    print("PRZYKŁAD 2: Z dodatkowym kontekstem")
    print("="*60)
    
    agent = BlogAgent()
    
    article = agent.create_article(
        topic="Najlepsze praktyki bezpieczeństwa w aplikacjach webowych",
        additional_context="""
        Grupa docelowa: Junior developers
        Ton: edukacyjny, z praktycznymi przykładami
        Uwzględnij: OWASP Top 10, konkretne fragmenty kodu
        Długość: średni artykuł (około 1500 słów)
        """
    )
    
    agent.save_article(article, "przyklad_2_z_kontekstem.md")


def example_3_custom_audit():
    """Przykład 3: Z własnymi kryteriami audytu"""
    print("\n" + "="*60)
    print("PRZYKŁAD 3: Z własnymi kryteriami audytu")
    print("="*60)
    
    agent = BlogAgent()
    
    # Kryteria dla artykułu technicznego
    tech_criteria = {
        "Dokładność techniczna": "Czy wszystkie informacje techniczne są poprawne i aktualne?",
        "Przykłady kodu": "Czy są praktyczne, działające przykłady kodu?",
        "Poziom trudności": "Czy poziom jest odpowiedni dla grupy docelowej?",
        "Best practices": "Czy wskazano sprawdzone rozwiązania branżowe?",
        "Troubleshooting": "Czy omówiono typowe problemy i ich rozwiązania?"
    }
    
    article = agent.create_article(
        topic="Wprowadzenie do React Hooks dla początkujących",
        additional_context="Artykuł dla osób, które znają podstawy React",
        audit_criteria=tech_criteria,
        max_improvement_attempts=3
    )
    
    agent.save_article(article, "przyklad_3_custom_audit.md")


def example_4_business():
    """Przykład 4: Artykuł biznesowy"""
    print("\n" + "="*60)
    print("PRZYKŁAD 4: Artykuł biznesowy")
    print("="*60)
    
    agent = BlogAgent()
    
    business_criteria = {
        "Wartość biznesowa": "Czy pokazano konkretny wpływ na biznes (ROI, wzrost, oszczędności)?",
        "Case studies": "Czy użyto rzeczywistych przykładów firm?",
        "Actionable insights": "Czy czytelnik wie, co konkretnie zrobić?",
        "Dane i statystyki": "Czy poparto twierdzenia liczbami?",
        "Perspektywa rynkowa": "Czy pokazano szerszy kontekst branżowy?"
    }
    
    article = agent.create_article(
        topic="Jak wdrożyć AI w małej firmie - praktyczny przewodnik",
        additional_context="""
        Dla: właściciele małych firm (10-50 pracowników)
        Budget: ograniczony
        Perspektywa: praktyczna, krok po kroku
        Uwzględnić: konkretne narzędzia i ich ceny, timeline wdrożenia
        """,
        audit_criteria=business_criteria
    )
    
    agent.save_article(article, "przyklad_4_biznesowy.md")


def example_5_lifestyle():
    """Przykład 5: Artykuł lifestylowy"""
    print("\n" + "="*60)
    print("PRZYKŁAD 5: Artykuł lifestylowy")
    print("="*60)
    
    agent = BlogAgent()
    
    lifestyle_criteria = {
        "Osobisty ton": "Czy tekst jest ciepły, przyjazny i osobisty?",
        "Storytelling": "Czy tekst opowiada historię?",
        "Inspiracja": "Czy motywuje do działania i zmian?",
        "Praktyczność": "Czy porady są łatwe do wdrożenia?",
        "Autentyczność": "Czy brzmi autentycznie i szczerze?"
    }
    
    article = agent.create_article(
        topic="Minimalizm w praktyce - jak uprościłam swoje życie w 30 dni",
        additional_context="""
        Ton: osobisty, ciepły, inspirujący
        Format: dziennik 30-dniowego wyzwania
        Elementy: konkretne kroki, osobiste refleksje, before/after
        """,
        audit_criteria=lifestyle_criteria
    )
    
    agent.save_article(article, "przyklad_5_lifestyle.md")


def interactive_mode():
    """Tryb interaktywny - użytkownik podaje temat"""
    print("\n" + "="*60)
    print("TRYB INTERAKTYWNY")
    print("="*60)
    
    topic = input("\n📝 Podaj temat artykułu: ").strip()
    
    if not topic:
        print("❌ Temat nie może być pusty!")
        return
    
    print("\n💡 Dodatkowy kontekst (opcjonalnie, Enter aby pominąć):")
    print("   Podaj wskazówki dla agenta, np. grupa docelowa, ton, długość...")
    context = input("   > ").strip()
    
    print("\n🎯 Wybierz typ artykułu:")
    print("   1. Techniczny")
    print("   2. Biznesowy")
    print("   3. Lifestyle")
    print("   4. Domyślny (uniwersalny)")
    
    choice = input("   Wybór (1-4): ").strip()
    
    criteria_map = {
        "1": {
            "Dokładność techniczna": "Czy informacje techniczne są poprawne?",
            "Przykłady": "Czy są praktyczne przykłady?",
            "Poziom trudności": "Czy poziom jest odpowiedni?",
            "Best practices": "Czy wskazano sprawdzone rozwiązania?"
        },
        "2": {
            "Wartość biznesowa": "Czy pokazano wpływ na biznes?",
            "Case studies": "Czy użyto przykładów firm?",
            "Actionable": "Czy czytelnik wie co zrobić?",
            "Dane": "Czy poparto twierdzenia liczbami?"
        },
        "3": {
            "Osobisty ton": "Czy tekst jest ciepły i osobisty?",
            "Inspiracja": "Czy motywuje do działania?",
            "Storytelling": "Czy opowiada historię?",
            "Praktyczność": "Czy porady są łatwe do wdrożenia?"
        }
    }
    
    criteria = criteria_map.get(choice)
    
    agent = BlogAgent()
    
    article = agent.create_article(
        topic=topic,
        additional_context=context if context else "",
        audit_criteria=criteria
    )
    
    # Generuj nazwę pliku z tematu
    filename = "artykul_" + "".join(c if c.isalnum() else "_" for c in topic[:30].lower()) + ".md"
    agent.save_article(article, filename)


def main():
    """Menu główne"""
    if not os.environ.get("ANTHROPIC_API_KEY"):
        print("\n❌ BŁĄD: Brak klucza API!")
        print("Ustaw zmienną środowiskową: export ANTHROPIC_API_KEY='twój-klucz'")
        return
    
    print("\n" + "="*60)
    print("🤖 Blog Agent - Przykłady użycia")
    print("="*60)
    print("\nWybierz przykład do uruchomienia:")
    print("  1. Podstawowe użycie")
    print("  2. Z dodatkowym kontekstem")
    print("  3. Z własnymi kryteriami audytu (artykuł techniczny)")
    print("  4. Artykuł biznesowy")
    print("  5. Artykuł lifestylowy")
    print("  6. Tryb interaktywny (podaj własny temat)")
    print("  0. Uruchom wszystkie przykłady")
    
    choice = input("\nWybór (0-6): ").strip()
    
    examples = {
        "1": example_1_basic,
        "2": example_2_with_context,
        "3": example_3_custom_audit,
        "4": example_4_business,
        "5": example_5_lifestyle,
        "6": interactive_mode
    }
    
    if choice == "0":
        for i in range(1, 6):
            examples[str(i)]()
            print("\n" + "="*60 + "\n")
    elif choice in examples:
        examples[choice]()
    else:
        print("❌ Nieprawidłowy wybór!")
        return
    
    print("\n✨ Gotowe! Sprawdź wygenerowane artykuły w katalogu outputs/")


if __name__ == "__main__":
    main()
