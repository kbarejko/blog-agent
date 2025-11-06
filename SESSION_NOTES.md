# Session Notes

## Purpose
This file tracks the progress and context of work sessions to prevent data loss and maintain continuity between sessions.

---

## Session: 2025-11-06

### Setup
- Initialized git repository
- Created environment for session tracking
- Added .gitignore for Python project
- Created SESSION_NOTES.md for documentation
- Created TODO.md for task management

### Context
- Project: blog-agent
- Working directory: /home/kbarejko/blog-agent
- Main files: blog_agent.py, blog_agent_openai.py (stare, do przebudowy)

### Zebrane wymagania (kompletne)

#### 1. Cel projektu
Automatyczny system AI do tworzenia artykułów blogowych:
- Generowanie konspektu → Pisanie po sekcjach → SEO review → Humanizacja → Przypisywanie kategorii
- Pełna automatyzacja po uruchomieniu z review AI na każdym etapie
- Git versioning w kluczowych momentach
- Claude (Sonnet 4) jako główny provider

#### 2. Struktura artykułów
```
artykuly/
├── [seria]/          # np. ecommerce, saas, ai (wiele serii)
│   ├── [silos]/      # np. operacje, platformy, seo, ux-ui
│   │   ├── [slug]/
│   │   │   ├── config.yaml       # user input
│   │   │   ├── outline.md        # AI generated
│   │   │   ├── sections/         # robocze
│   │   │   ├── draft.md          # przed humanizacją
│   │   │   ├── article.md        # finalna wersja
│   │   │   └── categories.yaml   # przypisane kategorie
```

**Struktura folderów = Struktura URL (1:1)**
- Folder: `artykuly/ecommerce/operacje/bezpieczenstwo-i-rodo/`
- URL: `https://www.digitalvantage.pl/artykuly/ecommerce/operacje/bezpieczenstwo-i-rodo/`

#### 3. Config artykułu (user input)
```yaml
title: "Tytuł H1"
target_audience: "Grupa docelowa"
tone: "ekspercki, ale naturalny i rozmowny"

# AI generuje:
meta_title: "SEO title (≠ H1)"
meta_description: "SEO description (160 chars)"
```

#### 4. Proces (8 kroków + opcjonalne sekcje)
1. **Init** - tworzenie struktury (opcjonalne)
2. **Konspekt** - outline.md (prompt_konspekt_artykulu.md) → git commit
   - AI decyduje: czy dodać Checklist i/lub FAQ (opcjonalne sekcje)
3. **Pisanie sekcji 1** - intro + pierwsza (prompt_artykul_start.md) → review AI
4. **Pisanie sekcji 2-N** - kolejne sekcje (prompt_artykul_kontynuacja.md) → review AI każdej
   - Opcjonalnie: Checklist (jeśli w konspekcie)
   - Opcjonalnie: FAQ do 10 pytań (jeśli w konspekcie)
5. **Draft** - połączenie sekcji → draft.md → git commit
6. **SEO review** - nagłówki (prompt_sprawdz_naglowki.md) → auto-fix
7. **Humanizacja** - naturalny język (prompt_sprawdz_styl.md) → article.md → git commit
8. **Kategorie** - AI analizuje artykuł, wybiera z Excel (147 kat.) → categories.yaml → git commit

**Czas:** ~5 min na artykuł (5 sekcji, 3000 słów)
**Koszt:** ~$0.08 per artykuł (Claude Sonnet 4)

#### 5. Review AI (automatyczny)
Po każdej sekcji sprawdza:
- Długość: 300-400 słów
- Czytelność: Flesch 40-60
- Styl: ekspercki ale rozmowny (zgodnie z prompt_artykul_common.md)
- Auto-fix jeśli nie spełnia (max 2 próby)

#### 6. Kategorie (many-to-many)
- **Źródło:** kategoria-artykulow.xlsx (147 kategorii hierarchicznych)
- **Przypisywanie:** PO napisaniu artykułu (krok 8)
- **Proces:** AI wybiera 1-5 najlepszych + sugeruje nowe jeśli brak
- **Niezależne od URL:** artykuł w `/ecommerce/operacje/X` może mieć kategorie ["Strategia IT", "RODO", "E-commerce"]
- **Użycie:** Filtrowanie na stronie, SEO, rekomendacje

#### 7. CLI Interface
```bash
# Inicjalizacja
python blog_agent.py init --series ecommerce --silo operacje --slug moj-artykul

# Generowanie
python blog_agent.py create --config artykuly/.../config.yaml

# Lista, status
python blog_agent.py list [--series ecommerce]
python blog_agent.py status --path artykuly/.../
```

#### 8. Git commits (automatyczne)
- Po outline
- Po draft
- Po publikacji article.md
- Po przypisaniu kategorii

Format: `[series/silo/slug] Action`

#### 9. Prompty (wykorzystanie istniejących)
- `prompts/konspekt/prompt_konspekt_artykulu.md`
- `prompts/articles/prompt_artykul_common.md` (wytyczne wspólne)
- `prompts/articles/prompt_artykul_start.md`
- `prompts/articles/prompt_artykul_kontynuacja.md`
- `prompts/audyt/prompt_sprawdz_naglowki.md`
- `prompts/audyt/prompt_sprawdz_styl.md`

Zmienne: `{{TEMAT_ARTYKULU}}`, `{{KONSPEKT_TRESC}}`, `{{WYTYCZNE_WSPOLNE}}`, etc.

### Changes Made
- Git initialized (initial commit)
- Zebranie kompletnych wymagań przez Q&A
- Analiza istniejącego kodu (blog_agent.py)
- Przeczytanie wszystkich promptów i dokumentacji
- Analiza struktury strony (digitalvantage.pl)
- Przeczytanie kategorii z Excel (147 kategorii)
- **Utworzenie REQUIREMENTS.md** - kompletna specyfikacja (15 sekcji, 3000+ linii)
- Cleanup projektu - archiwizacja starych plików
- **Update REQUIREMENTS.md** - dodano opcjonalne sekcje (Checklist, FAQ)
- **Update prompt_konspekt_artykulu.md** - instrukcje dla AI o decydowaniu o opcjonalnych sekcjach

### Important Decisions
1. **Struktura URL = Struktura folderów** (1:1, bez wyjątków)
2. **Kategorie niezależne** od URL (many-to-many z Excel)
3. **Przypisywanie kategorii PO napisaniu** artykułu (nie przed)
4. **Review AI automatyczny** z auto-fix (max 2 próby)
5. **Git commits w kluczowych momentach** (4 commity per artykuł)
6. **Claude Sonnet 4** jako główny provider (możliwość rozbudowy o OpenAI)
7. **Wykorzystanie istniejących promptów** z folderu prompts/
8. **Dowolna inicjalizacja** (user lub agent może stworzyć folder+config)
9. **Opcjonalne sekcje** - AI decyduje czy dodać Checklist i/lub FAQ (max 10 pytań)

### Next Steps
1. **Zapoznanie z REQUIREMENTS.md** (pełna specyfikacja)
2. **Planowanie architektury** systemu
3. **Implementacja** (nowy blog_agent.py)
4. **Testing** na przykładowym artykule
5. **Dokumentacja** API i usage examples

### Files Created
- `.gitignore` - Python project
- `SESSION_NOTES.md` - dokumentacja sesji
- `TODO.md` - task management
- **`REQUIREMENTS.md` - KOMPLETNA SPECYFIKACJA SYSTEMU (KLUCZOWY PLIK)**

---

## Instructions for Next Session
1. Read this file first to understand previous context
2. Check TODO.md for pending tasks
3. Run `git log` to see recent commits
4. Review `git status` to see current changes

## Tips
- Update this file before ending each session
- Commit changes frequently
- Document important decisions and reasons
