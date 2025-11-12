# Blog Agent

AI-powered blog article generation system for Digital Vantage.

## Features

- **Automated Article Generation**: 15-step workflow from outline to publication
- **Multi-Model Support**: Claude, OpenAI (GPT-4), Google Gemini, Ollama (local)
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

# Using specific provider
blog-agent create --config path/to/config.yaml --provider claude
blog-agent create --config path/to/config.yaml --provider openai
blog-agent create --config path/to/config.yaml --provider gemini
blog-agent create --config path/to/config.yaml --provider ollama
```

### Check Status

```bash
blog-agent status --path artykuly/ecommerce/operacje/bezpieczenstwo-rodo/
```

### List Articles

```bash
blog-agent list
blog-agent list --series ecommerce
```

## Workflow Steps

1. **Init** - Create folder structure
2. **Outline** - Generate article outline with optional sections (Checklist, FAQ)
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
15. **Generate Images** - Generate images with DALL-E 3 from multimedia prompts (optional, disabled by default)

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
model: "claude-sonnet-4-20250514"
```

**Optional Fields:**
```yaml
meta_title: "SEO meta title (auto-generated if empty)"
meta_description: "SEO meta description (auto-generated if empty)"
```

**Example:**
```yaml
title: Linkowanie wewnętrzne w e-commerce - jak zwiększyć sprzedaż i SEO
target_audience: Właściciele sklepów internetowych i specjaliści e-commerce
tone: ekspercki, ale naturalny i rozmowny
model: claude-sonnet-4-20250514
meta_title: ""
meta_description: ""
```

**Model Options:**
- `claude-sonnet-4-20250514` - Best quality (recommended)
- `claude-3-haiku-20240307` - Faster, cheaper
- `gpt-4-turbo` - OpenAI alternative
- `gemini-1.5-pro` - Google alternative
- `llama3:latest` - Local Ollama (requires setup)

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

Defines 15-step workflow with module paths and descriptions.

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

```yaml
providers:
  # Claude (Anthropic) - Best quality
  claude:
    api_key: ${ANTHROPIC_API_KEY}
    model: claude-sonnet-4-20250514
    max_tokens: 4000
    temperature: 1.0

  # OpenAI - GPT models
  openai:
    api_key: ${OPENAI_API_KEY}
    model: gpt-4-turbo
    max_tokens: 4000
    temperature: 0.7

  # Google Gemini - Fast and cheap
  gemini:
    api_key: ${GOOGLE_API_KEY}
    model: gemini-1.5-pro
    max_tokens: 8000
    temperature: 0.9

  # Ollama - Local models (free)
  ollama:
    model: llama3:latest
    host: http://192.168.0.136:11434
    max_tokens: 4000
    temperature: 0.7
```

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

### AI Provider Comparison

| Provider | Model | Cost/Article | Speed | Quality | Notes |
|----------|-------|--------------|-------|---------|-------|
| **Claude** | Sonnet 4 | $0.09 | Fast | ⭐⭐⭐⭐⭐ | Best quality |
| **Claude** | Haiku | $0.02 | Very Fast | ⭐⭐⭐⭐ | Cheap, good |
| **OpenAI** | GPT-4 Turbo | $0.30 | Fast | ⭐⭐⭐⭐⭐ | Expensive |
| **OpenAI** | GPT-3.5 | $0.015 | Very Fast | ⭐⭐⭐ | Cheapest cloud |
| **Gemini** | 1.5 Pro | $0.10 | Fast | ⭐⭐⭐⭐ | Large context |
| **Gemini** | 1.5 Flash | $0.01 | Very Fast | ⭐⭐⭐⭐ | Best value! |
| **Ollama** | llama3 | Free | Slow | ⭐⭐⭐ | Offline, free |

**Recommendation (Text):**
- **Production**: Claude Sonnet 4 (best quality)
- **Budget**: Gemini 1.5 Flash (best value)
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
- ✅ **E2E Workflow**: Complete 1-14 workflow validated
  - Tested with claude-3-haiku-20240307 (cheap model)
  - Generated article: 4410 words, Flesch 39.1, 3 categories
  - All 14 steps completed successfully (~15 minutes)
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

- None currently (all previous issues resolved)

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

- `REQUIREMENTS.md` - Complete specification (15 sections, 14-step workflow)
- `ARCHITECTURE.md` - Design patterns, DDD, SOLID principles
- `SESSION_NOTES.md` - Development history and decisions

## License

Proprietary - Digital Vantage

## Support

For issues or questions, contact the development team.
