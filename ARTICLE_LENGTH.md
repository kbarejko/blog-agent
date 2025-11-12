# Konfiguracja długości artykułu

## 📏 Jak działa długość artykułu

Długość artykułu jest kontrolowana na trzech poziomach:

### 1. Długość pojedynczej sekcji

**Plik:** `blog_agent/config/workflow.yaml`

```yaml
review:
  min_words: 300      # Minimum słów na sekcję
  max_words: 400      # Maximum słów na sekcję
  tolerance_percent: 10  # ±10% elastyczność na limity
```

**Jak to działa:**
- Każda sekcja artykułu jest sprawdzana przez AI
- System dąży do 300-400 słów na sekcję
- Tolerancja 10% oznacza akceptowalny zakres: 270-440 słów

### 2. Długość całkowita artykułu (szacowana)

**Obliczana automatycznie:**
```python
estimated_word_count = liczba_sekcji × 350
```

**Przykład:**
- 10 sekcji → ~3500 słów
- 5 sekcji → ~1750 słów
- 15 sekcji → ~5250 słów

**Gdzie to zmienić:**
- `blog_agent/core/workflow/steps/step_02_outline.py:314`
- `blog_agent/core/workflow/engine.py:208`

### 3. Faktyczna długość (po generacji)

Zliczana po utworzeniu `draft.md`:
- System zlicza wszystkie słowa w artykule
- Wyświetlane jako: "Total words: X"

## 🎯 Jak zmienić długość artykułu

### Opcja 1: Zmień długość sekcji (globalnie)

Edytuj `blog_agent/config/workflow.yaml`:

```yaml
review:
  min_words: 400      # Dłuższe sekcje
  max_words: 600      # Dłuższe sekcje
  tolerance_percent: 10
```

**Efekt:**
- Wszystkie artykuły będą miały dłuższe sekcje
- 10 sekcji × 500 słów = ~5000 słów całkowity artykuł

### Opcja 2: Zmień liczbę sekcji (per artykuł)

**Podczas tworzenia outline:**
- AI generuje strukturę z X sekcjami
- Możesz ręcznie edytować `outline.md` przed generacją

**Przykład - chcesz krótszy artykuł:**
1. Wygeneruj outline:
   ```bash
   python -m blog_agent create --config path/config.yaml --only outline
   ```

2. Edytuj `outline.md` - usuń niepotrzebne sekcje

3. Kontynuuj generację:
   ```bash
   python -m blog_agent create --config path/config.yaml --skip outline
   ```

### Opcja 3: Dodaj target_word_count do config.yaml (per artykuł) ✅

**✅ ZAIMPLEMENTOWANE**

```yaml
# artykuly/ecommerce/seo/config.yaml
title: "SEO w e-commerce"
target_audience: "Właściciele sklepów"
tone: "ekspercki, ale naturalny"
target_word_count: 2000  # Docelowa długość artykułu
```

System automatycznie:
- Informuje AI o docelowej długości podczas generowania outline
- Oblicza ile sekcji wygenerować (np. 2000 słów → 5-6 sekcji)
- Oblicza jak długa powinna być każda sekcja
- Przekazuje tę informację do AI podczas pisania każdej sekcji

**Przykład:**
```bash
# config.yaml z target_word_count: 2000
python -m blog_agent create --config artykuly/example/config.yaml

# System wyświetli:
# 📏 Target: 2000 words → 5 sections × 340 words/section
```

## 📊 Przykłady długości

### Artykuł krótki (~2000 słów)
```yaml
review:
  min_words: 300
  max_words: 400
```
→ 5-6 sekcji × 350 = ~1750-2100 słów

### Artykuł standardowy (~3500 słów)
```yaml
review:
  min_words: 300
  max_words: 400
```
→ 10 sekcji × 350 = ~3500 słów

### Artykuł długi (~5000 słów)
```yaml
review:
  min_words: 400
  max_words: 600
```
→ 10 sekcji × 500 = ~5000 słów

### Artykuł bardzo długi (~7000 słów)
```yaml
review:
  min_words: 500
  max_words: 700
```
→ 12 sekcji × 600 = ~7200 słów

## 🔍 Artykuły silosowe (specjalne)

Artykuły silosowe powinny być **krótsze** niż zwykłe artykuły:

```yaml
# Zalecane dla silosów
review:
  min_words: 200      # Krótsze sekcje
  max_words: 300      # Krótsze sekcje
```

**Dlaczego krótsze?**
- Są przeglądem, nie szczegółowym przewodnikiem
- Linkują do artykułów szczegółowych
- Cel: 1500-2500 słów całkowity

**Implementacja:**
- Można dodać osobny `workflow_silo.yaml` z innymi limitami
- Lub automatycznie wykrywać silos i stosować inne limity

## 💡 Porady

1. **Nie rób zbyt długich sekcji** - czytelność spada po ~500 słowach
2. **Lepiej więcej krótkich sekcji** niż mało długich
3. **FAQ i Checklist** - dodają 200-500 słów
4. **Artykuły silosowe** - zawsze krótsze (1500-2500 słów)
5. **Artykuły szczegółowe** - mogą być długie (3000-5000 słów)

## 🛠️ Planowane ulepszenia

- [ ] `target_word_count` w config.yaml artykułu
- [ ] Automatyczne obliczanie liczby sekcji na podstawie target
- [ ] Osobne limity dla artykułów silosowych
- [ ] Adaptacyjna długość sekcji (pierwsze dłuższe, ostatnie krótsze)
