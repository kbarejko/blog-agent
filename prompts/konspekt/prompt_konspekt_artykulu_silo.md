# 🧩 Konspekt artykułu SILO (artykuł kategorii)

**Zadanie:**
Przygotuj szczegółowy konspekt artykułu **typu SILO** - artykuł główny kategorii, który wprowadza do całego tematu i linkuje do artykułów szczegółowych w silosie.

## 🔖 Dane wejściowe
- **Temat artykułu (kategorii):** `{{TEMAT_ARTYKULU}}`
- **Adres (URL):** `{{URL_ARTYKULU}}`
- **Kontekst / główny cel:** `{{KONTEKST_TEMATU}}`
- **Istniejące artykuły w silosie:** `{{SILO_ARTICLES}}`

## 🎯 Specyfika artykułu SILO

Artykuł SILO różni się od zwykłego artykułu szczegółowego:

### ✅ POWINIEN:
- **Wprowadzać do całego tematu** - dać czytelnikowi szeroki obraz zagadnienia
- **Być przeglądem, nie szczegółowym przewodnikiem** - omówić główne aspekty, ale bez głębokiego wchodzenia w detale
- **Linkować do artykułów w silosie** - naturalnie kierować do bardziej szczegółowych materiałów
- **Być rozszerzalny** - struktura powinna pozwalać na łatwe dodawanie nowych artykułów do silosa
- **Być krótszy niż zwykły artykuł** - około 1500-2000 słów (vs. 3000+ dla artykułu szczegółowego)
- **Pokazywać "mapę tematu"** - pomóc czytelnikowi zrozumieć, jakie aspekty tematu może zgłębić

### ❌ NIE POWINIEN:
- Wchodzić w szczegóły - to zadanie artykułów podrzędnych
- Być kompletnym przewodnikiem - to ma być punkt wyjścia, nie punkt docelowy
- Duplikować treści z artykułów podrzędnych - tylko krótkie wprowadzenia

## ✍️ Wymagania dla konspektu

1. **Konspekt ma być szczegółowy, logicznie ułożony i unikalny**
2. **Struktura powinna wspierać linkowanie wewnętrzne:**
   - Każda sekcja H2 powinna naturalnie otwierać możliwość linku do artykułu szczegółowego
   - Używaj fraz typu "więcej o tym w...", "szczegóły znajdziesz w...", "dowiedz się więcej o..."
3. **Uwzględnij istniejące artykuły w silosie** - każdy z nich powinien być naturalnie wspomniany w odpowiedniej sekcji
4. **Zachowaj możliwość rozszerzania** - struktura powinna pozwalać na dodanie nowych artykułów bez przebudowy całości
5. **Zakończ propozycją tytułu H1 wspierającego SEO** - powinien sugerować, że to artykuł kategorii/przeglądu
6. **Uwzględnij strukturę nagłówków H2–H4** zgodną z zasadami SEO:
   - H2 = główne aspekty tematu (potencjalne miejsca na linki do artykułów)
   - H3 = krótkie rozwinięcia, wprowadzenia
   - H4 = przykłady lub konkretne punkty (opcjonalnie)
7. **Wynik ma być w formacie markdown** bez dodawania nagłówków H2–H4 na początku tytułu
8. **Nagłówki powinny:**
   - Zawierać naturalne słowa kluczowe
   - Być czytelne, zrozumiałe i spójne z tonem Digital Vantage
   - Sugerować szerszy kontekst (nie konkretne szczegóły)

## 📋 Przykładowa struktura artykułu SILO

```markdown
## Wprowadzenie do tematu
[Szeroki kontekst, dlaczego temat jest ważny]

## Główny aspekt #1
[Krótkie wprowadzenie]
[Link: "Dowiedz się więcej w naszym przewodniku: [Artykuł 1]"]

## Główny aspekt #2
[Krótkie wprowadzenie]
[Link: "Szczegóły znajdziesz w: [Artykuł 2]"]

## Główny aspekt #3
[Krótkie wprowadzenie]
[Link: "Przeczytaj więcej: [Artykuł 3]"]

## Jak zacząć? (Przewodnik startowy)
[Praktyczne kroki dla początkujących]

## Najczęstsze błędy
[Krótki przegląd pułapek]

## Najczęściej zadawane pytania (FAQ) ← OBOWIĄZKOWE!
[6-10 pytań z linkami do artykułów w silosie]

## Podsumowanie
[Zachęta do eksploracji szczegółowych artykułów]
```

## 🎯 Wymagane i opcjonalne sekcje

### FAQ (Najczęściej zadawane pytania) - WYMAGANE
**FAQ jest OBOWIĄZKOWE dla wszystkich artykułów SILO**, ponieważ:
- Pomaga w nawigacji po temacie
- Odpowiada na pytania typu "co powinienem przeczytać najpierw?", "od czego zacząć?"
- Może kierować do konkretnych artykułów szczegółowych w silosie
- Wzmacnia SEO dla szerszych zapytań long-tail
- Pomaga czytelnikowi zorientować się w strukturze całego silosa

**Format:**
```markdown
## Najczęściej zadawane pytania (FAQ)

### 1. Od czego zacząć z [temat]?
Zwięzła odpowiedź z linkiem do artykułu startowego (jeśli istnieje).

### 2. Jaka jest różnica między [aspekt A] a [aspekt B]?
Odpowiedź z linkami do odpowiednich artykułów szczegółowych.

### 3. Który artykuł powinienem przeczytać najpierw?
Wskazówki dotyczące kolejności czytania artykułów w silosie.

[...optimum: 6-10 pytań dla artykułów SILO]
```

**WAŻNE dla FAQ w artykułach SILO:**
- Minimum 5 pytań, optimum 6-10 pytań
- Przynajmniej 2-3 pytania powinny zawierać linki do artykułów szczegółowych w silosie
- Pytania powinny pomagać w nawigacji (np. "Który aspekt jest najważniejszy?", "Od czego zacząć?")
- Pytania typu "co dalej?" mogą wskazywać na potencjalne przyszłe artykuły

### Checklist (Lista kontrolna) - OPCJONALNY
**Dla artykułów SILO Checklist jest OPCJONALNY**:
- Dodaj TYLKO jeśli temat można podsumować jako listę kroków do wykonania
- Checklist powinien być high-level, nie szczegółowy
- Może zawierać linki do artykułów szczegółowych dla każdego kroku

**Format:**
```markdown
## Checklist - [Temat] w pigułce
- [ ] Krok 1 (high-level) → [Link do artykułu szczegółowego]
- [ ] Krok 2 (high-level) → [Link do artykułu szczegółowego]
- [ ] ...
```

## ⚠️ WAŻNE instrukcje dla AI

1. **ZAWSZE uwzględnij wszystkie istniejące artykuły** z listy {{SILO_ARTICLES}} w konspekcie
2. **FAQ jest OBOWIĄZKOWE** - każdy konspekt artykułu SILO MUSI zawierać sekcję FAQ z minimum 5 pytaniami (optimum 6-10)
3. **ZAPLANUJ miejsca na przyszłe artykuły** - struktura powinna mieć "luki", które można wypełnić
4. **Zachowaj balans** - artykuł ma być wartościowy sam w sobie, ale też zachęcać do czytania dalej
5. **Użyj natural language** dla linków wewnętrznych - nie "kliknij tutaj", ale "dowiedz się więcej o [temat konkretny]"
6. **Każda sekcja H2 to potencjalne miejsce na link** do artykułu szczegółowego (istniejącego lub przyszłego)
7. **FAQ musi zawierać linki** - przynajmniej 2-3 pytania w FAQ powinny kierować do konkretnych artykułów w silosie

## 📊 Długość i zakres

- **Długość docelowa:** 1500-2500 słów (krócej niż zwykły artykuł)
- **Liczba sekcji H2:** 5-8 (każda = potencjalny artykuł szczegółowy)
- **Głębokość:** Wprowadzająca, nie szczegółowa
- **Cel:** Dać czytelnikowi "mapę" tematu i skierować go do właściwego artykułu szczegółowego
