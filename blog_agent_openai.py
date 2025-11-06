#!/usr/bin/env python3
"""
Blog Agent - wersja dla OpenAI (GPT-4/GPT-3.5)
Identyczna funkcjonalność jak wersja Claude, tylko inna platforma AI
"""

from openai import OpenAI
import os
import sys
import json
from typing import List, Dict
from datetime import datetime


class BlogAgentOpenAI:
    def __init__(self, api_key: str = None, model: str = "gpt-4-turbo-preview"):
        """Inicjalizacja agenta z kluczem API OpenAI."""
        self.api_key = api_key or os.environ.get("OPENAI_API_KEY")
        if not self.api_key:
            raise ValueError("Brak klucza API. Ustaw OPENAI_API_KEY lub przekaż jako argument.")
        
        self.client = OpenAI(api_key=self.api_key)
        self.model = model  # Opcje: "gpt-4-turbo-preview", "gpt-4", "gpt-3.5-turbo"
        
    def _call_api(self, prompt: str, max_tokens: int = 4000) -> str:
        """Pomocnicza metoda do wywołania API."""
        response = self.client.chat.completions.create(
            model=self.model,
            max_tokens=max_tokens,
            messages=[{"role": "user", "content": prompt}]
        )
        return response.choices[0].message.content.strip()
        
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

        response_text = self._call_api(prompt)
        
        try:
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

        content = self._call_api(prompt, max_tokens=3000)
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

        response_text = self._call_api(prompt, max_tokens=2000)
        
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

        improved_content = self._call_api(prompt, max_tokens=3000)
        print(f"   ✅ Sekcja poprawiona")
        
        return improved_content
    
    def create_article(
        self, 
        topic: str, 
        additional_context: str = "",
        audit_criteria: Dict = None,
        max_improvement_attempts: int = 2
    ) -> str:
        """Tworzy kompletny artykuł blogowy."""
        if audit_criteria is None:
            audit_criteria = {
                "Wartość merytoryczna": "Czy sekcja dostarcza konkretnej, wartościowej wiedzy?",
                "Czytelność": "Czy tekst jest łatwy do czytania i dobrze sformatowany?",
                "Spójność": "Czy sekcja pasuje do całości artykułu?",
                "Angażowanie": "Czy treść jest interesująca i trzyma uwagę czytelnika?",
                "Kompletność": "Czy wszystkie kluczowe punkty zostały omówione?"
            }
        
        print("\n" + "=" * 60)
        print("🚀 START PROCESU TWORZENIA ARTYKUŁU (OpenAI)")
        print("=" * 60)
        print(f"Model: {self.model}")
        
        outline = self.create_outline(topic, additional_context)
        
        context = {
            "title": outline.get('title', 'Artykuł'),
            "introduction": outline.get('introduction', '')
        }
        
        article_parts = []
        article_parts.append(f"# {context['title']}\n")
        article_parts.append(f"{context['introduction']}\n")
        
        sections = outline.get('sections', [])
        
        for i, section in enumerate(sections, 1):
            print(f"\n{'=' * 60}")
            print(f"📝 SEKCJA {i}/{len(sections)}")
            print(f"{'=' * 60}")
            
            section_content = self.write_section(section, context)
            
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
        
        final_article = "\n".join(article_parts)
        
        print("\n" + "=" * 60)
        print("🎉 ARTYKUŁ UKOŃCZONY!")
        print("=" * 60)
        print(f"📊 Statystyki:")
        print(f"   - Model: {self.model}")
        print(f"   - Liczba sekcji: {len(sections)}")
        print(f"   - Długość: {len(final_article)} znaków")
        print(f"   - Liczba słów: ~{len(final_article.split())}")
        
        return final_article
    
    def save_article(self, article: str, filename: str = None) -> str:
        """Zapisuje artykuł do pliku."""
        if filename is None:
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            filename = f"article_openai_{timestamp}.md"
        
        filepath = f"/mnt/user-data/outputs/{filename}"
        
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(article)
        
        print(f"\n💾 Artykuł zapisany: {filename}")
        return filepath


def main():
    """Główna funkcja uruchamiająca agenta."""
    print("🤖 Blog Agent - OpenAI Version")
    print("=" * 60)
    
    if not os.environ.get("OPENAI_API_KEY"):
        print("\n❌ BŁĄD: Brak klucza API!")
        print("Ustaw zmienną środowiskową: export OPENAI_API_KEY='twój-klucz'")
        sys.exit(1)
    
    # Możesz wybrać model
    # "gpt-4-turbo-preview" - najlepszy, ale droższy
    # "gpt-4" - bardzo dobry
    # "gpt-3.5-turbo" - tańszy, szybszy, nieco gorsza jakość
    
    agent = BlogAgentOpenAI(model="gpt-4-turbo-preview")
    
    topic = "Jak AI zmienia sposób tworzenia treści w 2025 roku"
    
    additional_context = """
    Artykuł powinien być skierowany do marketerów i twórców treści.
    Skup się na praktycznych zastosowaniach i konkretnych przykładach.
    Uwzględnij zarówno korzyści jak i wyzwania.
    """
    
    custom_audit_criteria = {
        "Wartość praktyczna": "Czy sekcja zawiera konkretne, praktyczne wskazówki?",
        "Przykłady": "Czy użyto rzeczywistych przykładów lub case studies?",
        "Balans": "Czy przedstawiono różne perspektywy (za i przeciw)?",
        "Aktualność": "Czy informacje są aktualne i relewantne dla 2025?",
        "Call to action": "Czy sekcja zachęca do działania lub dalszego myślenia?"
    }
    
    article = agent.create_article(
        topic=topic,
        additional_context=additional_context,
        audit_criteria=custom_audit_criteria,
        max_improvement_attempts=2
    )
    
    agent.save_article(article)
    
    print("\n✨ Gotowe! Sprawdź artykuł w katalogu outputs/")


if __name__ == "__main__":
    main()
