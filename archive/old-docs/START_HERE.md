# 👋 Witaj w Blog Agent!

## 🎯 Czym jest Blog Agent?

Blog Agent to inteligentny system AI, który automatycznie tworzy wysokiej jakości artykuły blogowe. 

**Proces jest prosty:**
1. Podajesz temat
2. AI tworzy konspekt
3. AI pisze artykuł sekcja po sekcji
4. Każda sekcja jest audytowana i poprawiana
5. Otrzymujesz gotowy artykuł w Markdown

**Czas:** ~3-5 minut na artykuł  
**Wynik:** Profesjonalny, dobrze napisany artykuł gotowy do publikacji

---

## 🚀 Zacznij w 3 krokach

### 1️⃣ Instalacja (2 minuty)

```bash
./setup.sh
```

Skrypt automatycznie:
- ✅ Sprawdzi wymagania
- ✅ Zainstaluje zależności
- ✅ Pomoże skonfigurować klucz API

### 2️⃣ Uruchomienie (1 minuta)

```bash
python3 blog_agent.py
```

Lub wypróbuj różne przykłady:
```bash
python3 examples.py
```

### 3️⃣ Gotowe! (30 sekund)

Twój artykuł jest w katalogu `outputs/` gotowy do:
- 📝 Publikacji na blogu
- 📝 Wklejenia do WordPress/Medium
- 📝 Dalszej edycji

---

## 📚 Co dalej?

### Pierwszy raz tutaj?
1. **[QUICKSTART.md](QUICKSTART.md)** - Najszybsza droga do pierwszego artykułu (5 min)
2. **[PROCESS.md](PROCESS.md)** - Zobacz jak działa agent (wizualizacja procesu)

### Chcesz więcej opcji?
3. **[README.md](README.md)** - Pełna dokumentacja wszystkich funkcji (15 min)
4. **[examples.py](examples.py)** - 5 gotowych przykładów + tryb interaktywny

### Inna platforma AI?
5. **[PLATFORMS.md](PLATFORMS.md)** - Instrukcje dla OpenAI, Gemini, Ollama i 5+ innych

### Szukasz czegoś konkretnego?
6. **[INDEX.md](INDEX.md)** - Kompletny spis treści projektu

---

## 💡 Szybkie odpowiedzi

**Q: Czy to działa?**  
A: Tak! Uruchom `python3 examples.py` i wybierz przykład.

**Q: Czy to kosztuje?**  
A: Tak, potrzebujesz klucza API (Claude lub OpenAI). Koszt: ~$0.10-0.50 za artykuł. Lub użyj Ollama za darmo!

**Q: Ile to trwa?**  
A: 3-5 minut na typowy artykuł (5-7 sekcji).

**Q: Jaka jest jakość?**  
A: Bardzo dobra! Agent ma wbudowany system audytu i automatycznej poprawy.

**Q: Czy mogę to dostosować?**  
A: Tak! Wszystko jest konfigurowalne - długość, kryteria, styl, model AI.

**Q: Które API jest najlepsze?**  
A: Claude Sonnet 4 lub GPT-4 dla najwyższej jakości. GPT-3.5 dla balansu cena/jakość.

---

## 🎨 Przykłady artykułów

Agent radzi sobie świetnie z:

✅ **Artykuły techniczne**
- "Wprowadzenie do React Hooks"
- "Best practices w Node.js"
- "Jak zoptymalizować wydajność bazy danych"

✅ **Artykuły biznesowe**
- "Jak wdrożyć AI w małej firmie"
- "5 strategii content marketingu dla SaaS"
- "ROI z automatyzacji procesów"

✅ **Artykuły lifestylowe**
- "Minimalizm cyfrowy - praktyczny przewodnik"
- "Jak zbudować poranne rutyny"
- "30-dniowe wyzwanie produktywności"

✅ **Poradniki i tutoriale**
- "Jak zacząć blogować w 2025"
- "Kompletny przewodnik po SEO"
- "Instagram marketing dla początkujących"

---

## 🛠️ Szybkie komendy

```bash
# Podstawowy artykuł (domyślny temat)
python3 blog_agent.py

# Przykłady interaktywne
python3 examples.py

# Wersja OpenAI
python3 blog_agent_openai.py

# Setup / reinstalacja
./setup.sh

# Sprawdź wersje
python3 --version
pip list | grep anthropic
```

---

## 📁 Struktura projektu (dla ciekawskich)

```
blog-agent/
├── 🚀 blog_agent.py           # Główny skrypt (Claude)
├── 🚀 blog_agent_openai.py    # Wersja dla OpenAI
├── 🎯 examples.py             # 5 przykładów + tryb interaktywny
├── 🔧 setup.sh                # Instalator
├── 📦 requirements.txt        # Zależności Python
├── 📚 README.md               # Pełna dokumentacja
├── 🏃 QUICKSTART.md           # Szybki start
├── 🔄 PROCESS.md              # Wizualizacja procesu
├── 🌐 PLATFORMS.md            # Instrukcje dla innych AI
├── 📋 INDEX.md                # Spis treści
├── 📝 CHANGELOG.md            # Historia zmian
├── ⚙️ .env.example            # Przykładowa konfiguracja
└── 📄 LICENSE                 # Licencja MIT
```

---

## 🎁 Bonus: Tryb interaktywny

Nie wiesz od czego zacząć? Użyj trybu interaktywnego:

```bash
python3 examples.py
```

Wybierz opcję **6** (Tryb interaktywny) i agent poprowadzi Cię przez cały proces:
- ❓ Zapyta o temat
- ❓ Zapyta o dodatkowy kontekst
- ❓ Pozwoli wybrać typ artykułu
- ✅ Stworzy artykuł
- ✅ Zapisze go automatycznie

To idealny sposób na pierwszy kontakt z agentem!

---

## 🆘 Potrzebujesz pomocy?

### Problemy techniczne?
1. Sprawdź [INDEX.md](INDEX.md) - sekcja "Troubleshooting"
2. Zobacz logi w konsoli - agent wyświetla szczegółowe informacje
3. Uruchom ponownie `./setup.sh`

### Pytania o funkcje?
1. [README.md](README.md) - pełna dokumentacja API
2. [QUICKSTART.md](QUICKSTART.md) - najczęstsze scenariusze
3. [examples.py](examples.py) - zobacz kod w akcji

### Inna platforma AI?
1. [PLATFORMS.md](PLATFORMS.md) - instrukcje dla 8+ platform
2. [blog_agent_openai.py](blog_agent_openai.py) - gotowa wersja dla OpenAI

---

## 🌟 Tips & Tricks

### 💰 Oszczędność kosztów
- Użyj `gpt-3.5-turbo` zamiast `gpt-4` (10x taniej)
- Użyj **Ollama** z lokalnymi modelami (całkowicie za darmo!)
- Ogranicz `max_improvement_attempts` do 1

### ⚡ Szybsze wykonanie
- Zmniejsz liczbę sekcji (3-4 zamiast 7)
- Użyj szybszego modelu
- Złagodź kryteria audytu

### 🎨 Lepsza jakość
- Dodaj więcej szczegółów w `additional_context`
- Użyj Claude Opus 4 lub GPT-4
- Zwiększ `max_improvement_attempts` do 3-4
- Zdefiniuj dokładne kryteria audytu

---

## 🎉 Gotowy?

**Krok 1:** Uruchom setup
```bash
./setup.sh
```

**Krok 2:** Stwórz pierwszy artykuł
```bash
python3 examples.py
```

**Krok 3:** Ciesz się wynikiem! 🎊

---

## 📞 Wsparcie

- 📖 Dokumentacja: [README.md](README.md)
- 🏃 Szybki start: [QUICKSTART.md](QUICKSTART.md)
- 🔄 Jak to działa: [PROCESS.md](PROCESS.md)
- 🌐 Inne platformy: [PLATFORMS.md](PLATFORMS.md)

---

**Autor:** Blog Agent Contributors  
**Licencja:** MIT (wolne użytkowanie, nawet komercyjne!)  
**Wersja:** 1.0.0 (2025-11-06)

---

# 🚀 ZACZYNAMY!

Przejdź do → **[QUICKSTART.md](QUICKSTART.md)** ← aby stworzyć pierwszy artykuł!
