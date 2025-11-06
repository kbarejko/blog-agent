# Blog Agent

AI-powered blog article generation system for Digital Vantage.

## Features

- **Automated Article Generation**: 14-step workflow from outline to publication
- **AI Review**: Automatic quality checks (readability, word count, SEO)
- **Git Versioning**: Commits at key milestones
- **Hierarchical Categories**: 146 categories from YAML
- **Business Metadata**: Investment, timeline, complexity for entrepreneurs
- **SEO Optimization**: Meta tags, heading structure, Schema.org markup
- **CTA Generation**: Contextual "Co dalej?" sections
- **Multimedia Suggestions**: AI-generated image prompts

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
blog-agent create --config artykuly/ecommerce/operacje/bezpieczenstwo-rodo/config.yaml
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
6. **SEO Review** - Check headings, generate meta title/description
7. **Humanize** - Natural language transformation → article.md
8. **Multimedia** - Suggest 4-9 multimedia elements with DALL-E prompts
9. **Business Metadata** - Generate investment, timeline, complexity data
10. **CTA** - Create "Co dalej?" section with actionable steps
11. **Publish** - Mark as published, git commit
12. **Schema** - Generate Schema.org structured data (Article, FAQPage, HowTo)
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

Defines 14-step workflow with module paths and descriptions.

### providers.yaml

Configure AI providers (Claude, OpenAI).

```yaml
providers:
  claude:
    api_key: ${ANTHROPIC_API_KEY}
    model: claude-sonnet-4-20250514
    max_tokens: 4000
```

### payload.yaml (Optional)

Payload CMS v3 integration for publishing.

## Performance

- **Time**: ~6-7 minutes per article (5 sections, 3000 words)
- **Cost**: ~$0.09 per article (Claude Sonnet 4)
- **Quality**: Automatic review with 2 retry attempts per section

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

## Git Commits

Automatic commits at 4 key milestones:
- After outline creation
- After draft creation
- After article publication
- After category assignment

Format: `[series/silo/slug] Action`

## Testing

```bash
# Run with example article
blog-agent init --series test --silo example --slug test-article \
  --title "Test Article" --audience "Developers"

blog-agent create --config artykuly/test/example/test-article/config.yaml
```

## Documentation

- `REQUIREMENTS.md` - Complete specification (15 sections, 14-step workflow)
- `ARCHITECTURE.md` - Design patterns, DDD, SOLID principles
- `SESSION_NOTES.md` - Development history and decisions

## License

Proprietary - Digital Vantage

## Support

For issues or questions, contact the development team.
