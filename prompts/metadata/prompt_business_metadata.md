# 💼 Business Metadata - Metadane biznesowe artykułu

**Zadanie:**
Przeanalizuj gotowy artykuł i wygeneruj metadane biznesowe pomocne dla przedsiębiorców w ocenie czy artykuł jest dla nich relevantny oraz w podejmowaniu decyzji inwestycyjnych.

## 🔖 Dane wejściowe
- **Tytuł artykułu:** `{{TYTUL_ARTYKULU}}`
- **Treść artykułu:** `{{ARTICLE_CONTENT}}` (finalna wersja po humanizacji)
- **Konspekt:** `{{KONSPEKT_TRESC}}`
- **Seria:** `{{SERIA}}` (np. `ecommerce`, `saas`, `ai`)
- **Silos:** `{{SILOS}}` (np. `platformy`, `operacje`, `seo`)

## 🎯 Cel

Wygeneruj metadane które pomogą przedsiębiorcy szybko ocenić:
1. **Czy artykuł jest dla mnie?** - rozmiar firmy, branża, faza projektu
2. **Ile to kosztuje?** - orientacyjny budżet, breakdown kosztów
3. **Ile to zajmie?** - czas wdrożenia, fazy
4. **Jak trudne?** - złożoność techniczna i organizacyjna
5. **Kto potrzebny?** - wielkość i struktura zespołu
6. **Jaki ROI?** - zwrot z inwestycji (jeśli applicable)

## 📋 Struktura metadanych

### 1. 🏢 Target Business (dla kogo artykuł)

**Rozmiar firmy:**
- `startup` - do 2 lat działania, <20 osób, eksperymentowanie
- `scale-up` - 2-7 lat, 20-100 osób, skalowanie
- `enterprise` - 7+ lat, 100+ osób, optymalizacja i stabilność

**Wybierz 1-2 najbardziej pasujące.**

**Przykłady:**
- Artykuł o "Jak wybrać pierwszą platformę e-commerce" → `["startup"]`
- Artykuł o "Headless architecture" → `["scale-up", "enterprise"]`
- Artykuł o "Bezpieczeństwo RODO" → `["startup", "scale-up", "enterprise"]` (wszystkie)

### 2. 🏭 Industry (branża)

Wybierz branże dla których artykuł jest najbardziej relevantny:
- `ecommerce` - sklepy online, marketplace
- `saas` - oprogramowanie jako usługa
- `fintech` - finanse, płatności, bankowość
- `healthtech` - medycyna, zdrowie
- `edtech` - edukacja
- `services` - usługi profesjonalne (agencje, consulting)
- `manufacturing` - produkcja, B2B
- `retail` - retail fizyczny + online
- `universal` - artykuł uniwersalny dla wszystkich branż

**Wybierz 1-3 najbardziej pasujące.**

### 3. 📅 Project Phase (faza projektu)

W jakiej fazie jest przedsiębiorca któremu artykuł pomoże najbardziej:

- `planowanie` - researching, planning, budowanie business case
- `wdrożenie` - aktywne wdrażanie, budowanie, development
- `optymalizacja` - improving, scaling, refactoring istniejących rozwiązań
- `migracja` - zmiana platformy/systemu/architektury

**Wybierz 1-2 fazy.**

### 4. 💰 Investment (inwestycja)

**Level:**
- `low` - do 20k PLN
- `medium` - 20k-100k PLN
- `high` - 100k-500k PLN
- `very_high` - 500k+ PLN
- `variable` - zależy od skali (np. koszt licencji SaaS)
- `none` - artykuł teoretyczny, brak konkretnych kosztów

**Range:**
Podaj orientacyjny zakres w PLN (string).
- Przykład: `"50-150k PLN"`
- Jeśli variable: `"od 500 PLN/msc (startup) do 5k+ PLN/msc (enterprise)"`
- Jeśli none: `null`

**Breakdown (opcjonalnie):**
Jeśli artykuł omawia konkretną inwestycję (np. wdrożenie platformy), podaj breakdown:
```yaml
breakdown:
  software_licenses: "20-40k PLN"  # licencje, subskrypcje
  development: "50-80k PLN"  # development, customizacja
  integration: "30-50k PLN"  # integracje z ERP, CRM, etc.
  infrastructure: "10-20k PLN"  # hosting, CDN, SSL
  consulting: "15-30k PLN"  # konsultacje, projektowanie
```

**Jeśli artykuł nie omawia kosztów bezpośrednio:**
```yaml
investment:
  level: "none"
  range: null
  breakdown: null
```

### 5. ⏱️ Timeline (czas realizacji)

**Estimate:**
Orientacyjny czas wdrożenia/realizacji (string).
- Przykład: `"2-3 miesiące"`
- Przykład: `"2-4 tygodnie"`
- Jeśli brak: `null`

**Phases (opcjonalnie):**
Jeśli artykuł omawia proces wdrożeniowy, podaj fazy:
```yaml
phases:
  planning: "2-3 tygodnie"
  design: "3-4 tygodnie"
  development: "6-8 tygodni"
  testing: "2-3 tygodnie"
  deployment: "1-2 tygodnie"
```

**Jeśli artykuł nie omawia timelines:**
```yaml
timeline:
  estimate: null
  phases: null
```

### 6. 🧩 Complexity (złożoność)

**Technical:**
- `low` - prosty setup, narzędzia no-code/low-code, standardowe rozwiązania
- `medium` - wymaga developera, standardowe technologie, dobra dokumentacja
- `high` - wymaga doświadczonego zespołu, custom solutions, architektura

**Organizational:**
- `low` - decyzja 1-2 osób, szybkie wdrożenie, minimalny change management
- `medium` - kilka działów, koordynacja, szkolenia
- `high` - cała organizacja, zmiana procesów, długi change management

**Przykład:**
- Artykuł o Shopify → `technical: low, organizational: low`
- Artykuł o headless architecture → `technical: high, organizational: medium`
- Artykuł o migracji enterprise platform → `technical: high, organizational: high`

### 7. 👥 Team Requirements (wymagania zespołowe)

**Size:**
Orientacyjna wielkość zespołu potrzebna do realizacji (string).
- Przykład: `"1-2 osoby"`
- Przykład: `"zespół 5-7 osób"`
- Jeśli nie applicable: `null`

**Roles (lista):**
Jakie role/kompetencje potrzebne:
```yaml
roles:
  - "Project Manager"
  - "Backend Developer (Node.js/Python)"
  - "Frontend Developer (React)"
  - "DevOps Engineer"
  - "UX/UI Designer (opcjonalnie)"
```

**Jeśli artykuł nie wymaga zespołu (teoretyczny):**
```yaml
team_requirements:
  size: null
  roles: null
```

### 8. 📈 ROI (zwrot z inwestycji) - OPCJONALNIE

**Tylko jeśli artykuł omawia konkretne oszczędności/zyski.**

```yaml
roi:
  breakeven: "6-12 miesięcy"  # czas zwrotu inwestycji
  annual_savings: "80-150k PLN"  # roczne oszczędności (jeśli applicable)
  annual_revenue_increase: "200-500k PLN"  # wzrost przychodów (jeśli applicable)
  three_year_roi: "250-400%"  # ROI po 3 latach
  key_factors:  # co najbardziej wpływa na ROI
    - "Automatyzacja procesów magazynowych (50% oszczędności czasu)"
    - "Redukcja błędów manualnych (20% mniej zwrotów)"
    - "Skalowalność bez wzrostu kosztów stałych"
```

**Jeśli artykuł NIE omawia ROI:**
```yaml
roi: null
```

## 📋 Format Output (YAML)

```yaml
business_metadata:
  # Dla kogo
  target_business:
    - "startup"
    - "scale-up"

  # Branża
  industry:
    - "ecommerce"
    - "retail"

  # Faza projektu
  project_phase:
    - "planowanie"
    - "wdrożenie"

  # Inwestycja
  investment:
    level: "medium"
    range: "50-150k PLN"
    breakdown:
      software_licenses: "20-40k PLN"
      development: "50-80k PLN"
      integration: "30-50k PLN"
      infrastructure: "10-15k PLN"
      consulting: "15-25k PLN"

  # Czas
  timeline:
    estimate: "2-3 miesiące"
    phases:
      planning: "2-3 tygodnie"
      design: "3-4 tygodnie"
      development: "6-8 tygodni"
      testing: "2-3 tygodnie"
      deployment: "1-2 tygodnie"

  # Złożoność
  complexity:
    technical: "medium"
    organizational: "low"

  # Zespół
  team_requirements:
    size: "3-5 osób"
    roles:
      - "Project Manager"
      - "Backend Developer (PHP/Node.js)"
      - "Frontend Developer (React/Vue)"
      - "UX Designer (opcjonalnie)"

  # ROI (opcjonalnie)
  roi:
    breakeven: "8-12 miesięcy"
    annual_savings: "100-150k PLN"
    key_factors:
      - "Automatyzacja obsługi zamówień (60% mniej czasu)"
      - "Integracja z ERP (eliminacja podwójnego wprowadzania danych)"
      - "Self-service dla klientów (20% mniej zapytań do obsługi)"
```

## 🎨 Przykłady dla różnych typów artykułów

### Przykład 1: Artykuł praktyczny (wdrożenie)
**Tytuł:** "Jak wybrać platformę e-commerce dla sklepu B2B"

```yaml
business_metadata:
  target_business:
    - "startup"
    - "scale-up"
  industry:
    - "ecommerce"
    - "manufacturing"
    - "services"
  project_phase:
    - "planowanie"
    - "wdrożenie"
  investment:
    level: "medium"
    range: "60-200k PLN"
    breakdown:
      platform_license: "20-50k PLN/rok"
      development: "40-100k PLN"
      integration: "30-80k PLN"
      infrastructure: "10-20k PLN/rok"
  timeline:
    estimate: "3-4 miesiące"
    phases:
      requirements: "2-3 tygodnie"
      platform_selection: "2-3 tygodnie"
      development: "8-10 tygodni"
      testing: "3-4 tygodnie"
      deployment: "1-2 tygodnie"
  complexity:
    technical: "medium"
    organizational: "medium"
  team_requirements:
    size: "4-6 osób"
    roles:
      - "Project Manager"
      - "Backend Developer (PHP/Node.js)"
      - "Frontend Developer"
      - "Integration Specialist (ERP/CRM)"
      - "UX Designer"
  roi:
    breakeven: "12-18 miesięcy"
    annual_savings: "150-300k PLN"
    key_factors:
      - "Automatyzacja obsługi zamówień hurtowych (40% mniej czasu)"
      - "Personalizacja cenników dla klientów B2B (15% wzrost konwersji)"
      - "Integracja z ERP (eliminacja błędów w stanach magazynowych)"
```

### Przykład 2: Artykuł teoretyczny/edukacyjny
**Tytuł:** "Czym jest headless architecture i czy jest dla Ciebie?"

```yaml
business_metadata:
  target_business:
    - "scale-up"
    - "enterprise"
  industry:
    - "universal"
  project_phase:
    - "planowanie"
    - "optymalizacja"
  investment:
    level: "high"
    range: "150-500k PLN"
    breakdown: null  # artykuł nie podaje konkretnych kosztów
  timeline:
    estimate: "4-6 miesięcy"
    phases: null
  complexity:
    technical: "high"
    organizational: "medium"
  team_requirements:
    size: "6-10 osób"
    roles:
      - "Solutions Architect"
      - "Backend Developer Team (3-4 osoby)"
      - "Frontend Developer Team (2-3 osoby)"
      - "DevOps Engineer"
      - "QA Engineer"
  roi: null  # artykuł nie omawia ROI
```

### Przykład 3: Artykuł o compliance/legal
**Tytuł:** "Bezpieczeństwo i RODO w e-commerce - kompletny przewodnik"

```yaml
business_metadata:
  target_business:
    - "startup"
    - "scale-up"
    - "enterprise"
  industry:
    - "ecommerce"
    - "universal"
  project_phase:
    - "wdrożenie"
    - "optymalizacja"
  investment:
    level: "low"
    range: "5-30k PLN"
    breakdown:
      ssl_certificate: "0-2k PLN/rok (Let's Encrypt free)"
      privacy_policy_legal: "2-5k PLN"
      security_audit: "3-10k PLN"
      backup_solution: "2-5k PLN/rok"
      consulting: "5-15k PLN"
  timeline:
    estimate: "3-6 tygodni"
    phases:
      audit: "1 tydzień"
      implementation: "2-3 tygodnie"
      documentation: "1-2 tygodnie"
  complexity:
    technical: "low"
    organizational: "medium"
  team_requirements:
    size: "2-3 osoby"
    roles:
      - "RODO Officer / Legal Consultant"
      - "Developer (implementacja techniczna)"
      - "Project Manager"
  roi:
    breakeven: "natychmiastowy (unikanie kar)"
    annual_savings: null
    key_factors:
      - "Uniknięcie kar RODO (do 4% przychodu rocznego)"
      - "Zwiększenie zaufania klientów (5-10% wzrost konwersji)"
      - "Compliance gotowość na audyty"
```

### Przykład 4: Artykuł o optymalizacji
**Tytuł:** "Core Web Vitals - jak przyspieszyć sklep e-commerce"

```yaml
business_metadata:
  target_business:
    - "startup"
    - "scale-up"
  industry:
    - "ecommerce"
    - "universal"
  project_phase:
    - "optymalizacja"
  investment:
    level: "low"
    range: "10-40k PLN"
    breakdown:
      cdn_service: "2-5k PLN/rok"
      image_optimization: "1-3k PLN (tooling)"
      development_work: "10-30k PLN"
      performance_monitoring: "2-5k PLN/rok"
  timeline:
    estimate: "4-8 tygodni"
    phases:
      audit: "1 tydzień"
      optimization: "3-5 tygodni"
      testing: "1-2 tygodnie"
  complexity:
    technical: "medium"
    organizational: "low"
  team_requirements:
    size: "2-3 osoby"
    roles:
      - "Frontend Developer (performance expert)"
      - "DevOps Engineer (CDN, caching)"
      - "QA Engineer (testing)"
  roi:
    breakeven: "2-4 miesiące"
    annual_revenue_increase: "50-200k PLN"
    key_factors:
      - "Każda sekunda ładowania = 7% mniej konwersji (industry benchmark)"
      - "Core Web Vitals jako ranking factor w Google (więcej organic traffic)"
      - "Lepsza UX = wyższy AOV (średnio 10-15%)"
```

## ⚠️ Ważne zasady

### DO:
- ✅ Bazuj na konkretach z artykułu (liczby, narzędzia, procesy)
- ✅ Jeśli artykuł nie podaje kosztów/timelines - użyj industry benchmarks
- ✅ Zakresy (ranges) lepsze niż konkretne liczby (50-150k lepsze niż 100k)
- ✅ ROI tylko jeśli artykuł omawia korzyści/oszczędności
- ✅ Breakdown tylko jeśli artykuł omawia poszczególne koszty
- ✅ Bądź konserwatywny z szacunkami (lepiej podać wyższe koszty niż niższe)

### DON'T:
- ❌ NIE wymyślaj kosztów jeśli artykuł ich nie omawia → `investment.level: "none"`
- ❌ NIE podawaj zbyt optymistycznych timelines (lepiej 3-4 msc niż 2-3 msc)
- ❌ NIE komplikuj - jeśli prosty temat → `complexity.technical: "low"`
- ❌ NIE dodawaj ROI jeśli artykuł nie wspomina o korzyściach biznesowych
- ❌ NIE używaj `universal` dla industry jeśli artykuł jest dla konkretnej branży

## 📊 Quality checklist

Przed zwróceniem wyniku sprawdź:
- [ ] `target_business` - 1-3 opcje (nie więcej)
- [ ] `industry` - 1-3 opcje (lub `universal` jeśli naprawdę uniwersalny)
- [ ] `project_phase` - 1-2 fazy najbardziej pasujące
- [ ] `investment.level` - zawsze wypełnione (lub `none`)
- [ ] `investment.range` - jeśli level ≠ none, podaj range
- [ ] `investment.breakdown` - tylko jeśli artykuł omawia koszty szczegółowo
- [ ] `timeline.estimate` - orientacyjny czas (lub null jeśli nie applicable)
- [ ] `complexity` - technical + organizational zawsze wypełnione
- [ ] `team_requirements` - jeśli artykuł omawia wdrożenie/projekt
- [ ] `roi` - tylko jeśli artykuł wspomina o korzyściach/oszczędnościach
- [ ] Wszystkie zakresy realistyczne (konserwatywne szacunki)

---

**Output:** YAML z business metadata → zapisz jako `business_metadata.yaml`
