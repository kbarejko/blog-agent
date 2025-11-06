#!/usr/bin/env python3
"""
Agent do automatycznego pisania artykułów blogowych.
Proces: Konspekt → Pisanie sekcji → Audyt → Finalny artykuł
"""

import anthropic
import os
import sys
import json
from typing import List, Dict
from datetime import datetime


class BlogAgent:
    def __init__(self, api_key: str = None):
        """Inicjalizacja agenta z kluczem API."""
        self.api_key = api_key or os.environ.get("ANTHROPIC_API_KEY")
        if not self.api_key:
            raise ValueError("Brak klucza API. Ustaw ANTHROPIC_API_KEY lub przekaż jako argument.")
        
        self.client = anthropic.Anthropic(api_key=self.api_key)
        self.model = "claude-sonnet-4-20250514"
        
    def create_outline(self, topic: str, additional_context: str = "") -> Dict:
        """Tworzy konspekt artykułu na podstawie tematu."""
        print(f"\n📋 Tworzę konspekt dla tematu: {topic}")
        print("=" * 60)
        
        prompt = f"""Jesteś ekspertem od tworzenia konspektów artykułów blogowych.

Temat artykułu: {topic}

{f'Dodatkowy kontekst: {additional_context}' if additional_context else ''}

Stwórz szczegółowy konspekt artykułu. Konspekt powinien zawierać:
1. Tytuł artykułu (chwytliwy i SEO-friendly)
2. Krótkie wprowadzenie (2-3 zdania o czym będzie artykuł)
3. Lista sekcji (4-7 sekcji), gdzie każda sekcja zawiera:
   - Tytuł sekcji
   - Krótki opis co powinno się w niej znaleźć (2-3 zdania)
   - Kluczowe punkty do omówienia (3-5 punktów)

Zwróć odpowiedź w formacie JSON:
{{
  "title": "Tytuł artykułu",
  "introduction": "Wprowadzenie do artykułu",
  "sections": [
    {{
      "title": "Tytuł sekcji",
      "description": "Opis sekcji",
      "key_points": ["Punkt 1", "Punkt 2", "Punkt 3"]
    }}
  ]
}}"""

        message = self.client.messages.create(
            model=self.model,
            max_tokens=4000,
            messages=[{"role": "user", "content": prompt}]
        )
        
        response_text = message.content[0].text
        
        # Wyciągamy JSON z odpowiedzi
        try:
            # Szukamy JSON w odpowiedzi (może być otoczony tekstem)
            start = response_text.find('{')
            end = response_text.rfind('}') + 1
            json_str = response_text[start:end]
            outline = json.loads(json_str)
        except json.JSONDecodeError:
            print("⚠️  Nie udało się sparsować JSON. Próbuję ponownie...")
            outline = {
                "title": "Artykuł bez tytułu",
                "introduction": response_text[:200],
                "sections": []
            }
        
        print(f"✅ Konspekt utworzony: {outline['title']}")
        print(f"   Liczba sekcji: {len(outline.get('sections', []))}")
        
        return outline
    
    def write_section(self, section: Dict, context: Dict) -> str:
        """Pisze treść pojedynczej sekcji."""
        section_title = section.get('title', 'Bez tytułu')
        print(f"\n✍️  Piszę sekcję: {section_title}")
        
        prompt = f"""Jesteś ekspertem od pisania artykułów blogowych.

Kontekst artykułu:
- Tytuł: {context['title']}
- Wprowadzenie: {context['introduction']}

Napisz treść dla następującej sekcji:

Tytuł sekcji: {section['title']}
Opis: {section.get('description', '')}
Kluczowe punkty do omówienia:
{chr(10).join(f"- {point}" for point in section.get('key_points', []))}

Wymagania:
- Napisz kompletną treść sekcji (300-500 słów)
- Użyj formatu Markdown
- Rozpocznij od nagłówka ## {section['title']}
- Treść powinna być merytoryczna, angażująca i wartościowa dla czytelnika
- Użyj przykładów, analogii lub konkretnych danych jeśli są potrzebne
- Możesz użyć list, pogrubień, kursywy dla lepszej czytelności
- NIE dodawaj podsumowania ani wezwania do działania na końcu sekcji

Napisz tylko treść tej sekcji, bez dodatkowych komentarzy."""

        message = self.client.messages.create(
            model=self.model,
            max_tokens=3000,
            messages=[{"role": "user", "content": prompt}]
        )
        
        content = message.content[0].text.strip()
        print(f"   ✅ Sekcja napisana ({len(content)} znaków)")
        
        return content
    
    def audit_section(self, section_content: str, section_info: Dict, audit_criteria: Dict) -> Dict:
        """Przeprowadza audyt sekcji według zadanych kryteriów."""
        print(f"\n🔍 Audytuję sekcję: {section_info.get('title', 'Bez tytułu')}")
        
        criteria_text = "\n".join([f"- {k}: {v}" for k, v in audit_criteria.items()])
        
        prompt = f"""Jesteś ekspertem od audytu treści blogowych.

Przeprowadź audyt poniższej sekcji według następujących kryteriów:

{criteria_text}

Sekcja do audytu:
---
{section_content}
---

Oceń każde kryterium w skali 1-10 i podaj konkretne uwagi.

Zwróć odpowiedź w formacie JSON:
{{
  "overall_score": 8.5,
  "criteria_scores": {{
    "nazwa_kryterium": {{
      "score": 8,
      "comment": "Szczegółowy komentarz"
    }}
  }},
  "suggestions": ["Sugestia 1", "Sugestia 2"],
  "approved": true
}}

Sekcja jest zatwierdzona (approved: true) jeśli ogólny wynik >= 7.0"""

        message = self.client.messages.create(
            model=self.model,
            max_tokens=2000,
            messages=[{"role": "user", "content": prompt}]
        )
        
        response_text = message.content[0].text
        
        try:
            start = response_text.find('{')
            end = response_text.rfind('}') + 1
            json_str = response_text[start:end]
            audit_result = json.loads(json_str)
        except json.JSONDecodeError:
            print("⚠️  Nie udało się sparsować wyniku audytu")
            audit_result = {
                "overall_score": 7.0,
                "approved": True,
                "suggestions": []
            }
        
        score = audit_result.get('overall_score', 0)
        approved = audit_result.get('approved', False)
        
        status = "✅ ZATWIERDZONA" if approved else "❌ WYMAGA POPRAWY"
        print(f"   {status} (wynik: {score}/10)")
        
        return audit_result
    
    def improve_section(self, section_content: str, audit_result: Dict) -> str:
        """Poprawia sekcję na podstawie wyników audytu."""
        print("   🔧 Poprawiam sekcję...")
        
        suggestions = "\n".join([f"- {s}" for s in audit_result.get('suggestions', [])])
        
        prompt = f"""Na podstawie poniższych sugestii, popraw treść sekcji:

Sugestie do poprawy:
{suggestions}

Oryginalna treść sekcji:
---
{section_content}
---

Zwróć poprawioną wersję sekcji w formacie Markdown. Zachowaj strukturę, ale wprowadź sugerowane poprawki."""

        message = self.client.messages.create(
            model=self.model,
            max_tokens=3000,
            messages=[{"role": "user", "content": prompt}]
        )
        
        improved_content = message.content[0].text.strip()
        print(f"   ✅ Sekcja poprawiona")
        
        return improved_content
    
    def create_article(
        self, 
        topic: str, 
        additional_context: str = "",
        audit_criteria: Dict = None,
        max_improvement_attempts: int = 2
    ) -> str:
        """
        Tworzy kompletny artykuł blogowy.
        
        Args:
            topic: Temat artykułu
            additional_context: Dodatkowy kontekst dla konspektu
            audit_criteria: Słownik z kryteriami audytu
            max_improvement_attempts: Maksymalna liczba prób poprawy sekcji
            
        Returns:
            Pełny artykuł w formacie Markdown
        """
        if audit_criteria is None:
            audit_criteria = {
                "Wartość merytoryczna": "Czy sekcja dostarcza konkretnej, wartościowej wiedzy?",
                "Czytelność": "Czy tekst jest łatwy do czytania i dobrze sformatowany?",
                "Spójność": "Czy sekcja pasuje do całości artykułu?",
                "Angażowanie": "Czy treść jest interesująca i trzyma uwagę czytelnika?",
                "Kompletność": "Czy wszystkie kluczowe punkty zostały omówione?"
            }
        
        print("\n" + "=" * 60)
        print("🚀 START PROCESU TWORZENIA ARTYKUŁU")
        print("=" * 60)
        
        # Krok 1: Tworzenie konspektu
        outline = self.create_outline(topic, additional_context)
        
        # Przygotowanie kontekstu
        context = {
            "title": outline.get('title', 'Artykuł'),
            "introduction": outline.get('introduction', '')
        }
        
        # Budowanie artykułu
        article_parts = []
        
        # Nagłówek i wprowadzenie
        article_parts.append(f"# {context['title']}\n")
        article_parts.append(f"{context['introduction']}\n")
        
        # Krok 2: Pisanie i audyt sekcji
        sections = outline.get('sections', [])
        
        for i, section in enumerate(sections, 1):
            print(f"\n{'=' * 60}")
            print(f"📝 SEKCJA {i}/{len(sections)}")
            print(f"{'=' * 60}")
            
            # Pisanie sekcji
            section_content = self.write_section(section, context)
            
            # Audyt sekcji
            attempts = 0
            while attempts < max_improvement_attempts:
                audit_result = self.audit_section(section_content, section, audit_criteria)
                
                if audit_result.get('approved', False):
                    break
                    
                attempts += 1
                if attempts < max_improvement_attempts:
                    print(f"   🔄 Próba poprawy {attempts}/{max_improvement_attempts}")
                    section_content = self.improve_section(section_content, audit_result)
                else:
                    print(f"   ⚠️  Osiągnięto limit prób poprawy. Akceptuję obecną wersję.")
            
            article_parts.append(f"\n{section_content}\n")
        
        # Złożenie artykułu
        final_article = "\n".join(article_parts)
        
        print("\n" + "=" * 60)
        print("🎉 ARTYKUŁ UKOŃCZONY!")
        print("=" * 60)
        print(f"📊 Statystyki:")
        print(f"   - Liczba sekcji: {len(sections)}")
        print(f"   - Długość: {len(final_article)} znaków")
        print(f"   - Liczba słów: ~{len(final_article.split())}")
        
        return final_article
    
    def save_article(self, article: str, filename: str = None) -> str:
        """Zapisuje artykuł do pliku."""
        if filename is None:
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            filename = f"article_{timestamp}.md"
        
        filepath = f"/mnt/user-data/outputs/{filename}"
        
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(article)
        
        print(f"\n💾 Artykuł zapisany: {filename}")
        return filepath


def main():
    """Główna funkcja uruchamiająca agenta."""
    print("🤖 Blog Agent - Generator Artykułów")
    print("=" * 60)
    
    # Sprawdzenie klucza API
    if not os.environ.get("ANTHROPIC_API_KEY"):
        print("\n❌ BŁĄD: Brak klucza API!")
        print("Ustaw zmienną środowiskową: export ANTHROPIC_API_KEY='twój-klucz'")
        sys.exit(1)
    
    # Przykładowe użycie
    agent = BlogAgent()
    
    # Temat artykułu
    topic = "Jak AI zmienia sposób tworzenia treści w 2025 roku"
    
    # Opcjonalny dodatkowy kontekst
    additional_context = """
    Artykuł powinien być skierowany do marketerów i twórców treści.
    Skup się na praktycznych zastosowaniach i konkretnych przykładach.
    Uwzględnij zarówno korzyści jak i wyzwania.
    """
    
    # Własne kryteria audytu (opcjonalne)
    custom_audit_criteria = {
        "Wartość praktyczna": "Czy sekcja zawiera konkretne, praktyczne wskazówki?",
        "Przykłady": "Czy użyto rzeczywistych przykładów lub case studies?",
        "Balans": "Czy przedstawiono różne perspektywy (za i przeciw)?",
        "Aktualność": "Czy informacje są aktualne i relewantne dla 2025?",
        "Call to action": "Czy sekcja zachęca do działania lub dalszego myślenia?"
    }
    
    # Tworzenie artykułu
    article = agent.create_article(
        topic=topic,
        additional_context=additional_context,
        audit_criteria=custom_audit_criteria,
        max_improvement_attempts=2
    )
    
    # Zapisanie artykułu
    agent.save_article(article)
    
    print("\n✨ Gotowe! Sprawdź artykuł w katalogu outputs/")


if __name__ == "__main__":
    main()
