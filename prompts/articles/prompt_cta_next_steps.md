# 🎯 CTA / Next Steps - Co dalej?

**Zadanie:**
Wygeneruj sekcję końcową "Co dalej?" która pomoże przedsiębiorcy podjąć konkretne akcje po przeczytaniu artykułu.

## 🔖 Dane wejściowe
- **Tytuł artykułu:** `{{TYTUL_ARTYKULU}}`
- **Treść artykułu:** `{{ARTICLE_CONTENT}}` (finalna wersja)
- **Business metadata:** `{{BUSINESS_METADATA}}` (investment, timeline, complexity)
- **Related articles:** `{{RELATED_ARTICLES}}` (artykuły powiązane z internal linking)
- **Seria/Silos:** `{{SERIA}}/{{SILOS}}`

## 🎯 Cel

Sekcja "Co dalej?" powinna:
1. **Pomóc zdecydować** - czy czytelnik jest gotowy do działania
2. **Dać konkretne akcje** - co zrobić w pierwszej kolejności
3. **Zaproponować wsparcie** - gdzie szukać pomocy
4. **Zachęcić do eksploracji** - related content, resources

## ✍️ Struktura sekcji

### Wariant A: Artykuł praktyczny (wdrożeniowy)

Dla artykułów typu:
- "Jak wybrać..."
- "Przewodnik wdrożenia..."
- "X kroków do..."
- Business metadata: `project_phase: ["wdrożenie"]`

```markdown
## Co dalej?

### ✅ Jeśli planujesz wdrożenie w najbliższych {{TIMEFRAME}}:

**Pierwsze kroki:**
1. **{{ACTION_1}}** - {{ACTION_1_DESCRIPTION}}
2. **{{ACTION_2}}** - {{ACTION_2_DESCRIPTION}}
3. **{{ACTION_3}}** - {{ACTION_3_DESCRIPTION}}

**Przydatne narzędzia:**
- {{TOOL_1}} - {{TOOL_1_USE_CASE}}
- {{TOOL_2}} - {{TOOL_2_USE_CASE}}

**Potrzebujesz pomocy?**
- [Umów bezpłatną konsultację]({{CONSULTATION_LINK}}) - omówimy Twój case i pomożemy zaplanować wdrożenie
- [Pobierz RFP template]({{RFP_TEMPLATE_LINK}}) - gotowy brief do wysłania do agencji/dostawców

### 📚 Jeśli jeszcze zbierasz wiedzę:

**Polecane artykuły:**
- {{RELATED_ARTICLE_1}} - {{WHY_READ_1}}
- {{RELATED_ARTICLE_2}} - {{WHY_READ_2}}

**Zasoby:**
- [Subskrybuj newsletter]({{NEWSLETTER_LINK}}) - 1 artykuł/tydzień, konkretna wiedza bez spamu
- [Dołącz do webinaru]({{WEBINAR_LINK}}) - live Q&A z ekspertami

{{OPTIONAL_WARNING}}
```

### Wariant B: Artykuł teoretyczny/strategiczny

Dla artykułów typu:
- "Czym jest..."
- "Porównanie..."
- "Trendy..."
- Business metadata: `project_phase: ["planowanie"]`

```markdown
## Co dalej?

### 🎯 Oceń czy {{TOPIC}} jest dla Ciebie:

**Odpowiedz na te pytania:**
- [ ] {{QUESTION_1}}
- [ ] {{QUESTION_2}}
- [ ] {{QUESTION_3}}

Jeśli odpowiedziałeś "tak" na 2+ pytania, {{RECOMMENDATION}}.

### 📖 Pogłęb wiedzę:

**Następne kroki lektury:**
1. **{{NEXT_ARTICLE_1}}** - {{WHY_READ_1}}
2. **{{NEXT_ARTICLE_2}}** - {{WHY_READ_2}}

**Praktyczne zasoby:**
- {{RESOURCE_1}}
- {{RESOURCE_2}}

### 💬 Potrzebujesz pomocy w podjęciu decyzji?

- [Umów konsultację]({{CONSULTATION_LINK}}) - omówimy Twój case i pomożemy wybrać najlepsze rozwiązanie
- [Wypełnij ankietę potrzeb]({{SURVEY_LINK}}) - dostaniesz spersonalizowane rekomendacje

{{OPTIONAL_NOTE}}
```

### Wariant C: Artykuł o optymalizacji/compliance

Dla artykułów typu:
- "Jak przyspieszyć..."
- "Bezpieczeństwo i RODO..."
- "SEO audit..."
- Business metadata: `project_phase: ["optymalizacja"]`

```markdown
## Co dalej?

### 🔍 Oceń swój obecny stan:

**Użyj naszych narzędzi:**
- [{{AUDIT_TOOL_NAME}}]({{AUDIT_TOOL_LINK}}) - darmowy audyt {{TOPIC}} (5 minut)
- [{{CHECKLIST_NAME}}]({{CHECKLIST_LINK}}) - pobierz checklistę i oceń zgodność

### ⚡ Szybkie wdrożenie (quick wins):

**Możesz zrobić to samodzielnie:**
1. **{{QUICK_WIN_1}}** - impact: {{IMPACT_1}}, czas: {{TIME_1}}
2. **{{QUICK_WIN_2}}** - impact: {{IMPACT_2}}, czas: {{TIME_2}}
3. **{{QUICK_WIN_3}}** - impact: {{IMPACT_3}}, czas: {{TIME_3}}

### 🚀 Pełne wdrożenie (zalecane):

**Potrzebujesz wsparcia?**
- [Umów audyt]({{AUDIT_LINK}}) - kompleksowa analiza + rekomendacje (od {{AUDIT_PRICE}})
- [Zapytaj o wdrożenie]({{IMPLEMENTATION_LINK}}) - zajmiemy się wszystkim za Ciebie

### 📚 Dowiedz się więcej:

{{RELATED_ARTICLES_LIST}}
```

## 📋 Elementy do wypełnienia

### 1. Timeframe
Na podstawie `business_metadata.timeline.estimate`:
- "najbliższych 1-2 miesięcy"
- "najbliższych 3-6 miesięcy"
- "następnego roku"

### 2. Actions (akcje do wykonania)

**Format:**
```
ACTION_1: "Przeanalizuj obecną platformę e-commerce"
ACTION_1_DESCRIPTION: "Zrób listę funkcji których Ci brakuje i problemów które chcesz rozwiązać"

ACTION_2: "Ustal budżet wdrożenia"
ACTION_2_DESCRIPTION: "Na podstawie artykułu orientacyjny budżet to {{INVESTMENT_RANGE}} - uwzględnij bufór 20%"

ACTION_3: "Przygotuj listę integracji"
ACTION_3_DESCRIPTION: "Jakie systemy muszą być zintegrowane? (ERP, CRM, płatności, magazyn)"
```

**Skąd brać akcje:**
- Z checklist (jeśli jest w artykule)
- Z głównych sekcji artykułu (pierwsze kroki z każdej sekcji)
- Z business metadata (np. jeśli wymaga zespołu → "Zbuduj zespół projektowy")

### 3. Tools (narzędzia)

Narzędzia wspomniane w artykule + rekomendacje:
```
TOOL_1: "Calculator TCO (Total Cost of Ownership)"
TOOL_1_USE_CASE: "Oblicz rzeczywisty koszt platformy na 3 lata (licencje + hosting + development)"

TOOL_2: "Platform comparison spreadsheet"
TOOL_2_USE_CASE: "Porównaj 3-5 platform na podstawie Twoich wymagań"
```

### 4. Questions (pytania do self-assessment)

3-5 pytań yes/no które pomogą czytelnikowi ocenić czy temat jest dla niego:

```
QUESTION_1: "Czy Twój obecny system ogranicza rozwój biznesu?"
QUESTION_2: "Czy masz budżet {{INVESTMENT_RANGE}} na wdrożenie w ciągu {{TIMEFRAME}}?"
QUESTION_3: "Czy masz zespół IT (własny lub external) do wdrożenia?"
```

### 5. Recommendation

Na podstawie pytań:
```
RECOMMENDATION: "headless architecture może być dobrym wyborem - zacznij od konsultacji z architektem"
RECOMMENDATION: "lepiej zainwestuj w optymalizację obecnej platformy niż migrację"
```

### 6. Quick Wins (szybkie wygrane)

Dla artykułów optymalizacyjnych, 3 akcje które można zrobić szybko:
```
QUICK_WIN_1: "Włącz caching w przeglądarce"
IMPACT_1: "+15-25% szybkości"
TIME_1: "30 minut"

QUICK_WIN_2: "Skompresuj obrazy produktów"
IMPACT_2: "+20-30% szybkości"
TIME_2: "2-4 godziny (batch processing)"
```

### 7. Related Articles

Z `{{RELATED_ARTICLES}}` (internal linking), wybierz 2-3 najbardziej pasujące:
```
RELATED_ARTICLE_1: "[Integracje ERP w e-commerce](link)"
WHY_READ_1: "dowiesz się jak połączyć platformę z systemem magazynowym"

RELATED_ARTICLE_2: "[Koszty wdrożenia platform](link)"
WHY_READ_2: "szczegółowy breakdown kosztów dla różnych rozwiązań"
```

### 8. Optional Warning/Note

Jeśli `complexity.technical: "high"` lub `investment.level: "high"`:

```
⚠️ **Ważne:** {{TOPIC}} to złożone wdrożenie wymagające doświadczonego zespołu. Zalecamy konsultację z ekspertem przed podjęciem decyzji - źle przeprowadzona migracja może kosztować 2-3x więcej niż planowano.
```

Jeśli `complexity.organizational: "high"`:
```
💡 **Wskazówka:** Sukces wdrożenia {{TOPIC}} to w 70% change management, a w 30% technologia. Zadbaj o komunikację, szkolenia i buy-in od zespołu od pierwszego dnia.
```

## 🎨 Przykłady gotowych sekcji

### Przykład 1: Artykuł wdrożeniowy (platforma e-commerce)

```markdown
## Co dalej?

### ✅ Jeśli planujesz wdrożenie w najbliższych 3-6 miesięcy:

**Pierwsze kroki:**
1. **Zdefiniuj wymagania biznesowe** - zrób listę funkcji must-have vs nice-to-have, uwzględnij przyszły rozwój (2-3 lata)
2. **Ustal realny budżet** - na podstawie artykułu orientacyjny koszt to 60-200k PLN - uwzględnij bufор 20% na nieprzewidziane
3. **Wybierz 3-5 platform do porównania** - skup się na tych które pasują do Twojego modelu biznesowego (B2B vs B2C)

**Przydatne narzędzia:**
- [Platform comparison spreadsheet](#) - gotowy Excel do porównania platform (30+ kryteriów)
- [RFP template dla e-commerce](#) - wyślij do agencji i dostań porównywalne oferty

**Potrzebujesz pomocy?**
- [Umów bezpłatną konsultację](#) - omówimy Twój case i pomożemy wybrać najlepszą platformę (30 min)
- [Zapytaj o wdrożenie](#) - otrzymasz wycenę i plan projektu w 2-3 dni robocze

### 📚 Jeśli jeszcze zbierasz wiedzę:

**Polecane artykuły:**
- [Integracje ERP, WMS i CRM](../operacje/integracje-erp-wms-crm) - dowiesz się jak połączyć platformę z systemami backendowymi
- [Koszty utrzymania e-commerce](../operacje/koszty-utrzymania) - ukryte koszty których nie widzisz przy wyborze platformy

**Zasoby:**
- [Subskrybuj newsletter](#) - co tydzień case study z prawdziwych wdrożeń (bez spamu)
- [E-book: Wybór platformy B2B](#) - 40-stronicowy przewodnik z checklistami

⚠️ **Ważne:** Wybór platformy e-commerce to decyzja na 3-5 lat. Źle dobrana platforma może kosztować 2-3x więcej w maintenance niż początkowe wdrożenie. Warto poświęcić czas na research i konsultacje przed decyzją.
```

### Przykład 2: Artykuł teoretyczny (headless architecture)

```markdown
## Co dalej?

### 🎯 Oceń czy headless architecture jest dla Ciebie:

**Odpowiedz na te pytania:**
- [ ] Czy potrzebujesz obsługi wielu kanałów sprzedaży? (web, mobile app, IoT, voice)
- [ ] Czy masz budżet 150-500k PLN na wdrożenie i zespół 6+ developerów?
- [ ] Czy Twoja obecna platforma ogranicza rozwój frontendu i UX?
- [ ] Czy planujesz międzynarodową ekspansję z różnymi frontendami per region?

Jeśli odpowiedziałeś "tak" na 3+ pytania, headless może być dobrym wyborem - zacznij od konsultacji z solutions architect.

Jeśli mniej niż 2 "tak", prawdopodobnie lepiej zoptymalizować obecną platformę.

### 📖 Pogłęb wiedzę:

**Następne kroki lektury:**
1. **[Headless vs Traditional - case studies](../platformy/headless-case-studies)** - 5 prawdziwych wdrożeń, co zadziałało, co nie
2. **[API-first e-commerce platforms](../platformy/api-first)** - przegląd platform wspierających headless out-of-the-box

**Praktyczne zasoby:**
- [Headless readiness assessment](#) - 20 pytań które pokażą czy jesteś gotowy na headless
- [TCO calculator: Headless vs Traditional](#) - porównaj koszty na 3 lata

### 💬 Potrzebujesz pomocy w podjęciu decyzji?

- [Umów konsultację z Solutions Architect](#) - omówimy Twój tech stack i dopasowanie do headless (60 min, 500 PLN)
- [Proof of Concept](#) - zbudujemy prosty headless frontend dla Twojego backendu (2-3 tygodnie, od 15k PLN)

💡 **Wskazówka:** Headless to nie trend ale tool. Działa świetnie dla complex use cases (omnichannel, international, high traffic). Dla prostych sklepów B2C to często overengineering. Wybieraj na podstawie problemu który rozwiązujesz, nie technologii która brzmi cool.
```

### Przykład 3: Artykuł optymalizacyjny (Core Web Vitals)

```markdown
## Co dalej?

### 🔍 Oceń swój obecny stan:

**Użyj naszych narzędzi:**
- [PageSpeed Insights](https://pagespeed.web.dev/) - darmowy audyt Core Web Vitals (2 minuty)
- [Core Web Vitals checklist](#) - pobierz PDF i oceń zgodność (15 punktów)

### ⚡ Szybkie wdrożenie (quick wins):

**Możesz zrobić to samodzielnie (lub z developerem):**
1. **Włącz lazy loading dla obrazów** - impact: +20-30% LCP, czas: 1-2 godziny
2. **Zmień hosting na Cloudflare** - impact: +15-25% wszystkie metryki, czas: 2-4 godziny, koszt: 20$/msc
3. **Skompresuj obrazy produktów (WebP)** - impact: +25-40% LCP, czas: 4-8 godzin (batch), koszt: 0 PLN

**Łączny impact quick wins: 40-60% poprawa metryk w 2-3 dni pracy.**

### 🚀 Pełne wdrożenie (zalecane dla najlepszych wyników):

**Potrzebujesz wsparcia?**
- [Zamów performance audit](#) - kompleksowa analiza + plan optymalizacji (od 3k PLN, 3-5 dni)
- [Zapytaj o wdrożenie](#) - zajmiemy się wszystkim, gwarantujemy wyniki (od 15k PLN, 4-6 tygodni)

**Spodziewany efekt:** 80-95 punktów w PageSpeed Insights, 2-3s Total Load Time, 15-25% wzrost konwersji.

### 📚 Dowiedz się więcej:

- [CDN dla e-commerce - przewodnik](../operacje/cdn-ecommerce) - jak wybrać i skonfigurować CDN
- [Image optimization strategies](../operacje/image-optimization) - wszystko o formatach, kompresji, lazy loading

💡 **Wskazówka:** Core Web Vitals to nie tylko SEO - każda sekunda ładowania to 7% mniej konwersji (industry average). Inwestycja 10-20k PLN w performance może zwrócić się ROI 300-500% w ciągu roku dzięki wyższej konwersji.
```

## ⚠️ Ważne zasady

### DO:
- ✅ Personalizuj na podstawie business metadata (budżet, czas, zespół)
- ✅ Dawaj konkretne akcje (nie "przeczytaj więcej" ale "pobierz template X")
- ✅ Używaj liczb (timeframes, budżety, impact)
- ✅ Dodawaj warnings jeśli complexity/investment high
- ✅ Linkuj do 2-3 related articles z kontekstem "dlaczego przeczytać"
- ✅ Proponuj różne ścieżki (ready vs researching)

### DON'T:
- ❌ NIE używaj ogólników ("skontaktuj się z nami")
- ❌ NIE przeciążaj linkami (max 5-7 total)
- ❌ NIE obiecuj rzeczy których nie możesz dostarczyć
- ❌ NIE rob hard sell - edukuj i proponuj wsparcie
- ❌ NIE duplikuj treści z sekcji "Powiązane artykuły" (internal linking)

## 📊 Quality checklist

Przed zwróceniem wyniku sprawdź:
- [ ] Sekcja dopasowana do typu artykułu (practical/theoretical/optimization)
- [ ] Akcje konkretne i actionable (nie ogólniki)
- [ ] Timeframes z business metadata
- [ ] Budżety/koszty wspomniane (z business metadata)
- [ ] 2-3 related articles z kontekstem "dlaczego przeczytać"
- [ ] Warning/Note jeśli high complexity lub high investment
- [ ] Różne ścieżki dla różnych readers (ready vs researching)
- [ ] Wszystkie linki placeholders ({{LINK}}) - user wypełni prawdziwe URLs
- [ ] Ton ekspercki ale pomocny (nie sprzedażowy)

---

**WAŻNE - Format zwrotki:**
- Zwróć CZYSTY markdown bez opakowywania w \`\`\`markdown ... \`\`\`
- Output powinien zaczynać się bezpośrednio od `## Co dalej?`
- Gotowe do bezpośredniego wklejenia na koniec artykułu

**Output:** Markdown sekcja "Co dalej?" (czysty markdown, bez wrapper)
