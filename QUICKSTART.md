# 🚀 Szybki Start - Blog Agent

## W 3 krokach do swojego pierwszego artykułu!

### Krok 1: Instalacja

```bash
# Uruchom skrypt setup
./setup.sh
```

Skrypt automatycznie:
- ✅ Sprawdzi Pythona
- ✅ Zainstaluje zależności
- ✅ Pomoże skonfigurować klucz API

### Krok 2: Uruchomienie

**Opcja A: Podstawowy artykuł**
```bash
python3 blog_agent.py
```

**Opcja B: Wybór z przykładów**
```bash
python3 examples.py
```

**Opcja C: Własny kod**
```python
from blog_agent import BlogAgent

agent = BlogAgent()
article = agent.create_article(topic="Twój temat")
agent.save_article(article)
```

### Krok 3: Gotowe!

Artykuł został zapisany w formacie Markdown i jest gotowy do:
- 📝 Wklejenia na WordPress
- 📝 Publikacji na Medium
- 📝 Dodania do Jekyll/Hugo
- 📝 Użycia w dowolnym CMS

---

## ⚡ Najczęstsze scenariusze

### Chcę artykuł techniczny

```python
agent = BlogAgent()

tech_criteria = {
    "Dokładność": "Czy technicznie poprawne?",
    "Przykłady kodu": "Czy są przykłady?",
    "Best practices": "Czy wskazano dobre praktyki?"
}

article = agent.create_article(
    topic="Wprowadzenie do React Hooks",
    audit_criteria=tech_criteria
)

agent.save_article(article)
```

### Chcę artykuł biznesowy

```python
agent = BlogAgent()

business_criteria = {
    "ROI": "Czy pokazano wartość biznesową?",
    "Case studies": "Czy są przykłady firm?",
    "Dane": "Czy są konkretne liczby?"
}

article = agent.create_article(
    topic="Jak wdrożyć AI w małej firmie",
    additional_context="Dla firm 10-50 osób, ograniczony budżet",
    audit_criteria=business_criteria
)

agent.save_article(article)
```

### Chcę dostosować długość

Otwórz `blog_agent.py` i znajdź metodę `write_section`. Zmień:

```python
# Zamiast: (300-500 słów)
# Użyj:
- Krótki artykuł: (200-300 słów)
- Średni artykuł: (400-600 słów)  
- Długi artykuł: (700-1000 słów)
```

### Chcę więcej/mniej sekcji

Otwórz `blog_agent.py` i znajdź metodę `create_outline`. Zmień:

```python
# Zamiast: (4-7 sekcji)
# Użyj:
- Krótki artykuł: (3-4 sekcji)
- Średni artykuł: (5-7 sekcji)
- Długi artykuł: (8-12 sekcji)
```

---

## 🔧 Rozwiązywanie problemów

### Brak klucza API
```bash
export ANTHROPIC_API_KEY='sk-ant-api...'
```

### Import error
```bash
pip install anthropic --break-system-packages
```

### Artykuł za krótki
Zwiększ zakres słów w `write_section` lub dodaj więcej sekcji

### Sekcje nie przechodzą audytu
```python
# Zwiększ liczbę prób
article = agent.create_article(
    topic="...",
    max_improvement_attempts=3  # zamiast 2
)
```

---

## 📚 Dalsze kroki

1. **Przeczytaj pełną dokumentację**: `README.md`
2. **Zobacz przykłady**: `python3 examples.py`
3. **Dostosuj kryteria audytu** do swoich potrzeb
4. **Eksperymentuj z różnymi tematami**

---

## 💡 Pro tipy

### 1. Dobry temat = dobry artykuł

✅ **Dobre tematy:**
- "Jak zoptymalizować wydajność React aplikacji"
- "5 strategii content marketingu dla SaaS"
- "Minimalizm cyfrowy - 30 dniowe wyzwanie"

❌ **Słabe tematy:**
- "React" (zbyt ogólne)
- "Marketing" (zbyt szerokie)
- "Wszystko o programowaniu" (niemożliwe do pokrycia)

### 2. Użyj kontekstu

```python
additional_context = """
- Grupa docelowa: początkujący programiści
- Ton: przyjazny i edukacyjny
- Uwzględnij: praktyczne przykłady z GitHub
- Długość: około 1500 słów
- Unikaj: zaawansowanego żargonu
"""
```

### 3. Dostosuj kryteria audytu

Im bardziej szczegółowe kryteria, tym lepszy końcowy artykuł!

### 4. Eksperymentuj z modelami

```python
agent = BlogAgent()
agent.model = "claude-opus-4-20250514"  # Dla najwyższej jakości
```

---

**Masz pytania?** Sprawdź pełną dokumentację w `README.md`

**Gotowy?** Uruchom `python3 examples.py` i wybierz tryb interaktywny!
