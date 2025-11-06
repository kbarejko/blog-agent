# 🎨 Sugestie multimediów - Multimedia suggestions

**Zadanie:**
Przeanalizuj gotowy artykuł i zaproponuj multimedia (obrazy, grafiki, wykresy, screenshoty), które wzbogacą treść i poprawią UX.

## 🔖 Dane wejściowe
- **Tytuł artykułu:** `{{TYTUL_ARTYKULU}}`
- **Treść artykułu:** `{{ARTICLE_CONTENT}}` (po humanizacji)
- **Konspekt:** `{{KONSPEKT_TRESC}}`
- **Grupa docelowa:** `{{TARGET_AUDIENCE}}`

## 🎯 Cel

Zasugeruj multimedia które:
1. **Wzmacniają zrozumienie** - wizualizują złożone koncepcje
2. **Zwiększają engagement** - łamią monotonię tekstu
3. **Poprawiają SEO** - alt text z keywords
4. **Są praktyczne** - user może je wygenerować/pobrać/zlecić

## 📋 Typy multimediów do sugerowania

### 1. 📷 **Zdjęcia**
- Hero image (główny obraz artykułu)
- Zdjęcia kontekstowe w sekcjach
- Zdjęcia produktów, zespołów, przestrzeni

**Kiedy sugerować:**
- Hero: ZAWSZE (każdy artykuł)
- W sekcjach: gdy wspominasz konkretne narzędzia, produkty, środowiska

**Przykład:**
```json
{
  "type": "photo",
  "subtype": "hero",
  "section": "Top of article",
  "description": "Profesjonalne zdjęcie właściciela sklepu e-commerce pracującego przy laptopie z dashboardem bezpieczeństwa",
  "alt_text": "Właściciel sklepu e-commerce analizuje dashboard bezpieczeństwa RODO",
  "placement": "after_title",
  "image_prompt": "Professional photo of an e-commerce business owner working on laptop showing security dashboard, modern office environment, natural lighting, authentic workspace, stock photo style",
  "keywords": ["e-commerce", "bezpieczeństwo", "RODO", "sklep online"],
  "reason": "Hero image wprowadza w tematykę artykułu i buduje profesjonalny wizerunek"
}
```

### 2. 📊 **Wykresy i diagramy**
- Wykresy słupkowe, liniowe, kołowe
- Diagramy przepływu (flowcharts)
- Diagramy Venna, mind maps
- Porównania, trendy, statystyki

**Kiedy sugerować:**
- Sekcje z danymi liczbowymi
- Porównania (platform, kosztów, funkcji)
- Procesy krok-po-kroku
- Trendy czasowe

**Przykład:**
```json
{
  "type": "chart",
  "subtype": "bar_chart",
  "section": "Sekcja: Kary za naruszenie RODO",
  "description": "Wykres słupkowy pokazujący wzrost kar RODO w e-commerce 2020-2024",
  "alt_text": "Wykres wzrostu kar RODO w polskim e-commerce 2020-2024",
  "placement": "after paragraph 3",
  "image_prompt": "Clean bar chart showing RODO penalties growth in Polish e-commerce from 2020 to 2024, professional infographic style, blue and red colors, values in PLN, minimalist design",
  "data_suggestion": {
    "labels": ["2020", "2021", "2022", "2023", "2024"],
    "values": [50000, 120000, 450000, 890000, 1200000],
    "unit": "PLN"
  },
  "keywords": ["RODO", "kary", "e-commerce", "statystyki"],
  "reason": "Wizualizacja trendu rosnących kar motywuje do działania i jest łatwa do zapamiętania"
}
```

### 3. 🎨 **Grafiki i ilustracje**
- Infografiki (zestawienia, porównania)
- Schematy (architektury, struktury)
- Ikony i symbole
- Ilustracje koncepcyjne

**Kiedy sugerować:**
- Złożone koncepcje wymagające uproszczenia
- Listy 5+ elementów (lepsze jako infografika)
- Architektury systemów
- Procesy wieloetapowe

**Przykład:**
```json
{
  "type": "illustration",
  "subtype": "infographic",
  "section": "Sekcja: 5 wymagań RODO dla sklepów",
  "description": "Infografika przedstawiająca 5 kluczowych wymagań RODO w formie pionowego flowchart z ikonami",
  "alt_text": "Infografika 5 wymagań RODO dla sklepów e-commerce",
  "placement": "after paragraph 1",
  "image_prompt": "Vertical infographic showing 5 key RODO requirements for e-commerce: 1) Privacy policy, 2) Cookie consent, 3) Data encryption, 4) Backup system, 5) Right to deletion. Clean design, icons for each point, blue and white color scheme, professional style",
  "keywords": ["RODO", "wymagania", "e-commerce", "compliance"],
  "reason": "Infografika z 5 punktami jest łatwiejsza do przyswojenia niż lista tekstowa"
}
```

### 4. 📸 **Screenshoty**
- Interfejsy narzędzi
- Dashboardy, panele administracyjne
- Przykłady konfiguracji
- Przed/Po (comparisons)

**Kiedy sugerować:**
- Artykuły praktyczne ("jak zrobić")
- Omówienie konkretnych narzędzi
- Tutoriale, instrukcje
- Case studies

**Przykład:**
```json
{
  "type": "screenshot",
  "subtype": "interface",
  "section": "Sekcja: Instalacja certyfikatu SSL",
  "description": "Screenshot panelu Let's Encrypt pokazujący proces instalacji certyfikatu SSL",
  "alt_text": "Panel Let's Encrypt z konfiguracją certyfikatu SSL dla sklepu e-commerce",
  "placement": "after paragraph 2",
  "image_prompt": "Clean screenshot mockup of Let's Encrypt SSL certificate installation panel, showing domain verification step, professional interface design, highlighted important buttons, annotations if needed",
  "keywords": ["SSL", "Let's Encrypt", "certyfikat", "instalacja"],
  "reason": "Screenshot pokazuje realny interfejs narzędzia i redukuje strach przed implementacją"
}
```

## ✍️ Zasady tworzenia sugestii

### Liczba sugestii
- **Hero image:** 1 (ZAWSZE)
- **Obrazy w sekcjach:** 3-8 (zależnie od długości artykułu)
- **TOTAL:** 4-9 sugestii

**Rozkład na artykuł 5-sekcyjny:**
- 1 hero
- 2-3 wykresy/diagramy (dla sekcji z danymi)
- 1-2 infografiki (dla list/procesów)
- 1-2 screenshoty (dla sekcji praktycznych)
- 0-1 zdjęć kontekstowych

### Priorytetyzacja

**HIGH priority** (3-4 sugestie):
- Hero image (zawsze)
- Multimedia dla najważniejszych sekcji
- Wizualizacje danych/statystyk (jeśli są)
- Infografiki dla kluczowych koncepcji

**MEDIUM priority** (2-3 sugestie):
- Screenshoty narzędzi
- Diagramy przepływów
- Grafiki pomocnicze

**LOW priority** (1-2 sugestie):
- Zdjęcia dekoracyjne
- Dodatkowe ilustracje

### Umiejscowienie

**Dobre miejsca:**
- Po tytule (hero)
- Po 2-3 akapitach tekstu (break monotonii)
- Przy pierwszym wspomnieniu konkretnego narzędzia/produktu
- Przy danych liczbowych (wykres)
- Przy listach 5+ elementów (infografika)

**Złe miejsca:**
- W środku akapitu (przerywa flow)
- Zbyt blisko siebie (min. 2 akapity między)
- W FAQ (tekst wystarczy)
- W Checklist (tekst wystarczy)

### Image prompts (dla DALL-E/Midjourney)

**Zasady tworzenia promptów:**
1. **Język:** angielski (standardowe narzędzia)
2. **Styl:** opisowy, konkretny
3. **Elementy:**
   - Główny obiekt/scena
   - Styl wizualny (minimalist, professional, modern)
   - Kolory (brand colors jeśli znane, default: blue/green professional)
   - Format (photo, illustration, diagram, infographic)
   - Jakość (high quality, professional, stock photo style)

4. **Długość:** 30-60 słów (sweet spot dla quality)

**Przykłady dobrych promptów:**

✅ **DOBRY:**
```
"Modern e-commerce dashboard showing security metrics and RODO compliance indicators, clean UI design, blue and white color scheme, professional software interface, detailed but readable, high quality screenshot style"
```

✅ **DOBRY:**
```
"Minimalist flowchart diagram showing 5-step SSL certificate installation process, numbered steps with icons, arrows connecting steps, professional infographic style, blue gradient colors, white background"
```

❌ **ZŁY (zbyt ogólny):**
```
"E-commerce security"
```

❌ **ZŁY (zbyt szczegółowy/niejasny):**
```
"A person sitting in front of computer with lines of code visible on screen showing encryption algorithms while holding coffee cup in modern office with plants in background during sunset lighting"
```

### Alt text (dla SEO i accessibility)

**Zasady:**
1. **Długość:** 100-125 znaków (optimum dla SEO)
2. **Język:** polski (język artykułu)
3. **Zawartość:**
   - Dokładny opis tego co widać
   - 1-2 keywords naturalne wplecione
   - Bez "obraz przedstawia", "zdjęcie pokazuje"
   - Kontekst dla niewidomych

**Przykłady:**

✅ **DOBRY:**
```
"Dashboard analytics e-commerce z metrykami bezpieczeństwa RODO i wskaźnikami compliance"
```

✅ **DOBRY:**
```
"Diagram procesu instalacji certyfikatu SSL w 5 krokach dla sklepu WooCommerce"
```

❌ **ZŁY (keyword stuffing):**
```
"Bezpieczeństwo e-commerce RODO sklep online certyfikat SSL ochrona danych"
```

❌ **ZŁY (zbyt ogólny):**
```
"Obraz pokazujący dashboard"
```

## 📋 Format Output (JSON)

```json
{
  "multimedia_suggestions": [
    {
      "id": 1,
      "type": "photo",
      "subtype": "hero",
      "priority": "high",
      "section": "Top of article",
      "title": "Hero image - Bezpieczeństwo e-commerce",
      "description": "Profesjonalne zdjęcie właściciela sklepu e-commerce pracującego przy dashboardzie bezpieczeństwa",
      "alt_text": "Właściciel sklepu e-commerce analizuje dashboard bezpieczeństwa RODO",
      "placement": "after_title",
      "image_prompt": "Professional photo of an e-commerce business owner working on laptop showing security dashboard, modern office environment, natural lighting, authentic workspace, stock photo style",
      "dimensions": "1920x1080 (16:9)",
      "keywords": ["e-commerce", "bezpieczeństwo", "RODO"],
      "reason": "Hero image wprowadza w tematykę i buduje profesjonalny wizerunek",
      "alternatives": [
        "Stock photo: Unsplash query 'e-commerce security'",
        "Custom: Zlecić designerowi ilustrację bezpieczeństwa"
      ]
    },
    {
      "id": 2,
      "type": "chart",
      "subtype": "bar_chart",
      "priority": "high",
      "section": "Sekcja: Kary za naruszenie RODO",
      "title": "Wykres wzrostu kar RODO 2020-2024",
      "description": "Wykres słupkowy pokazujący wzrost kar RODO w polskim e-commerce",
      "alt_text": "Wykres wzrostu kar RODO w polskim e-commerce od 2020 do 2024",
      "placement": "after_paragraph_3",
      "image_prompt": "Clean bar chart showing RODO penalties growth in Polish e-commerce 2020-2024, blue bars, red trend line, values in PLN, minimalist professional design",
      "data_suggestion": {
        "chart_type": "bar",
        "labels": ["2020", "2021", "2022", "2023", "2024"],
        "values": [50000, 120000, 450000, 890000, 1200000],
        "unit": "PLN"
      },
      "dimensions": "800x600",
      "keywords": ["RODO", "kary", "statystyki", "e-commerce"],
      "reason": "Wizualizacja trendu rosnących kar motywuje do działania",
      "alternatives": [
        "Tool: Create with ChartJS or Google Charts",
        "Tool: Canva chart template"
      ]
    },
    {
      "id": 3,
      "type": "illustration",
      "subtype": "infographic",
      "priority": "high",
      "section": "Sekcja: 5 wymagań RODO",
      "title": "Infografika - 5 wymagań RODO dla sklepów",
      "description": "Pionowa infografika z 5 kluczowymi wymaganiami RODO i ikonami",
      "alt_text": "Infografika 5 wymagań RODO dla sklepów e-commerce z ikonami",
      "placement": "after_paragraph_1",
      "image_prompt": "Vertical infographic showing 5 RODO requirements: privacy policy, cookie consent, data encryption, backup, right to deletion. Icons for each, blue and white, professional clean design",
      "dimensions": "800x1200 (portrait)",
      "keywords": ["RODO", "wymagania", "compliance", "infografika"],
      "reason": "Infografika z 5 punktami łatwiejsza do przyswojenia niż lista tekstowa",
      "alternatives": [
        "Tool: Canva infographic template",
        "Tool: Piktochart",
        "Custom: Zlecić designerowi"
      ]
    }
  ],
  "summary": {
    "total": 6,
    "by_type": {
      "photo": 1,
      "chart": 2,
      "illustration": 2,
      "screenshot": 1
    },
    "by_priority": {
      "high": 3,
      "medium": 2,
      "low": 1
    },
    "hero_image": true
  }
}
```

## ⚠️ Ważne zasady

### DO:
- ✅ Hero image ZAWSZE (każdy artykuł)
- ✅ Sugeruj tylko multimedia które mają WARTOŚĆ (nie dla ozdoby)
- ✅ Image prompts konkretne i szczegółowe (30-60 słów)
- ✅ Alt text SEO-friendly (100-125 znaków, keywords naturalne)
- ✅ Placement logiczny (po 2-3 akapitach, przy wspomnieniu tematu)
- ✅ Alternatives (stock photos, tools, custom design)
- ✅ Data dla wykresów (jeśli są w treści)
- ✅ Keywords dla każdego (min 3)

### DON'T:
- ❌ NIE sugeruj więcej niż 9 multimediów (przesada)
- ❌ NIE umieszczaj zbyt blisko siebie (min 2 akapity)
- ❌ NIE twórz ogólnych promptów ("security dashboard")
- ❌ NIE rób keyword stuffing w alt text
- ❌ NIE sugeruj multimediów które nie dodają wartości
- ❌ NIE pomijaj hero image (ZAWSZE musi być)
- ❌ NIE duplikuj typów w tej samej sekcji (1 wykres na sekcję max)

## 📊 Quality checklist

Przed zwróceniem wyniku sprawdź:
- [ ] Hero image jako pierwsza sugestia (id: 1)
- [ ] 4-9 sugestii total (nie mniej, nie więcej)
- [ ] Każda ma image_prompt (30-60 słów)
- [ ] Każda ma alt_text (100-125 znaków)
- [ ] Keywords naturalne (min 3 per multimedia)
- [ ] Placement logiczny (nie za często, nie za rzadko)
- [ ] Priorytety przypisane (high/medium/low)
- [ ] Alternatives podane (stock/tools/custom)
- [ ] Reason jasny dla każdego (dlaczego potrzebne)
- [ ] Data suggestion dla wykresów (jeśli są dane w tekście)
- [ ] Dimensions podane (standard web formats)
- [ ] Summary poprawne (sumy się zgadzają)

---

**Output:** JSON z listą sugestii multimediów + image prompts + placement
