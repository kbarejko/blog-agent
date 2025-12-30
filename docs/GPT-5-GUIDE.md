# GPT-5 Models Guide

## Overview

GPT-5 is OpenAI's latest generation AI model series. GPT-5 models are **reasoning models** that use internal reasoning tokens before generating output, making them particularly effective for complex tasks like coding and agentic workflows.

**Current version:** GPT-5.2 (December 2025)

## Available Models

### GPT-5.2 (Flagship) - Current
- **Model ID:** `gpt-5.2`
- **Aliases:** `gpt5`, `gpt-5`, `gpt-5.2`, `openai-gpt5`
- **Best for:** Complex content generation, high-quality writing, reasoning tasks
- **Max output tokens:** 128K (including reasoning tokens)

### GPT-5.2 Mini
- **Model ID:** `gpt-5.2-mini`
- **Aliases:** `gpt5-mini`, `gpt-5-mini`, `gpt-5.2-mini`, `openai-gpt5-mini`
- **Best for:** Humanization, SEO optimization, summaries
- **Faster and cheaper than GPT-5.2**

### GPT-5.2 Nano
- **Model ID:** `gpt-5.2-nano`
- **Aliases:** `gpt5-nano`, `gpt-5-nano`, `gpt-5.2-nano`, `openai-gpt5-nano`
- **Best for:** FAQ generation, quick tasks, metadata generation
- **Smallest and cheapest variant**

### Legacy GPT-5.1 (August 2025)
- **Model ID:** `gpt-5-2025-08-07`
- **Aliases:** `gpt-5.1`, `gpt-5.1-mini`, `gpt-5.1-nano`
- **Note:** Use explicit `gpt-5.1` alias to use legacy version

## Key Characteristics

### 1. Reasoning Tokens

GPT-5 models use **internal reasoning tokens** before generating output:

```
User Request → [Reasoning Phase] → [Output Phase]
                 (hidden tokens)     (visible response)
```

Both phases count toward the `max_completion_tokens` limit.

**Example:**
- Requested limit: 800 tokens
- Reasoning uses: ~7000 tokens
- Output uses: ~1000 tokens
- **Result:** Need 8000+ tokens total

### 2. Temperature Restriction

**GPT-5 only supports `temperature=1.0`** (default value).

❌ **This will fail:**
```python
client.chat.completions.create(
    model="gpt-5-2025-08-07",
    temperature=0.7  # Error: Unsupported value
)
```

✅ **This works:**
```python
client.chat.completions.create(
    model="gpt-5-2025-08-07"
    # temperature omitted (uses default 1.0)
)
```

### 3. Token Parameter

GPT-5 uses `max_completion_tokens` instead of `max_tokens`:

❌ **This will fail:**
```python
max_tokens=4000
```

✅ **This works:**
```python
max_completion_tokens=4000
```

## Auto-Adjustment in blog-agent

The `OpenAIProvider` automatically handles GPT-5 specifics:

### Token Limit Auto-Adjustment

When you request low token limits, they're automatically increased for GPT-5:

| Requested | Multiplier | Adjusted | Use Case |
|-----------|------------|----------|----------|
| < 1000 | x10 | 800 → 8,000 | Summary, metadata |
| 1000-3000 | x6 | 2,500 → 15,000 | Outline, FAQ |
| 3000-6000 | x4 | 4,000 → 16,000 | Headers, sections |
| 6000+ | x2 | 8,000 → 16,000 | Large content |

**Why?** Leaves room for both reasoning and output tokens.

### Temperature Handling

Temperature is automatically omitted for GPT-5 models (uses default 1.0).

### Parameter Selection

Automatically uses `max_completion_tokens` for GPT-5, `max_tokens` for older models.

## Usage Examples

### 1. Use in CLI

```bash
# Use GPT-5 as default provider
blog-agent create --config article/config.yaml --provider gpt5

# Use GPT-5 Mini
blog-agent create --config article/config.yaml --provider gpt5-mini
```

### 2. Use in workflow.yaml

```yaml
steps:
  - name: outline
    provider: gpt5-nano  # Fast and cheap

  - name: write_sections
    provider: gpt5  # High quality

  - name: humanize
    provider: gpt5-mini  # Good balance
```

### 3. Use in article config.yaml

```yaml
title: "My Article"
target_audience: "developers"
model: gpt-5.2  # Use GPT-5.2 for this article
```

## Setup

Set your OpenAI API key:

```bash
export OPENAI_API_KEY="sk-proj-..."
```

Or add to `~/.bashrc` for permanent setup:

```bash
echo 'export OPENAI_API_KEY="sk-proj-..."' >> ~/.bashrc
source ~/.bashrc
```

## Common Issues

### Empty Response / "finish_reason: length"

**Symptom:** Model returns empty content, finish_reason is "length"

**Cause:** Token limit too low - all tokens consumed by reasoning

**Solution:** Increase token limit (automatically handled in blog-agent)

### "Unsupported value: temperature"

**Symptom:** API error about temperature parameter

**Cause:** GPT-5 doesn't support custom temperature

**Solution:** Omit temperature or use 1.0 (automatically handled in blog-agent)

### "Unsupported parameter: max_tokens"

**Symptom:** API error about max_tokens parameter

**Cause:** GPT-5 uses max_completion_tokens

**Solution:** Use max_completion_tokens (automatically handled in blog-agent)

## Performance Comparison

| Model | Speed | Cost | Quality | Best For |
|-------|-------|------|---------|----------|
| **GPT-5** | Slow | $$$ | Excellent | Complex reasoning, high-quality content |
| **GPT-5 Mini** | Medium | $$ | Very Good | Humanization, SEO, summaries |
| **GPT-5 Nano** | Fast | $ | Good | FAQ, metadata, quick tasks |
| GPT-4o | Medium | $$ | Very Good | General purpose, proven reliability |
| Claude Sonnet 4 | Medium | $$ | Excellent | High-quality content, coding |

## Additional Resources

- [OpenAI GPT-5 Documentation](https://platform.openai.com/docs/models/gpt-5)
- [Introducing GPT-5 for developers](https://openai.com/index/introducing-gpt-5-for-developers/)
- [GPT-5 API Guide](https://www.cursor-ide.com/blog/gpt-5-api-guide)
- [OpenAI Responses API vs Chat Completions](https://platform.openai.com/docs/guides/responses-vs-chat-completions)

## Version History

- **August 2025:** GPT-5, GPT-5 Mini, GPT-5 Nano released
- **November 2025:** GPT-5.1 released (improved adaptive reasoning)
- **December 2025:** GPT-5.2 released (current default)
