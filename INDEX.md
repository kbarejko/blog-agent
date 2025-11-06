# 📦 Blog Agent - Struktura Projektu

## 📂 Spis plików

### 📄 Główne pliki wykonywalne

| Plik | Opis | Użycie |
|------|------|--------|
| **blog_agent.py** | Główny skrypt agenta (Claude/Anthropic) | `python3 blog_agent.py` |
| **blog_agent_openai.py** | Wersja dla OpenAI/GPT-4 | `python3 blog_agent_openai.py` |
| **examples.py** | Interaktywne przykłady użycia | `python3 examples.py` |
| **setup.sh** | Skrypt instalacyjny | `./setup.sh` |

### 📚 Dokumentacja

| Plik | Co znajdziesz? |
|------|----------------|
| **README.md** | Pełna dokumentacja projektu, API, przykłady |
| **QUICKSTART.md** | Szybki start w 3 krokach |
| **PLATFORMS.md** | Instrukcje dla różnych platform AI (OpenAI, Gemini, Ollama, etc.) |
| **INDEX.md** | Ten plik - spis treści projektu |

### ⚙️ Konfiguracja

| Plik | Opis |
|------|------|
| **requirements.txt** | Zależności Python |
| **.env.example** | Przykładowa konfiguracja kluczy API |

---

## 🚀 Szybki Start

### Krok 1: Instalacja
```bash
./setup.sh
```

### Krok 2: Konfiguracja API
```bash
export ANTHROPIC_API_KEY='twój-klucz'
# LUB
export OPENAI_API_KEY='twój-klucz'
```

### Krok 3: Uruchomienie
```bash
# Podstawowa wersja (Claude)
python3 blog_agent.py

# Wersja OpenAI
python3 blog_agent_openai.py

# Przykłady interaktywne
python3 examples.py
```

---

## 📖 Który plik czytać jako pierwszy?

1. **QUICKSTART.md** - Jeśli chcesz szybko zacząć (5 min)
2. **README.md** - Jeśli chcesz poznać wszystkie opcje (15 min)
3. **PLATFORMS.md** - Jeśli chcesz użyć innej platformy AI (10 min)
4. **examples.py** - Jeśli uczysz się przez przykłady (kod)

---

## 🎯 Use Cases - Który skrypt wybrać?

### Chcę stworzyć jeden artykuł szybko
```bash
python3 blog_agent.py
```
Otwórz plik, zmień temat w funkcji `main()`, uruchom.

### Chcę przetestować różne przykłady
```bash
python3 examples.py
```
Wybierz przykład z menu lub użyj trybu interaktywnego.

### Chcę zintegrować z moją aplikacją
```python
from blog_agent import BlogAgent

agent = BlogAgent()
article = agent.create_article(topic="Mój temat")
```
Zobacz sekcję "Użycie" w README.md

### Chcę użyć OpenAI zamiast Claude
```bash
python3 blog_agent_openai.py
```
Albo zmodyfikuj swój kod używając `BlogAgentOpenAI` zamiast `BlogAgent`.

### Chcę użyć innej platformy (Gemini, Ollama, etc.)
Przeczytaj **PLATFORMS.md** - znajdziesz gotowe instrukcje dla 8+ platform.

---

## 🔧 Struktura kodu

### blog_agent.py

```
BlogAgent
├── __init__()              # Inicjalizacja z kluczem API
├── create_outline()        # Tworzenie konspektu
├── write_section()         # Pisanie pojedynczej sekcji
├── audit_section()         # Audyt jakości sekcji
├── improve_section()       # Poprawa sekcji
├── create_article()        # Główny proces (orkiestracja)
└── save_article()          # Zapis do pliku
```

### examples.py

```
Przykłady:
├── example_1_basic()           # Podstawowe użycie
├── example_2_with_context()    # Z dodatkowym kontekstem
├── example_3_custom_audit()    # Własne kryteria audytu
├── example_4_business()        # Artykuł biznesowy
├── example_5_lifestyle()       # Artykuł lifestylowy
└── interactive_mode()          # Tryb interaktywny
```

---

## 📊 Porównanie wersji

| Cecha | blog_agent.py | blog_agent_openai.py |
|-------|---------------|----------------------|
| Platforma | Anthropic Claude | OpenAI GPT |
| Jakość | ⭐⭐⭐⭐⭐ | ⭐⭐⭐⭐⭐ |
| Koszt | $$$ | $$$$ |
| Zmienna env | ANTHROPIC_API_KEY | OPENAI_API_KEY |
| Model domyślny | claude-sonnet-4 | gpt-4-turbo-preview |

Funkcjonalność jest identyczna - wybierz według preferencji platformy!

---

## 🛠️ Modyfikacje i customizacja

### Zmienić długość sekcji?
Edytuj metodę `write_section()`, znajdź:
```python
# Napisz kompletną treść sekcji (300-500 słów)
```
Zmień na np. `(500-800 słów)` dla dłuższych sekcji.

### Zmienić liczbę sekcji?
Edytuj metodę `create_outline()`, znajdź:
```python
# Lista sekcji (4-7 sekcji)
```
Zmień na np. `(8-12 sekcji)` dla dłuższych artykułów.

### Dodać własne kryteria audytu?
Przekaż parametr `audit_criteria` do `create_article()`:
```python
my_criteria = {
    "SEO": "Czy zawiera słowa kluczowe?",
    "CTA": "Czy ma call-to-action?"
}

article = agent.create_article(
    topic="...",
    audit_criteria=my_criteria
)
```

### Zmienić model AI?
```python
# Dla Claude
agent = BlogAgent()
agent.model = "claude-opus-4-20250514"  # Najwyższa jakość

# Dla OpenAI
agent = BlogAgentOpenAI(model="gpt-3.5-turbo")  # Tańszy
```

---

## 🆘 Troubleshooting

### Problem: "Brak klucza API"
**Rozwiązanie:**
```bash
export ANTHROPIC_API_KEY='twój-klucz'
```

### Problem: "ModuleNotFoundError: No module named 'anthropic'"
**Rozwiązanie:**
```bash
pip install -r requirements.txt --break-system-packages
```

### Problem: Artykuł jest za krótki
**Rozwiązanie:**
- Zwiększ zakres słów w `write_section()`
- Dodaj więcej sekcji modyfikując `create_outline()`
- Dodaj więcej kontekstu w `additional_context`

### Problem: Sekcje nie przechodzą audytu
**Rozwiązanie:**
```python
article = agent.create_article(
    topic="...",
    max_improvement_attempts=3  # Więcej prób
)
```

### Problem: Zbyt wysokie koszty API
**Rozwiązanie:**
- Użyj tańszego modelu: `gpt-3.5-turbo` lub `claude-haiku`
- Użyj Ollama (lokalnie, za darmo) - zobacz PLATFORMS.md
- Ogranicz liczbę prób poprawy: `max_improvement_attempts=1`

---

## 🎓 Learning Path

### Poziom 1: Podstawy (30 min)
1. Przeczytaj QUICKSTART.md
2. Uruchom `./setup.sh`
3. Uruchom `python3 blog_agent.py`
4. Otwórz wygenerowany artykuł

### Poziom 2: Customizacja (1h)
1. Przeczytaj README.md
2. Uruchom `python3 examples.py`
3. Wypróbuj tryb interaktywny
4. Zmodyfikuj kryteria audytu

### Poziom 3: Integracja (2h)
1. Zintegruj z własną aplikacją
2. Dostosuj długość i strukturę artykułów
3. Dodaj własne kryteria audytu
4. Eksperymentuj z różnymi modelami

### Poziom 4: Advanced (3h+)
1. Przeczytaj PLATFORMS.md
2. Wypróbuj różne platformy AI
3. Stwórz własne warianty skryptu
4. Dodaj nowe funkcje (np. generowanie obrazów)

---

## 📞 Wsparcie

### Gdzie szukać pomocy?

1. **Dokumentacja w projekcie** - Najpierw sprawdź README.md
2. **Przykłady** - Zobacz examples.py
3. **Platformy AI** - Sprawdź PLATFORMS.md dla swojej platformy
4. **Logi** - Agent wyświetla szczegółowe informacje podczas działania

### Częste pytania (FAQ)

**Q: Który model AI jest najlepszy?**
A: Claude Sonnet 4 lub GPT-4 dla najwyższej jakości. GPT-3.5-turbo dla balansu cena/jakość.

**Q: Czy mogę używać tego komercyjnie?**
A: Tak, projekt ma licencję MIT.

**Q: Jak długo trwa generowanie artykułu?**
A: 2-5 minut zależnie od długości i liczby sekcji.

**Q: Czy mogę użyć tego bez klucza API?**
A: Tak, użyj Ollama z lokalnymi modelami (zobacz PLATFORMS.md).

---

## 🗺️ Roadmap

Możliwe przyszłe rozszerzenia:

- [ ] Generowanie obrazów do artykułów (DALL-E, Midjourney)
- [ ] Automatyczne SEO metadata
- [ ] Multi-language support
- [ ] Direct publishing (WordPress, Medium API)
- [ ] A/B testing tytułów
- [ ] Integracja z CMS
- [ ] Web UI / Dashboard
- [ ] Batch processing (wiele artykułów naraz)

---

**Ostatnia aktualizacja:** 2025-11-06

**Wersja:** 1.0.0

**Licencja:** MIT

---

🎉 **Gotowy do tworzenia świetnych artykułów? Zacznij od QUICKSTART.md!**
