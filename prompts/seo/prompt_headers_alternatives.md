# Zadanie: Wygeneruj alternatywne propozycje nagłówków SEO

Artykuł: **{{ARTICLE_TITLE}}**

## Aktualne nagłówki w artykule:
{{HEADERS_LIST}}

## Kontekst artykułu (pierwsze 1500 znaków):
{{ARTICLE_EXCERPT}}

---

## Cel zadania:

Dla **KAŻDEGO** nagłówka z listy powyżej wygeneruj **3-4 alternatywne propozycje** które:

1. **Są lepsze od oryginału pod kątem SEO:**
   - Zawierają naturalne słowa kluczowe (keywords)
   - Odpowiadają na user intent (co użytkownik chce znaleźć)
   - Są konkretne i opisowe
   - Przyciągają uwagę w wynikach wyszukiwania

2. **Zachowują naturalność języka:**
   - Brzmią jak normalne zdania, nie jak lista keywordów
   - Są przystępne dla polskich przedsiębiorców
   - Unikają nadmiernej optymalizacji (keyword stuffing)

3. **Różnią się długością i szczegółowością:**
   - **Propozycja 1-2:** Krótka, konkretna (4-8 słów)
   - **Propozycja 3:** **Long-tail** - dłuższa, bardziej szczegółowa fraza (8-12 słów), odpowiadająca na konkretne pytanie użytkownika
   - **Propozycja 4:** Wariant z liczbami/danymi (jeśli pasuje)

## Format odpowiedzi:

Dla KAŻDEGO nagłówka zwróć w formacie:

```
# Original: [Oryginalny nagłówek H1]

**Propozycje SEO:**
1. [Propozycja 1 - krótka i konkretna]
2. [Propozycja 2 - z keyword naturalnie wpleconym]
3. [Propozycja 3 - LONG TAIL - szczegółowa fraza 8-12 słów]
4. [Propozycja 4 - wariant z liczbami/danymi lub inny wymiar]

---

## Original: [Oryginalny nagłówek H2]

**Propozycje SEO:**
1. [Propozycja 1]
2. [Propozycja 2]
3. [Propozycja 3 - LONG TAIL]
4. [Propozycja 4]

---

### Original: [Oryginalny nagłówek H3]

**Propozycje SEO:**
1. [Propozycja 1]
2. [Propozycja 2]
3. [Propozycja 3 - LONG TAIL]
4. [Propozycja 4]

---
```

## Przykład dla nagłówka H2:

**Original:** "Koszty wdrożenia"

**Propozycje SEO:**
1. Ile kosztuje wdrożenie platformy e-commerce?
2. Budżet i koszty wdrożenia sklepu online
3. Ile musisz przeznaczyć na wdrożenie profesjonalnego sklepu internetowego w 2024 roku? (LONG TAIL)
4. Koszty wdrożenia: 5 rzeczy które wpływają na finalny budżet

---

## Ważne zasady:

✅ **Musisz wygenerować propozycje dla KAŻDEGO nagłówka z listy**
✅ Zachowaj hierarchię nagłówków (# dla H1, ## dla H2, ### dla H3)
✅ Oznaczaj long-tail jako "(LONG TAIL)" lub wyraźnie rozbuduj frazę
✅ Uwzględnij polskie słowa kluczowe typowe dla e-commerce/biznesu
✅ Każda propozycja powinna być unikalna i wartościowa

❌ NIE twórz generycznych nagłówków typu "Wprowadzenie", "Podsumowanie"
❌ NIE duplikuj nagłówków - każda propozycja różna
❌ NIE używaj clickbait ("Nie uwierzysz...")
❌ NIE opakowuj w \`\`\`markdown ... \`\`\` - zwróć czysty markdown

---

**Output:** Zwróć czysty markdown zaczynający się od pierwszego nagłówka. Format jak w przykładzie powyżej.
