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
│   │   ├── prompt_artykul_kontynuacja.md
│   │   ├── prompt_streszczenie_artykulu.md
│   │   ├── prompt_linkowanie_wewnetrzne.md
│   │   ├── prompt_multimedia_suggestions.md
│   │   └── prompt_cta_next_steps.md
│   ├── audyt/
│   │   ├── prompt_sprawdz_naglowki.md
│   │   └── prompt_sprawdz_styl.md
│   └── metadata/
│       ├── prompt_business_metadata.md
│       └── prompt_schema_markup.md
│
├── categories.yaml                     # 146 kategorii hierarchicznych (git-friendly)
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

### 4.1 Workflow (20 kroków)

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
│  KROK 2: STRESZCZENIE - "Co znajdziesz w artykule?"        │
│  • Prompt: prompt_streszczenie_artykulu.md                  │
│  • Input: outline, title, target_audience                   │
│  • Output: sections/00-summary.md (3-5 punktów)            │
│  • Konkretne wnioski i wartość (NIE spis treści!)          │
│  • Umiejscowienie: PO tytule, PRZED wprowadzeniem          │
└─────────────────┬───────────────────────────────────────────┘
                  │
                  ▼
┌─────────────────────────────────────────────────────────────┐
│  KROK 3: INTERNAL LINKING - Wybór powiązanych artykułów    │
│  • Prompt: prompt_linkowanie_wewnetrzne.md                  │
│  • Input: outline, article_path, seria, silos              │
│  • Skanuje: folder artykuly/[seria]/* dla dostępnych art.  │
│  • AI wybiera: 5-8 najbardziej powiązanych artykułów       │
│  • Podział: 2-4 contextual (w treści), 3-5 end section     │
│  • Output: related_articles.json (lista + anchor text)     │
│  • Strategia: 60% z tego silosu, 40% cross-silo            │
└─────────────────┬───────────────────────────────────────────┘
                  │
                  ▼
┌─────────────────────────────────────────────────────────────┐
│  KROK 4: PISANIE - Wprowadzenie + Sekcja 1                 │
│  • Prompt: prompt_artykul_start.md + prompt_artykul_common │
│  • Input: outline, wytyczne wspólne, related_articles.json │
│  • Output: sections/01-intro.md (300-400 słów)             │
│  • AI wstawia 0-1 contextual link (gdzie naturalnie pasuje)│
│  • Review AI: długość, styl, czytelność                     │
│  • Auto-fix jeśli nie spełnia kryteriów                     │
└─────────────────┬───────────────────────────────────────────┘
                  │
                  ▼
┌─────────────────────────────────────────────────────────────┐
│  KROK 5: PISANIE - Sekcje 2, 3, 4...N + Opcjonalne         │
│  • Prompt: prompt_artykul_kontynuacja.md + common          │
│  • Input: outline, poprzednia sekcja, related_articles.json│
│  • Output: sections/02-xxx.md, 03-xxx.md...                │
│  • AI wstawia contextual links (2-4 total w całym art.)    │
│  • Review AI po każdej sekcji                               │
│  • Loop: dla każdej sekcji z outline                        │
│  • Opcjonalnie: Checklist (jeśli w outline)                │
│  • Opcjonalnie: FAQ (do 10 pytań, jeśli w outline)         │
└─────────────────┬───────────────────────────────────────────┘
                  │
                  ▼
┌─────────────────────────────────────────────────────────────┐
│  KROK 6: DRAFT + SEKCJA "Powiązane artykuły"               │
│  • Połączenie: streszczenie + sekcje → draft.md            │
│  • Dodaj sekcję końcową: pozostałe linki (3-5) z           │
│    related_articles.json (te które nie użyte w treści)     │
│  • Format: grupowanie po silosach                           │
│  • Git commit: "[series/silo/slug] Complete draft"         │
└─────────────────┬───────────────────────────────────────────┘
                  │
                  ▼
┌─────────────────────────────────────────────────────────────┐
│  KROK 7: SEO REVIEW - Nagłówki                             │
│  • Prompt: prompt_sprawdz_naglowki.md                       │
│  • Input: draft.md                                          │
│  • Check: struktura H1-H4, słowa kluczowe, hierarchia      │
│  • Auto-fix: poprawia nagłówki jeśli potrzeba              │
└─────────────────┬───────────────────────────────────────────┘
                  │
                  ▼
┌─────────────────────────────────────────────────────────────┐
│  KROK 8: HUMANIZACJA                                        │
│  • Prompt: prompt_sprawdz_styl.md                           │
│  • Input: draft.md (po SEO review)                          │
│  • Output: article.md (finalna wersja)                      │
│  • Cél: naturalny język, brak AI tone, Flesch 40-60        │
└─────────────────┬───────────────────────────────────────────┘
                  │
                  ▼
┌─────────────────────────────────────────────────────────────┐
│  KROK 9: MULTIMEDIA SUGGESTIONS                             │
│  • Prompt: prompt_multimedia_suggestions.md                 │
│  • Input: article.md (po humanizacji), konspekt             │
│  • AI analizuje treść i sugeruje multimedia                 │
│  • Output: multimedia.json (4-9 sugestii)                   │
│  • Sugestie:                                                 │
│    - 1 hero image (zawsze)                                  │
│    - 3-8 w sekcjach (zdjęcia, wykresy, infografiki, screens)│
│  • Dla każdego: opis + image prompt (DALL-E/MJ) + alt text │
│  • User może: wygenerować/pobrać/zlecić/pominąć            │
└─────────────────┬───────────────────────────────────────────┘
                  │
                  ▼
┌─────────────────────────────────────────────────────────────┐
│  KROK 10: BUSINESS METADATA                                 │
│  • Prompt: prompt_business_metadata.md                      │
│  • Input: article.md (po humanizacji), konspekt             │
│  • AI generuje metadane biznesowe dla przedsiębiorców:      │
│    - target_business (startup/scale-up/enterprise)          │
│    - investment (level + range + breakdown)                 │
│    - timeline (estimate + phases)                           │
│    - complexity (technical + organizational)                │
│    - team_requirements (size + roles)                       │
│    - ROI (jeśli applicable)                                 │
│  • Output: business_metadata.yaml                           │
│  • Użycie: filtrowanie, SEO, rekomendacje                   │
└─────────────────┬───────────────────────────────────────────┘
                  │
                  ▼
┌─────────────────────────────────────────────────────────────┐
│  KROK 11: CTA / NEXT STEPS - "Co dalej?"                   │
│  • Prompt: prompt_cta_next_steps.md                         │
│  • Input: article.md, business_metadata, related_articles   │
│  • AI generuje sekcję końcową z konkretnymi akcjami:       │
│    - Pierwsze kroki (dla gotowych do działania)            │
│    - Self-assessment (pytania do oceny gotowości)          │
│    - Narzędzia i resources                                  │
│    - CTA (konsultacje, narzędzia, resources)               │
│  • Dopasowana do typu artykułu (practical/theoretical/opt.) │
│  • Output: sekcja "Co dalej?" w article.md                 │
└─────────────────┬───────────────────────────────────────────┘
                  │
                  ▼
┌─────────────────────────────────────────────────────────────┐
│  KROK 12: PUBLIKACJA                                        │
│  • Finalna wersja zapisana jako article.md                  │
│  • Multimedia suggestions w multimedia.json                 │
│  • Business metadata w business_metadata.yaml               │
│  • Git commit: "[series/silo/slug] Publish article"        │
└─────────────────┬───────────────────────────────────────────┘
                  │
                  ▼
┌─────────────────────────────────────────────────────────────┐
│  KROK 13: SCHEMA.ORG MARKUP                                 │
│  • Prompt: prompt_schema_markup.md                          │
│  • Input: article.md, metadata, FAQ, Checklist, images      │
│  • AI generuje structured data (JSON-LD):                   │
│    - Article schema (zawsze)                                │
│    - FAQPage schema (jeśli artykuł ma FAQ)                 │
│    - HowTo schema (jeśli artykuł ma Checklist)             │
│    - BreadcrumbList schema (zawsze)                         │
│  • Output: schema.json → wklejenie w <head>                │
│  • Użycie: rich snippets w Google, lepsze SEO, wyższe CTR │
└─────────────────┬───────────────────────────────────────────┘
                  │
                  ▼
┌─────────────────────────────────────────────────────────────┐
│  KROK 14: INTERNAL LINKING                                  │
│  • AI analizuje artykuł i znajduje powiązane artykuły       │
│  • Automatycznie dodaje 3-5 linków wewnętrznych             │
│  • Linki do artykułów w tym samym silosie (AI-driven)       │
│  • Output: zaktualizowany article.md z linkami              │
└─────────────────┬───────────────────────────────────────────┘
                  │
                  ▼
┌─────────────────────────────────────────────────────────────┐
│  KROK 15: GENERATE IMAGES (opcjonalne)                      │
│  • Generuje obrazy z DALL-E 3 lub Stability AI              │
│  • Hero image (automatycznie) + sugestie stock photos       │
│  • Output: images/hero.png + multimedia.json (updated)      │
│  • Domyślnie wyłączone (kosztuje $0.01-0.12 per artykuł)   │
└─────────────────┬───────────────────────────────────────────┘
                  │
                  ▼
┌─────────────────────────────────────────────────────────────┐
│  KROK 16: SOCIAL MEDIA                                      │
│  • Generuje posty na Facebook/LinkedIn/Instagram            │
│  • Hook-based post (80±5 znaków)                           │
│  • 4 alternatywne tytuły z mocnymi hookami                  │
│  • Pierwszy komentarz z bulletami i 10 hashtagami           │
│  • Output: social_media.md (Markdown format)                │
└─────────────────┬───────────────────────────────────────────┘
                  │
                  ▼
┌─────────────────────────────────────────────────────────────┐
│  KROK 17: FAQ (jeśli w outline)                            │
│  • Generuje FAQ z 5-8 pytaniami                             │
│  • Semantic internal linking do powiązanych artykułów       │
│  • Output: faq.md + faq_outline.md                          │
│  • Odpowiedzi 50-70 słów każda                              │
└─────────────────┬───────────────────────────────────────────┘
                  │
                  ▼
┌─────────────────────────────────────────────────────────────┐
│  KROK 18: CHECKLIST (jeśli w outline)                      │
│  • Generuje actionable checklist z 8-12 itemami             │
│  • Humanizacja treści checklist                             │
│  • Output: checklist.md + checklist_outline.md              │
└─────────────────┬───────────────────────────────────────────┘
                  │
                  ▼
┌─────────────────────────────────────────────────────────────┐
│  KROK 19: HEADERS ALTERNATIVES (opcjonalne)                 │
│  • Generuje 3-4 alternatywy SEO dla H1/H2/H3                │
│  • Long-tail warianty dla każdego nagłówka                  │
│  • Output: headers_alternatives.md                          │
│  • Domyślnie włączone                                       │
│  • Git commit: "[series/silo/slug] Add SEO alternatives"   │
└─────────────────┬───────────────────────────────────────────┘
                  │
                  ▼
┌─────────────────────────────────────────────────────────────┐
│  KROK 20: META ALTERNATIVES                                 │
│  • Generuje 2-3 propozycje meta title i meta description    │
│  • Meta title różny od H1 (50-60 znaków)                    │
│  • Meta description (140-160 znaków)                        │
│  • Używa taniego modelu (openai-gpt4o-mini)                 │
│  • Output: meta_alternatives.md                             │
│  • Przydatne do A/B testingu i optymalizacji CTR            │
└─────────────────────────────────────────────────────────────┘
```

**Uwaga:** Krok 13 (Categories) został przeniesiony wcześniej w workflow i nie jest już ostatnim krokiem.

### 4.2 Timing (szacunkowy)

| Krok | Czas | % |
|------|------|---|
| Init | ~5s | 1% |
| Konspekt | ~30s | 6% |
| Streszczenie "Co znajdziesz" | ~15s | 3% |
| Pisanie sekcji (x5) | ~2m | 25% |
| Review sekcji (x5) | ~1m | 13% |
| Create draft | ~5s | 1% |
| SEO Review | ~20s | 4% |
| Humanizacja | ~40s | 9% |
| Multimedia suggestions | ~20s | 4% |
| Business metadata | ~25s | 5% |
| CTA/Next Steps | ~20s | 4% |
| Publish | ~5s | 1% |
| Schema.org markup | ~15s | 3% |
| Kategorie | ~20s | 4% |
| Internal linking | ~25s | 5% |
| Generate images (jeśli włączone) | ~30s | 6% |
| Social media | ~30s | 6% |
| FAQ (jeśli w outline) | ~45s | 9% |
| Checklist (jeśli w outline) | ~20s | 4% |
| Headers alternatives (jeśli włączone) | ~25s | 5% |
| Meta alternatives | ~15s | 3% |
| Git commits | ~20s | 4% |
| **RAZEM** | **~7-8min** | **100%** |

**Uwaga:** Czas zależy od włączonych opcjonalnych kroków (images, FAQ, checklist, headers alternatives, meta alternatives)

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
1. **"Co znajdziesz w artykule?"** (zawsze, Krok 2)
2. Wprowadzenie
3. Sekcje główne (z konspektu)
4. **Checklist** (jeśli jest)
5. **FAQ** (jeśli jest)
6. Podsumowanie (opcjonalne)

**Nie ma:**
- Nagłówków typu "Podsumowanie" lub "Wnioski" (nudne, sztuczne)
- Wezwań do działania (CTA) - to blog, nie landing page
- Autopromoacji

### 4.4 Sekcja "Co znajdziesz w artykule?" (obowiązkowa)

**Cel:** Krótkie streszczenie najważniejszych wniosków/wartości z artykułu, które pomaga czytelnikowi szybko zdecydować, czy warto czytać dalej.

**Charakterystyka:**
- **ZAWSZE generowana** (w przeciwieństwie do Checklist/FAQ które są opcjonalne)
- Generowana w **Kroku 2** (po konspekcie, przed pisaniem sekcji)
- Umiejscowiona **na początku** artykułu (po tytule H1, przed wprowadzeniem)
- **3-5 punktów** (nie mniej, nie więcej)
- **Konkretne wnioski** i praktyczne wartości (NIE spis treści!)

**Format:**
```markdown
## Co znajdziesz w artykule?

- **Pogrubiona fraza kluczowa** - Rozwinięcie konkretnej wartości (1 zdanie)
- **Kolejna fraza** - Następny konkretny wniosek lub wskazówka
- **Trzecia fraza** - Kolejna wartość
```

**Zasady:**
1. ❌ **NIE jest spisem treści** - nie wymieniaj tytułów sekcji
2. ✅ **Jest streszczeniem wartości** - konkretne wnioski, liczby, rozwiązania
3. ❌ **Unikaj fraz** typu "Dowiesz się...", "Poznasz...", "Artykuł omawia..."
4. ✅ **Używaj konkretów** - nazwy narzędzi, liczby, fakty, rozwiązania
5. ✅ **Pogrubiona fraza na początku** - 2-4 słowa kluczowe
6. ✅ **1 zdanie na punkt** (maksymalnie 2 zdania jeśli konieczne)

**Przykład DOBRY:**
```markdown
## Co znajdziesz w artykule?

- **Certyfikat SSL to podstawa** - bez niego Google obniża ranking, a klienci widzą ostrzeżenia
- **RODO wymaga 5 konkretnych działań** - polityka prywatności, zgody, szyfrowanie, backup i prawo do usunięcia
- **Kary do 4% przychodu** - UOKiK nie żartuje, brak zabezpieczeń to najczęstszy powód kontroli
- **Gotowa checklist 15 punktów** - audyt bezpieczeństwa możesz przeprowadzić samodzielnie w 30 minut
```

**Przykład ZŁY (spis treści):**
```markdown
## Co znajdziesz w artykule?

- Wprowadzenie do bezpieczeństwa e-commerce
- Wymagania RODO dla sklepów online
- Implementacja certyfikatów SSL
- Polityka prywatności i cookies
```

**Prompt:** `prompts/articles/prompt_streszczenie_artykulu.md`

**Input:** outline, title, target_audience

**Output:** `sections/00-summary.md`

### 4.5 Multimedia Suggestions (automatyczne przed publikacją)

**Cel:** Sugestie obrazów, grafik, wykresów i screenshotów które wzbogacą artykuł wizualnie i poprawią UX oraz SEO.

**Charakterystyka:**
- **ZAWSZE generowane** (automatycznie przed publikacją)
- Generowane w **Kroku 9** (po humanizacji, przed publikacją)
- **4-9 sugestii** (1 hero + 3-8 w sekcjach)
- **Dla każdego:** opis + image prompt (DALL-E/Midjourney) + alt text + placement

**Typy multimediów:**
1. **📷 Zdjęcia** - hero image (zawsze), zdjęcia kontekstowe
2. **📊 Wykresy/diagramy** - dane, procesy, porównania, trendy
3. **🎨 Grafiki/ilustracje** - infografiki, schematy, ikony
4. **📸 Screenshoty** - interfejsy, dashboardy, konfiguracje

**Format sugestii:**
```json
{
  "id": 1,
  "type": "photo",
  "subtype": "hero",
  "priority": "high",
  "section": "Top of article",
  "title": "Hero image - Bezpieczeństwo e-commerce",
  "description": "Profesjonalne zdjęcie właściciela sklepu przy dashboardzie",
  "alt_text": "Właściciel sklepu e-commerce analizuje dashboard bezpieczeństwa RODO",
  "placement": "after_title",
  "image_prompt": "Professional photo of an e-commerce business owner working on laptop showing security dashboard, modern office environment, natural lighting, authentic workspace, stock photo style",
  "dimensions": "1920x1080 (16:9)",
  "keywords": ["e-commerce", "bezpieczeństwo", "RODO"],
  "reason": "Hero image wprowadza w tematykę i buduje profesjonalny wizerunek",
  "alternatives": [
    "Stock photo: Unsplash query 'e-commerce security'",
    "Custom: Zlecić designerowi"
  ]
}
```

**Image prompts (dla DALL-E/Midjourney):**
- Język: angielski
- Długość: 30-60 słów
- Zawartość: główny obiekt, styl wizualny, kolory, format, jakość
- Przykład: *"Modern e-commerce dashboard showing security metrics and RODO compliance indicators, clean UI design, blue and white color scheme, professional software interface, detailed but readable, high quality screenshot style"*

**Alt text (SEO i accessibility):**
- Długość: 100-125 znaków (optimum dla SEO)
- Język: polski
- Keywords: 1-2 naturalne wplecione
- Bez: "obraz przedstawia", "zdjęcie pokazuje"
- Przykład: *"Dashboard analytics e-commerce z metrykami bezpieczeństwa RODO i wskaźnikami compliance"*

**Zasady:**
1. ✅ Hero image ZAWSZE (każdy artykuł)
2. ✅ 4-9 sugestii total (nie mniej, nie więcej)
3. ✅ Image prompts konkretne (30-60 słów)
4. ✅ Alt text SEO-friendly (100-125 znaków)
5. ✅ Placement logiczny (min 2 akapity między)
6. ✅ Alternatives (stock photos, tools, custom design)
7. ❌ NIE więcej niż 9 multimediów (przesada)
8. ❌ NIE umieszczaj zbyt blisko siebie

**Rozkład typowy (artykuł 5-sekcyjny):**
- 1 hero image
- 2-3 wykresy/diagramy (dla danych)
- 1-2 infografiki (dla list/procesów)
- 1-2 screenshoty (dla sekcji praktycznych)
- 0-1 zdjęć kontekstowych

**User może:**
- Wygenerować obrazy (DALL-E, Midjourney z podanego promptu)
- Pobrać z stock (Unsplash, Pexels - queries podane)
- Zlecić designerowi (opis i prompt jako brief)
- Pominąć (opublikować artykuł bez obrazów)

**Prompt:** `prompts/articles/prompt_multimedia_suggestions.md`

**Input:** article.md (po humanizacji), konspekt

**Output:** `multimedia.json`

**Przykład usage:**
```bash
# User po otrzymaniu multimedia.json może:

# 1. Wygenerować przez DALL-E
curl -X POST "https://api.openai.com/v1/images/generations" \
  -d '{"prompt": "[image_prompt z JSON]", "size": "1792x1024"}'

# 2. Pobrać z Unsplash
# Query: "e-commerce security" (z alternatives)

# 3. Zlecić designerowi
# Brief: description + image_prompt

# 4. Pominąć
python blog_agent.py publish --skip-multimedia
```

### 4.6 Business Metadata (Krok 10)

**Cel:** Wygenerować metadane biznesowe które pomogą przedsiębiorcom ocenić czy artykuł jest dla nich relevantny i wspomogą w podejmowaniu decyzji inwestycyjnych.

**Dla kogo:**
Przedsiębiorcy podejmujący decyzje inwestycyjne w IT, oprogramowanie, strony internetowe, rozwój biznesu.

**Co generuje AI:**

1. **Target Business** - dla kogo artykuł (startup, scale-up, enterprise)
2. **Industry** - branża (ecommerce, saas, fintech, universal, etc.)
3. **Project Phase** - faza projektu (planowanie, wdrożenie, optymalizacja, migracja)
4. **Investment** - inwestycja:
   - Level (low, medium, high, very_high, variable, none)
   - Range ("50-150k PLN")
   - Breakdown (jeśli applicable): software, development, integration, infrastructure, consulting
5. **Timeline** - czas realizacji:
   - Estimate ("2-3 miesiące")
   - Phases (planning, design, development, testing, deployment)
6. **Complexity** - złożoność:
   - Technical (low, medium, high)
   - Organizational (low, medium, high)
7. **Team Requirements** - wymagania zespołowe:
   - Size ("3-5 osób")
   - Roles (lista ról/kompetencji)
8. **ROI** - zwrot z inwestycji (opcjonalnie):
   - Breakeven ("6-12 miesięcy")
   - Annual savings/revenue increase
   - Key factors (co wpływa na ROI)

**Użycie metadanych:**
- Filtrowanie artykułów ("pokaż artykuły dla startupów z budżetem <50k PLN")
- SEO (structured data dla business content)
- Rekomendacje ("podobne projekty o tej złożoności")
- Personalizacja (dopasowanie treści do fazy projektu użytkownika)

**Prompt:** `prompts/metadata/prompt_business_metadata.md`

**Input:** article.md (po humanizacji), konspekt, seria, silos

**Output:** `business_metadata.yaml`

**Przykład output:**
```yaml
business_metadata:
  target_business:
    - "startup"
    - "scale-up"
  industry:
    - "ecommerce"
    - "retail"
  project_phase:
    - "planowanie"
    - "wdrożenie"
  investment:
    level: "medium"
    range: "50-150k PLN"
    breakdown:
      software_licenses: "20-40k PLN"
      development: "50-80k PLN"
      integration: "30-50k PLN"
      infrastructure: "10-15k PLN"
  timeline:
    estimate: "2-3 miesiące"
    phases:
      planning: "2-3 tygodnie"
      development: "6-8 tygodni"
      testing: "2-3 tygodnie"
      deployment: "1-2 tygodnie"
  complexity:
    technical: "medium"
    organizational: "low"
  team_requirements:
    size: "3-5 osób"
    roles:
      - "Project Manager"
      - "Backend Developer"
      - "Frontend Developer"
      - "UX Designer (opcjonalnie)"
  roi:
    breakeven: "8-12 miesięcy"
    annual_savings: "100-150k PLN"
    key_factors:
      - "Automatyzacja obsługi zamówień (60% mniej czasu)"
      - "Integracja z ERP (eliminacja podwójnego wprowadzania)"
```

### 4.7 CTA / Next Steps - "Co dalej?" (Krok 11)

**Cel:** Sekcja końcowa artykułu która pomaga przedsiębiorcy podjąć konkretne akcje po przeczytaniu.

**Dla kogo:**
Przedsiębiorcy którzy przeczytali artykuł i zastanawiają się "ok, to co teraz?".

**Co generuje AI:**

Sekcja dopasowana do typu artykułu:

**A) Artykuł praktyczny/wdrożeniowy:**
- ✅ Pierwsze kroki (3-5 akcji do wykonania)
- ✅ Przydatne narzędzia (templates, calculators, checklists)
- ✅ CTA wsparcia (konsultacje, RFP templates)
- ✅ Polecane artykuły (2-3 z related articles)
- ⚠️ Optional warning (jeśli high complexity/investment)

**B) Artykuł teoretyczny/strategiczny:**
- 🎯 Self-assessment (3-5 pytań yes/no)
- 🎯 Rekomendacja (na podstawie odpowiedzi)
- 📖 Następne kroki lektury (2-3 artykuły)
- 📖 Praktyczne zasoby
- 💬 CTA konsultacji/ankiety potrzeb

**C) Artykuł optymalizacyjny/compliance:**
- 🔍 Narzędzia do audytu (darmowe checkers)
- ⚡ Quick wins (3 akcje, impact + czas)
- 🚀 Pełne wdrożenie (CTA audyt/wdrożenie)
- 📚 Powiązane artykuły (2-3)

**Elementy wypełniane z kontekstu:**
- Timeframes z business_metadata.timeline
- Actions z checklist lub głównych sekcji
- Tools wspomniane w artykule + rekomendacje
- Questions do self-assessment (3-5 pytań)
- Related articles z internal linking (2-3 najbardziej pasujące)

**Prompt:** `prompts/articles/prompt_cta_next_steps.md`

**Input:** article.md, business_metadata, related_articles, seria/silos

**Output:** Sekcja "Co dalej?" wstawiona na koniec article.md (przed "Powiązane artykuły")

**Przykład output (artykuł wdrożeniowy):**
```markdown
## Co dalej?

### ✅ Jeśli planujesz wdrożenie w najbliższych 3-6 miesięcy:

**Pierwsze kroki:**
1. **Zdefiniuj wymagania biznesowe** - zrób listę funkcji must-have vs nice-to-have
2. **Ustal realny budżet** - orientacyjny koszt 50-150k PLN, uwzględnij bufór 20%
3. **Wybierz 3-5 platform do porównania** - skup się na tych pasujących do B2B/B2C

**Przydatne narzędzia:**
- [Platform comparison spreadsheet](#) - gotowy Excel (30+ kryteriów)
- [RFP template](#) - wyślij do agencji i dostań porównywalne oferty

**Potrzebujesz pomocy?**
- [Umów bezpłatną konsultację](#) - omówimy case i pomożemy wybrać (30 min)
- [Zapytaj o wdrożenie](#) - wycena + plan projektu w 2-3 dni

### 📚 Jeśli jeszcze zbierasz wiedzę:

**Polecane artykuły:**
- [Integracje ERP, WMS i CRM](link) - dowiesz się jak połączyć z systemami backend
- [Koszty utrzymania e-commerce](link) - ukryte koszty których nie widzisz

⚠️ **Ważne:** Wybór platformy to decyzja na 3-5 lat. Źle dobrana może kosztować 2-3x więcej w maintenance. Warto poświęcić czas na research.
```

### 4.8 Schema.org Markup (Krok 13)

**Cel:** Wygenerować structured data (JSON-LD) dla artykułu aby poprawić SEO i wyświetlanie w wynikach wyszukiwania Google (rich snippets).

**Dlaczego to ważne:**
- **Rich snippets w Google** - FAQ, HowTo, ratings wyświetlane bezpośrednio w wynikach
- **Wyższe CTR** - rich snippets zwiększają klikalność o 20-30%
- **Lepsze SEO** - Google lepiej rozumie strukturę i treść artykułu
- **Przewaga konkurencyjna** - większość polskich blogów nie używa structured data

**Co generuje AI:**

**1. Article Schema (ZAWSZE)**
- headline, description, image, datePublished, author, publisher, keywords

**2. FAQPage Schema (jeśli artykuł ma FAQ)**
- Lista pytań i odpowiedzi w formacie Schema.org
- Google wyświetla je jako rich snippets w wynikach

**3. HowTo Schema (jeśli artykuł ma Checklist)**
- Kroki z checklisty jako HowTo steps
- Google wyświetla jako step-by-step guide

**4. BreadcrumbList Schema (ZAWSZE)**
- Nawigacja: Home → Artykuły → Seria → Silos → Artykuł
- Wyświetlana jako breadcrumbs w Google

**Format output:**
Osobne bloki `<script type="application/ld+json">` dla każdego typu schema (nie łączyć w jeden obiekt).

**Prompt:** `prompts/metadata/prompt_schema_markup.md`

**Input:** article.md, meta_title, meta_description, FAQ, Checklist, images, article_url, dates

**Output:** `schema.json` → bloki HTML gotowe do wklejenia w `<head>`

**Przykład output:**
```html
<!-- Article Schema -->
<script type="application/ld+json">
{
  "@context": "https://schema.org",
  "@type": "Article",
  "headline": "Bezpieczeństwo e-commerce: praktyczny przewodnik RODO 2025",
  "description": "Dowiedz się jak zabezpieczyć sklep online i spełnić wymogi RODO...",
  "image": ["https://www.digitalvantage.pl/images/hero.jpg"],
  "datePublished": "2025-01-06T10:00:00+01:00",
  "author": {
    "@type": "Organization",
    "name": "Digital Vantage"
  },
  "keywords": ["RODO", "e-commerce", "bezpieczeństwo"]
}
</script>

<!-- FAQPage Schema (jeśli artykuł ma FAQ) -->
<script type="application/ld+json">
{
  "@context": "https://schema.org",
  "@type": "FAQPage",
  "mainEntity": [
    {
      "@type": "Question",
      "name": "Czy każdy sklep musi mieć politykę prywatności?",
      "acceptedAnswer": {
        "@type": "Answer",
        "text": "<p>Tak, polityka prywatności jest obowiązkowa...</p>"
      }
    }
  ]
}
</script>

<!-- BreadcrumbList Schema -->
<script type="application/ld+json">
{
  "@context": "https://schema.org",
  "@type": "BreadcrumbList",
  "itemListElement": [
    {"@type": "ListItem", "position": 1, "name": "Strona główna", "item": "https://..."},
    {"@type": "ListItem", "position": 2, "name": "Artykuły", "item": "https://..."},
    {"@type": "ListItem", "position": 3, "name": "E-commerce", "item": "https://..."}
  ]
}
</script>
```

**Testing:**
User powinien przetestować output w:
- Google Rich Results Test: https://search.google.com/test/rich-results
- Schema.org Validator: https://validator.schema.org/

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
| `prompt_streszczenie_artykulu.md` | Krok 2: Streszczenie "Co znajdziesz" | KONSPEKT_TRESC, TYTUL_ARTYKULU, TARGET_AUDIENCE |
| `prompt_linkowanie_wewnetrzne.md` | Krok 3: Internal linking | TYTUL_ARTYKULU, KONSPEKT_TRESC, ARTICLE_PATH, SERIA, SILOS, AVAILABLE_ARTICLES |
| `prompt_artykul_common.md` | Kroki 4-5: Wytyczne | (wklejane jako WYTYCZNE_WSPOLNE) |
| `prompt_artykul_start.md` | Krok 4: Pierwsza sekcja | KONSPEKT_TRESC, WYTYCZNE_WSPOLNE, TYTUL_ARTYKULU, RELATED_ARTICLES |
| `prompt_artykul_kontynuacja.md` | Krok 5: Kolejne sekcje | KONSPEKT_TRESC, OSTATNIA_SEKCJA, WYTYCZNE_WSPOLNE, TYTUL_ARTYKULU, RELATED_ARTICLES |
| `prompt_sprawdz_naglowki.md` | Krok 7: SEO review | (treść draft) |
| `prompt_sprawdz_styl.md` | Krok 8: Humanizacja | (treść draft) |
| `prompt_multimedia_suggestions.md` | Krok 9: Multimedia | TYTUL_ARTYKULU, ARTICLE_CONTENT, KONSPEKT_TRESC, TARGET_AUDIENCE |
| `prompt_business_metadata.md` | Krok 10: Business metadata | TYTUL_ARTYKULU, ARTICLE_CONTENT, KONSPEKT_TRESC, SERIA, SILOS |
| `prompt_cta_next_steps.md` | Krok 11: CTA / Next Steps | TYTUL_ARTYKULU, ARTICLE_CONTENT, BUSINESS_METADATA, RELATED_ARTICLES, SERIA, SILOS |
| `prompt_schema_markup.md` | Krok 13: Schema.org markup | TYTUL_ARTYKULU, META_TITLE, META_DESCRIPTION, ARTICLE_CONTENT, ARTICLE_URL, PUBLISH_DATE, MODIFIED_DATE, IMAGES, FAQ_CONTENT, CHECKLIST_CONTENT |

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

**Plik:** `categories.yaml`
**Format:** YAML hierarchiczny (git-friendly):
- Tytuł (nazwa kategorii)
- Slug (URL-friendly)
- Element nadrzędny (hierarchia)
- Liczba artykułów
- Pełna ścieżka URL

**Liczba kategorii:** 146 (hierarchicznych)

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
- Lista kategorii z categories.yaml (146 kategorii)

**Proces:**
1. AI analizuje treść artykułu
2. Wybiera 1-5 najbardziej pasujących kategorii z categories.yaml
3. Jeśli brak odpowiednich → sugeruje nowe kategorie
4. Zapisuje do `categories.yaml` w folderze artykułu

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
- ✅ Kategorie z categories.yaml (git-friendly)
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
5. ✓ Przypisywanie kategorii z categories.yaml (YAML hierarchiczny)
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
