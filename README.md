# Blog Agent

AI-powered blog article generation system for Digital Vantage.

## Features

- **Automated Article Generation**: 20-step workflow from outline to publication
- **Silo Article Support**: Special handling for category hub pages with automatic sub-article detection and FAQ
- **FAQ/Checklist Pipeline**: Separate mini-article pipeline with humanization and internal linking (50-70 word answers)
- **Per-Step Provider Configuration**: Use different AI models for different workflow steps (optimize cost vs. quality)
- **Flexible Workflow Control**: Skip steps or step groups (writing, metadata, post-processing)
- **Target Word Count**: Per-article length control (e.g., 2000, 3500, 5000 words) - automatically adjusts sections
- **Auto-Load Existing Files**: Skipped steps automatically load existing content (outline.md, draft.md, etc.)
- **Multi-Model Support**: Claude, OpenAI (GPT-4, GPT-5), Google Gemini, Ollama (local)
- **AI Review**: Automatic quality checks (readability, word count, SEO)
- **Git Versioning**: Commits at key milestones
- **Hierarchical Categories**: 146 categories from YAML
- **Business Metadata**: Investment, timeline, complexity for entrepreneurs
- **SEO Optimization**: Meta tags, heading structure, Schema.org markup
- **CTA Generation**: Contextual "Co dalej?" sections
- **Multimedia Suggestions**: AI-generated image prompts
- **Image Generation**: DALL-E 3 & Stability AI integration for automatic image creation (optional)
- **Internal Linking**: Automatic cross-references between related articles in silos
- **Local Models**: Ollama support for offline generation (llama3, mistral, codellama)
- **Multiple Providers**: 4 text AI providers + 2 image providers with 20+ model options

## Architecture

- **Domain-Driven Design**: Article as Aggregate Root with Value Objects
- **3-Layer Architecture**: Core / Infrastructure / Adapters
- **Step Functions**: Callable-based workflow (not classes)
- **Provider Registry**: Easy swapping of AI providers (Claude, OpenAI)
- **Configuration-Driven**: YAML workflow definition

## Installation

```bash
# Install dependencies
pip install -r requirements.txt

# Install blog-agent CLI
pip install -e .

# Set API key
export ANTHROPIC_API_KEY="your-api-key-here"
```

## Usage

### Initialize Article

```bash
blog-agent init \
  --series ecommerce \
  --silo operacje \
  --slug bezpieczenstwo-rodo \
  --title "Bezpieczeństwo i RODO w e-commerce" \
  --audience "Właściciele sklepów e-commerce"
```

### Generate Article

```bash
# Using default provider (Claude)
blog-agent create --config artykuly/ecommerce/operacje/bezpieczenstwo-rodo/config.yaml

# Using specific provider (explicit)
blog-agent create --config path/to/config.yaml --provider claude
blog-agent create --config path/to/config.yaml --provider gpt5            # GPT-5.2 (latest)
blog-agent create --config path/to/config.yaml --provider gpt5-mini       # GPT-5.2 Mini
blog-agent create --config path/to/config.yaml --provider openai-gpt4o     # GPT-4o
blog-agent create --config path/to/config.yaml --provider openai-gpt4o-mini # GPT-4o Mini
blog-agent create --config path/to/config.yaml --provider gemini
blog-agent create --config path/to/config.yaml --provider ollama
```

**Auto-Detection from config.yaml:**

The system automatically detects the provider from the `model` field in your article's `config.yaml`:

```yaml
# config.yaml
model: gpt-5.2      # Auto-detects gpt5 provider (GPT-5.2)
model: gpt-5.2-mini # Auto-detects gpt5-mini provider
model: gpt-4o                # Auto-detects openai-gpt4o provider
model: gpt-4o-mini           # Auto-detects openai-gpt4o-mini provider
model: gpt-4-turbo           # Auto-detects openai provider
model: gemini-2.5-pro        # Auto-detects gemini provider
model: claude-sonnet-4-20250514 # Uses claude provider (default)
```

No need to specify `--provider` when the model is in your config!

### Per-Step Provider Configuration

**NEW:** Configure different AI providers for different workflow steps!

Each step in `workflow.yaml` can use a different AI provider or model. This allows you to optimize for cost, speed, or quality at each stage:

```yaml
# blog_agent/config/workflow.yaml
steps:
  - name: outline
    module: blog_agent.core.workflow.steps.step_02_outline
    enabled: true
    provider: gemini  # Fast and cheap for structure generation
    
  - name: write_sections
    module: blog_agent.core.workflow.steps.step_04_write_sections
    enabled: true
    model: claude-sonnet-4-20250514  # Best quality for content
    
  - name: humanize
    module: blog_agent.core.workflow.steps.step_07_humanize
    enabled: true
    model: gpt-4o  # Excellent at natural language refinement
```

**Benefits:**
- 💰 **Cost optimization**: Use cheaper models for simpler tasks (outline, FAQ)
- ⚡ **Speed**: Use faster models where quality matters less
- 🎯 **Quality**: Use best models where it counts (content writing)
- 🔄 **Flexibility**: Mix providers based on their strengths

**Example configurations:**

```yaml
# Budget-friendly: Gemini for everything
steps:
  - name: outline
    provider: gemini-flash
  - name: write_sections
    provider: gemini-flash
  - name: humanize
    provider: gemini-flash
# Cost: ~$0.02 per article

# Balanced: Gemini for structure, Claude for content
steps:
  - name: outline
    model: gemini-2.5-flash
  - name: write_sections
    model: claude-sonnet-4-20250514
  - name: humanize
    model: gemini-2.5-pro
# Cost: ~$0.12 per article

# Premium: Claude for everything
steps:
  - name: outline
    provider: claude
  - name: write_sections
    provider: claude
  - name: humanize
    provider: claude
# Cost: ~$0.15 per article

# GPT-5 Reasoning: Best quality, higher cost
steps:
  - name: outline
    provider: gpt5-nano  # Fast and cheap for structure
  - name: write_sections
    provider: gpt5       # Highest quality reasoning
  - name: humanize
    provider: gpt5-mini  # Good balance for refinement
# Cost: ~$0.20-0.30 per article (reasoning models use more tokens)
```

If a step doesn't specify a provider/model, it uses the default from CLI (`--provider`) or article config.


**Available Providers:**

| Provider | Model | Quality | Speed | Cost |
|----------|-------|---------|-------|------|
| `claude` | Claude Sonnet 4 | ⭐⭐⭐⭐⭐ | Fast | $$ |
| `gpt5` / `gpt-5.2` | GPT-5.2 (reasoning) | ⭐⭐⭐⭐⭐ | Slow | $$$ |
| `gpt5-mini` / `gpt-5.2-mini` | GPT-5.2 Mini (reasoning) | ⭐⭐⭐⭐ | Medium | $$ |
| `gpt5-nano` / `gpt-5.2-nano` | GPT-5.2 Nano (reasoning) | ⭐⭐⭐⭐ | Fast | $ |
| `openai-gpt4o` | GPT-4o | ⭐⭐⭐⭐⭐ | Fast | $$ |
| `openai-gpt4o-mini` | GPT-4o Mini | ⭐⭐⭐⭐ | Very Fast | $ |
| `openai` | GPT-4 Turbo | ⭐⭐⭐⭐ | Medium | $$ |
| `gemini` | Gemini 2.5 Pro | ⭐⭐⭐⭐ | Fast | $ |
| `gemini-flash` | Gemini 2.5 Flash | ⭐⭐⭐⭐ | Very Fast | $ |
| `ollama` | Llama 3 | ⭐⭐ | Slow | Free |

**Note:** GPT-5 models are reasoning models that use internal reasoning tokens before generating output. Token limits are automatically adjusted 5-10x higher. See [GPT-5 Guide](docs/GPT-5-GUIDE.md) for details.

Configure providers in `blog_agent/config/providers.yaml`

### Check Status

```bash
blog-agent status --path artykuly/ecommerce/operacje/bezpieczenstwo-rodo/
```

### List Articles

```bash
blog-agent list
blog-agent list --series ecommerce
```

## Helper Scripts

The repository includes several helper scripts for batch processing and testing:

### Batch Processing

**Generate all articles** (skip existing):
```bash
./generate_all_articles.sh                    # Process all articles
./generate_all_articles.sh artykuly/ecommerce # Process only ecommerce series
```

Features:
- Finds all `config.yaml` files in specified directory
- Skips articles that already have `article.md`
- Shows progress counter and summary
- Handles errors gracefully

**Load environment variables** before running commands:
```bash
./run_with_env.sh blog-agent create --config path/to/config.yaml
./run_with_env.sh python test_hero_generation.py
```

Automatically loads `.env` file and passes environment to command.

### Testing Scripts

**Test hero image generation**:
```bash
python test_hero_generation.py  # Test DALL-E 3 hero generation
```

**Test multimedia with stock suggestions**:
```bash
python test_multimedia_stock.py  # Test multimedia.json with stock_suggestions
```

**Test Stability AI**:
```bash
python test_stability_ai.py  # Test Stability AI (SDXL) integration
```

**Other test scripts**:
- `test_gemini.py` - Test Gemini API integration
- `test_ollama.py` - Test Ollama local models
- `test_openai.py` - Test OpenAI GPT models
- `test_internal_linking.py` - Test internal linking step
- `test_cta.py` - Test CTA generation
- `test_schema.py` - Test Schema.org generation

## Workflow Steps

1. **Init** - Create folder structure
2. **Outline** - Generate article outline (main sections only - FAQ/Checklist have separate outlines)
3. **Summary** - Create "Co znajdziesz w artykule?" (3-5 value points)
4. **Write Sections** - Write all sections with AI review (300-400 words, Flesch 40-60)
5. **Create Draft** - Combine summary + sections → draft.md
6. **SEO Review** - Check headings, generate meta title/description (with retry logic, max 3 attempts, improved validation)
7. **Humanize** - Section-by-section natural language transformation (prevents truncation, 121% content preservation) → article.md
8. **Multimedia** - Suggest 4-9 multimedia elements with DALL-E prompts (JSON parsing with graceful fallback)
9. **Business Metadata** - Generate investment, timeline, complexity data (extracts series/silo from path)
10. **CTA** - Create "Co dalej?" section with actionable steps (all template variables, 3000 max_tokens)
11. **Publish** - Mark as published, git commit
12. **Schema** - Generate Schema.org structured data with 22 template variables (Article, FAQPage, HowTo)
13. **Categories** - AI selects 1-5 categories from 146 available
14. **Internal Linking** - Automatically add 3-5 internal links to related articles in the same silo (AI-driven anchor selection)
15. **Generate Images** - Generate images with DALL-E 3 or Stability AI from multimedia prompts (optional, disabled by default)
16. **Social Media** - Generate social media posts (Facebook/LinkedIn/Instagram) with hooks, alternative titles, and hashtags (saved as Markdown)
17. **FAQ** - Generate FAQ section with 5-8 questions and semantic internal linking to related articles (separate faq.md file with faq_outline.md)
18. **Checklist** - Generate actionable checklist with 8-12 items and humanization (separate checklist.md file with checklist_outline.md)
19. **Headers Alternatives** - Generate 3-4 SEO-optimized alternatives for all H1/H2/H3 headers, including long-tail variants (optional, disabled by default)
20. **Meta Alternatives** - Generate 2-3 alternative proposals for meta title and meta description for A/B testing and SEO optimization (uses cheap model: gpt-4o-mini)

### Advanced Workflow Control

**Skip steps** to use existing content:
```bash
# Skip outline (use existing outline.md)
blog-agent create --config path/config.yaml --skip outline

# Skip multiple steps with groups
blog-agent create --config path/config.yaml --skip writing,metadata
```

**Available step groups:**
- `writing` - outline, summary, write_sections, create_draft
- `post-processing` - seo_review, humanize
- `metadata` - multimedia, business_metadata, schema, categories, internal_linking
- `all-except-outline` - Everything except outline (keeps existing outline.md)

**📖 See [WORKFLOW.md](WORKFLOW.md) for complete workflow documentation, examples, and tips.**

## Article Structure

```
artykuly/
├── [series]/              # e.g., ecommerce, saas
│   ├── [silo]/            # e.g., operacje, platformy
│   │   ├── [slug]/
│   │   │   ├── config.yaml
│   │   │   ├── outline.md
│   │   │   ├── sections/
│   │   │   │   ├── 00-summary.md
│   │   │   │   ├── 01-section.md
│   │   │   │   ├── 02-section.md
│   │   │   │   └── ...
│   │   │   ├── draft.md
│   │   │   ├── article.md          # Final
│   │   │   ├── categories.yaml
│   │   │   ├── business_metadata.yaml
│   │   │   ├── multimedia.json
│   │   │   └── schema.json
```

**URL = Folder structure (1:1)**
- Folder: `artykuly/ecommerce/operacje/bezpieczenstwo-rodo/`
- URL: `https://www.digitalvantage.pl/artykuly/ecommerce/operacje/bezpieczenstwo-rodo/`

## Configuration

### Article Configuration (config.yaml)

Each article has its own `config.yaml` file that controls content generation.

**Location:** `artykuly/{series}/{silo}/{slug}/config.yaml`

**Required Fields:**
```yaml
title: "Your Article Title"
target_audience: "Who this article is for"
tone: "ekspercki, ale naturalny i rozmowny"
model: "claude-sonnet-4-20250514"  # AI model (auto-detects provider)
```

**Optional Fields:**
```yaml
target_word_count: 2500  # Target article length (e.g., 2000, 3500, 5000)
meta_title: "SEO meta title (auto-generated if empty)"
meta_description: "SEO meta description (auto-generated if empty)"
```

**Example:**
```yaml
title: Linkowanie wewnętrzne w e-commerce - jak zwiększyć sprzedaż i SEO
target_audience: Właściciele sklepów internetowych i specjaliści e-commerce
tone: ekspercki, ale naturalny i rozmowny
model: gpt-4o
target_word_count: 2000
meta_title: ""
meta_description: ""
```

**Model Options:**
- `claude-sonnet-4-20250514` - Claude Sonnet 4 (best quality, recommended)
- `gpt-5.2` - OpenAI GPT-5.2 (flagship reasoning model)
- `gpt-5.2-mini` - OpenAI GPT-5.2 Mini (faster reasoning)
- `gpt-5.2-nano` - OpenAI GPT-5.2 Nano (cheapest reasoning)
- `gpt-4o` - OpenAI GPT-4o (previous generation, still capable)
- `gpt-4o-mini` - OpenAI GPT-4o Mini (faster, cheaper)
- `gemini-2.5-pro` - Google Gemini 2.5 Pro (most capable)
- `gemini-2.5-flash` - Google Gemini 2.5 Flash (fast, cheap)
- `gemini-2.0-flash` - Google Gemini 2.0 Flash (recommended for Polish content)
- `llama3:latest` - Local Ollama (requires setup, free)

⚠️ **Note:** Gemini 2.5 models may block Polish educational content due to safety filters. Use `gemini-2.0-flash` for Polish content.

**Tone Guidelines:**
- `ekspercki, ale naturalny i rozmowny` - Expert but conversational (default)
- `techniczny i szczegółowy` - Technical and detailed
- `przyjazny dla początkujących` - Beginner-friendly
- Custom tone - describe your preferred style

**Target Audience Examples:**
- `Właściciele sklepów internetowych i specjaliści e-commerce`
- `Przedsiębiorcy i właściciele firm`
- `Programiści i zespoły techniczne`
- `Startup founders i product managers`

**Auto-Generation:**
When using `./create_articles_tree.sh -c`, config.yaml is created with:
- Title auto-generated from article slug
- Default target audience: "Przedsiębiorcy i właściciele firm"
- Default tone: "ekspercki, ale naturalny i rozmowny"
- Default model: "claude-sonnet-4-20250514"
- Empty meta fields (filled during SEO step)

### workflow.yaml

Defines 20-step workflow with module paths and descriptions.

**Quality Review Configuration:**

The `review` section controls section quality validation during article generation:

```yaml
review:
  min_words: 300      # Minimum words per section
  max_words: 400      # Maximum words per section
  min_flesch: 40      # Minimum Flesch Reading Ease (40 = college level)
  max_flesch: 60      # Maximum Flesch Reading Ease (60 = 8th-9th grade)
  tolerance_percent: 0  # Tolerance margin (0-20%, adds flexibility to limits)
```

**Tolerance Parameter:**
The `tolerance_percent` adds flexibility to all limits. For example, with `tolerance_percent: 10`:
- `min_words: 300` → accepts 270+ words (300 - 10%)
- `max_words: 400` → accepts up to 440 words (400 + 10%)
- `min_flesch: 40` → accepts 36+ (40 - 10%)
- `max_flesch: 60` → accepts up to 66 (60 + 10%)

**Recommended values:**
- `0%` - Strict validation (default)
- `5-10%` - Balanced (recommended for most use cases)
- `15-20%` - Lenient (more AI freedom)

**Flesch Reading Ease Scale:**
- 90-100: Very Easy (5th grade)
- 60-70: Easy (8th-9th grade)
- 30-50: Difficult (College level)
- 0-30: Very Difficult (University graduate)

**Defaults work well for most business articles. Adjust if:**
- Writing technical docs → lower min_flesch (30-40)
- Writing beginner content → raise min_flesch (50-60)
- Need longer sections → raise max_words (500-600)
- Content often "almost passes" → add tolerance (5-10%)

### providers.yaml

Configure AI providers (Claude, OpenAI, Gemini, Ollama).

The system supports **provider prefixes** for fine-grained control. For example:
- `openai-gpt4o` → uses `gpt-4o` model with OpenAI provider
- `openai-gpt4o-mini` → uses `gpt-4o-mini` model with OpenAI provider
- `gemini-flash` → uses `gemini-2.5-flash` model with Gemini provider

Configure each variant in `providers.yaml`:

```yaml
providers:
  # Claude (Anthropic) - Best quality
  claude:
    api_key: ${ANTHROPIC_API_KEY}
    model: claude-sonnet-4-20250514
    max_tokens: 4000
    temperature: 1.0

  # OpenAI - GPT-4o (latest and most capable)
  openai-gpt4o:
    api_key: ${OPENAI_API_KEY}
    model: gpt-4o
    max_tokens: 4000
    temperature: 0.7

  # OpenAI - GPT-4o Mini (faster, cheaper)
  openai-gpt4o-mini:
    api_key: ${OPENAI_API_KEY}
    model: gpt-4o-mini
    max_tokens: 4000
    temperature: 0.7

  # OpenAI - GPT-4 Turbo
  openai:
    api_key: ${OPENAI_API_KEY}
    model: gpt-4-turbo
    max_tokens: 4000
    temperature: 0.7

  # Google Gemini - Fast and cheap
  gemini:
    api_key: ${GOOGLE_API_KEY}
    model: gemini-2.5-pro
    max_tokens: 8000
    temperature: 0.9

  # Ollama - Local models (free)
  ollama:
    model: llama3:latest
    host: http://192.168.0.136:11434
    max_tokens: 4000
    temperature: 0.7
```

**Auto-Detection:**
When you set `model: gpt-4o` in your article's `config.yaml`, the system automatically:
1. Normalizes the model name (`gpt-4o` → `gpt4o`)
2. Detects the provider prefix (`openai-gpt4o`)
3. Loads the matching provider config from `providers.yaml`
4. Uses the `OpenAIProvider` class with the configured settings

No need to manually specify `--provider` on the command line!

### Ollama Setup

For local model generation with Ollama, see [OLLAMA_SETUP.md](OLLAMA_SETUP.md) for WSL configuration.

Available Ollama models:
- `llama3:latest` (4.7 GB) - Meta Llama 3
- `mistral:latest` (4.1 GB) - Mistral 7B
- `codellama:13b` (7.4 GB) - Code Llama 13B
- `phi3:mini` (2.2 GB) - Microsoft Phi-3 (fastest)
- And more (see `ollama list`)

### Image Generation Setup

Step 15 generates images using AI providers (disabled by default). Supports **DALL-E** and **Stability AI**.

#### Option 1: DALL-E (OpenAI)

**Setup:**
```bash
# 1. Get OpenAI API key from https://platform.openai.com/api-keys
export OPENAI_API_KEY='sk-...'

# 2. Enable step in workflow.yaml (set enabled: true)

# 3. Run workflow with image generation
blog-agent create --config path/config.yaml
```

**Cost:**
- DALL-E 3 Standard (1792x1024): $0.08 per image
- DALL-E 3 HD (1792x1024): $0.12 per image
- DALL-E 2 (1024x1024): $0.02 per image

For typical article (6 images):
- **DALL-E 3 Standard: ~$0.48 per article**
- **DALL-E 2: ~$0.12 per article**

#### Option 2: Stability AI (Recommended for cost)

**Setup:**
```bash
# 1. Get API key from https://platform.stability.ai/
export STABILITY_API_KEY='sk-...'

# 2. Enable step in workflow.yaml (set enabled: true)
# 3. Uncomment Stability AI settings in workflow.yaml

# 4. Run workflow with image generation
blog-agent create --config path/config.yaml
```

**Cost:**
- SDXL: $0.011 per image **(Best value!)**
- SD3: $0.037 per image
- SD3.5 Large: $0.065 per image

For typical article (6 images):
- **SDXL: ~$0.07 per article** (55% cheaper than DALL-E 2!)
- **SD3: ~$0.22 per article**

**Configuration in workflow.yaml:**
```yaml
- name: generate_images
  enabled: true  # Enable image generation
  # Provider auto-detected from OPENAI_API_KEY or STABILITY_API_KEY

  # For DALL-E:
  model: "dall-e-3"  # dall-e-2, dall-e-3
  size: "1792x1024"  # 1024x1024, 1792x1024, 1024x1792
  quality: "standard"  # standard, hd

  # For Stability AI (uncomment to use):
  # model: "sdxl"  # sdxl, sd3, sd3-medium
  # width: 1024
  # height: 1024
  # steps: 40
  # cfg_scale: 7.0

  skip_existing: true
```

**Testing:**
```bash
# Test DALL-E
python test_image_generation.py

# Test Stability AI
python test_stability_ai.py
```

### SEO Headers Alternatives (Optional)

Generate 3-4 SEO-optimized alternatives for all H1, H2, H3 headers in your articles. Each header gets alternative proposals including long-tail variants.

**Quick Start:**
```bash
# Single article
blog-agent create --config path/config.yaml --only headers_alternatives

# All articles in directory
./generate_headers_alternatives_all.sh artykuly/ecommerce

# Python version (cross-platform)
python generate_headers_alternatives_all.py artykuly/ecommerce/seo
```

**Output:** Creates `headers_alternatives.md` in each article directory with format:
```markdown
# Original: Your Article Title

**Propozycje SEO:**
1. Short variant with keyword
2. Natural SEO-friendly version
3. Detailed long-tail variant describing exactly what the article covers (LONG TAIL)
4. Variant with numbers or data

---

## Original: Section Header

**Propozycje SEO:**
1. ...
```

**Enable in workflow:** Set `enabled: true` in `blog_agent/config/workflow.yaml` for automatic generation.

**Documentation:** See [README_HEADERS_ALTERNATIVES.md](README_HEADERS_ALTERNATIVES.md) for complete guide, batch processing, and cost estimates.

### AI Provider Comparison

| Provider | Model | Cost/Article | Speed | Quality | Notes |
|----------|-------|--------------|-------|---------|-------|
| **Claude** | Sonnet 4 | $0.09 | Fast | ⭐⭐⭐⭐⭐ | Best quality |
| **Claude** | Haiku | $0.02 | Very Fast | ⭐⭐⭐⭐ | Cheap, good |
| **OpenAI** | GPT-5 | $0.20 | Medium | ⭐⭐⭐⭐⭐ | Reasoning model |
| **OpenAI** | GPT-5 Mini | $0.10 | Fast | ⭐⭐⭐⭐⭐ | Cost-effective reasoning |
| **OpenAI** | GPT-5 Nano | $0.05 | Very Fast | ⭐⭐⭐⭐ | Cheapest reasoning |
| **OpenAI** | GPT-4o | $0.15 | Fast | ⭐⭐⭐⭐⭐ | Previous generation |
| **Gemini** | 2.5 Pro | $0.10 | Fast | ⭐⭐⭐⭐ | Large context |
| **Gemini** | 2.5 Flash | $0.01 | Very Fast | ⭐⭐⭐⭐ | Best value! |
| **Gemini** | 2.0 Flash | $0.01 | Very Fast | ⭐⭐⭐⭐ | Best for Polish |
| **Ollama** | llama3 | Free | Slow | ⭐⭐⭐ | Offline, free |

**Recommendation (Text):**
- **Production**: Claude Sonnet 4 or GPT-5 Mini (best quality)
- **Budget**: Gemini 2.5 Flash (best value)
- **Polish content**: Gemini 2.0 Flash (avoids safety blocks)
- **Testing**: Ollama llama3 (free, offline)

### Image Provider Comparison

| Provider | Model | Cost/Image | Cost/Article (6 imgs) | Quality | Notes |
|----------|-------|------------|----------------------|---------|-------|
| **Stability AI** | SDXL | $0.011 | **$0.07** | ⭐⭐⭐⭐ | **Best value!** |
| **Stability AI** | SD3 | $0.037 | $0.22 | ⭐⭐⭐⭐⭐ | High quality |
| **Stability AI** | SD3.5 Large | $0.065 | $0.39 | ⭐⭐⭐⭐⭐ | Premium |
| **OpenAI** | DALL-E 2 | $0.020 | $0.12 | ⭐⭐⭐⭐ | Good value |
| **OpenAI** | DALL-E 3 Std | $0.040-0.080 | $0.48 | ⭐⭐⭐⭐⭐ | Best quality |
| **OpenAI** | DALL-E 3 HD | $0.080-0.120 | $0.72 | ⭐⭐⭐⭐⭐ | Premium |

**Recommendation (Images):**
- **Production**: Stability AI SDXL (best value, great quality)
- **Premium**: DALL-E 3 or Stability AI SD3 (highest quality)
- **Budget**: Stability AI SDXL (cheapest option)

### payload.yaml (Optional)

Payload CMS v3 integration for publishing.

## Performance

- **Time**: ~6-7 minutes per article (Claude Sonnet 4), ~15 minutes (Haiku)
- **Cost**:
  - Claude Sonnet 4: ~$0.09 per article
  - Claude Haiku: ~$0.02 per article
  - Ollama (local): Free (uses local compute)
- **Quality**: Automatic review with 2 retry attempts per section
- **SEO Validation**: 3-attempt retry with intelligent fallback (120-160 char descriptions)
- **Humanization**: Section-by-section processing with 121-134% content preservation
  - Processes each section individually (2000-8000 tokens per section)
  - Prevents text truncation in long articles (>2500 words)
  - Real-time progress tracking per section
  - Maintains 110-182% word preservation rate across sections
- **Multimedia Parsing**: Intelligent JSON extraction with error handling
  - Handles markdown-wrapped JSON responses (```json blocks)
  - Separates hero image (subtype='hero') from section media
  - Graceful fallback to placeholder if parsing fails
- **Multi-Model Support**:
  - Claude: Best quality, faster generation
  - Ollama: Free, offline, good for testing
  - Note: Local models may produce different output formats

## Categories

- **Source**: `categories.yaml` (146 hierarchical categories)
- **Selection**: AI selects 1-5 best matches after article completion
- **Format**: Git-friendly YAML (no Excel dependency)

## Development

### Project Structure

```
blog_agent/
├── core/
│   ├── domain/              # Article, Value Objects, Config
│   ├── workflow/            # Engine, Step functions
│   └── services/            # PromptLoader, ReviewService, CategoryMatcher
├── infrastructure/
│   ├── ai/                  # AI providers (Claude, OpenAI)
│   ├── storage/             # File operations
│   ├── git/                 # Git wrapper
│   ├── yaml/                # Category reader
│   └── cms/                 # Payload adapter
├── adapters/
│   └── cli/                 # CLI commands
└── config/
    ├── workflow.yaml
    ├── providers.yaml
    └── payload.yaml
```

### Adding New Steps

1. Create step file: `blog_agent/core/workflow/steps/step_XX_name.py`
2. Implement: `execute_name(article, deps, config) -> article`
3. Add to `workflow.yaml`

### Adding New AI Provider

1. Create provider: `blog_agent/infrastructure/ai/provider_name.py`
2. Extend `BaseAIProvider`
3. Register in `ProviderRegistry`
4. Add config to `providers.yaml`

Example providers:
- `claude_provider.py` - Anthropic Claude API
- `openai_provider.py` - OpenAI GPT models
- `gemini_provider.py` - Google Gemini models
- `ollama_provider.py` - Local Ollama models

## Git Commits

Automatic commits at 4 key milestones:
- After outline creation
- After draft creation
- After article publication
- After category assignment

Format: `[series/silo/slug] Action`

## Testing

### Full Workflow Test

```bash
# Initialize test article
blog-agent init --series test --silo example --slug test-article \
  --title "Test Article" --audience "Developers"

# Run complete workflow
blog-agent create --config artykuly/test/example/test-article/config.yaml
```

### Individual Step Testing

```bash
# Test CTA step (step 10)
python test_cta.py

# Test Schema step (step 12)
python test_schema.py

# Test steps 11-13 (publish, schema, categories)
python test_remaining_steps.py

# Test Internal Linking step (step 14)
python test_internal_linking.py

# Test Image Generation step (step 15)
python test_image_generation.py  # DALL-E
python test_stability_ai.py      # Stability AI

# Test Social Media step (step 16)
python test_social_media.py

# Test Ollama integration
python test_ollama.py

# Test OpenAI integration
python test_openai.py

# Test Gemini integration
python test_gemini.py
```

### Validation Status

- ✅ **Steps 1-9**: Validated (outline, summary, sections, draft, SEO, humanize, multimedia, business metadata)
- ✅ **Step 10 (CTA)**: Validated with all template variables
- ✅ **Step 11 (Publish)**: Validated
- ✅ **Step 12 (Schema)**: Validated with 22 template variables
- ✅ **Step 13 (Categories)**: Validated
- ✅ **Step 14 (Internal Linking)**: Validated
  - Finds related articles in same silo
  - Uses AI to suggest anchor text from existing content
  - Gracefully handles cases where no good links exist
  - Works best with thematically related articles
- ✅ **Step 15 (Image Generation)**: Implemented (requires OPENAI_API_KEY)
  - Generates images using DALL-E 3 or DALL-E 2
  - Reads prompts from multimedia.json
  - Saves images to images/ folder
  - Updates multimedia.json with local paths
  - Disabled by default (opt-in, costs money)
  - Test script: test_image_generation.py
- ✅ **Step 16 (Social Media)**: Validated
  - Generates social media posts for Facebook/LinkedIn/Instagram
  - Creates 80±5 char hook-based post
  - Provides 4 alternative titles with strong hooks
  - Generates first comment with bullets, link, acronym explanations, and 10 hashtags
  - Targets non-technical business owners (25-55)
  - Outputs to social_media.md (readable Markdown format)
  - Test script: test_social_media.py
- ✅ **E2E Workflow**: Complete 1-20 workflow validated
  - Tested with claude-3-haiku-20240307 (cheap model)
  - Generated article: 4410 words, Flesch 39.1, 3 categories
  - All 20 steps completed successfully (~7-8 minutes)
  - Step 15 (images) is optional add-on
- ✅ **Ollama Integration**: Tested with llama3:latest
  - Provider connection working
  - Text generation working
  - Note: Output format may differ from Claude
- ✅ **OpenAI Integration**: Implemented and tested
  - Full GPT-4, GPT-4 Turbo, GPT-3.5 support
  - Test script validates API key and connection
  - Ready for production use
- ✅ **Gemini Integration**: Implemented and tested
  - Gemini 1.5 Pro, 1.5 Flash, Pro support
  - Test script validates API key and connection
  - Free tier available (1M tokens/day)
- ✅ **Stability AI Integration**: Implemented (not yet tested)
  - SDXL, SD3, SD3-Medium, SD3-Large-Turbo support
  - Test script created: test_stability_ai.py
  - Auto-detection based on STABILITY_API_KEY
  - 55% cheaper than DALL-E for images

### Known Issues

- **Gemini 2.5 blocks Polish content**: Gemini 2.5 (Flash & Pro) may block Polish educational content with empty safety_ratings. Use `gemini-2.0-flash` as a workaround (older model, stable, no false positives).

### Future Enhancements

**Image Generation:**
- **Midjourney Integration** - Waiting for official API release
  - Currently no public API available (Discord-only access)
  - Unofficial APIs exist but violate Terms of Service
  - Will integrate when Midjourney releases official API
  - Expected to provide industry-leading image quality

**Workflow Improvements:**
- Error resilience testing (workflow should continue on non-critical errors)
- Resume capability (restart from failed step)
- Batch processing mode (generate multiple articles in one run)
- Performance benchmarking (optimize for 6-7 minute target)

**Content Features:**
- Video generation integration (when APIs become available)
- Audio/podcast generation from articles
- Multi-language support (automatic translation)
- A/B testing for headlines and CTAs

## Documentation

- `REQUIREMENTS.md` - Complete specification (15 sections, 20-step workflow)
- `ARCHITECTURE.md` - Design patterns, DDD, SOLID principles
- `WORKFLOW.md` - Workflow guide with step descriptions and groups
- `SESSION_NOTES.md` - Development history and decisions

## License

Proprietary - Digital Vantage

## Support

For issues or questions, contact the development team.
