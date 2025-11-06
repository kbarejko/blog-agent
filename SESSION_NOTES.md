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

#### 4. Proces (11 kroków + opcjonalne sekcje + internal linking + multimedia)
1. **Init** - tworzenie struktury (opcjonalne)
2. **Konspekt** - outline.md (prompt_konspekt_artykulu.md) → git commit
   - AI decyduje: czy dodać Checklist i/lub FAQ (opcjonalne sekcje)
3. **Streszczenie "Co znajdziesz w artykule?"** - sections/00-summary.md (prompt_streszczenie_artykulu.md)
   - 3-5 punktów z konkretnymi wnioskami/wartościami (NIE spis treści!)
   - Zawsze generowane, na początku artykułu
4. **Pisanie sekcji 1** - intro + pierwsza (prompt_artykul_start.md) → review AI
5. **Pisanie sekcji 2-N** - kolejne sekcje (prompt_artykul_kontynuacja.md) → review AI każdej
   - Opcjonalnie: Checklist (jeśli w konspekcie)
   - Opcjonalnie: FAQ do 10 pytań (jeśli w konspekcie)
6. **Draft** - połączenie: streszczenie + sekcje → draft.md → git commit
7. **SEO review** - nagłówki (prompt_sprawdz_naglowki.md) → auto-fix
8. **Humanizacja** - naturalny język (prompt_sprawdz_styl.md) → article.md → git commit
9. **Kategorie** - AI analizuje artykuł, wybiera z Excel (147 kat.) → categories.yaml → git commit

**Czas:** ~5min 40s na artykuł (5 sekcji, 3000 słów)
**Koszt:** ~$0.08 per artykuł (Claude Sonnet 4)

**Nowe kroki:**
- Krok 3: Internal linking (auto-select 5-8 powiązanych artykułów)
- Krok 9: Multimedia suggestions (4-9 sugestii z image prompts)

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

#### 9. Prompty (9 plików)
- `prompts/konspekt/prompt_konspekt_artykulu.md` - konspekt + decyzja o opcjonalnych sekcjach
- `prompts/articles/prompt_streszczenie_artykulu.md` - **NOWY** - sekcja "Co znajdziesz w artykule?"
- `prompts/articles/prompt_artykul_common.md` - wytyczne wspólne
- `prompts/articles/prompt_artykul_start.md` - intro + pierwsza sekcja
- `prompts/articles/prompt_artykul_kontynuacja.md` - kolejne sekcje
- `prompts/audyt/prompt_sprawdz_naglowki.md` - SEO review nagłówków
- `prompts/audyt/prompt_sprawdz_styl.md` - humanizacja
- `prompts/articles/prompt_linkowanie_wewnetrzne.md` - **NOWY** - internal linking strategy
- `prompts/articles/prompt_multimedia_suggestions.md` - **NOWY** - sugestie multimediów

Zmienne: `{{TEMAT_ARTYKULU}}`, `{{KONSPEKT_TRESC}}`, `{{WYTYCZNE_WSPOLNE}}`, `{{TARGET_AUDIENCE}}`, `{{ARTICLE_CONTENT}}`, etc.

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
- **Update prompt_konspekt_artykulu.md** - instrukcje dla AI o opcjonalnych sekcjach
- **Utworzenie prompt_streszczenie_artykulu.md** - nowy prompt dla sekcji "Co znajdziesz w artykule?"
- **Update REQUIREMENTS.md** - dodano Krok 2 (streszczenie), workflow 8→9 kroków
- **Utworzenie prompt_linkowanie_wewnetrzne.md** - internal linking (hybrid: contextual + end section)
- **Utworzenie prompt_multimedia_suggestions.md** - sugestie multimediów (hero + 3-8 w sekcjach)
- **Update REQUIREMENTS.md** - dodano Krok 3 (internal linking) i Krok 9 (multimedia), workflow 9→11 kroków
- **Update SESSION_NOTES.md** - zaktualizowano proces z nowymi krokami

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
10. **Sekcja "Co znajdziesz w artykule?"** - ZAWSZE generowana (Krok 2), 3-5 konkretnych punktów wartości (NIE spis treści)
11. **Internal linking** - AI auto-select 5-8 powiązanych artykułów (60% ten sam silos), 2-4 contextual + 3-5 end section
12. **Multimedia suggestions** - AI sugeruje 4-9 multimediów (hero + obrazy/wykresy/infografiki), image prompts dla DALL-E/MJ

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

### Session Summary

**Status:** ✅ Requirements gathering and design phase COMPLETE

**What was accomplished:**
- 🎯 Complete requirements specification (REQUIREMENTS.md - 15 sections)
- 📝 9 prompt templates created/updated
- 🔄 Workflow designed: 11-step automated article generation
- 🏗️ Architecture decisions: 12 key decisions documented
- 📊 Feature set finalized: optional sections, summary, internal linking, multimedia
- 📂 Project organized: old files archived, git initialized, documentation in place
- ⏱️ Performance estimated: ~5min 40s per article, ~$0.08 cost
- 💾 All work committed to git (8 commits)

**Ready for next phase:**
The system is fully specified and documented. All prompts are ready. Architecture design and implementation can begin when user confirms.

**Token usage:** Session consumed ~122k tokens (design phase with extensive documentation)

---

## Instructions for Next Session
1. Read this file first to understand previous context
2. Check TODO.md for pending tasks
3. Run `git log` to see recent commits
4. Review `git status` to see current changes
5. **IMPORTANT:** Review REQUIREMENTS.md before starting implementation

## Tips
- Update this file before ending each session
- Commit changes frequently
- Document important decisions and reasons
- REQUIREMENTS.md is the single source of truth - always refer to it
