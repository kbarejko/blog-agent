# Generowanie alternatywnych nagłówków SEO - Batch Processing

## Opis

Skrypty do masowego generowania alternatywnych propozycji nagłówków SEO dla wszystkich artykułów w drzewie katalogowym.

Dla każdego artykułu generują plik `headers_alternatives.md` zawierający:
- Oryginalne nagłówki H1, H2, H3
- 3-4 propozycje SEO-friendly dla każdego nagłówka
- Przynajmniej jedna propozycja long-tail (szczegółowa fraza 8-12 słów)

## Dostępne skrypty

### 1. Bash script (Linux/Mac)
```bash
./generate_headers_alternatives_all.sh [katalog]
```

**Przykłady:**
```bash
# Wszystkie artykuły
./generate_headers_alternatives_all.sh

# Tylko seria ecommerce
./generate_headers_alternatives_all.sh artykuly/ecommerce

# Tylko konkretny silos
./generate_headers_alternatives_all.sh artykuly/ecommerce/platnosci-logistyka
```

### 2. Python script (uniwersalny)
```bash
python generate_headers_alternatives_all.py [katalog]
```

**Przykłady:**
```bash
# Wszystkie artykuły
python generate_headers_alternatives_all.py

# Tylko seria ecommerce
python generate_headers_alternatives_all.py artykuly/ecommerce

# Tylko konkretny silos
python generate_headers_alternatives_all.py artykuly/ecommerce/seo
```

## Wymagania

1. **Artykuł musi mieć `article.md`** - skrypt pominie artykuły bez opublikowanej treści
2. **Virtual environment** - skrypt Bash automatycznie aktywuje `.venv`
3. **API Key** - dla provider'a AI (domyślnie Claude, fallback na ustawionego providera)

## Szacowany czas wykonania

- **1 artykuł**: ~30-60 sekund (zależy od liczby nagłówków i providera AI)
- **10 artykułów**: ~5-10 minut
- **30 artykułów**: ~15-30 minut

💡 **Tip:** Uruchamiaj w sesji screen/tmux dla dużych batch'y:
```bash
screen -S headers
./generate_headers_alternatives_all.sh
# Ctrl+A, D (detach)
# Później: screen -r headers (attach)
```

## Output

Dla każdego artykułu tworzy plik: `[katalog_artykułu]/headers_alternatives.md`

**Format pliku:**
```markdown
# Original: Tytuł artykułu

**Propozycje SEO:**
1. Krótka propozycja z keyword
2. Naturalna propozycja SEO
3. Szczegółowa propozycja long-tail opisująca dokładnie temat (LONG TAIL)
4. Wariant z liczbami lub innymi danymi

---

## Original: Nazwa sekcji

**Propozycje SEO:**
1. ...
```

## Podsumowanie wykonania

Po zakończeniu skrypt wyświetla statystyki:
```
════════════════════════════════════════
📊 Summary
════════════════════════════════════════
Total articles:    30
Successful:        27
Skipped (no article.md): 2
Failed:            1
════════════════════════════════════════
```

## Pojedynczy artykuł (bez batch)

Jeśli chcesz wygenerować dla pojedynczego artykułu:

```bash
python -m blog_agent create \
  --config artykuly/ecommerce/seo/config.yaml \
  --only headers_alternatives
```

## Włączenie w normalnym workflow

Jeśli chcesz, aby `headers_alternatives` generowały się automatycznie przy każdym nowym artykule:

1. Edytuj `blog_agent/config/workflow.yaml`
2. Zmień dla kroku `headers_alternatives`:
   ```yaml
   enabled: false  # ← zmień na true
   ```

## Troubleshooting

### Timeout errors
Zwiększ timeout w skrypcie Python (linia z `timeout=120`) lub bash (linia z `timeout 300`).

### Out of API credits
Skrypty korzystają z tego samego providera AI co reszta systemu. Sprawdź limity API.

### Memory errors
Przetwarzaj mniejsze batch'e (np. po silosie, nie całą serię naraz).

## Koszty

Szacowane koszty API (zależne od providera):
- **Claude Sonnet 4**: ~$0.01-0.03 per artykuł
- **GPT-4o**: ~$0.02-0.05 per artykuł
- **Gemini 2.5 Flash**: ~$0.001-0.005 per artykuł

Dla 30 artykułów: **~$0.30-1.50** (zależy od liczby nagłówków i wybranego modelu)
