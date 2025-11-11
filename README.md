# Blog Agent

AI-powered blog article generation system for Digital Vantage.

## Features

- **Automated Article Generation**: 13-step workflow from outline to publication
- **Multi-Model Support**: Claude (Anthropic), Ollama (local models), OpenAI (planned)
- **AI Review**: Automatic quality checks (readability, word count, SEO)
- **Git Versioning**: Commits at key milestones
- **Hierarchical Categories**: 146 categories from YAML
- **Business Metadata**: Investment, timeline, complexity for entrepreneurs
- **SEO Optimization**: Meta tags, heading structure, Schema.org markup
- **CTA Generation**: Contextual "Co dalej?" sections
- **Multimedia Suggestions**: AI-generated image prompts
- **Local Models**: Ollama support for offline generation (llama3, mistral, codellama)

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

### workflow.yaml

Defines 13-step workflow with module paths and descriptions.

### providers.yaml

Configure AI providers (Claude, Ollama, OpenAI).

```yaml
providers:
  # Cloud API (Claude)
  claude:
    api_key: ${ANTHROPIC_API_KEY}
    model: claude-sonnet-4-20250514
    max_tokens: 4000
    temperature: 1.0

  # Local models (Ollama)
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
- `ollama_provider.py` - Local Ollama models
- `openai_provider.py` - OpenAI API (stub)

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

# Test Ollama integration
python test_ollama.py
```

### Validation Status

- ✅ **Steps 1-9**: Validated (outline, summary, sections, draft, SEO, humanize, multimedia, business metadata)
- ✅ **Step 10 (CTA)**: Validated with all template variables
- ✅ **Step 11 (Publish)**: Validated
- ✅ **Step 12 (Schema)**: Validated with 22 template variables
- ✅ **Step 13 (Categories)**: Validated
- ✅ **E2E Workflow**: Complete 1-13 workflow validated
  - Tested with claude-3-haiku-20240307 (cheap model)
  - Generated article: 4410 words, Flesch 39.1, 3 categories
  - All 13 steps completed successfully (~15 minutes)
- ✅ **Ollama Integration**: Tested with llama3:latest
  - Provider connection working
  - Text generation working
  - Note: Output format may differ from Claude

### Known Issues

- CLI `--only` option requires debugging (not critical - use test scripts as workaround)

## Documentation

- `REQUIREMENTS.md` - Complete specification (15 sections, 14-step workflow)
- `ARCHITECTURE.md` - Design patterns, DDD, SOLID principles
- `SESSION_NOTES.md` - Development history and decisions

## License

Proprietary - Digital Vantage

## Support

For issues or questions, contact the development team.
