# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## System Overview

Blog Agent is an AI-powered **article generation system** that automates Polish blog creation through a 20-step workflow. The system uses Domain-Driven Design with clean architecture, supports 4 AI providers (Claude, OpenAI, Gemini, Ollama), and features automatic quality review with git versioning at milestones.

## Core Architecture

### Three-Layer Architecture

```
CLI (Click commands in cli/)
    ↓
Core Domain (Article aggregate, Value Objects, Workflow Engine in core/)
    ↓
Infrastructure (AI Providers, Git, Storage in infrastructure/)
```

**Key Principles:**
- **Article** is the Aggregate Root - all state flows through it
- **Step functions** are pure: `execute_step(article, deps, config) -> article`
- **Dependencies injected** via `deps` dict from `DependencyFactory`
- **Configuration in YAML**, never hardcoded in Python
- **Value Objects** are immutable domain concepts (Outline, SEOData, Summary, etc.)

### Multi-Provider AI System

**Provider Registry** (`infrastructure/ai/provider_registry.py`):
- Supports prefix matching: `openai-gpt4o`, `gemini-flash`, `gpt5`, etc.
- Auto-detects from model names: `gpt-4o` → `openai-gpt4o`, `gpt-5` → `openai-gpt5`
- Per-step provider override in `workflow.yaml`

**GPT-5 Models** (Released Aug 2025):
- `gpt-5` / `gpt5` / `openai-gpt5` - flagship reasoning model
- `gpt-5-mini` / `gpt5-mini` - faster and cheaper
- `gpt-5-nano` / `gpt5-nano` - smallest and cheapest
- GPT-5 uses internal reasoning tokens, supports only `temperature=1.0`
- Token limits auto-adjusted 5-10x for reasoning (e.g., 800 → 8000)

**Important:** Use `gemini-2.0-flash` for Polish content (2.5 has safety blocking issues documented in TODO.md).

### Workflow Engine

**20-step workflow** defined in `blog_agent/config/workflow.yaml`:

1. **init** - Create folder structure
2. **outline** - Generate article outline (git commit)
3. **summary** - "Co znajdziesz w artykule?" section
4. **write_sections** - Write 2-5 sections with quality review
5. **create_draft** - Combine summary + sections (git commit)
6. **seo_review** - Meta title/description validation
7. **humanize** - Section-by-section natural language refinement
8. **multimedia** - Suggest 4-9 multimedia elements
9. **business_metadata** - Investment, timeline, complexity
10. **cta** - "Co dalej?" section with silo article links
11. **publish** - Mark as published (git commit)
12. **schema** - Schema.org JSON-LD
13. **categories** - Select 1-5 from 146 categories (git commit)
14. **internal_linking** - Add 3-5 contextual links to silo articles
15. **generate_images** - DALL-E/Stability AI (optional, hero only)
16. **social_media** - Facebook/LinkedIn/Instagram posts
17. **faq** - FAQ section with semantic internal linking
18. **checklist** - Actionable checklist items
19. **headers_alternatives** - SEO header alternatives
20. **meta_alternatives** - Alternative meta proposals

**Key Features:**
- Automatic 529 API overload retry (3 attempts, 60s delays)
- Skip/resume capability via `--skip` or `--only` flags
- Auto-loads existing files when skipping steps
- Per-step provider configuration for cost/quality optimization

## File Structure Conventions

**Article Directory Structure:**
```
artykuly/[series]/[silo]/[slug]/
├── config.yaml              # User-created input
├── outline.md               # Step 2
├── sections/*.md            # Step 4
├── draft.md                 # Step 5
├── article.md               # Step 7 (final)
├── categories.yaml          # Step 13
├── social_media.md          # Step 16
├── faq.md                   # Step 17
├── checklist.md             # Step 18
└── images/hero.png          # Step 15
```

**URL = Folder structure (1:1 mapping):**
- Folder: `artykuly/ecommerce/operacje/bezpieczenstwo/`
- URL: `https://digitalvantage.pl/artykuly/ecommerce/operacje/bezpieczenstwo/`

**Git Commit Pattern:**
```
[series/silo/slug] Action

Example: [ecommerce/operacje/bezpieczenstwo] Publish article (2811 words)
```

Commits occur at key milestones: outline, draft, publish, categories, internal_linking, social_media.

## Development Commands

### Running Workflows

```bash
# Generate single article
python -m blog_agent create --config artykuly/ecommerce/operacje/slug/config.yaml

# With specific provider
python -m blog_agent create --config path/config.yaml --provider gpt5-mini

# Skip steps (for resume)
python -m blog_agent create --config path/config.yaml --skip outline,summary

# Only specific steps
python -m blog_agent create --config path/config.yaml --only faq,checklist
```

### Initialization

```bash
# Initialize entire series from article_structure.yaml
python -m blog_agent init --series strony-internetowe

# Initialize single article
python -m blog_agent init \
  --series ecommerce --silo operacje --slug bezpieczenstwo \
  --title "Bezpieczeństwo e-commerce" --audience "E-commerce owners"
```

### Status and Listing

```bash
python -m blog_agent list
python -m blog_agent list --series ecommerce
python -m blog_agent status --path artykuly/ecommerce/operacje/slug
```

## Step Implementation Pattern

Every step follows this template:

```python
def execute_step_name(article: Article, deps: Dict[str, Any], config: Dict[str, Any]) -> Article:
    """Step description"""
    # 1. Extract dependencies
    ai = deps['ai']
    prompts = deps['prompts']
    storage = deps['storage']
    git = deps['git']  # If git commit needed

    # 2. Check if can skip (file exists)
    output_path = article.path / "file.md"
    if output_path.exists():
        content = storage.read_file(output_path)
        article.set_value_object(ValueObject.from_markdown(content))
        return article

    # 3. Load & render prompt template
    prompt = prompts.load_and_render(
        "category/prompt_name.md",
        {
            'TEMAT_ARTYKULU': article.config.title,
            'TARGET_AUDIENCE': article.config.target_audience,
            'TONE': article.config.tone,
        }
    )

    # 4. Call AI provider
    response = ai.generate(prompt, max_tokens=4000)

    # 5. Parse to Value Object
    vo = ValueObject.from_markdown(response)

    # 6. Update article domain object
    article.set_value_object(vo)

    # 7. Save to disk
    storage.write_file(output_path, response)

    # 8. Optional: Git commit
    git.commit_article_stage(
        article.path,
        "step_name",
        f"Description ({count} items)"
    )

    return article
```

## Important Conventions

### Prompt Template Variables

Standard variables available in all prompts:
- `{{TEMAT_ARTYKULU}}` - Article title
- `{{TARGET_AUDIENCE}}` - Target audience
- `{{TONE}}` - Writing tone
- `{{KONSPEKT_TRESC}}` - Outline markdown
- `{{CURRENT_YEAR}}` - Auto-injected
- `{{CURRENT_DATE}}` - Auto-injected

### Quality Review Configuration

In `workflow.yaml`:
```yaml
review:
  min_words: 300          # Per section
  max_words: 400
  min_flesch: 40          # College level
  max_flesch: 60          # 8th-9th grade
  tolerance_percent: 10   # +/-10% flexibility
```

**Flesch Reading Ease:**
- 90-100: Very Easy (5th grade)
- 60-70: Easy (8th-9th grade)
- 30-50: Difficult (College level)
- 0-30: Very Difficult (Graduate)

### Content Preservation

Humanization uses **section-by-section processing** to achieve 110-182% word preservation (vs 62% with whole-document approach). Each section gets `max_tokens` calculated as `section_word_count * 2000/300`.

### Error Handling Patterns

**529 API Overload** (handled in WorkflowEngine):
- 3 retry attempts with 60-second delays
- Automatic detection via `_is_overloaded_error()`

**JSON Parsing with Markdown Cleanup:**
```python
try:
    data = json.loads(response)
except json.JSONDecodeError:
    # Strip markdown code blocks
    if response.startswith('```json'):
        response = response[7:-3]
    data = json.loads(response)
```

## Testing Individual Steps

```python
from blog_agent.core.workflow.steps.step_02_outline import execute_outline
from blog_agent.core.factory import DependencyFactory

# Setup
article = Article(path=Path("."), config=ArticleConfig(...))
factory = DependencyFactory(Path("."))
deps = factory.create_deps()

# Execute
result = execute_outline(article, deps, {})

# Verify
assert result.outline is not None
assert (article.path / "outline.md").exists()
```

## Git Commit Integration

**Steps that create git commits:**
- step_02_outline (outline)
- step_05_create_draft (draft)
- step_11_publish (publication)
- step_13_categories (categories)
- step_14_internal_linking (internal links)
- step_15_generate_images (hero image, if enabled)
- step_16_social_media (social media posts)

**Pattern:**
```python
git.commit_article_stage(
    article_path=article.path,
    stage_name="step_name",
    description="Action (count units)"
)
```

This creates commit: `[series/silo/slug] Action`

## Key Domain Objects

**Article** (`core/domain/article.py`):
- Aggregate Root with status tracking
- Methods: `set_outline()`, `add_section()`, `set_seo_data()`, etc.
- Status flow: initialized → outline_created → writing → draft_ready → seo_reviewed → humanized → published

**Value Objects** (`core/domain/value_objects.py`):
- **Outline** - Section structure with FAQ/Checklist flags
- **SEOData** - Meta title (<60 chars), description (<160 chars)
- **Summary** - 3-5 bullet points
- **BusinessMetadata** - Investment, timeline, complexity, team, ROI
- **InternalLinks** - Related article URLs with anchor text
- **CTASection** - Call-to-action with recommended articles
- **MultimediaSuggestion** - Hero image + section media suggestions
- **SchemaMarkup** - Schema.org JSON-LD (Article, FAQPage, HowTo)

**ArticleConfig** (`core/domain/config.py`):
- User input: title, target_audience, tone, model, target_word_count
- Derived from path: series, silo, slug

## Performance Characteristics

- **Time:** 7-8 minutes per article (Claude Sonnet 4)
- **Cost:** ~$0.09 (Claude), ~$0.10-0.20 (GPT-5 variants), ~$0.01 (Gemini Flash) per article
- **Quality:** Automatic review with 2-3 retry attempts
- **Word Preservation:** 110-182% in humanization step
- **Concurrency:** Can run parallel articles with GNU parallel

## Common Issues

| Issue | Solution |
|-------|----------|
| API key missing | Set env var: `export ANTHROPIC_API_KEY=sk-...` |
| Need to resume | Use `--skip` to skip completed steps |
| Gemini blocks Polish content | Use `gemini-2.0-flash` not `gemini-2.5-flash` |
| Word count validation fails | Increase `tolerance_percent` in workflow.yaml |
| Git commits fail | Run `git init` in repo root |
| 529 overload errors | Already handled with auto-retry |

## Architecture Documentation

For deeper architectural details, see:
- **ARCHITECTURE.md** - DDD patterns, layer responsibilities
- **REQUIREMENTS.md** - Complete specifications
- **TODO.md** - Recent work, known issues, future enhancements
- **README.md** - Quick start, features overview
- Use SOLID for code development