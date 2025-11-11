# TODO List

## Current Session Tasks (2025-11-07)
- [x] Setup venv and install blog-agent CLI
- [x] Run end-to-end test #1 (identified truncation issue)
- [x] Fix CLI status command (PosixPath error)
- [x] Implement section-by-section humanization (121.8% preservation)
- [x] Fix multimedia step (missing variables)
- [x] Fix business metadata step (missing SILOS, SERIA)
- [x] Implement multimedia JSON parsing
- [x] Update documentation (README, ARCHITECTURE, SESSION_NOTES)

## Next Steps (Testing & Validation)
- [x] Fix CTA step CHECKLIST_NAME variable (added CHECKLIST_NAME and RELATED_ARTICLES)
- [x] Fix CTA step additional variables (INVESTMENT_RANGE, TIMEFRAME)
- [x] Add final missing template variables to CTA step (TOPIC, OPTIONAL_WARNING, OPTIONAL_NOTE)
- [x] Fix CTA step max_tokens (increased from 1000 to 3000)
- [x] Test CTA step with all fixes (COMPLETED - all variables working correctly)
- [x] Fix schema step missing variables (added all 22 template variables)
- [x] Test remaining steps: publish, schema, categories (ALL PASSED)
- [x] Validate complete 13-step workflow end-to-end (Haiku test passed)
- [ ] Fix CLI --only option (Click parsing issue - not critical)
- [ ] Test error resilience (workflow should continue on non-critical errors)
- [ ] Fix Python output buffering for real-time logs
- [ ] Performance benchmarking (target: 6-7 minutes per article)

## Future Enhancements - Multi-Model Support
- [x] Add Ollama local model support (llama3, mistral, codellama, etc.)
  - ✅ Implement Ollama provider class
  - ✅ Add to ProviderRegistry
  - ✅ Test with article generation
  - ✅ Documentation (OLLAMA_SETUP.md)
- [x] Add OpenAI provider support (gpt-4, gpt-4-turbo, gpt-3.5-turbo)
  - ✅ Implement OpenAI provider class (replaced stub)
  - ✅ Add to ProviderRegistry
  - ✅ Test with connection validation
  - ✅ Documentation and cost comparison
- [x] Add Google Gemini provider support (gemini-1.5-pro, gemini-1.5-flash)
  - ✅ Implement Gemini provider class
  - ✅ Add to ProviderRegistry
  - ✅ Test with connection validation
  - ✅ Documentation with free tier info
- [x] Model selection per article (already implemented in config)
  - ✅ Document model options in README
  - ✅ CLI option for model selection works (--provider flag)
  - ✅ 4 providers, 15+ models available

## Future Enhancements - Other
- [x] Add internal linking step (automatic article cross-references)
  - ✅ Implemented step_14_internal_linking.py
  - ✅ Finds related articles in same silo
  - ✅ AI suggests 3-5 contextual links with anchor text
  - ✅ Graceful handling when no good links exist
  - ✅ Added to workflow.yaml as step 14
  - ✅ Test script created (test_internal_linking.py)
- [ ] Improve error handling and rollback mechanism
- [ ] Add resume capability (restart from failed step)
- [ ] Add batch processing mode
- [ ] Add image generation integration (DALL-E/Midjourney)

## Backlog
- Image generation integration (Phase 2)
- Multi-language support (Phase 3)
- Batch processing (Phase 3)

## Completed

### Session 2025-11-06
- Git repository initialized
- Session tracking environment created
- Requirements gathering via Q&A
- Analysis of existing code and prompts
- Analysis of website structure (digitalvantage.pl)
- Reading categories from Excel (147 categories)
- **REQUIREMENTS.md created - Complete specification**
- **ARCHITECTURE.md created - Complete design**
- **Full implementation of 14-step workflow**

### Session 2025-11-07
- CLI status command fix (PosixPath error)
- Section-by-section humanization (121.8% content preservation)
- Multimedia step variable fix (KONSPEKT_TRESC, TARGET_AUDIENCE)
- Business metadata step variable fix (SILOS, SERIA extraction)
- Multimedia JSON parsing implementation (graceful fallback)
- Documentation updates (README, ARCHITECTURE, SESSION_NOTES)
- Steps 1-9 validated through end-to-end testing
- Model configuration moved to per-article config.yaml
- **Step 10 (CTA) complete fix:**
  - Added all template variables: TOPIC, OPTIONAL_WARNING, OPTIONAL_NOTE, CHECKLIST_NAME, RELATED_ARTICLES, INVESTMENT_RANGE, TIMEFRAME
  - Increased max_tokens from 1000 to 3000 (prevents AI response truncation)
  - Validated through isolated testing (test_cta.py)
- **Step 12 (Schema) complete fix:**
  - Added all 22 missing template variables (ARTICLE_URL, PUBLISH_DATE, MODIFIED_DATE, IMAGES, etc.)
  - Validated through isolated testing (test_schema.py)
- **Steps 11-13 validated:**
  - Step 11: Publish (marks article as published, creates git commit)
  - Step 12: Schema (generates schema.json with Schema.org markup)
  - Step 13: Categories (AI selects 1-5 categories, creates categories.yaml)

### Session 2025-11-11
- **E2E workflow validation:**
  - Complete 13-step workflow tested with claude-3-haiku-20240307 (tani model)
  - Generated article: 4410 words, Flesch 39.1, 3 categories
  - All steps completed successfully (outline → categories)
  - Time: ~15 minutes (on cheap model)
- **Ollama local model support:**
  - Implemented OllamaProvider class with full BaseAIProvider interface
  - Registered in ProviderRegistry
  - Added ollama>=0.6.0 to requirements.txt
  - Configured providers.yaml with multiple Ollama models
  - Created OLLAMA_SETUP.md with WSL configuration guide
  - Created test_ollama.py for integration testing
  - Successfully tested with llama3:latest (connection + text generation)
  - Available models: llama3, mistral, codellama (7b/13b), gemma3, phi3, gpt-oss
  - Usage: `blog-agent create --config path/config.yaml --provider ollama`
- **OpenAI provider support:**
  - Implemented OpenAIProvider class (replaced stub)
  - Full GPT-4, GPT-4 Turbo, GPT-3.5 Turbo support
  - Added openai>=1.0.0 to requirements.txt
  - Configured providers.yaml with 3 OpenAI variants
  - Created test_openai.py with cost comparison
  - Models: gpt-4o ($0.15), gpt-4-turbo ($0.30), gpt-3.5-turbo ($0.015/article)
  - Usage: `blog-agent create --config path/config.yaml --provider openai`
- **Google Gemini provider support:**
  - Implemented GeminiProvider class
  - Full Gemini 1.5 Pro, 1.5 Flash, Pro support
  - Added google-generativeai>=0.8.0 to requirements.txt
  - Configured providers.yaml with 3 Gemini variants
  - Created test_gemini.py with cost and free tier info
  - Models: gemini-1.5-pro ($0.10), gemini-1.5-flash ($0.01/article - cheapest!)
  - Free tier: 15 req/min, 1M tokens/day
  - Usage: `blog-agent create --config path/config.yaml --provider gemini`
- **Multi-provider summary:**
  - 4 AI providers: Claude, OpenAI, Gemini, Ollama
  - 15+ models available across all providers
  - Cost range: Free (Ollama) to $0.30/article (GPT-4)
  - Best value: Gemini 1.5 Flash ($0.01/article)
  - Best quality: Claude Sonnet 4 ($0.09/article)
- **Internal Linking (Step 14):**
  - Implemented step_14_internal_linking.py
  - Automatically finds related articles in same silo
  - Uses AI to suggest 3-5 contextual internal links
  - AI selects anchor text from existing article content
  - Validates anchor text exists before insertion
  - Graceful handling when articles aren't thematically related
  - Added to workflow.yaml as step 14
  - Created test_internal_linking.py for validation
  - Updated README.md and TODO.md documentation
  - Fixed bug: was searching parent.parent (series) instead of parent (silo)

---

## How to Use This File
- Add new tasks at the top of "Current Session Tasks"
- Move completed tasks to "Completed" section with date
- Use checkboxes [ ] for pending, [x] for done
- Keep this file updated throughout the session
- Review before ending session to document progress
