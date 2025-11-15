# 🧩 Konspekt artykułu

**Zadanie:**  
Przygotuj szczegółowy i unikalny konspekt artykułu na blog Digital Vantage.

## 🔖 Dane wejściowe
- **Temat artykułu:** `{{TEMAT_ARTYKULU}}`
- **Adres (URL):** `{{URL_ARTYKULU}}`
- **Kontekst / główny cel:** `{{KONTEKST_TEMATU}}`

## ✍️ Wymagania dla konspektu

**WAŻNE:** Konspekt to PLAN artykułu, nie gotowy artykuł. Każda sekcja powinna zawierać:
1. Tytuł sekcji (H2)
2. **Docelową długość w formacie `(~XXX słów)`** - KRYTYCZNE!
3. Punkty/tematy do omówienia (lista)

Dodatkowe wymagania:
1. Konspekt ma być szczegółowy, logicznie ułożony i unikalny.
2. Uwzględnij pytania, które może zadać czytelnik.
3. Artykuł powinien dawać realną wartość – praktyczne wskazówki i inspiracje.
4. Zakończ propozycją **tytułu H1 wspierającego SEO**.
5. Uwzględnij **strukturę nagłówków H2–H4** zgodną z zasadami SEO:
   - H2 = główne sekcje
   - H3 = rozwinięcia
   - H4 = szczegóły lub przykłady
6. Wynik ma byc w formacie **markdown** bez dodawania nagłówków H2–H4 na poczatku tytułu
7. Nagłówki powinny:
   - zawierać naturalne słowa kluczowe,
   - być czytelne, zrozumiałe i spójne z tonem Digital Vantage.

## 📋 FORMAT KONSPEKTU - JAK POWINIEN WYGLĄDAĆ

**Przykład poprawnego konspektu:**

```markdown
## 1. Wprowadzenie
(~200 słów)
- Przedstawienie problemu/tematu
- Dlaczego jest ważny
- Co czytelnik zyska z artykułu

## 2. Kluczowy aspekt #1
(~300 słów)

### Podtemat A
- Główne punkty do omówienia
- Przykłady lub case study
- Praktyczne wskazówki

## 3. Kluczowy aspekt #2
(~350 słów)

### Podtemat B
- Szczegółowe rozwinięcie
- Konkretne techniki
- Częste błędy i jak ich unikać

## 4. Podsumowanie
(~150 słów)
- Kluczowe wnioski
- Następne kroki dla czytelnika
- Call to action
```

**NIE** pisz pełnych akapitów w konspekcie - pisz tylko punkty do omówienia!

---

## 📊 Długość i zakres

**KRYTYCZNE:** Konspekt musi zawierać docelową długość dla KAŻDEJ sekcji w formacie `(~XXX słów)`.

Zasady planowania długości:
- **Rozkład słów:** Suma długości wszystkich sekcji MUSI być równa docelowej długości artykułu (z kontekstu)
- **Typowe długości sekcji:**
  - Wprowadzenie: 150-250 słów
  - Sekcje główne (H2): 300-400 słów każda
  - Podsumowanie: 100-200 słów

**Przykład dla artykułu 1500 słów:**
- Wprowadzenie (200) + 4 sekcje główne (4×300=1200) + Podsumowanie (100) = 1500 słów

**Przykład dla artykułu 2500 słów:**
- Wprowadzenie (250) + 6 sekcji głównych (6×350=2100) + Podsumowanie (150) = 2500 słów

Dostosuj liczbę i długość sekcji do docelowej długości artykułu podanej w kontekście.

**UWAGA:** FAQ i Checklist są generowane w oddzielnych krokach workflow i NIE są częścią głównego artykułu.

---

## ⚠️ KLUCZOWE PRZYPOMNIENIE

**TO MA BYĆ KONSPEKT, NIE GOTOWY ARTYKUŁ!**

✅ **DOBRZE:**
```markdown
## 2. Jak wybrać model LLM dla swojego projektu
(~350 słów)
- Porównanie wielkości modeli (7B, 13B, 70B+)
- Trade-offy: jakość vs. koszt vs. szybkość
- Kryteria wyboru dla różnych use case
- Przykłady dobrych dopasowań (chatbot, generowanie treści, analiza)
```

❌ **ŹLE:**
```markdown
## 2. Jak wybrać model LLM dla swojego projektu
Wybór odpowiedniego modelu LLM to kluczowa decyzja, która wpływa na sukces całego projektu. Musisz wziąć pod uwagę wiele czynników, takich jak rozmiar modelu, jakość odpowiedzi, koszt... [pełne akapity...]
```

**Pisz PLAN (punkty), nie pełne treści!** Treści będą generowane w kolejnym kroku workflow.