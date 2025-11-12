# Workflow Guide - Blog Agent

This document describes the 15-step article generation workflow and how to control it.

## 📋 Workflow Steps

The blog-agent follows a 15-step workflow to generate complete articles:

> **Note:** When you skip a step (using `--skip`), the system automatically loads existing files (like `outline.md`, `draft.md`, `article.md`) so subsequent steps can continue without errors.

### 1. **init** - Initialize Article Structure
Creates the article directory structure and basic files.

### 2. **outline** - Generate Article Outline
Creates `outline.md` with AI-generated structure.
- For **silo articles** (2-level path like `artykuly/series/silo/`), uses special silo prompt
- For **regular articles** (3-level path like `artykuly/series/silo/slug/`), uses standard prompt
- **Silo articles** automatically include FAQ section and links to sub-articles

### 3. **summary** - Generate Article Summary
Creates the "Co znajdziesz w artykule?" (What's in this article?) section.

### 4. **write_sections** - Write Article Sections
Writes all article sections based on outline, with AI quality review.

### 5. **create_draft** - Create Draft
Combines summary and sections into `draft.md`.

### 6. **seo_review** - SEO Review
Reviews and fixes SEO issues (headings, keywords, etc.).

### 7. **humanize** - Humanize Content
Makes content more natural and conversational.

### 8. **multimedia** - Generate Multimedia Suggestions
Creates `multimedia.json` with image/video suggestions.

### 9. **business_metadata** - Generate Business Metadata
Creates `business_metadata.yaml` with tags, focus keywords, etc.

### 10. **cta** - Generate CTA Section
Adds Call-To-Action / Next Steps section.

### 11. **publish** - Publish Article
Creates final `article.md` and marks as published.

### 12. **schema** - Generate Schema.org Markup
Creates `schema.json` with structured data for SEO.

### 13. **categories** - Assign Categories
Creates `categories.yaml` - assigns article to CMS categories.

### 14. **internal_linking** - Add Internal Links
Adds links to related articles in the same silo.

### 15. **generate_images** - Generate Images
(Disabled by default) Generates images using DALL-E or Stability AI.

## 🎯 Controlling Workflow Execution

### Basic Usage

```bash
# Run full workflow (all 15 steps)
python -m blog_agent create --config artykuly/ecommerce/seo/config.yaml
```

### Skip Specific Steps

```bash
# Skip single step
python -m blog_agent create --config path/config.yaml --skip outline

# Skip multiple steps (comma-separated)
python -m blog_agent create --config path/config.yaml --skip outline,init,seo_review
```

### Run Only Specific Steps

```bash
# Run only outline generation
python -m blog_agent create --config path/config.yaml --only outline

# Run only writing steps
python -m blog_agent create --config path/config.yaml --only write_sections,create_draft
```

## 🎭 Step Groups

For convenience, you can use predefined step groups:

### Available Groups

| Group | Included Steps | Use Case |
|-------|---------------|----------|
| **writing** | outline, summary, write_sections, create_draft | Skip all content creation (use existing drafts) |
| **post-processing** | seo_review, humanize | Skip content refinement |
| **metadata** | multimedia, business_metadata, schema, categories, internal_linking | Skip all metadata generation |
| **all-except-outline** | All steps except outline | Keep existing outline, regenerate everything else |

### Group Usage Examples

```bash
# Skip all writing steps (use existing content)
python -m blog_agent create --config path/config.yaml --skip writing

# Skip outline and all metadata
python -m blog_agent create --config path/config.yaml --skip outline,metadata

# Skip post-processing (keep draft as-is)
python -m blog_agent create --config path/config.yaml --skip post-processing

# Regenerate everything except outline
python -m blog_agent create --config path/config.yaml --skip all-except-outline
```

### Combining Groups and Individual Steps

```bash
# Skip writing group + specific step
python -m blog_agent create --config path/config.yaml --skip writing,cta

# Skip metadata group but keep categories
python -m blog_agent create --config path/config.yaml --skip multimedia,business_metadata,schema,internal_linking
```

## 📊 Common Workflows

### 1. Update Existing Article (Keep Outline)

```bash
# Regenerate content but keep outline.md
python -m blog_agent create --config path/config.yaml --skip outline
```

### 2. Only Generate Outline

```bash
# Just create outline.md (for review before full generation)
python -m blog_agent create --config path/config.yaml --only outline
```

### 3. Write Content From Existing Outline

```bash
# You have outline.md, generate rest of content
python -m blog_agent create --config path/config.yaml --skip init,outline
```

### 4. Only Metadata Updates

```bash
# Regenerate only metadata (use existing article.md)
python -m blog_agent create --config path/config.yaml --only metadata
```

### 5. Quick Draft (Skip All Extras)

```bash
# Just generate core content, no metadata/extras
python -m blog_agent create --config path/config.yaml --skip metadata,cta,internal_linking
```

### 6. Final Polish Only

```bash
# Article exists, just do final humanization and SEO
python -m blog_agent create --config path/config.yaml --only seo_review,humanize,publish
```

## 🔄 Workflow for Silo Articles

Silo articles (category hub pages) have special handling:

### What Makes a Silo Article?

- Path structure: `artykuly/[series]/[silo]/` (2 levels, no slug)
- Example: `artykuly/ecommerce/seo/`

### Silo-Specific Behavior

1. **Different Prompt**: Uses `prompt_konspekt_artykulu_silo.md`
2. **Article Detection**: Automatically finds sub-articles in the silo
3. **Required FAQ**: FAQ section is mandatory (not optional)
4. **Natural Linking**: Includes links to all sub-articles
5. **More Tokens**: Gets 3500 tokens vs 2000 for regular articles

### Creating a Silo Article

```bash
# 1. Initialize silo article
python -m blog_agent init artykuly/ecommerce/marketing

# 2. Edit config.yaml (set title, audience, tone)

# 3. Generate article (will auto-detect as silo)
python -m blog_agent create --config artykuly/ecommerce/marketing/config.yaml
```

The system will:
- Detect it's a silo article (no slug in path)
- Find existing sub-articles (like `marketing/google-ads`, `marketing/facebook-ads`)
- Generate outline with links to those articles
- Include comprehensive FAQ section

## 🎛️ Provider Selection

Choose AI provider for generation:

```bash
# Use Claude (default)
python -m blog_agent create --config path/config.yaml

# Use Ollama (local)
python -m blog_agent create --config path/config.yaml --provider ollama

# Use OpenAI
python -m blog_agent create --config path/config.yaml --provider openai

# Use Gemini
python -m blog_agent create --config path/config.yaml --provider gemini
```

## 📝 Configuration Files

### Article Config (`config.yaml`)

```yaml
title: "SEO w e-commerce - kompletny przewodnik"
target_audience: "Właściciele sklepów internetowych"
tone: "ekspercki, ale naturalny i rozmowny"
model: "claude-sonnet-4-20250514"
```

### Workflow Config (`blog_agent/config/workflow.yaml`)

Controls step behavior, quality thresholds, and default settings.

## 📏 Article Length Control

You can control article length at three levels:

### 1. Global Settings (workflow.yaml)

Controls default section length for all articles:

```yaml
# blog_agent/config/workflow.yaml
review:
  min_words: 300      # Minimum words per section
  max_words: 400      # Maximum words per section
  tolerance_percent: 10
```

### 2. Per-Article Target (config.yaml) ⭐ Recommended

Set target word count for individual articles:

```yaml
# artykuly/ecommerce/seo/config.yaml
title: "SEO w e-commerce"
target_audience: "Właściciele sklepów"
tone: "ekspercki, ale naturalny"
target_word_count: 2500  # Target total article length
```

**How it works:**
- System calculates optimal number of sections (e.g., 2500 words → 6-7 sections)
- Calculates words per section (~350-400 words/section)
- AI receives guidance: "Target length: ~380 words for this section"

**Example output:**
```bash
📏 Target: 2500 words → 7 sections × 357 words/section
```

**Common targets:**
- Short article: 1500-2000 words
- Standard article: 2500-3500 words
- Long article: 4000-5000 words
- Silo article (hub): 1500-2500 words

### 3. Manual Control

Edit `outline.md` to control sections:

```bash
# Generate outline only
python -m blog_agent create --config path/config.yaml --only outline

# Edit outline.md - add/remove sections

# Continue with edited outline
python -m blog_agent create --config path/config.yaml --skip outline
```

**📖 See [ARTICLE_LENGTH.md](ARTICLE_LENGTH.md) for detailed length configuration guide.**

## 🚨 Error Handling

If a step fails:
1. The workflow stops at the failed step
2. Error message is displayed
3. Fix the issue (e.g., edit outline.md manually)
4. Resume workflow by skipping completed steps

Example:
```bash
# Outline generation failed, fixed it manually
python -m blog_agent create --config path/config.yaml --skip outline
```

## 💡 Tips

1. **Always review outline first**: Run `--only outline` and review before full generation
2. **Set target_word_count**: Add `target_word_count: 2500` to config.yaml for length control
3. **Iterative refinement**: Run with `--skip` to regenerate specific parts
4. **Group shortcuts**: Use groups like `writing`, `metadata` for bulk operations
5. **Silo articles**: Create silo articles before sub-articles for better context
6. **Manual edits**: Feel free to edit generated files - skip those steps on next run

## 📚 Related Documentation

- [README.md](README.md) - Project overview and setup
- [ARTICLE_LENGTH.md](ARTICLE_LENGTH.md) - Article length configuration guide
- [ARCHITECTURE.md](ARCHITECTURE.md) - Technical architecture
- [OLLAMA_SETUP.md](OLLAMA_SETUP.md) - Local AI setup
