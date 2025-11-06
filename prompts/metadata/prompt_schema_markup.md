# 🏷️ Schema.org Markup - Structured Data

**Zadanie:**
Wygeneruj Schema.org structured data (JSON-LD) dla artykułu, aby poprawić SEO i wyświetlanie w wynikach wyszukiwania Google (rich snippets).

## 🔖 Dane wejściowe
- **Tytuł artykułu:** `{{TYTUL_ARTYKULU}}`
- **Meta title:** `{{META_TITLE}}`
- **Meta description:** `{{META_DESCRIPTION}}`
- **Treść artykułu:** `{{ARTICLE_CONTENT}}` (finalna wersja)
- **URL artykułu:** `{{ARTICLE_URL}}` (pełny URL, np. `https://www.digitalvantage.pl/artykuly/ecommerce/operacje/bezpieczenstwo-i-rodo/`)
- **Data publikacji:** `{{PUBLISH_DATE}}` (ISO 8601, np. `2025-01-06`)
- **Data modyfikacji:** `{{MODIFIED_DATE}}` (ISO 8601)
- **Obrazy:** `{{IMAGES}}` (lista URL do obrazów w artykule, szczególnie hero image)
- **FAQ:** `{{FAQ_CONTENT}}` (jeśli artykuł ma sekcję FAQ)
- **Checklist:** `{{CHECKLIST_CONTENT}}` (jeśli artykuł ma sekcję Checklist)
- **Business metadata:** `{{BUSINESS_METADATA}}` (opcjonalnie, dla dodatkowych metadanych)

## 🎯 Cel

Wygenerować structured data które:
1. **Poprawią SEO** - lepsze pozycje w wynikach wyszukiwania
2. **Zwiększą CTR** - rich snippets w Google (FAQ, HowTo, ratings)
3. **Będą zgodne ze standardem** - Schema.org + Google guidelines
4. **Będą łatwe do wdrożenia** - gotowy JSON-LD do wklejenia w `<head>`

## 📋 Typy Schema.org do wygenerowania

### 1. 📄 Article (ZAWSZE)

Podstawowe schema dla każdego artykułu:

```json
{
  "@context": "https://schema.org",
  "@type": "Article",
  "headline": "{{META_TITLE}}",
  "description": "{{META_DESCRIPTION}}",
  "image": [
    "{{HERO_IMAGE_URL}}",
    "{{IMAGE_2_URL}}"
  ],
  "datePublished": "{{PUBLISH_DATE}}",
  "dateModified": "{{MODIFIED_DATE}}",
  "author": {
    "@type": "Organization",
    "name": "Digital Vantage",
    "url": "https://www.digitalvantage.pl",
    "logo": {
      "@type": "ImageObject",
      "url": "https://www.digitalvantage.pl/logo.png"
    }
  },
  "publisher": {
    "@type": "Organization",
    "name": "Digital Vantage",
    "url": "https://www.digitalvantage.pl",
    "logo": {
      "@type": "ImageObject",
      "url": "https://www.digitalvantage.pl/logo.png",
      "width": 600,
      "height": 60
    }
  },
  "mainEntityOfPage": {
    "@type": "WebPage",
    "@id": "{{ARTICLE_URL}}"
  },
  "articleSection": "{{SERIA}} - {{SILOS}}",
  "keywords": [
    "{{KEYWORD_1}}",
    "{{KEYWORD_2}}",
    "{{KEYWORD_3}}"
  ],
  "wordCount": {{WORD_COUNT}},
  "inLanguage": "pl-PL"
}
```

**Wymagane pola:**
- `headline` - użyj meta_title (max 110 znaków)
- `description` - użyj meta_description
- `image` - lista obrazów (min 1, preferowane 3+), wymiary min 1200px szerokości
- `datePublished` - data w formacie ISO 8601
- `dateModified` - data ostatniej modyfikacji
- `author` - Digital Vantage (Organization, nie Person)
- `publisher` - Digital Vantage z logo
- `mainEntityOfPage` - pełny URL artykułu
- `keywords` - 5-10 keywords z artykułu

**Opcjonalne pola:**
- `articleSection` - seria i silos (np. "E-commerce - Operacje")
- `wordCount` - liczba słów w artykule
- `inLanguage` - język artykułu (zawsze "pl-PL")

### 2. ❓ FAQPage (jeśli artykuł ma FAQ)

Jeśli artykuł zawiera sekcję FAQ z pytaniami i odpowiedziami:

```json
{
  "@context": "https://schema.org",
  "@type": "FAQPage",
  "mainEntity": [
    {
      "@type": "Question",
      "name": "{{QUESTION_1}}",
      "acceptedAnswer": {
        "@type": "Answer",
        "text": "{{ANSWER_1}}"
      }
    },
    {
      "@type": "Question",
      "name": "{{QUESTION_2}}",
      "acceptedAnswer": {
        "@type": "Answer",
        "text": "{{ANSWER_2}}"
      }
    }
  ]
}
```

**Zasady:**
- Każde pytanie z FAQ jako osobny element w `mainEntity`
- `name` - pytanie (tekst pytania)
- `acceptedAnswer.text` - odpowiedź (może zawierać HTML: `<p>`, `<ul>`, `<strong>`)
- Google wyświetla max 10 pytań w rich snippets
- Jeśli FAQ ma >10 pytań, wybierz 10 najważniejszych

### 3. ✅ HowTo (jeśli artykuł ma Checklist)

Jeśli artykuł zawiera Checklist (lista kroków do wykonania):

```json
{
  "@context": "https://schema.org",
  "@type": "HowTo",
  "name": "{{CHECKLIST_TITLE}}",
  "description": "{{CHECKLIST_DESCRIPTION}}",
  "totalTime": "{{ESTIMATED_TIME}}",
  "estimatedCost": {
    "@type": "MonetaryAmount",
    "currency": "PLN",
    "value": "{{ESTIMATED_COST}}"
  },
  "step": [
    {
      "@type": "HowToStep",
      "name": "{{STEP_1_NAME}}",
      "text": "{{STEP_1_DESCRIPTION}}",
      "position": 1
    },
    {
      "@type": "HowToStep",
      "name": "{{STEP_2_NAME}}",
      "text": "{{STEP_2_DESCRIPTION}}",
      "position": 2
    }
  ]
}
```

**Zasady:**
- `name` - tytuł checklist (np. "Checklist wdrożenia RODO w e-commerce")
- `description` - opis czego dotyczy checklist
- `totalTime` - szacowany czas (format ISO 8601, np. `"PT2H"` = 2 godziny)
- `estimatedCost` - szacowany koszt (jeśli applicable, z business metadata)
- `step` - każdy element checklist jako osobny krok
- `position` - numeracja kroków (1, 2, 3...)

**Opcjonalne pola:**
- `image` - obrazy ilustrujące kroki
- `tool` - narzędzia potrzebne do wykonania

### 4. 🗺️ BreadcrumbList (dla nawigacji)

Breadcrumbs dla struktury URL:

```json
{
  "@context": "https://schema.org",
  "@type": "BreadcrumbList",
  "itemListElement": [
    {
      "@type": "ListItem",
      "position": 1,
      "name": "Strona główna",
      "item": "https://www.digitalvantage.pl"
    },
    {
      "@type": "ListItem",
      "position": 2,
      "name": "Artykuły",
      "item": "https://www.digitalvantage.pl/artykuly"
    },
    {
      "@type": "ListItem",
      "position": 3,
      "name": "{{SERIA_NAME}}",
      "item": "https://www.digitalvantage.pl/artykuly/{{SERIA}}"
    },
    {
      "@type": "ListItem",
      "position": 4,
      "name": "{{SILOS_NAME}}",
      "item": "https://www.digitalvantage.pl/artykuly/{{SERIA}}/{{SILOS}}"
    },
    {
      "@type": "ListItem",
      "position": 5,
      "name": "{{ARTICLE_TITLE}}",
      "item": "{{ARTICLE_URL}}"
    }
  ]
}
```

**Zasady:**
- Każdy poziom URL jako osobny element
- `name` - czytelna nazwa (nie slug)
- Przykład nazw:
  - `ecommerce` → `"E-commerce"`
  - `operacje` → `"Operacje"`
  - `bezpieczenstwo-i-rodo` → tytuł artykułu

### 5. 🏢 Organization (Digital Vantage)

Informacje o organizacji (do użycia w `author` i `publisher`):

```json
{
  "@type": "Organization",
  "name": "Digital Vantage",
  "url": "https://www.digitalvantage.pl",
  "logo": {
    "@type": "ImageObject",
    "url": "https://www.digitalvantage.pl/logo.png",
    "width": 600,
    "height": 60
  },
  "sameAs": [
    "https://www.linkedin.com/company/digital-vantage",
    "https://twitter.com/digitalvantage"
  ],
  "contactPoint": {
    "@type": "ContactPoint",
    "contactType": "Customer Service",
    "email": "kontakt@digitalvantage.pl"
  }
}
```

## 📋 Format Output (JSON-LD)

Wygeneruj **osobne bloki JSON-LD** dla każdego typu schema (nie łącz w jednym obiekcie):

```html
<!-- Article Schema -->
<script type="application/ld+json">
{
  "@context": "https://schema.org",
  "@type": "Article",
  ...
}
</script>

<!-- FAQPage Schema (jeśli applicable) -->
<script type="application/ld+json">
{
  "@context": "https://schema.org",
  "@type": "FAQPage",
  ...
}
</script>

<!-- HowTo Schema (jeśli applicable) -->
<script type="application/ld+json">
{
  "@context": "https://schema.org",
  "@type": "HowTo",
  ...
}
</script>

<!-- BreadcrumbList Schema -->
<script type="application/ld+json">
{
  "@context": "https://schema.org",
  "@type": "BreadcrumbList",
  ...
}
</script>
```

**Dlaczego osobne bloki?**
- Google preferuje osobne schemas dla każdego typu
- Łatwiejsze do testowania (Google Rich Results Test)
- Lepsze error handling

## 🎨 Przykład kompletnego output

### Przykład 1: Artykuł z FAQ i Checklist

**Artykuł:** "Bezpieczeństwo i RODO w e-commerce - kompletny przewodnik"
- Ma FAQ (10 pytań)
- Ma Checklist (15 punktów)
- Ma obrazy

```html
<!-- Article Schema -->
<script type="application/ld+json">
{
  "@context": "https://schema.org",
  "@type": "Article",
  "headline": "Bezpieczeństwo i RODO w e-commerce - Kompletny przewodnik 2025",
  "description": "Dowiedz się jak zabezpieczyć sklep online i spełnić wymogi RODO. Checklist 15 punktów, kary do 4% przychodu, praktyczne rozwiązania.",
  "image": [
    "https://www.digitalvantage.pl/images/articles/bezpieczenstwo-rodo-hero.jpg",
    "https://www.digitalvantage.pl/images/articles/ssl-certificate.jpg",
    "https://www.digitalvantage.pl/images/articles/rodo-compliance.jpg"
  ],
  "datePublished": "2025-01-06T10:00:00+01:00",
  "dateModified": "2025-01-06T10:00:00+01:00",
  "author": {
    "@type": "Organization",
    "name": "Digital Vantage",
    "url": "https://www.digitalvantage.pl",
    "logo": {
      "@type": "ImageObject",
      "url": "https://www.digitalvantage.pl/logo.png"
    }
  },
  "publisher": {
    "@type": "Organization",
    "name": "Digital Vantage",
    "url": "https://www.digitalvantage.pl",
    "logo": {
      "@type": "ImageObject",
      "url": "https://www.digitalvantage.pl/logo.png",
      "width": 600,
      "height": 60
    }
  },
  "mainEntityOfPage": {
    "@type": "WebPage",
    "@id": "https://www.digitalvantage.pl/artykuly/ecommerce/operacje/bezpieczenstwo-i-rodo/"
  },
  "articleSection": "E-commerce - Operacje",
  "keywords": [
    "RODO e-commerce",
    "bezpieczeństwo sklepu online",
    "certyfikat SSL",
    "polityka prywatności",
    "compliance",
    "kary UOKiK",
    "szyfrowanie danych"
  ],
  "wordCount": 3200,
  "inLanguage": "pl-PL"
}
</script>

<!-- FAQPage Schema -->
<script type="application/ld+json">
{
  "@context": "https://schema.org",
  "@type": "FAQPage",
  "mainEntity": [
    {
      "@type": "Question",
      "name": "Czy każdy sklep e-commerce musi mieć politykę prywatności?",
      "acceptedAnswer": {
        "@type": "Answer",
        "text": "<p>Tak, polityka prywatności jest obowiązkowa dla każdego sklepu online który przetwarza dane osobowe klientów (imię, nazwisko, adres, email). Zgodnie z RODO musisz poinformować klientów jak ich dane są przetwarzane, przechowywane i chronione. Brak polityki prywatności to kara do 20 milionów EUR lub 4% globalnego przychodu firmy.</p>"
      }
    },
    {
      "@type": "Question",
      "name": "Ile kosztuje wdrożenie RODO w sklepie online?",
      "acceptedAnswer": {
        "@type": "Answer",
        "text": "<p>Orientacyjne koszty: SSL certyfikat (0-2k PLN/rok z Let's Encrypt free), polityka prywatności i regulamin (2-5k PLN za usługę prawną), audyt bezpieczeństwa (3-10k PLN), rozwiązanie do backup (2-5k PLN/rok), konsultacje (5-15k PLN). Łącznie: 5-30k PLN dla małego/średniego sklepu.</p>"
      }
    },
    {
      "@type": "Question",
      "name": "Jak długo można przechowywać dane klientów?",
      "acceptedAnswer": {
        "@type": "Answer",
        "text": "<p>Dane możesz przechowywać tylko tak długo jak jest to niezbędne do realizacji celu dla którego je zebrałeś. Dla zamówień: 5 lat (przepisy podatkowe), dla marketingu: do momentu wycofania zgody przez klienta, dla kont użytkowników: do czasu usunięcia konta. Po tym czasie dane muszą być usunięte lub zanonimizowane.</p>"
      }
    }
  ]
}
</script>

<!-- HowTo Schema -->
<script type="application/ld+json">
{
  "@context": "https://schema.org",
  "@type": "HowTo",
  "name": "Checklist wdrożenia RODO w sklepie e-commerce",
  "description": "15-punktowa lista kontrolna do samodzielnego sprawdzenia zgodności sklepu online z wymogami RODO",
  "totalTime": "PT2H",
  "estimatedCost": {
    "@type": "MonetaryAmount",
    "currency": "PLN",
    "value": "5000-30000"
  },
  "step": [
    {
      "@type": "HowToStep",
      "name": "Zainstaluj certyfikat SSL/TLS",
      "text": "Upewnij się że cała strona działa na HTTPS. Użyj Let's Encrypt (darmowy) lub zakup certyfikat od dostawcy hostingu. Sprawdź czy formularz zamówienia, logowanie i panel klienta są szyfrowane.",
      "position": 1
    },
    {
      "@type": "HowToStep",
      "name": "Przygotuj politykę prywatności i regulamin",
      "text": "Stwórz politykę prywatności zgodną z RODO (info o administratorze danych, cele przetwarzania, prawa klientów). Skonsultuj z prawnikiem lub użyj generatora polityk (ale zweryfikuj prawnie).",
      "position": 2
    },
    {
      "@type": "HowToStep",
      "name": "Wdróż cookie consent banner",
      "text": "Dodaj banner zgody na cookies zgodny z RODO. Klient musi móc odrzucić cookies marketingowe. Popularne rozwiązania: Cookiebot, OneTrust, Iubenda.",
      "position": 3
    }
  ]
}
</script>

<!-- BreadcrumbList Schema -->
<script type="application/ld+json">
{
  "@context": "https://schema.org",
  "@type": "BreadcrumbList",
  "itemListElement": [
    {
      "@type": "ListItem",
      "position": 1,
      "name": "Strona główna",
      "item": "https://www.digitalvantage.pl"
    },
    {
      "@type": "ListItem",
      "position": 2,
      "name": "Artykuły",
      "item": "https://www.digitalvantage.pl/artykuly"
    },
    {
      "@type": "ListItem",
      "position": 3,
      "name": "E-commerce",
      "item": "https://www.digitalvantage.pl/artykuly/ecommerce"
    },
    {
      "@type": "ListItem",
      "position": 4,
      "name": "Operacje",
      "item": "https://www.digitalvantage.pl/artykuly/ecommerce/operacje"
    },
    {
      "@type": "ListItem",
      "position": 5,
      "name": "Bezpieczeństwo i RODO w e-commerce",
      "item": "https://www.digitalvantage.pl/artykuly/ecommerce/operacje/bezpieczenstwo-i-rodo/"
    }
  ]
}
</script>
```

## ⚠️ Ważne zasady

### DO:
- ✅ Generuj osobne `<script type="application/ld+json">` dla każdego typu schema
- ✅ Używaj pełnych URLs (nie relatywnych)
- ✅ Daty w formacie ISO 8601 (`2025-01-06T10:00:00+01:00`)
- ✅ Obrazy min 1200px szerokości (Google requirement)
- ✅ Keywords 5-10 najważniejszych (nie keyword stuffing)
- ✅ HTML w answer text dozwolony (`<p>`, `<ul>`, `<strong>`)
- ✅ Escape cudzysłowy w JSON (`\"`)
- ✅ Testuj output w Google Rich Results Test

### DON'T:
- ❌ NIE łącz multiple schemas w jeden obiekt (osobne bloki!)
- ❌ NIE dodawaj FAQPage jeśli artykuł NIE ma FAQ
- ❌ NIE dodawaj HowTo jeśli artykuł NIE ma Checklist
- ❌ NIE używaj relatywnych URLs (`/images/x.jpg` → `https://...`)
- ❌ NIE przekraczaj 110 znaków w headline
- ❌ NIE duplikuj informacji między schemas
- ❌ NIE używaj nieprawidłowych dat (muszą być ISO 8601)

## 📊 Quality checklist

Przed zwróceniem wyniku:
- [ ] Article schema - ZAWSZE present
- [ ] FAQPage schema - tylko jeśli artykuł ma FAQ
- [ ] HowTo schema - tylko jeśli artykuł ma Checklist
- [ ] BreadcrumbList schema - ZAWSZE present
- [ ] Wszystkie URLs pełne (https://...)
- [ ] Daty w ISO 8601
- [ ] Obrazy (min 1, preferowane 3+)
- [ ] Keywords 5-10 (relevantne)
- [ ] Headline max 110 znaków
- [ ] Description max 160 znaków
- [ ] JSON valid (cudzysłowy escaped)
- [ ] Osobne `<script>` bloki dla każdego schema

## 🧪 Testing

User powinien przetestować output tutaj:
- **Google Rich Results Test:** https://search.google.com/test/rich-results
- **Schema.org Validator:** https://validator.schema.org/

---

**Output:** HTML z blokami `<script type="application/ld+json">` gotowymi do wklejenia w `<head>` strony
