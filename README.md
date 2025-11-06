# 🤖 Blog Agent - Automatyczny Generator Artykułów

Agent AI do automatycznego tworzenia wysokiej jakości artykułów blogowych z wbudowanym systemem audytu i poprawy treści.

## 📋 Jak to działa?

Agent działa w kilku etapach:

1. **Tworzenie konspektu** - Na podstawie tematu generuje szczegółowy konspekt z sekcjami
2. **Pisanie sekcji** - Dla każdej sekcji tworzy wartościową, dobrze sformatowaną treść
3. **Audyt jakości** - Każda sekcja jest audytowana według zdefiniowanych kryteriów
4. **Poprawa treści** - Sekcje, które nie przejdą audytu, są automatycznie poprawiane
5. **Finalny artykuł** - Wszystkie sekcje są łączone w kompletny artykuł Markdown

## 🚀 Instalacja

### Wymagania

- Python 3.8+
- Klucz API do Claude (Anthropic)

### Kroki instalacji

```bash
# 1. Zainstaluj zależności
pip install -r requirements.txt

# 2. Ustaw klucz API
export ANTHROPIC_API_KEY='twój-klucz-api'

# 3. Uruchom agenta
python blog_agent.py
```

## 📖 Użycie

### Podstawowe użycie

```python
from blog_agent import BlogAgent

# Inicjalizacja agenta
agent = BlogAgent()

# Tworzenie artykułu
article = agent.create_article(
    topic="Twój temat artykułu"
)

# Zapisanie do pliku
agent.save_article(article, "moj_artykul.md")
```

### Zaawansowane użycie

```python
# Z dodatkowym kontekstem
article = agent.create_article(
    topic="Jak AI zmienia marketing",
    additional_context="""
    Artykuł dla marketerów B2B.
    Skup się na ROI i konkretnych metrykach.
    Uwzględnij case studies z branży tech.
    """
)

# Z własnymi kryteriami audytu
custom_criteria = {
    "SEO": "Czy sekcja zawiera naturalne słowa kluczowe?",
    "Data-driven": "Czy użyto konkretnych liczb i statystyk?",
    "Storytelling": "Czy tekst opowiada historię?",
    "Actionable": "Czy czytelnik wie co zrobić po przeczytaniu?"
}

article = agent.create_article(
    topic="Twój temat",
    audit_criteria=custom_criteria,
    max_improvement_attempts=3  # Więcej prób poprawy
)
```

### Modyfikacja skryptu dla własnych potrzeb

Otwórz `blog_agent.py` i zmodyfikuj funkcję `main()`:

```python
def main():
    agent = BlogAgent()
    
    # TUTAJ zmień temat
    topic = "Twój temat artykułu"
    
    # TUTAJ dodaj kontekst
    additional_context = """
    Twoje wskazówki dla agenta...
    """
    
    # TUTAJ zdefiniuj kryteria audytu
    custom_audit_criteria = {
        "Kryterium 1": "Opis kryterium...",
        "Kryterium 2": "Opis kryterium..."
    }
    
    article = agent.create_article(
        topic=topic,
        additional_context=additional_context,
        audit_criteria=custom_audit_criteria
    )
    
    agent.save_article(article)
```

## ⚙️ Konfiguracja

### Domyślne kryteria audytu

```python
{
    "Wartość merytoryczna": "Czy sekcja dostarcza konkretnej, wartościowej wiedzy?",
    "Czytelność": "Czy tekst jest łatwy do czytania i dobrze sformatowany?",
    "Spójność": "Czy sekcja pasuje do całości artykułu?",
    "Angażowanie": "Czy treść jest interesująca i trzyma uwagę czytelnika?",
    "Kompletność": "Czy wszystkie kluczowe punkty zostały omówione?"
}
```

### Parametry agenta

- `max_improvement_attempts` (domyślnie: 2) - Maksymalna liczba prób poprawy sekcji
- `model` (domyślnie: "claude-sonnet-4-20250514") - Model Claude do użycia

### Próg zatwierdzenia sekcji

Sekcja jest automatycznie zatwierdzana, jeśli otrzyma ocenę >= 7.0/10 w audycie.

## 📁 Struktura projektu

```
.
├── blog_agent.py          # Główny skrypt agenta
├── requirements.txt       # Zależności Python
└── README.md             # Dokumentacja
```

## 🎯 Przykłady tematów

Agent radzi sobie dobrze z różnymi tematami:

- **Technologia**: "Jak blockchain zmienia e-commerce"
- **Marketing**: "10 strategii content marketingu na 2025"
- **Lifestyle**: "Minimalizm cyfrowy - praktyczny przewodnik"
- **Business**: "Jak zbudować zdalny zespół w startupie"
- **Edukacja**: "Efektywne metody nauki języków obcych"

## 📊 Proces tworzenia

```
📋 Konspekt
    ↓
✍️  Pisanie sekcji 1
    ↓
🔍 Audyt sekcji 1
    ↓ (jeśli niezatwierdzona)
🔧 Poprawa sekcji 1
    ↓
✍️  Pisanie sekcji 2
    ↓
🔍 Audyt sekcji 2
    ↓
... (powtarzaj dla każdej sekcji)
    ↓
🎉 Gotowy artykuł!
```

## 💡 Wskazówki

### Jak napisać dobry temat?

- ✅ "Jak AI zmienia tworzenie treści w marketingu B2B"
- ✅ "5 strategii automatyzacji sprzedaży dla małych firm"
- ❌ "AI" (zbyt ogólne)
- ❌ "Wszystko o marketingu" (zbyt szerokie)

### Jak wykorzystać dodatkowy kontekst?

```python
additional_context = """
- Grupa docelowa: przedsiębiorcy e-commerce
- Ton: profesjonalny, ale przystępny
- Długość: około 2000 słów
- Uwzględnij: konkretne narzędzia i ich ceny
- Unikaj: zbyt technicznego żargonu
"""
```

### Jak dostosować kryteria audytu?

Stwórz kryteria pasujące do typu treści:

**Blog techniczny:**
```python
{
    "Precyzja techniczna": "Czy informacje techniczne są dokładne?",
    "Przykłady kodu": "Czy użyto praktycznych przykładów kodu?",
    "Best practices": "Czy wskazano najlepsze praktyki?"
}
```

**Blog lifestylowy:**
```python
{
    "Osobisty ton": "Czy tekst jest ciepły i osobisty?",
    "Relatable": "Czy czytelnik może się z tym utożsamić?",
    "Inspiracja": "Czy tekst inspiruje do działania?"
}
```

## 🔧 Rozwiązywanie problemów

### "Brak klucza API"
```bash
export ANTHROPIC_API_KEY='sk-ant-api...'
```

### "Nie udało się sparsować JSON"
Agent automatycznie powtórzy próbę lub użyje domyślnej struktury.

### Artykuł jest za krótki/długi
Zmodyfikuj prompt w metodzie `write_section()` i zmień zakres słów (domyślnie: 300-500).

### Sekcje nie przechodzą audytu
- Zwiększ `max_improvement_attempts`
- Złagodź kryteria audytu
- Dodaj więcej kontekstu w `additional_context`

## 📝 Format wyjściowy

Artykuł jest zapisywany w formacie Markdown:

```markdown
# Tytuł Artykułu

Wprowadzenie do artykułu...

## Pierwsza Sekcja

Treść pierwszej sekcji...

## Druga Sekcja

Treść drugiej sekcji...

...
```

Gotowy do wklejenia na:
- WordPress
- Medium
- Ghost
- Jekyll/Hugo
- Dowolną platformę blogową obsługującą Markdown

## 🚀 Możliwe rozszerzenia

1. **Generowanie obrazów** - Integracja z DALL-E lub Midjourney
2. **SEO metadata** - Automatyczne tworzenie meta opisów i tagów
3. **Multi-language** - Tłumaczenie artykułów
4. **A/B testing** - Generowanie wielu wariantów tytułów
5. **Publikacja** - Bezpośrednia publikacja przez API WordPress/Medium

## 📄 Licencja

MIT License - Możesz swobodnie używać i modyfikować kod.

## 🤝 Wsparcie

W razie problemów sprawdź:
- [Dokumentacja Anthropic API](https://docs.anthropic.com/)
- Logi w konsoli (agent wyświetla szczegółowe informacje o procesie)

---

Stworzono z ❤️ przy użyciu Claude AI
