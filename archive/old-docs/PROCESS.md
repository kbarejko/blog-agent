# 🔄 Blog Agent - Przepływ Procesu

## Wizualizacja działania agenta

```
┌─────────────────────────────────────────────────────────────┐
│                    📝 UŻYTKOWNIK                             │
│                                                              │
│  Podaje:                                                     │
│  • Temat artykułu                                           │
│  • Dodatkowy kontekst (opcjonalnie)                        │
│  • Kryteria audytu (opcjonalnie)                           │
└────────────────────┬────────────────────────────────────────┘
                     │
                     ▼
┌─────────────────────────────────────────────────────────────┐
│               🤖 BLOG AGENT - START                          │
└────────────────────┬────────────────────────────────────────┘
                     │
                     ▼
┌─────────────────────────────────────────────────────────────┐
│         FAZA 1: TWORZENIE KONSPEKTU                         │
│                                                              │
│  AI Agent analizuje temat i tworzy:                         │
│  ✓ Chwytliwy tytuł (SEO-friendly)                          │
│  ✓ Wprowadzenie (2-3 zdania)                               │
│  ✓ Strukturę sekcji (4-7 sekcji)                           │
│  ✓ Dla każdej sekcji:                                       │
│    - Tytuł sekcji                                           │
│    - Opis zawartości                                        │
│    - Kluczowe punkty (3-5)                                  │
│                                                              │
│  Output: JSON z konspektem                                  │
└────────────────────┬────────────────────────────────────────┘
                     │
                     ▼
┌─────────────────────────────────────────────────────────────┐
│         FAZA 2: PĘTLA PISANIA SEKCJI                        │
│                                                              │
│  Dla każdej sekcji z konspektu:                            │
└────────────────────┬────────────────────────────────────────┘
                     │
                     ▼
        ┌────────────────────────────┐
        │  KROK 2.1: Pisanie sekcji  │
        │                            │
        │  AI Agent pisze:           │
        │  • 300-500 słów treści     │
        │  • Format Markdown         │
        │  • Nagłówek ## Tytuł       │
        │  • Merytoryczna treść      │
        │  • Przykłady i analogie    │
        │  • Listy, formatowanie     │
        └────────────┬───────────────┘
                     │
                     ▼
        ┌────────────────────────────┐
        │  KROK 2.2: Audyt sekcji    │
        │                            │
        │  AI Agent ocenia według    │
        │  kryteriów (1-10):         │
        │  • Wartość merytoryczna    │
        │  • Czytelność              │
        │  • Spójność                │
        │  • Angażowanie             │
        │  • Kompletność             │
        │                            │
        │  Wynik: Ocena + Sugestie   │
        └────────────┬───────────────┘
                     │
                     ▼
              ┌─────────────┐
              │ Ocena >= 7? │
              └──────┬──────┘
                     │
         ┌───────────┴───────────┐
         │ TAK                   │ NIE
         ▼                       ▼
    ┌─────────┐         ┌──────────────────┐
    │ Sekcja  │         │ KROK 2.3: Poprawa │
    │ OK!     │         │                   │
    └────┬────┘         │ AI Agent poprawia │
         │              │ sekcję na podstawie│
         │              │ sugestii z audytu │
         │              └────────┬───────────┘
         │                       │
         │                       │ Próba <= Max?
         │                       │
         │              ┌────────┴─────────┐
         │              │ TAK              │ NIE
         │              │                  │
         │              ▼                  ▼
         │      Wraca do audytu      Akceptuje
         │      (2.2)                obecną wersję
         │              │                  │
         └──────────────┴──────────────────┘
                        │
                        ▼
            ┌───────────────────────┐
            │ Czy są jeszcze sekcje?│
            └───────────┬───────────┘
                        │
            ┌───────────┴───────────┐
            │ TAK                   │ NIE
            ▼                       ▼
    Następna sekcja          Wszystkie sekcje
    (Wraca do 2.1)           gotowe!
                                    │
                                    ▼
                    ┌───────────────────────────────┐
                    │  FAZA 3: SKŁADANIE ARTYKUŁU   │
                    │                               │
                    │  Agent łączy wszystko:        │
                    │  • # Tytuł główny             │
                    │  • Wprowadzenie               │
                    │  • ## Sekcja 1                │
                    │  • Treść sekcji 1             │
                    │  • ## Sekcja 2                │
                    │  • Treść sekcji 2             │
                    │  • ...                        │
                    │                               │
                    │  Output: Pełny artykuł MD     │
                    └───────────┬───────────────────┘
                                │
                                ▼
                    ┌───────────────────────────────┐
                    │  FAZA 4: ZAPIS DO PLIKU       │
                    │                               │
                    │  • Format: Markdown (.md)     │
                    │  • Lokalizacja: /outputs/     │
                    │  • Nazwa: article_TIMESTAMP   │
                    │  • Encoding: UTF-8            │
                    └───────────┬───────────────────┘
                                │
                                ▼
                    ┌───────────────────────────────┐
                    │     ✅ GOTOWE!                │
                    │                               │
                    │  Statystyki:                  │
                    │  • Liczba sekcji: X           │
                    │  • Długość: Y znaków          │
                    │  • Słowa: ~Z                  │
                    │  • Czas: T minut              │
                    └───────────┬───────────────────┘
                                │
                                ▼
                    ┌───────────────────────────────┐
                    │      📄 ARTYKUŁ READY         │
                    │                               │
                    │  Gotowy do:                   │
                    │  • Publikacji na blogu        │
                    │  • Wklejenia do CMS           │
                    │  • Dalszej edycji             │
                    └───────────────────────────────┘
```

---

## 📊 Szczegółowy timing procesu

Dla artykułu z 5 sekcjami (typowy case):

| Faza | Czas | % całości |
|------|------|-----------|
| **Tworzenie konspektu** | ~20s | 10% |
| **Pisanie sekcji 1** | ~25s | 12% |
| **Audyt sekcji 1** | ~15s | 7% |
| **Pisanie sekcji 2** | ~25s | 12% |
| **Audyt sekcji 2** | ~15s | 7% |
| **Pisanie sekcji 3** | ~25s | 12% |
| **Audyt sekcji 3** | ~15s | 7% |
| **Pisanie sekcji 4** | ~25s | 12% |
| **Audyt sekcji 4** | ~15s | 7% |
| **Pisanie sekcji 5** | ~25s | 12% |
| **Audyt sekcji 5** | ~15s | 7% |
| **Składanie artykułu** | ~5s | 2% |
| **Zapis do pliku** | <1s | <1% |
| **RAZEM** | **~3-4 min** | **100%** |

⚠️ Jeśli sekcje wymagają poprawy, czas może wzrosnąć o 20-40% na sekcję.

---

## 🔀 Scenariusze alternatywne

### Scenariusz 1: Wszystkie sekcje przechodzą za pierwszym razem
```
Konspekt → Sekcja 1 → Audyt ✅ → Sekcja 2 → Audyt ✅ → ... → Gotowe!
Czas: ~3 minuty
```

### Scenariusz 2: Niektóre sekcje wymagają poprawy
```
Konspekt → Sekcja 1 → Audyt ✅ → 
Sekcja 2 → Audyt ❌ → Poprawa → Audyt ✅ → 
Sekcja 3 → Audyt ✅ → ... → Gotowe!
Czas: ~4-5 minut
```

### Scenariusz 3: Maksymalna liczba poprawek
```
Konspekt → Sekcja 1 → Audyt ❌ → Poprawa → Audyt ❌ → 
Poprawa → Audyt ❌ → Akceptacja (max attempts) → ... → Gotowe!
Czas: ~6-8 minut
```

---

## 🎯 Punkty decyzyjne

### Decision Point 1: Długość artykułu
```
Krótki (3-4 sekcje) → ~2-3 min
Średni (5-7 sekcji) → ~3-5 min
Długi (8-12 sekcji) → ~6-10 min
```

### Decision Point 2: Rygorystyczność audytu
```
Luźne kryteria → Więcej sekcji przechodzi → Szybciej
Ścisłe kryteria → Więcej poprawek → Dłużej, ale wyższa jakość
```

### Decision Point 3: Max improvement attempts
```
1 próba → ~30s oszczędności, ale niższa jakość
2 próby (default) → Balans
3-4 próby → +1-2 min, najwyższa jakość
```

---

## 💡 Optymalizacja procesu

### Dla szybszego wykonania:
1. Użyj szybszego modelu (gpt-3.5-turbo)
2. Zmniejsz max_improvement_attempts do 1
3. Złagodź kryteria audytu
4. Ogranicz liczbę sekcji do 3-4

### Dla najwyższej jakości:
1. Użyj najlepszego modelu (claude-opus-4, gpt-4)
2. Zwiększ max_improvement_attempts do 3-4
3. Zaostrz kryteria audytu
4. Dodaj więcej szczegółów w additional_context

---

## 🧩 Komponenty systemu

```
BlogAgent
│
├── Moduł Planowania
│   └── create_outline()
│       └── Prompt Engineering dla konspektu
│
├── Moduł Pisania
│   └── write_section()
│       └── Prompt Engineering dla treści
│
├── Moduł Audytu
│   └── audit_section()
│       └── Prompt Engineering dla oceny
│
├── Moduł Poprawy
│   └── improve_section()
│       └── Prompt Engineering dla korekty
│
├── Orkiestrator
│   └── create_article()
│       └── Zarządza całym procesem
│
└── I/O Handler
    └── save_article()
        └── Zapis do pliku
```

---

## 📈 Metryki jakości

Agent śledzi i raportuje:

✅ **Struktura:**
- Liczba sekcji
- Długość sekcji (słowa/znaki)
- Spójność struktury

✅ **Jakość treści:**
- Wyniki audytu (1-10)
- Liczba poprawek na sekcję
- Procent sekcji zatwierdzonych za pierwszym razem

✅ **Performance:**
- Czas całkowity
- Czas na sekcję
- Liczba wywołań API

✅ **Output:**
- Całkowita długość artykułu
- Liczba słów
- Format zgodny z Markdown

---

**Aktualizacja diagramu:** 2025-11-06
**Wersja procesu:** 1.0.0
