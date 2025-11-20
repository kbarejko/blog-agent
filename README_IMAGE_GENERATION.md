# 🎨 Image Generation Guide

Automatyczne generowanie obrazów hero z brand style digitalvantage.pl + sugestie stock photos dla artykułów.

## 📋 Podsumowanie

**Co generujemy:**
- ✅ **Hero image 1920x1200** - automatycznie przez AI (Stability AI lub DALL-E) + upscale
- 🎨 **Brand Style** - zgodny z digitalvantage.pl (minimalistyczny, profesjonalny, black/white/gray + yellow accent)
- 📋 **Inne obrazy** - sugestie z promptami AI + linki do stock photos

**Rozmiary:**
- Hero: **1920x1200 px** (generowane 1024x1024, upscale do 1920x1200)
- Inne: według sugestii w multimedia.json

**Koszty:**
- Stability AI (SDXL): **$0.011/artykuł** ($1.10/100 artykułów) ⭐ NAJTANIEJ
- DALL-E 3 Standard: **$0.080/artykuł** ($8/100 artykułów)
- DALL-E 3 HD: **$0.120/artykuł** ($12/100 artykułów)

---

## 🚀 Quick Start

### 1. Ustaw API key

**Opcja A: Stability AI (tanie, dobre)** ⭐ Rekomendowane
```bash
# Dodaj do .env
echo "STABILITY_API_KEY=sk-..." >> .env
```

**Opcja B: DALL-E (droższe, najlepsza jakość)**
```bash
# Dodaj do .env
echo "OPENAI_API_KEY=sk-..." >> .env
```

### 2. Generuj hero image (CLI command)

**Po zakończeniu artykułu:**
```bash
# Z Stability AI (cheap, fast) - domyślnie 1920x1200
blog-agent generate-hero --config artykuly/seria/silos/slug/config.yaml

# Z DALL-E (premium quality)
blog-agent generate-hero --config artykuly/seria/silos/slug/config.yaml --provider dalle

# Custom size
blog-agent generate-hero --config artykuly/seria/silos/slug/config.yaml --size 1920x1080

# Force regenerate (jeśli hero już istnieje)
blog-agent generate-hero --config artykuly/seria/silos/slug/config.yaml --no-skip-existing
```

**Wynik:**
- Hero image 1920x1200: `artykuly/seria/silos/slug/images/hero.png`
- Sugestie innych obrazów: `artykuly/seria/silos/slug/multimedia.json`

### Alternatywnie: Auto-generate w workflow

Jeśli chcesz automatycznie podczas tworzenia artykułu:

Edytuj `blog_agent/config/workflow.yaml`:
```yaml
- name: multimedia
  enabled: true  # Włącz generowanie sugestii

- name: generate_images
  enabled: true  # Włącz auto-generation
  provider: "stability"
  model: "sdxl"
```

Potem:
```bash
blog-agent create --config artykuly/seria/silos/slug/config.yaml
```

---

## 🎨 Brand Style Guidelines

Wszystkie generowane obrazy są zgodne ze stylem digitalvantage.pl:

### Visual Style:
- **Typ:** Fotorealistyczny, profesjonalny, minimalistyczny
- **Mood:** Nowoczesny, tech-forward, B2B
- **Kompozycja:** Czysta, niezagęszczona, dużo przestrzeni

### Paleta Kolorów:
- **Podstawowe:** Czarny (#000000), biały (#FFFFFF), szary (różne odcienie)
- **Akcent:** Żółty (#FFCC00) - używany oszczędnie
- **Tła:** Białe lub jasno-szare

### Typowe Sceny:
- Profesjonalne biuro z naturalnym światłem
- Ludzie pracujący z technologią (laptop, tablet)
- Minimalistyczne tła, clean desk
- Muted colors, soft lighting

### Przykładowy Prompt (Hero):
```
"Professional business person working on laptop in modern minimalist office,
white walls, natural soft window lighting, clean desk with minimal items,
muted colors (black/white/gray), subtle yellow accent on notebook,
stock photo aesthetic, high quality, shallow depth of field"
```

---

## 📁 Struktura plików

```
artykuly/seria/silos/slug/
├── article.md
├── multimedia.json       # Sugestie multimediów
└── images/
    └── hero.png         # Wygenerowany automatycznie ✅
```

### multimedia.json - format

```json
{
  "hero_image": {
    "title": "Hero image - Tytuł artykułu",
    "description": "Opis obrazu",
    "alt_text": "SEO-friendly alt text",
    "prompt": "Professional photo of e-commerce business owner...",
    "generated": true,
    "local_path": "images/hero.png",
    "stock_suggestions": {
      "unsplash_query": "business owner laptop dashboard modern office",
      "pexels_query": "entrepreneur working computer professional",
      "keywords_for_search": ["e-commerce workspace", "online business"],
      "style_notes": "Modern office, natural lighting"
    }
  },
  "section_media": [
    {
      "type": "chart",
      "title": "Wykres wzrostu kar RODO",
      "prompt": "Clean bar chart showing RODO penalties growth...",
      "alt_text": "Wykres wzrostu kar RODO 2020-2024",
      "generated": false,
      "stock_suggestions": {
        "unsplash_query": "business growth chart statistics",
        "pexels_query": "financial chart data visualization",
        "keywords_for_search": ["infographic chart", "data viz"],
        "style_notes": "Clean professional chart. Use Canva or ChartJS."
      }
    }
  ]
}
```

---

## 🎨 Jak użyć sugestii stock photos

### Automatycznie wygenerowany hero
Hero jest już gotowy w `images/hero.png` - nic nie musisz robić!

### Inne obrazy - 3 opcje:

#### Opcja 1: Stock photos (FREE, najszybsze)

1. Otwórz `multimedia.json`
2. Znajdź `stock_suggestions` dla obrazu
3. Wklej `unsplash_query` lub `pexels_query` w:
   - [Unsplash](https://unsplash.com) (FREE, wysokiej jakości)
   - [Pexels](https://pexels.com) (FREE, różnorodne)
   - [Pixabay](https://pixabay.com) (FREE)

**Przykład:**
```json
"stock_suggestions": {
  "unsplash_query": "business owner laptop dashboard modern office"
}
```

Wejdź na Unsplash → wklej "business owner laptop dashboard modern office" → pobierz → zapisz jako `images/section-1.png`

#### Opcja 2: Wygeneruj AI (płatne)

Użyj `prompt` z `multimedia.json`:

**DALL-E (via ChatGPT Plus):**
```
1. Skopiuj "prompt" z multimedia.json
2. ChatGPT → DALL-E → wklej prompt
3. Pobierz obraz
```

**Midjourney:**
```
/imagine Professional photo of e-commerce business owner working on laptop...
```

**Stable Diffusion (lokalnie, FREE):**
- [Stability AI Playground](https://platform.stability.ai/sandbox)
- Lokalna instalacja Stable Diffusion WebUI

#### Opcja 3: Canva (custom design)

Dla wykresów/infografik użyj `style_notes`:
```json
"style_notes": "Vertical infographic, numbered steps with icons. Canva has templates."
```

1. [Canva.com](https://canva.com) → Templates → Infographic
2. Dostosuj według `style_notes`
3. Eksportuj PNG

---

## ⚙️ Konfiguracja

### Stability AI (rekomendowane - tanie)

**Uzyskaj API key:**
1. https://platform.stability.ai/account/keys
2. Stwórz konto → Generate API Key
3. Dodaj $10 credits (wystarczy na ~900 hero images!)

**Ustaw klucz:**
```bash
export STABILITY_API_KEY=sk-...
```

**Konfiguruj w workflow.yaml:**
```yaml
- name: generate_images
  enabled: true
  provider: "stability"
  model: "sdxl"          # sdxl ($0.011), sd3 ($0.037)
  width: 1024
  height: 1024
  steps: 40              # więcej = lepsza jakość
  cfg_scale: 7.0         # jak blisko promptu (1-20)
```

### DALL-E (alternatywa - droższa, lepsza jakość)

**Uzyskaj API key:**
1. https://platform.openai.com/api-keys
2. Create new secret key
3. Dodaj payment method

**Ustaw klucz:**
```bash
export OPENAI_API_KEY=sk-...
```

**Konfiguruj w workflow.yaml:**
```yaml
- name: generate_images
  enabled: true
  provider: "dalle"
  model: "dall-e-3"
  size: "1792x1024"      # 1024x1024, 1792x1024, 1024x1792
  quality: "standard"    # standard lub hd
```

---

## 💰 Porównanie kosztów

### 1 hero image:
| Provider | Model | Koszt | Jakość | Szybkość |
|----------|-------|-------|--------|----------|
| **Stability** | SDXL | **$0.011** | ⭐⭐⭐⭐ | ~5s |
| Stability | SD3 | $0.037 | ⭐⭐⭐⭐⭐ | ~8s |
| DALL-E 3 | Standard 1024px | $0.040 | ⭐⭐⭐⭐ | ~10s |
| DALL-E 3 | Standard 1792px | $0.080 | ⭐⭐⭐⭐⭐ | ~10s |
| DALL-E 3 | HD 1792px | $0.120 | ⭐⭐⭐⭐⭐ | ~15s |

### 100 artykułów (hero only):
| Provider | Koszt/miesiąc | Koszt/rok |
|----------|---------------|-----------|
| **Stability SDXL** | **$1.10** | **$13** ⭐ NAJTANIEJ |
| Stability SD3 | $3.70 | $44 |
| DALL-E 3 Standard | $4-8 | $48-96 |
| DALL-E 3 HD | $12 | $144 |

---

## 🔧 Troubleshooting

### "No image provider available"
**Problem:** Brak API key

**Rozwiązanie:**
```bash
# Sprawdź czy klucz jest ustawiony
echo $STABILITY_API_KEY
echo $OPENAI_API_KEY

# Ustaw klucz
export STABILITY_API_KEY=sk-...
```

### "API error 401: Invalid API Key"
**Problem:** Nieprawidłowy klucz

**Rozwiązanie:**
1. Sprawdź klucz na platform.stability.ai lub platform.openai.com
2. Upewnij się że skopiowałeś cały klucz (zaczyna się od `sk-`)
3. Sprawdź czy masz credits/payment method

### "Generation failed: Rate limit exceeded"
**Problem:** Zbyt wiele requestów

**Rozwiązanie:**
- Stability AI: 500 req/month na free tier → upgrade plan
- DALL-E: 50 req/min → poczekaj chwilę

### Hero wygląda źle
**Problem:** AI źle zinterpretował prompt

**Opcje:**
1. Usuń `images/hero.png` → uruchom ponownie (nowy prompt)
2. Użyj stock photo z `multimedia.json → stock_suggestions → unsplash_query`
3. Wygeneruj ręcznie w ChatGPT/Midjourney używając `prompt` z multimedia.json

---

## 📊 Przykładowy workflow

```bash
# 1. Ustaw API key (raz, na początku)
export STABILITY_API_KEY=sk-...

# 2. Włącz generate_images w workflow.yaml
# enabled: true

# 3. Generuj artykuł
blog-agent create --config artykuly/seria/silos/slug/config.yaml

# 4. Sprawdź wyniki
ls artykuly/seria/silos/slug/images/
# hero.png ✅

cat artykuly/seria/silos/slug/multimedia.json
# Sugestie innych obrazów ✅

# 5. Dodaj inne obrazy (opcjonalnie):
# - Stock photos z Unsplash (FREE)
# - Wygeneruj w ChatGPT/Midjourney
# - Stwórz w Canva
```

---

## 🎯 Best Practices

### Hero image
✅ **Zawsze generuj automatycznie** - to tylko $0.011-0.12, a artykuł wygląda profesjonalnie

### Section images (wykresy, diagramy)
✅ **Używaj Canva** - szybsze i bardziej custom niż AI
- Templates → Chart/Infographic
- Dostosuj kolory/dane
- Export PNG

### Section images (zdjęcia, scenki)
✅ **Stock photos** - FREE i wysokiej jakości
- Unsplash/Pexels query z `multimedia.json`
- Wyszukaj → Download → Rename → Done

### Screenshots
✅ **Rób własne** - prawdziwe screenshoty > AI generacje
- Zrób screenshot narzędzia
- Przytnij/adnotuj w Snagit/Lightshot
- Zapisz jako `images/screenshot-X.png`

---

## 📚 Dodatkowe zasoby

**FREE stock photos:**
- [Unsplash](https://unsplash.com) - najwyższa jakość
- [Pexels](https://pexels.com) - różnorodne
- [Pixabay](https://pixabay.com) - duża baza

**Design tools:**
- [Canva](https://canva.com) - infografiki, wykresy
- [Figma](https://figma.com) - profesjonalne mockupy
- [ChartJS](https://chartjs.org) - wykresy z kodu

**AI generators:**
- [DALL-E (ChatGPT)](https://chat.openai.com) - jeśli masz Plus
- [Midjourney](https://midjourney.com) - najlepsza jakość
- [Stability AI](https://platform.stability.ai/sandbox) - playground

---

**Pytania? Zobacz dokumentację providerów:**
- Stability AI: [docs](https://platform.stability.ai/docs)
- DALL-E: [docs](https://platform.openai.com/docs/guides/images)
