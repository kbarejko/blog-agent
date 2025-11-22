# Prompt: Generowanie Alternatywnych Meta Title i Meta Description

Wygeneruj 2-3 propozycje meta title i meta description dla poniższego artykułu.

## Kontekst

**Tytuł artykułu (H1):** {{TYTUL_ARTYKULU}}

**Aktualny Meta Title:** {{CURRENT_META_TITLE}}

**Aktualna Meta Description:** {{CURRENT_META_DESCRIPTION}}

**Treść artykułu (fragment):**
```
{{ARTICLE_CONTENT}}
```

## Wymagania

### Meta Title (2-3 propozycje)
- **Długość:** 50-60 znaków (krytyczne dla SEO)
- **Różny od H1:** Musi być inny niż tytuł artykułu (H1)
- **Słowa kluczowe:** Zawiera główne słowa kluczowe z artykułu
- **CTA element:** Może zawierać element zachęty (np. "Sprawdź", "Dowiedz się", "Poznaj")
- **Unikalność:** Każda propozycja powinna mieć inny kąt/approach

### Meta Description (2-3 propozycje)
- **Długość:** 140-160 znaków (krytyczne dla SEO)
- **Wartość:** Konkretna wartość dla czytelnika, nie ogólniki
- **CTA:** Element zachęty do kliknięcia
- **Słowa kluczowe:** Naturalne wplecenie głównych słów kluczowych
- **Liczby/dane:** Jeśli artykuł zawiera konkretne dane, użyj ich

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
- ✅ "Strony internetowe 2025: Koszty, technologie i wybór [Poradnik]"
- ✅ "Jak wybrać CMS? Porównanie WordPress, Payload i Strapi"
- ✅ "RODO w e-commerce: Praktyczny checklist dla przedsiębiorców"

### Meta Title - Złe praktyki:
- ❌ "Artykuł o stronach internetowych" (za ogólny, brak value)
- ❌ "Wszystko co musisz wiedzieć o RODO w sklepach internetowych e-commerce" (za długi, >60 znaków)
- ❌ Identyczny z H1 (brak różnicowania)

### Meta Description - Dobre praktyki:
- ✅ "Sprawdź koszty budowy strony www w 2025. Porównanie CMS, hosting, domeny + ukryte koszty. Praktyczny przewodnik dla przedsiębiorców."
- ✅ "WordPress czy headless CMS? Poznaj zalety i wady 7 platform. Wybierz najlepsze rozwiązanie dla swojego biznesu + checklist 15 pkt."

### Meta Description - Złe praktyki:
- ❌ "Artykuł o RODO" (za krótki, brak wartości)
- ❌ "Dowiedz się wszystko o..." (za ogólny, clickbait bez value)
- ❌ Przekracza 160 znaków (zostanie ucięty w wynikach wyszukiwania)

## Wskazówki

1. **Diversification:** Każda propozycja powinna mieć inny kąt (np. koszty, porównanie, przewodnik krok po kroku)
2. **Keywords:** Naturalnie wpleć słowa kluczowe z artykułu
3. **Numbers:** Użyj liczb jeśli artykuł je zawiera (wzrasta CTR o ~30%)
4. **Action words:** Użyj czasowników akcji (Sprawdź, Poznaj, Dowiedz się, Porównaj)
5. **Target audience:** Dopasuj język do grupy docelowej (przedsiębiorcy, developerzy, etc.)

**WAŻNE:** Każda propozycja musi mieścić się w limitach znaków. To kluczowe dla SEO!
