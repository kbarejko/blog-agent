# 🔗 Linkowanie wewnętrzne - Internal linking

**Zadanie:**
Zidentyfikuj powiązane artykuły w strukturze bloga i zaplanuj internal linking strategy dla bieżącego artykułu.

## 🔖 Dane wejściowe
- **Tytuł artykułu:** `{{TYTUL_ARTYKULU}}`
- **Konspekt artykułu:** `{{KONSPEKT_TRESC}}`
- **Ścieżka artykułu:** `{{ARTICLE_PATH}}` (np. `artykuly/ecommerce/operacje/bezpieczenstwo-i-rodo`)
- **Seria:** `{{SERIA}}` (np. `ecommerce`)
- **Silos:** `{{SILOS}}` (np. `operacje`)
- **Dostępne artykuły:** `{{AVAILABLE_ARTICLES}}` (lista artykułów w strukturze z tytułami i ścieżkami)

## 🎯 Cel

Stwórz strategię internal linking która:
1. **Wzmacnia SEO** - contextual links z naturalnym anchor text
2. **Pomaga czytelnikowi** - sugeruje wartościowe materiały powiązane tematycznie
3. **Buduje silosy** - linkuje w obrębie serii/silosu + cross-linking między silosami

## ✍️ Proces

### KROK 1: Analiza i wybór artykułów (5-8 artykułów)

Przeanalizuj dostępne artykuły i wybierz **5-8 najbardziej powiązanych** na podstawie:

**Kryteria wyboru:**
1. **Tematyczna bliskość** - czy artykuł rozszerza/uzupełnia temat?
2. **Seria/silos** - priorytet dla artykułów z tej samej serii
3. **Komplementarność** - czy artykuł odpowiada na pytanie powstające przy czytaniu?
4. **Kontekst użytkownika** - co czytelnik może chcieć przeczytać dalej?

**Strategia wyboru:**
- **60% z tego samego silosu** - głębsze zagłębienie w temat
- **40% z innych silosów tej serii** - szerszy kontekst
- Przykład dla `ecommerce/operacje/bezpieczenstwo-i-rodo`:
  - 3-4 artykuły z `operacje/` (np. integracje-erp, kpi-ecommerce)
  - 2-3 artykuły z `platformy/` lub `platnosci-logistyka/` (np. wybor-platformy, platnosci-online)

**NIE linkuj do:**
- Artykułów z innych serii (jeśli `{{SERIA}}` = ecommerce, NIE linkuj do `saas/*`)
- Artykułów bardzo odległych tematycznie
- Artykułów konkurencyjnych (pokrywających dokładnie ten sam temat)

### KROK 2: Podział na contextual vs sekcja końcowa

Z wybranych 5-8 artykułów:
- **2-4 artykuły:** oznacz jako `contextual: true` (użyte w treści)
- **Pozostałe (3-5):** oznacz jako `contextual: false` (sekcja końcowa)

**Wybór do contextual linking:**
- Artykuły najsilniej powiązane z konkretnymi sekcjami konspektu
- Artykuły które można naturalnie wspomnieć w treści
- Priorytet: artykuły z tego samego silosu

**Przykład:**
Dla artykułu "Bezpieczeństwo i RODO":
- Contextual: "Integracje ERP" (bo będzie sekcja o systemach), "Certyfikaty SSL" (bezpośrednio związane)
- Sekcja końcowa: "Wybór platformy", "Polityka cookies", "Audyt SEO"

### KROK 3: Zaplanuj anchor text i umiejscowienie

Dla **contextual links (2-4)**:
```json
{
  "slug": "../operacje/integracje-erp-wms-crm",
  "title": "Integracje ERP, WMS i CRM w e-commerce",
  "contextual": true,
  "suggested_anchor": "integracje z systemami ERP",
  "suggested_section": "Sekcja o systemach / automatyzacji",
  "context_hint": "Wstaw gdy omawiasz automatyzację procesów lub systemy backendowe"
}
```

**Zasady anchor text (naturalny):**
- ❌ NIE: pełny tytuł artykułu - "przeczytaj artykuł Integracje ERP, WMS i CRM w e-commerce"
- ✅ TAK: naturalny anchor - "musisz uwzględnić [integracje z systemami ERP](link)"
- ✅ TAK: skrócony - "więcej o [integracjach ERP](link)"
- ✅ TAK: keyword-rich - "[automatyzacja procesów w e-commerce](link)"

**Długość anchor:** 2-6 słów (sweet spot dla SEO)

Dla **sekcji końcowej (3-5)**:
```json
{
  "slug": "../platformy/wybor-platformy",
  "title": "Jak wybrać platformę e-commerce",
  "contextual": false,
  "description": "Szczegółowy przewodnik po wyborze najlepszej platformy dla Twojego sklepu",
  "silos": "platformy"
}
```

## 📋 Format Output (JSON)

Zwróć JSON z następującą strukturą:

```json
{
  "related_articles": [
    {
      "slug": "../operacje/integracje-erp-wms-crm",
      "title": "Integracje ERP, WMS i CRM w e-commerce",
      "contextual": true,
      "suggested_anchor": "integracje z systemami ERP",
      "suggested_section": "Sekcja: Automatyzacja procesów bezpieczeństwa",
      "context_hint": "Wstaw gdy omawiasz automatyczne backup'y lub zarządzanie danymi"
    },
    {
      "slug": "../operacje/kpi-ecommerce-gmv-aov-ltv",
      "title": "KPI w e-commerce: GMV, AOV, LTV",
      "contextual": true,
      "suggested_anchor": "kluczowe metryki e-commerce",
      "suggested_section": "Sekcja: Monitoring zgodności RODO",
      "context_hint": "Wstaw gdy mówisz o mierzeniu skuteczności procesów bezpieczeństwa"
    },
    {
      "slug": "../platnosci-logistyka/platnosci-online-polska",
      "title": "Płatności online w Polsce - kompletny przewodnik",
      "contextual": true,
      "suggested_anchor": "bezpieczeństwo płatności online",
      "suggested_section": "Sekcja: Certyfikaty SSL/TLS",
      "context_hint": "Wstaw przy omawianiu szyfrowania danych płatności"
    },
    {
      "slug": "../platformy/wybor-platformy",
      "title": "Jak wybrać platformę e-commerce",
      "contextual": false,
      "description": "Szczegółowy przewodnik po wyborze platformy z uwzględnieniem bezpieczeństwa i zgodności RODO",
      "silos": "platformy"
    },
    {
      "slug": "../seo/tresci-produktowe-seo",
      "title": "Treści produktowe a SEO",
      "contextual": false,
      "description": "Jak pisać opisy produktów które sprzedają i są zgodne z wymogami prawnymi",
      "silos": "seo"
    },
    {
      "slug": "../operacje/automatyzacja-ecommerce-roi",
      "title": "Automatyzacja e-commerce - ROI i zwrot z inwestycji",
      "contextual": false,
      "description": "Praktyczne wdrożenie automatyzacji procesów bezpieczeństwa i compliance",
      "silos": "operacje"
    }
  ],
  "summary": {
    "total": 6,
    "contextual": 3,
    "end_section": 3,
    "silos_distribution": {
      "operacje": 3,
      "platformy": 1,
      "platnosci-logistyka": 1,
      "seo": 1
    }
  }
}
```

## 🎨 Przykład sekcji końcowej (dla humanizacji)

Na podstawie `contextual: false` artykułów, wygeneruj sekcję:

```markdown
## Powiązane artykuły

### Platformy
- **[Jak wybrać platformę e-commerce](../platformy/wybor-platformy)** - szczegółowy przewodnik po wyborze platformy z uwzględnieniem bezpieczeństwa i zgodności RODO

### SEO i Optymalizacja
- **[Treści produktowe a SEO](../seo/tresci-produktowe-seo)** - jak pisać opisy produktów które sprzedają i są zgodne z wymogami prawnymi

### Operacje
- **[Automatyzacja e-commerce - ROI](../operacje/automatyzacja-ecommerce-roi)** - praktyczne wdrożenie automatyzacji procesów bezpieczeństwa i compliance
```

## ⚠️ Ważne zasady

### DO:
- ✅ Wybieraj artykuły które **realnie pomagają** czytelnikowi
- ✅ Anchor text naturalny, wpleciony w kontekst zdania
- ✅ Priorytet dla artykułów z tego samego silosu
- ✅ Opisy w sekcji końcowej krótkie ale wartościowe (1 zdanie)
- ✅ Grupuj po silosach w sekcji końcowej
- ✅ Link tylko do artykułów które **istnieją** w `{{AVAILABLE_ARTICLES}}`

### DON'T:
- ❌ NIE linkuj do nieistniejących artykułów
- ❌ NIE używaj "kliknij tutaj", "przeczytaj więcej" jako anchor
- ❌ NIE linkuj do artykułów z innych serii (ecommerce → saas)
- ❌ NIE przepełniaj treści linkami (max 4 contextual)
- ❌ NIE duplikuj linków (jeśli w treści, nie dawaj na końcu)
- ❌ NIE linkuj do bardzo odległych tematów
- ❌ NIE używaj pełnych tytułów jako anchor text

## 📊 Quality checklist

Przed zwróceniem wyniku sprawdź:
- [ ] Wybrano 5-8 artykułów (nie mniej, nie więcej)
- [ ] 2-4 oznaczone jako contextual
- [ ] 3-5 oznaczone jako end_section
- [ ] Wszystkie slug'i prowadzą do artykułów z `{{AVAILABLE_ARTICLES}}`
- [ ] Anchor text naturalny (2-6 słów)
- [ ] Opisy w sekcji końcowej krótkie (1 zdanie)
- [ ] Minimum 60% z tego samego silosu
- [ ] Każdy link ma wartość dla czytelnika (nie wypełniacz)
- [ ] Brak duplikatów między contextual a end_section
- [ ] Sekcja końcowa pogrupowana po silosach

---

**Output:** JSON z listą artykułów + sugestiami anchor text i umiejscowienia
