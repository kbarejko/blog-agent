# Prompt: Generowanie postów na social media

ZADANIE: Na podstawie artykułu przygotuj zestaw do social mediów.

## ARTYKUŁ

**Tytuł:** {{ARTICLE_TITLE}}

**URL:** {{ARTICLE_URL}}

**Treść artykułu:**
{{ARTICLE_CONTENT}}

---

## PARAMETRY

**GRUPA DOCELOWA:** {{TARGET_AUDIENCE}}

**JĘZYK I TON:** polski, profesjonalny i ekspercki, prosty (bez żargonu).

**CEL:** zwiększyć wejścia na artykuł (edukacyjny charakter, mocny hook).

---

## WYGENERUJ:

### 1) POST (Facebook/LinkedIn/Instagram)
**Długość:** 80 znaków ±5

**Wymagania:**
- Jasny hook
- Korzyść dla czytelnika
- Bez skrótów w nagłówku
- Fokus na problem/korzyść (nie parafrazuj tytułu 1:1)

### 2) 4 ALTERNATYWNE TYTUŁY
**Wymagania:**
- Mocny hook
- Krótkie, zrozumiałe dla nietechnicznych
- Fokus na korzyść/rozwiązanie problemu

### 3) PIERWSZY KOMENTARZ

**Struktura:**

**Co znajdziesz w artykule?**
- [4-6 punktorów z konkretnymi korzyściami/tematami]

**Link:** {{ARTICLE_URL}}

**Wyjaśnienia skrótów:**
[Jeśli występują skróty w komentarzu (np. SEO, ERP, LTV) - rozwiń je prosto]

**Hashtagi:**
[10 hasztagów dobranych do tematu i grupy docelowej]

---

## ZASADY:

1. **Jasność:** Pisz jasno, konkretnie, bez żargonu
2. **Skróty:** Zawsze rozwijaj w sekcji "Wyjaśnienia skrótów"
3. **Hashtagi:** TYLKO w pierwszym komentarzu (nie w poście)
4. **Ton:** Spójny, biznesowy, fokus na korzyści
5. **Hook:** Ukierunkowany na problem/korzyść, nie parafrazowanie tytułu

---

## FORMAT ODPOWIEDZI:

Zwróć odpowiedź w formacie JSON:

```json
{
  "post": "Treść posta (80±5 znaków)",
  "alternative_titles": [
    "Tytuł alternatywny 1",
    "Tytuł alternatywny 2",
    "Tytuł alternatywny 3",
    "Tytuł alternatywny 4"
  ],
  "first_comment": {
    "intro": "Co znajdziesz w artykule?",
    "bullets": [
      "Punkt 1 - konkretna korzyść",
      "Punkt 2 - konkretna korzyść",
      "Punkt 3 - konkretna korzyść",
      "Punkt 4 - konkretna korzyść"
    ],
    "link": "{{ARTICLE_URL}}",
    "acronym_explanations": {
      "SEO": "Search Engine Optimization - optymalizacja pod wyszukiwarki",
      "ROI": "Return on Investment - zwrot z inwestycji"
    },
    "hashtags": [
      "#ecommerce",
      "#biznesonline",
      "#digitalmarketing",
      "#przedsiębiorczość",
      "#marketing",
      "#sprzedaż",
      "#biznes",
      "#startup",
      "#rozwójbiznesu",
      "#strategia"
    ]
  }
}
```

**WAŻNE:** Zwróć TYLKO JSON bez dodatkowych komentarzy czy markdown blocków.
