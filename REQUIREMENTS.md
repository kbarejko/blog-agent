# Blog Agent - Specyfikacja Wymagań

**Data utworzenia:** 2025-11-06
**Status:** Finalna specyfikacja przed implementacją
**Wersja:** 1.0

---

## 1. Przegląd systemu

### 1.1 Cel projektu
Automatyczny system do tworzenia wysokiej jakości artykułów blogowych z wykorzystaniem AI (Claude), wspierający:
- Generowanie konspektów na podstawie tematu
- Pisanie artykułów po sekcjach z automatycznym review
- Optymalizację SEO i humanizację treści
- Automatyczne przypisywanie kategorii
- Wersjonowanie z git commits

### 1.2 Kluczowe założenia
- **Struktura folderów = Struktura URL** (1:1 mapping)
- **Serie/Huby → Silosy → Artykuły** (hierarchiczna organizacja)
- **Kategorie niezależne** od struktury folderów (many-to-many)
- **Proces w pełni automatyczny** po uruchomieniu
- **Review AI** na każdym etapie z auto-fix
- **Git versioning** w kluczowych momentach

---

## 2. Struktura projektu

### 2.1 Organizacja folderów

```
blog-agent/
├── artykuly/                           # Root artykułów
│   ├── [seria]/                        # np. ecommerce, saas, ai, mobile
│   │   ├── [silos]/                    # np. operacje, platformy, seo
│   │   │   ├── [slug-artykulu]/        # slug z tytułu (kebab-case)
│   │   │   │   ├── config.yaml         # konfiguracja artykułu (user input)
│   │   │   │   ├── outline.md          # konspekt (AI generated)
│   │   │   │   ├── sections/           # sekcje robocze (opcjonalne)
│   │   │   │   │   ├── 01-intro.md
│   │   │   │   │   ├── 02-section.md
│   │   │   │   │   └── ...
│   │   │   │   ├── draft.md            # draft przed humanizacją
│   │   │   │   ├── article.md          # finalna wersja (publikowana)
│   │   │   │   └── categories.yaml     # przypisane kategorie
│
├── prompts/                            # Szablony promptów
│   ├── konspekt/
│   │   └── prompt_konspekt_artykulu.md
│   ├── articles/
│   │   ├── prompt_artykul_common.md    # wspólne wytyczne
│   │   ├── prompt_artykul_start.md
│   │   └── prompt_artykul_kontynuacja.md
│   └── audyt/
│       ├── prompt_sprawdz_naglowki.md
│       └── prompt_sprawdz_styl.md
│
├── kategoria-artykulow.xlsx            # 147 kategorii hierarchicznych
├── blog_agent.py                       # główny skrypt (do przebudowy)
└── requirements.txt                    # zależności Python
```

### 2.2 Przykład struktury artykułu

**Folder:**
```
artykuly/ecommerce/operacje/bezpieczenstwo-i-rodo/
```

**URL:**
```
https://www.digitalvantage.pl/artykuly/ecommerce/operacje/bezpieczenstwo-i-rodo/
```

**Kategorie (niezależne od URL):**
```
- E-commerce
- Strategia IT
- RODO i Zgodność
- Bezpieczeństwo IT
```

---

## 3. Konfiguracja artykułu (config.yaml)

### 3.1 Format pliku

```yaml
# === USER INPUT (wymagane) ===
title: "Bezpieczeństwo i RODO w e-commerce - minimum higieniczne które chroni sprzedaż"
target_audience: "Właściciele sklepów e-commerce, małe i średnie firmy"
tone: "ekspercki, ale naturalny i rozmowny"

# === AI GENERATED (automatyczne) ===
# Generowane przez AI podczas procesu:
meta_title: "Bezpieczeństwo e-commerce: praktyczny przewodnik RODO 2025"
meta_description: "Dowiedz się jak zabezpieczyć sklep online i spełnić wymagania RODO. Praktyczne wskazówki dla e-commerce w 2025."

# === COMPUTED (z struktury folderów) ===
# Automatycznie wypełniane przez system:
# slug: bezpieczenstwo-i-rodo
# series: ecommerce
# silo: operacje
# url: /artykuly/ecommerce/operacje/bezpieczenstwo-i-rodo/
# full_path: artykuly/ecommerce/operacje/bezpieczenstwo-i-rodo
```

### 3.2 Pola wymagane od użytkownika

| Pole | Typ | Opis | Przykład |
|------|-----|------|----------|
| `title` | string | Tytuł artykułu (H1) | "Bezpieczeństwo i RODO w e-commerce..." |
| `target_audience` | string | Grupa docelowa | "Właściciele sklepów e-commerce" |
| `tone` | string | Ton/styl artykułu | "ekspercki, ale naturalny i rozmowny" |

### 3.3 Pola generowane przez AI

| Pole | Typ | Kiedy | Opis |
|------|-----|-------|------|
| `meta_title` | string | Po outline | Tytuł SEO (≠ H1, max 60 znaków) |
| `meta_description` | string | Po outline | Opis SEO (max 160 znaków) |

---

## 4. Proces tworzenia artykułu

### 4.1 Workflow (8 kroków)

```
┌─────────────────────────────────────────────────────────────┐
│  KROK 0: INICJALIZACJA (opcjonalne)                        │
│  • User tworzy folder + config.yaml                         │
│  • LUB: `blog_agent.py init` tworzy strukturę              │
└─────────────────┬───────────────────────────────────────────┘
                  │
                  ▼
┌─────────────────────────────────────────────────────────────┐
│  KROK 1: KONSPEKT                                           │
│  • Prompt: prompt_konspekt_artykulu.md                      │
│  • Input: title, target_audience, tone z config            │
│  • Output: outline.md (struktura H2-H4, kluczowe punkty)   │
│  • AI generuje: meta_title, meta_description                │
│  • AI decyduje: czy dodać Checklist i/lub FAQ (opcjonalne) │
│  • Git commit: "[series/silo/slug] Create outline"         │
└─────────────────┬───────────────────────────────────────────┘
                  │
                  ▼
┌─────────────────────────────────────────────────────────────┐
│  KROK 2: PISANIE - Wprowadzenie + Sekcja 1                 │
│  • Prompt: prompt_artykul_start.md + prompt_artykul_common │
│  • Input: outline, wytyczne wspólne                         │
│  • Output: sections/01-intro.md (300-400 słów)             │
│  • Review AI: długość, styl, czytelność                     │
│  • Auto-fix jeśli nie spełnia kryteriów                     │
└─────────────────┬───────────────────────────────────────────┘
                  │
                  ▼
┌─────────────────────────────────────────────────────────────┐
│  KROK 3: PISANIE - Sekcje 2, 3, 4...N + Opcjonalne         │
│  • Prompt: prompt_artykul_kontynuacja.md + common          │
│  • Input: outline, poprzednia sekcja                        │
│  • Output: sections/02-xxx.md, 03-xxx.md...                │
│  • Review AI po każdej sekcji                               │
│  • Loop: dla każdej sekcji z outline                        │
│  • Opcjonalnie: Checklist (jeśli w outline)                │
│  • Opcjonalnie: FAQ (do 10 pytań, jeśli w outline)         │
└─────────────────┬───────────────────────────────────────────┘
                  │
                  ▼
┌─────────────────────────────────────────────────────────────┐
│  KROK 4: DRAFT                                              │
│  • Połączenie wszystkich sekcji → draft.md                  │
│  • Git commit: "[series/silo/slug] Complete draft"         │
└─────────────────┬───────────────────────────────────────────┘
                  │
                  ▼
┌─────────────────────────────────────────────────────────────┐
│  KROK 5: SEO REVIEW - Nagłówki                             │
│  • Prompt: prompt_sprawdz_naglowki.md                       │
│  • Input: draft.md                                          │
│  • Check: struktura H1-H4, słowa kluczowe, hierarchia      │
│  • Auto-fix: poprawia nagłówki jeśli potrzeba              │
└─────────────────┬───────────────────────────────────────────┘
                  │
                  ▼
┌─────────────────────────────────────────────────────────────┐
│  KROK 6: HUMANIZACJA                                        │
│  • Prompt: prompt_sprawdz_styl.md                           │
│  • Input: draft.md (po SEO review)                          │
│  • Output: article.md (finalna wersja)                      │
│  • Cél: naturalny język, brak AI tone, Flesch 40-60        │
└─────────────────┬───────────────────────────────────────────┘
                  │
                  ▼
┌─────────────────────────────────────────────────────────────┐
│  KROK 7: PUBLIKACJA                                         │
│  • Finalna wersja zapisana jako article.md                  │
│  • Git commit: "[series/silo/slug] Publish article"        │
└─────────────────┬───────────────────────────────────────────┘
                  │
                  ▼
┌─────────────────────────────────────────────────────────────┐
│  KROK 8: KATEGORIE                                          │
│  • AI analizuje gotowy artykuł (article.md)                 │
│  • Wybiera 1-5 kategorii z kategoria-artykulow.xlsx        │
│  • Sugeruje nowe jeśli brak odpowiednich                    │
│  • Output: categories.yaml (lub sekcja w outline.md)       │
│  • Git commit: "[series/silo/slug] Assign categories"      │
└─────────────────────────────────────────────────────────────┘
```

### 4.2 Timing (szacunkowy)

| Krok | Czas | % |
|------|------|---|
| Konspekt | ~30s | 10% |
| Pisanie sekcji (x5) | ~2m | 40% |
| Review sekcji (x5) | ~1m | 20% |
| SEO Review | ~20s | 7% |
| Humanizacja | ~40s | 13% |
| Kategorie | ~20s | 7% |
| Git commits | ~10s | 3% |
| **RAZEM** | **~5min** | **100%** |

### 4.3 Opcjonalne sekcje (AI decision)

AI podczas tworzenia konspektu (Krok 1) decyduje, czy artykuł będzie zawierał opcjonalne sekcje:

#### 4.3.1 Checklist (Lista kontrolna)

**Kiedy stosować:**
- Artykuły typu "jak zrobić", "przewodnik", "implementacja"
- Tematy wymagające kroków do wykonania
- Audyty, przeglądy, procesy wdrożeniowe

**Format:**
```markdown
## Checklist - [Tytuł Checklisty]

Użyj tej listy, aby upewnić się, że niczego nie pominąłeś:

- [ ] Krok 1: Opis co zrobić
- [ ] Krok 2: Kolejny krok
- [ ] Krok 3: Jeszcze jeden krok
- [ ] ...

💡 **Tip:** Możesz zapisać tę listę i wykorzystać ją podczas wdrożenia.
```

**Przykłady tematów z Checklist:**
- "Bezpieczeństwo i RODO w e-commerce" → Checklist audytu bezpieczeństwa
- "Migracja sklepu e-commerce" → Checklist migracji
- "Wdrożenie nowej platformy" → Checklist wdrożenia

**Kiedy NIE stosować:**
- Artykuły teoretyczne/koncepcyjne
- Porównania, analizy, opinie
- Historie, case studies

#### 4.3.2 FAQ (Najczęściej zadawane pytania)

**Kiedy stosować:**
- Tematy budzące wiele wątpliwości
- Złożone zagadnienia wymagające wyjaśnień
- Popularne pytania od czytelników/klientów
- Tematy SEO (FAQ dobre dla long-tail keywords)

**Format:**
```markdown
## Najczęściej zadawane pytania (FAQ)

### 1. Pytanie pierwsze?

Odpowiedź na pytanie pierwsze. Konkretna, merytoryczna, 2-4 zdania.

### 2. Pytanie drugie?

Odpowiedź na pytanie drugie...

### 3. Pytanie trzecie?

Odpowiedź...

[...do 10 pytań maksymalnie]
```

**Zasady dla FAQ:**
- Maksymalnie 10 pytań (optimum: 5-7)
- Pytania konkretne, naturalne (jak by zadał użytkownik)
- Odpowiedzi zwięzłe ale merytoryczne (2-4 zdania)
- Pytania uporządkowane od podstawowych do zaawansowanych
- Odpowiedzi w spójnym tonie z resztą artykułu

**Przykłady tematów z FAQ:**
- "Bezpieczeństwo i RODO w e-commerce" → FAQ o certyfikatach, zgodności, karach
- "Wybór platformy e-commerce" → FAQ o kosztach, integracji, skalowaniu
- "Płatności online w Polsce" → FAQ o prowizjach, bezpieczeństwie, integracji

**Kiedy NIE stosować:**
- Artykuł krótki/prosty (FAQ byłby dłuższy niż treść główna)
- Temat bardzo niszowy bez popularnych pytań
- Listy typu "10 narzędzi" (FAQ nie ma sensu)

#### 4.3.3 Kombinacje

AI może zdecydować o:
- **Tylko Checklist** - artykuły implementacyjne
- **Tylko FAQ** - artykuły wyjaśniające
- **Oba** - kompleksowe przewodniki
- **Żadne** - artykuły teoretyczne, opinie, case studies

**Przykład kombinacji OBA:**
"Wdrożenie RODO w sklepie e-commerce"
- Główne sekcje: wymagania, implementacja, dokumentacja
- Checklist: 15 punktów kontrolnych do sprawdzenia
- FAQ: 7 pytań o kary, terminy, zgody użytkowników

#### 4.3.4 Umiejscowienie w artykule

**Kolejność sekcji:**
1. Wprowadzenie
2. Sekcje główne (z konspektu)
3. **Checklist** (jeśli jest)
4. **FAQ** (jeśli jest)
5. Podsumowanie (opcjonalne)

**Nie ma:**
- Nagłówków typu "Podsumowanie" lub "Wnioski" (nudne, sztuczne)
- Wezwań do działania (CTA) - to blog, nie landing page
- Autopromoacji

---

## 5. Prompty i szablony

### 5.1 Zmienne w promptach

Prompty używają placeholder'ów, które system wypełnia:

| Zmienna | Źródło | Przykład |
|---------|--------|----------|
| `{{TEMAT_ARTYKULU}}` | config.yaml: title | "Bezpieczeństwo i RODO..." |
| `{{URL_ARTYKULU}}` | computed z folderu | "/artykuly/ecommerce/operacje/..." |
| `{{KONTEKST_TEMATU}}` | config.yaml: target_audience + tone | "Artykuł dla właścicieli sklepów..." |
| `{{KONSPEKT_TRESC}}` | outline.md | Treść konspektu |
| `{{WYTYCZNE_WSPOLNE}}` | prompt_artykul_common.md | Wspólne wytyczne stylu |
| `{{TYTUL_ARTYKULU}}` | config.yaml: title | "Bezpieczeństwo i RODO..." |
| `{{OSTATNIA_SEKCJA}}` | sections/XX.md | Treść poprzedniej sekcji |

### 5.2 Lista promptów

| Plik | Kiedy używany | Zmienne |
|------|---------------|---------|
| `prompt_konspekt_artykulu.md` | Krok 1: Konspekt | TEMAT_ARTYKULU, URL_ARTYKULU, KONTEKST_TEMATU |
| `prompt_artykul_common.md` | Kroki 2-3: Wytyczne | (wklejane jako WYTYCZNE_WSPOLNE) |
| `prompt_artykul_start.md` | Krok 2: Pierwsza sekcja | KONSPEKT_TRESC, WYTYCZNE_WSPOLNE, TYTUL_ARTYKULU |
| `prompt_artykul_kontynuacja.md` | Krok 3: Kolejne sekcje | KONSPEKT_TRESC, OSTATNIA_SEKCJA, WYTYCZNE_WSPOLNE, TYTUL_ARTYKULU |
| `prompt_sprawdz_naglowki.md` | Krok 5: SEO review | (treść draft) |
| `prompt_sprawdz_styl.md` | Krok 6: Humanizacja | (treść draft) |

### 5.3 Wytyczne wspólne (prompt_artykul_common.md)

Każda sekcja musi spełniać:
- **Długość:** 300-400 słów
- **Czytelność:** 40-60 (Flesch Reading Ease)
- **Styl:** ekspercki, ale naturalny i rozmowny
- **Struktura:** krótkie akapity, zróżnicowana długość zdań
- **Ton:** profesjonalnie ludzki (nie akademicki, nie AI-like)
- **Treść:** konkretne przykłady, brak ogólników

---

## 6. Review i kontrola jakości

### 6.1 Review automatyczny (AI)

**Kiedy:** Po napisaniu każdej sekcji (kroki 2-3)

**Kryteria:**
1. **Długość** - czy 300-400 słów?
2. **Struktura** - czy krótkie akapity (3-5 zdań)?
3. **Styl** - czy naturalne przejścia, brak powtórzeń na początku akapitów?
4. **Merytoryka** - czy omówione wszystkie punkty z konspektu?
5. **Czytelność** - czy Flesch 40-60?
6. **Ton** - czy ekspercki ale przystępny?

**Akcja:**
- Jeśli **wszystkie spełnione** → Akceptacja sekcji
- Jeśli **nie spełnia** → Auto-fix (max 2 próby)
- Po 2 nieudanych próbach → Akceptacja z warningiem

### 6.2 SEO Review (Krok 5)

**Prompt:** prompt_sprawdz_naglowki.md

**Sprawdza:**
- Hierarchia H1 → H2 → H3 → H4 (bez przeskoków)
- H1 tylko jeden (title)
- H2-H4 zawierają naturalne słowa kluczowe
- Nagłówki są czytelne i spójne
- Brak nagłówków typu "Wprowadzenie", "Podsumowanie" (nudne)

**Akcja:**
- Auto-fix nagłówków jeśli problemów

### 6.3 Humanizacja (Krok 6)

**Prompt:** prompt_sprawdz_styl.md

**Cel:**
- Zmienność długości i rytmu zdań
- Subtelne wahania intelektualne (*może sugerować, wydaje się, prawdopodobnie*)
- Naturalność języka (brak sztucznego tonu AI)
- Unikanie powtórzeń w rozpoczęciach zdań
- Realistyczne przykłady

**Output:**
- Przepisany artykuł w naturalnym stylu
- Zachowanie struktury Markdown (##, ###, listy, pogrubienia)

---

## 7. Kategorie

### 7.1 Źródło kategorii

**Plik:** `kategoria-artykulow.xlsx`
**Format:** Excel z kolumnami:
- Tytuł (nazwa kategorii)
- Slug (URL-friendly)
- Element nadrzędny (hierarchia)
- Liczba artykułów
- Pełna ścieżka URL

**Liczba kategorii:** 147 (hierarchicznych)

**Przykłady:**
```
E-commerce
├── Sklepy Internetowe
├── Płatności Online
└── Logistyka E-commerce

Strategia IT
├── Decyzje strategiczne IT
├── Koszty i budżetowanie IT
└── Utrzymanie i rozwój systemów

Strony Internetowe
├── Content Management Systems (CMS)
│   └── E-commerce
│       └── Sklepy Internetowe
├── Projektowanie UX/UI
└── Hosting i Infrastruktura
```

### 7.2 Proces przypisywania kategorii

**Kiedy:** Krok 8 (po publikacji artykułu)

**Input:**
- Gotowy artykuł (article.md)
- Lista kategorii z Excel (147 kategorii)

**Proces:**
1. AI analizuje treść artykułu
2. Wybiera 1-5 najbardziej pasujących kategorii z Excel
3. Jeśli brak odpowiednich → sugeruje nowe kategorie
4. Zapisuje do `categories.yaml`

**Format output (categories.yaml):**
```yaml
categories:
  - slug: "e-commerce"
    name: "E-commerce"
    confidence: 95

  - slug: "strategia-it"
    name: "Strategia IT"
    confidence: 85

  - slug: "bezpieczenstwo-it"
    name: "Bezpieczeństwo IT"
    confidence: 90

suggested_new_categories:
  - name: "RODO dla E-commerce"
    slug: "rodo-dla-ecommerce"
    parent: "e-commerce"
    reason: "Artykuł szczegółowo omawia RODO w kontekście e-commerce, brak dedykowanej kategorii"
```

### 7.3 Relacja URL ↔ Kategorie

**WAŻNE:** Struktura folderów i kategorie są NIEZALEŻNE.

**Przykład:**

| Artykuł | URL | Kategorie |
|---------|-----|-----------|
| Bezpieczeństwo w e-commerce | `/artykuly/ecommerce/operacje/bezpieczenstwo-i-rodo/` | E-commerce, Strategia IT, RODO, Bezpieczeństwo IT |
| Wybór platformy | `/artykuly/ecommerce/platformy/porownanie-platform/` | E-commerce, Content Management Systems, Decyzje strategiczne IT |

**Użycie kategorii:**
- Filtrowanie na stronie (np. filtr "Strategia IT" pokazuje wszystkie artykuły z tą kategorią)
- SEO (breadcrumbs, internal linking)
- Rekomendacje (pokrewne artykuły)

---

## 8. CLI Interface

### 8.1 Komendy

```bash
# 1. Inicjalizacja nowego artykułu (tworzy folder + config template)
python blog_agent.py init \
  --series ecommerce \
  --silo operacje \
  --slug bezpieczenstwo-i-rodo

# Output:
# Created: artykuly/ecommerce/operacje/bezpieczenstwo-i-rodo/
# Created: artykuly/ecommerce/operacje/bezpieczenstwo-i-rodo/config.yaml
# → Edytuj config.yaml i uruchom 'create'

# 2. Generowanie artykułu
python blog_agent.py create \
  --config artykuly/ecommerce/operacje/bezpieczenstwo-i-rodo/config.yaml

# Output (live progress):
# [1/8] Creating outline... ✓ (25s)
# [2/8] Writing intro + section 1... ✓ (35s)
# [3/8] Writing section 2... ✓ (30s)
# [4/8] Writing section 3... ✓ (30s)
# [5/8] Creating draft... ✓ (5s)
# [6/8] SEO review... ✓ (20s)
# [7/8] Humanization... ✓ (40s)
# [8/8] Assigning categories... ✓ (20s)
#
# ✅ Article published: article.md
# 📊 Stats: 3,245 words, 5 sections, 4 categories
# 🏷️  Categories: E-commerce, Strategia IT, RODO, Bezpieczeństwo IT
# ⏱️  Total time: 3m 45s

# 3. Lista artykułów
python blog_agent.py list [--series ecommerce] [--status draft|published]

# Output:
# Found 12 articles:
#
# ecommerce/operacje/bezpieczenstwo-i-rodo    [published]  2025-11-06
# ecommerce/platformy/wybor-platformy         [draft]      2025-11-05
# ...

# 4. Status artykułu
python blog_agent.py status \
  --path artykuly/ecommerce/operacje/bezpieczenstwo-i-rodo

# Output:
# Article: Bezpieczeństwo i RODO w e-commerce
# Status: Published
# URL: /artykuly/ecommerce/operacje/bezpieczenstwo-i-rodo/
# Created: 2025-11-06 10:30
# Modified: 2025-11-06 14:45
#
# Files:
# ✓ config.yaml
# ✓ outline.md
# ✓ sections/ (5 files)
# ✓ draft.md
# ✓ article.md (3,245 words)
# ✓ categories.yaml
#
# Categories: E-commerce, Strategia IT, RODO, Bezpieczeństwo IT
# Git commits: 4

# 5. Weryfikacja promptów
python blog_agent.py check-prompts

# Output:
# Checking prompts...
# ✓ prompts/konspekt/prompt_konspekt_artykulu.md
# ✓ prompts/articles/prompt_artykul_common.md
# ✓ prompts/articles/prompt_artykul_start.md
# ✓ prompts/articles/prompt_artykul_kontynuacja.md
# ✓ prompts/audyt/prompt_sprawdz_naglowki.md
# ✓ prompts/audyt/prompt_sprawdz_styl.md
#
# All prompts found!
```

### 8.2 Parametry globalne

```bash
--verbose, -v          # Verbose output (show AI prompts/responses)
--dry-run             # Dry run (don't write files, don't commit)
--no-git              # Skip git commits
--provider            # AI provider: anthropic (default), openai (future)
--model               # Model: claude-sonnet-4 (default), claude-opus-4
```

---

## 9. Git Integration

### 9.1 Automatyczne commity

**Kiedy:**
1. Po utworzeniu outline (Krok 1)
2. Po zakończeniu draft (Krok 4)
3. Po publikacji (Krok 7)
4. Po przypisaniu kategorii (Krok 8)

**Format commit message:**
```
[series/silo/slug] Action

Body (optional)
```

**Przykłady:**
```bash
# Commit 1
[ecommerce/operacje/bezpieczenstwo-i-rodo] Create outline

Generated outline with 5 sections:
- Wprowadzenie do bezpieczeństwa e-commerce
- Wymagania RODO dla sklepów
- Implementacja certyfikatów SSL
- Polityka prywatności i cookies
- Audyt bezpieczeństwa

# Commit 2
[ecommerce/operacje/bezpieczenstwo-i-rodo] Complete draft

Article draft completed:
- 5 sections written
- 3,245 words total
- Ready for SEO review and humanization

# Commit 3
[ecommerce/operacje/bezpieczenstwo-i-rodo] Publish article

Published article:
- SEO optimized headers
- Humanized content (Flesch: 52)
- Meta title and description added

# Commit 4
[ecommerce/operacje/bezpieczenstwo-i-rodo] Assign categories

Assigned categories:
- E-commerce (95%)
- Strategia IT (85%)
- RODO (90%)
- Bezpieczeństwo IT (88%)
```

### 9.2 Polityka commitów

- **Auto-commit:** Włączone domyślnie
- **Branch:** Commituje na obecnym branchu
- **Staged files:** Tylko pliki artykułu (folder artykułu)
- **Disable:** `--no-git` flag

### 9.3 Historia wersji

Każdy artykuł ma pełną historię w git:
```bash
git log --oneline -- artykuly/ecommerce/operacje/bezpieczenstwo-i-rodo/

a1b2c3d [ecommerce/operacje/bezpieczenstwo-i-rodo] Assign categories
d4e5f6g [ecommerce/operacje/bezpieczenstwo-i-rodo] Publish article
h7i8j9k [ecommerce/operacje/bezpieczenstwo-i-rodo] Complete draft
l0m1n2o [ecommerce/operacje/bezpieczenstwo-i-rodo] Create outline
```

---

## 10. AI Provider

### 10.1 Anthropic (Claude) - Domyślny

**Model:** `claude-sonnet-4-20250514`
**API Key:** `ANTHROPIC_API_KEY` env variable

**Dlaczego:**
- Doskonała jakość tekstu (naturalny język)
- Dobry stosunek cena/jakość
- Długi context window (200K tokens)
- Szybkie odpowiedzi

**Konfiguracja:**
```python
client = anthropic.Anthropic(api_key=os.environ["ANTHROPIC_API_KEY"])
model = "claude-sonnet-4-20250514"
max_tokens = 4000  # per request
```

### 10.2 OpenAI - Przyszłość

**Model:** `gpt-4o` (planowane)
**API Key:** `OPENAI_API_KEY` env variable

**Architektura:**
```python
# Provider-agnostic interface
class AIProvider:
    def generate(self, prompt: str, max_tokens: int) -> str:
        pass

class ClaudeProvider(AIProvider):
    # Implementacja dla Claude
    pass

class OpenAIProvider(AIProvider):
    # Implementacja dla OpenAI (future)
    pass
```

### 10.3 Koszty szacunkowe

**Dla artykułu ~3000 słów (5 sekcji):**

| Krok | Tokens in | Tokens out | Koszt (Claude Sonnet) |
|------|-----------|------------|----------------------|
| Konspekt | ~1,000 | ~1,500 | $0.004 |
| Sekcje (x5) | ~2,000 | ~2,500 | $0.018 |
| SEO Review | ~4,000 | ~4,000 | $0.024 |
| Humanizacja | ~4,000 | ~4,000 | $0.024 |
| Kategorie | ~4,000 | ~500 | $0.014 |
| **RAZEM** | | | **~$0.08** |

*Ceny Claude Sonnet 4: $3/MTok input, $15/MTok output (styczeń 2025)*

---

## 11. Obsługa błędów

### 11.1 Walidacja config.yaml

Przed rozpoczęciem sprawdź:
- ✓ Wszystkie wymagane pola (title, target_audience, tone)
- ✓ Folder istnieje
- ✓ Brak konfliktu (article.md już istnieje)
- ✓ API key ustawiony

**Błąd:**
```
❌ ERROR: Missing required field 'title' in config.yaml
→ Edit config.yaml and try again
```

### 11.2 API Errors

**Rate limit:**
```
⚠️  WARNING: API rate limit reached
→ Waiting 60s before retry...
→ Retry 1/3...
```

**Invalid response:**
```
❌ ERROR: AI returned invalid response (step: writing section 2)
→ Retrying with adjusted prompt...
→ Retry 1/2...
```

### 11.3 Rollback

Jeśli proces się przewraca w połowie:

```bash
# Automatyczny rollback ostatniego commitu
❌ ERROR: Humanization failed after 2 retries
→ Rolling back git commit...
→ Draft preserved in draft.md
→ Fix the issue and run again with --resume
```

### 11.4 Resume

```bash
# Wznowienie od ostatniego checkpointu
python blog_agent.py create \
  --config artykuly/.../config.yaml \
  --resume

# Output:
# Found checkpoint: draft.md
# Resuming from step 6 (SEO review)...
```

---

## 12. Przyszłe rozszerzenia (roadmap)

### 12.1 Faza 1 (teraz)
- ✅ Konspekt → Pisanie → Review → Publikacja
- ✅ Kategorie z Excel
- ✅ Git commits
- ✅ CLI interface
- ✅ Claude (Sonnet 4)

### 12.2 Faza 2 (Q1 2025)
- 🔲 OpenAI support
- 🔲 Generowanie obrazów (DALL-E / Midjourney)
- 🔲 A/B testing tytułów
- 🔲 Internal linking suggestions
- 🔲 WordPress API integration (auto-publish)

### 12.3 Faza 3 (Q2 2025)
- 🔲 Multi-language (polski → angielski)
- 🔲 Batch processing (wiele artykułów naraz)
- 🔲 Analytics integration (GSC, GA4)
- 🔲 Plagiarism check
- 🔲 Readability scoring

---

## 13. Przykładowy przebieg (end-to-end)

### 13.1 User actions

```bash
# 1. Inicjalizacja
$ python blog_agent.py init \
    --series ecommerce \
    --silo operacje \
    --slug bezpieczenstwo-i-rodo

Created: artykuly/ecommerce/operacje/bezpieczenstwo-i-rodo/config.yaml
→ Edit config and run 'create'

# 2. Edycja config.yaml
$ nano artykuly/ecommerce/operacje/bezpieczenstwo-i-rodo/config.yaml

# Wypełnia:
# title: "Bezpieczeństwo i RODO w e-commerce..."
# target_audience: "Właściciele sklepów..."
# tone: "ekspercki, ale naturalny..."

# 3. Generowanie
$ python blog_agent.py create \
    --config artykuly/ecommerce/operacje/bezpieczenstwo-i-rodo/config.yaml

[1/8] Creating outline...
      → Generated 5 sections
      → Meta title: "Bezpieczeństwo e-commerce: praktyczny przewodnik..."
      → Git commit: [ecommerce/operacje/bezpieczenstwo-i-rodo] Create outline
      ✓ (28s)

[2/8] Writing intro + section 1...
      → Section: "Wprowadzenie do bezpieczeństwa e-commerce"
      → 385 words, Flesch: 54
      → Review: PASSED
      ✓ (42s)

[3/8] Writing section 2...
      → Section: "Wymagania RODO dla sklepów online"
      → 412 words, Flesch: 48
      → Review: PASSED
      ✓ (38s)

[4/8] Writing section 3...
      → Section: "Implementacja certyfikatów SSL/TLS"
      → 368 words, Flesch: 51
      → Review: PASSED
      ✓ (35s)

[5/8] Writing section 4...
      → Section: "Polityka prywatności i zarządzanie cookies"
      → 395 words, Flesch: 52
      → Review: PASSED
      ✓ (37s)

[6/8] Writing section 5...
      → Section: "Audyt bezpieczeństwa - praktyczne kroki"
      → 401 words, Flesch: 49
      → Review: PASSED
      ✓ (39s)

[7/8] Creating draft...
      → Combined 5 sections
      → Total: 3,245 words
      → Git commit: [ecommerce/operacje/bezpieczenstwo-i-rodo] Complete draft
      ✓ (3s)

[8/8] SEO review...
      → Checked H1-H4 hierarchy: OK
      → Fixed 2 headers (added keywords)
      ✓ (24s)

[9/9] Humanization...
      → Rewrote for natural tone
      → Final Flesch: 52
      → Git commit: [ecommerce/operacje/bezpieczenstwo-i-rodo] Publish article
      ✓ (43s)

[10/10] Assigning categories...
      → Found 4 matching categories
      → E-commerce (95%), Strategia IT (85%), RODO (90%), Bezpieczeństwo IT (88%)
      → Git commit: [ecommerce/operacje/bezpieczenstwo-i-rodo] Assign categories
      ✓ (22s)

✅ Article published successfully!

📄 File: artykuly/ecommerce/operacje/bezpieczenstwo-i-rodo/article.md
📊 Stats: 3,245 words | 5 sections | 4 categories
🏷️  Categories: E-commerce, Strategia IT, RODO, Bezpieczeństwo IT
⏱️  Time: 4m 51s
💰 Cost: ~$0.08

Next steps:
→ Review: artykuly/ecommerce/operacje/bezpieczenstwo-i-rodo/article.md
→ Publish: Copy to WordPress or commit to main branch
```

---

## 14. Metryki i KPI

### 14.1 Output quality metrics

Agent powinien logować:
- **Flesch Reading Ease:** 40-60 (target)
- **Długość sekcji:** 300-400 słów (target)
- **Review pass rate:** % sekcji zatwierdzonych za 1 razem
- **Kategorie confidence:** Avg confidence score

### 14.2 Performance metrics

- **Total time:** Per artykuł
- **Time per section:** Avg
- **API calls:** Total + per step
- **Cost:** Per artykuł

### 14.3 Logging

```python
# Przykładowy log
{
    "article": "ecommerce/operacje/bezpieczenstwo-i-rodo",
    "timestamp": "2025-11-06T14:30:00Z",
    "duration_seconds": 291,
    "sections": 5,
    "words": 3245,
    "flesch_score": 52,
    "categories": 4,
    "review_pass_rate": 100,
    "api_calls": 12,
    "cost_usd": 0.08,
    "git_commits": 4
}
```

---

## 15. Podsumowanie wymagań

### ✅ Must-have (Faza 1)

1. ✓ Generowanie konspektu z promptu
2. ✓ Pisanie sekcji po kolei z review
3. ✓ SEO optimization (nagłówki)
4. ✓ Humanizacja treści
5. ✓ Przypisywanie kategorii z Excel
6. ✓ Git commits w kluczowych momentach
7. ✓ CLI interface (init, create, list, status)
8. ✓ Support dla Claude Sonnet 4
9. ✓ Walidacja i error handling
10. ✓ Progress reporting

### 🔲 Nice-to-have (Faza 2+)

1. OpenAI support
2. Generowanie obrazów
3. WordPress integration
4. Multi-language
5. A/B testing
6. Analytics
7. Batch processing

---

**Koniec specyfikacji - gotowe do implementacji!**
