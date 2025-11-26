# Prompt: Generowanie Alternatywnych Meta Title i Meta Description

Wygeneruj 2-3 propozycje meta title i meta description dla poniższego artykułu.

**Aktualna data:** {{CURRENT_DATE}} (rok: {{CURRENT_YEAR}})

## Kontekst

**Tytuł artykułu (H1):** {{TYTUL_ARTYKULU}}

**Aktualny Meta Title:** {{CURRENT_META_TITLE}}

**Aktualna Meta Description:** {{CURRENT_META_DESCRIPTION}}

**Grupa docelowa:** {{TARGET_AUDIENCE}}

{{KEYWORDS_SECTION}}

{{SUMMARY_SECTION}}

{{OUTLINE_SECTION}}

## Wymagania

### Meta Title (2-3 propozycje)
- **Długość:** 50-60 znaków (krytyczne dla SEO)
- **Różny od H1:** Musi być inny niż tytuł artykułu (H1)
- **Słowa kluczowe:** Zawiera główne słowa kluczowe z artykułu
- **CTA element:** Może zawierać element zachęty (np. "Sprawdź", "Dowiedz się", "Poznaj")
- **Unikalność:** Każda propozycja powinna mieć inny kąt/approach

### Meta Description (2-3 propozycje)
- **Długość:** 140-160 znaków (krytyczne dla SEO)
- **Wartość:** Odpowiedz na pytanie "Dlaczego warto przeczytać TEN artykuł?" - co konkretnie czytelnik znajdzie w środku
- **CTA:** Element zachęty do kliknięcia (opcjonalny)
- **Słowa kluczowe:** Naturalne wplecenie głównych słów kluczowych
- **Odzwierciedlaj treść:** Bazuj na summary points i outline - opisz co NAPRAWDĘ jest w artykule

## Format Odpowiedzi

```
=== PROPOZYCJA 1 ===

Meta Title: [50-60 znaków]
Meta Description: [140-160 znaków]

Approach: [Krótki opis podejścia, np. "Fokus na konkretne korzyści"]

---

=== PROPOZYCJA 2 ===

Meta Title: [50-60 znaków]
Meta Description: [140-160 znaków]

Approach: [Krótki opis podejścia]

---

=== PROPOZYCJA 3 ===

Meta Title: [50-60 znaków]
Meta Description: [140-160 znaków]

Approach: [Krótki opis podejścia]
```

## Przykłady Dobrych Praktyk

### Meta Title - Dobre praktyki:
- ✅ "Strony internetowe: Koszty, technologie i wybór [Poradnik]"
- ✅ "Jak wybrać CMS? Porównanie WordPress, Payload i Strapi"
- ✅ "RODO w e-commerce: Praktyczny checklist dla przedsiębiorców"

**WAŻNE - Aktualna data:** Jeśli dodajesz rok w meta title lub description, ZAWSZE użyj aktualnego roku ({{CURRENT_YEAR}}), NIE używaj starych dat!

### Meta Title - Złe praktyki:
- ❌ "Artykuł o stronach internetowych" (za ogólny, brak value)
- ❌ "Wszystko co musisz wiedzieć o RODO w sklepach internetowych e-commerce" (za długi, >60 znaków)
- ❌ Identyczny z H1 (brak różnicowania)

### Meta Description - Dobre praktyki:
- ✅ "Praktyczny przewodnik migracji strony bez utraty ruchu. Poznaj proces przenoszenia, backup, testy i monitorowanie. Sprawdź najlepsze praktyki."
- ✅ "Headless CMS oddziela frontend od backendu dla pełnej elastyczności. Poznaj architekturę, narzędzia i kiedy warto zmienić podejście do zarządzania treścią."
- ✅ "Redesign czy optymalizacja istniejącej strony? Framework decyzyjny z analizą potrzeb, kosztów i ryzyk. Podejmij świadomą decyzję dla swojej firmy."

### Meta Description - Złe praktyki:
- ❌ "Artykuł o RODO" (za krótki, brak wartości)
- ❌ "Dowiedz się wszystko o..." (za ogólny, clickbait bez value)
- ❌ Przekracza 160 znaków (zostanie ucięty w wynikach wyszukiwania)

## Wskazówki

1. **Różne kąty:** Każda propozycja powinna mieć inne podejście (np. problem-rozwiązanie, porównanie, przewodnik praktyczny)
2. **Keywords:** Naturalnie wpleć słowa kluczowe z artykułu (focus_keyword + additional_keywords)
3. **Odzwierciedlaj treść artykułu:** Bazuj na tym co NAPRAWDĘ jest w artykule:
   - **Summary points** - główne tematy i wartości dla czytelnika
   - **Outline** - jakie konkretne sekcje są omówione
   - **Unikalny kąt** - co wyróżnia TEN artykuł (np. focus na praktyczne narzędzia, case studies, porównania)
4. **Zachęć do przeczytania:** Odpowiedz na pytanie "Co konkretnie czytelnik znajdzie w tym artykule?"
5. **Target audience:** Dopasuj język do grupy docelowej (przedsiębiorcy, developerzy, etc.)
6. **Naturalność:** Pisz naturalnie - bez wymuszonych fraz, liczb czy szablonów

**WAŻNE:** Każda propozycja musi mieścić się w limitach znaków. To kluczowe dla SEO!
