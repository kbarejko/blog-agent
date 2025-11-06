# Blog Agent - Architecture Documentation

**Version:** 2.0
**Date:** 2025-01-06
**Status:** Design phase - ready for implementation

---

## 1. Architecture Overview

### 1.1 Layered Architecture (3 warstwy)

```
┌─────────────────────────────────────────────┐
│              CLI / Adapters                 │
│  • blog_agent.py (Click CLI)                │
│  • payload_adapter.py (CMS integration)     │
└────────────────┬────────────────────────────┘
                 │
┌────────────────▼────────────────────────────┐
│         Core (Domain + Orchestration)       │
│  • Article (Aggregate Root)                 │
│  • Value Objects (Outline, SEO, etc.)       │
│  • Workflow Engine                          │
│  • Step Functions (callables)               │
│  • Domain Services                          │
└────────────────┬────────────────────────────┘
                 │
┌────────────────▼────────────────────────────┐
│           Infrastructure                    │
│  • AI Providers (Claude, OpenAI)            │
│  • Git Operations                           │
│  • File Storage                             │
│  • YAML Reader (categories)                 │
│  • Payload CMS API                          │
└─────────────────────────────────────────────┘
```

**Zasady:**
- **Core** - logika domenowa, niezależna od infrastructure
- **Infrastructure** - konkretne implementacje (AI, Git, CMS)
- **Adapters** - porty wejścia/wyjścia (CLI, API)

### 1.2 SOLID Principles

1. **Single Responsibility** - każdy step function robi jedną rzecz
2. **Open/Closed** - nowe steps/providers bez modyfikacji core
3. **Liskov Substitution** - AIProvider protocol (Claude ↔ OpenAI)
4. **Interface Segregation** - małe, focused interfaces
5. **Dependency Inversion** - core depends on abstractions, not concretions

---

## 2. Project Structure

```
blog_agent/
├── cli.py                          # Entry point (Click CLI)
├── config.yaml                     # Main configuration
├── pyproject.toml                  # Dependencies (Poetry/pip)
│
├── core/                           # Domain + Orchestration
│   ├── __init__.py
│   ├── domain/                     # Domain model (DDD)
│   │   ├── __init__.py
│   │   ├── article.py              # Article (Aggregate Root)
│   │   ├── value_objects/
│   │   │   ├── __init__.py
│   │   │   ├── outline.py          # Outline VO
│   │   │   ├── seo_data.py         # SEOData VO
│   │   │   ├── summary.py          # Summary VO
│   │   │   ├── business_metadata.py # BusinessMetadata VO
│   │   │   └── related_article.py  # RelatedArticle VO
│   │   └── exceptions.py           # Custom exceptions
│   │
│   ├── workflow.py                 # Workflow Engine
│   ├── steps/                      # Step implementations (callables)
│   │   ├── __init__.py
│   │   ├── step_01_outline.py
│   │   ├── step_02_summary.py
│   │   ├── step_03_linking.py
│   │   ├── step_04_write_intro.py
│   │   ├── step_05_write_sections.py
│   │   ├── step_06_draft.py
│   │   ├── step_07_seo_review.py
│   │   ├── step_08_humanize.py
│   │   ├── step_09_multimedia.py
│   │   ├── step_10_business_metadata.py
│   │   ├── step_11_cta.py
│   │   ├── step_12_publish.py
│   │   ├── step_13_schema.py
│   │   └── step_14_categories.py
│   │
│   └── services/                   # Domain services
│       ├── __init__.py
│       ├── prompt_loader.py        # Load & render prompts
│       ├── review_service.py       # AI review logic
│       └── category_matcher.py     # Match categories from YAML
│
├── infrastructure/                 # Concrete implementations
│   ├── __init__.py
│   ├── ai/
│   │   ├── __init__.py
│   │   ├── base.py                 # AIProvider Protocol
│   │   ├── claude_provider.py      # Claude implementation
│   │   └── openai_provider.py      # OpenAI implementation
│   ├── storage/
│   │   ├── __init__.py
│   │   └── file_storage.py         # File system operations
│   ├── git/
│   │   ├── __init__.py
│   │   └── git_ops.py              # Git wrapper
│   ├── yaml/
│   │   ├── __init__.py
│   │   └── category_reader.py      # Read categories.yaml
│   └── cms/
│       ├── __init__.py
│       └── payload_adapter.py      # Payload CMS v3 API
│
├── adapters/                       # Adapters (ports)
│   ├── __init__.py
│   └── payload/
│       ├── __init__.py
│       ├── transformer.py          # Article → Payload format
│       └── blocks.py               # Block definitions
│
├── config/                         # Configuration files
│   ├── workflow.yaml               # Workflow steps definition
│   ├── providers.yaml              # AI providers config
│   └── payload.yaml                # Payload CMS config
│
├── prompts/                        # Prompt templates (już istnieje)
│   ├── konspekt/
│   ├── articles/
│   ├── audyt/
│   └── metadata/
│
├── tests/                          # Tests
│   ├── unit/
│   ├── integration/
│   └── fixtures/
│
└── artykuly/                       # Generated articles (output)
    └── [seria]/[silos]/[slug]/
```

---

## 3. Domain Model (DDD)

### 3.1 Article (Aggregate Root)

```python
@dataclass
class Article:
    """
    Aggregate Root - represents article lifecycle

    Responsibilities:
    - Maintain article state consistency
    - Enforce business rules
    - Provide domain operations

    All modifications go through methods (not direct field access)
    """
    path: Path
    config: ArticleConfig

    # Value Objects (immutable)
    outline: Optional[Outline] = None
    seo_data: Optional[SEOData] = None
    summary: Optional[Summary] = None
    business_metadata: Optional[BusinessMetadata] = None

    # Content
    sections: List[str] = field(default_factory=list)
    draft_content: Optional[str] = None
    final_content: Optional[str] = None

    # Metadata
    related_articles: List[RelatedArticle] = field(default_factory=list)
    multimedia: List[dict] = field(default_factory=list)
    categories: List[str] = field(default_factory=list)
    schema_json: Optional[dict] = None

    # State tracking
    completed_steps: List[str] = field(default_factory=list)
    created_at: datetime = field(default_factory=datetime.now)
    updated_at: datetime = field(default_factory=datetime.now)

    # === Domain operations ===

    def set_outline(self, outline: Outline) -> None:
        """Set outline with validation"""
        if not isinstance(outline, Outline):
            raise ValueError("Must be Outline value object")
        self.outline = outline
        self._mark_updated()

    def add_section(self, content: str) -> None:
        """Add section to article"""
        self.sections.append(content)
        self._mark_updated()

    def assemble_draft(self) -> str:
        """Assemble draft from parts"""
        parts = [
            f"# {self.config.title}\n",
            self.summary.to_markdown() if self.summary else "",
            *self.sections
        ]
        self.draft_content = "\n\n".join(filter(None, parts))
        return self.draft_content

    def finalize(self, content: str) -> None:
        """Set final content after humanization"""
        self.final_content = content
        self._mark_updated()

    def complete_step(self, step_name: str) -> None:
        """Mark step as completed"""
        if step_name not in self.completed_steps:
            self.completed_steps.append(step_name)
            self._mark_updated()

    def is_step_completed(self, step_name: str) -> bool:
        """Check if step completed"""
        return step_name in self.completed_steps

    def _mark_updated(self) -> None:
        """Mark article as updated"""
        self.updated_at = datetime.now()

    # === Persistence ===

    def save_to_disk(self) -> None:
        """Save current state to disk"""
        if self.outline:
            (self.path / "outline.md").write_text(self.outline.to_markdown())
        if self.draft_content:
            (self.path / "draft.md").write_text(self.draft_content)
        if self.final_content:
            (self.path / "article.md").write_text(self.final_content)
        # ... save other artifacts

    @classmethod
    def load_from_disk(cls, path: Path) -> 'Article':
        """Load article from disk"""
        # Load config.yaml
        import yaml
        config_data = yaml.safe_load((path / "config.yaml").read_text())
        config = ArticleConfig(**config_data)

        # Create article
        article = cls(path=path, config=config)

        # Load existing artifacts
        if (path / "outline.md").exists():
            content = (path / "outline.md").read_text()
            article.outline = Outline.from_markdown(content)
            article.completed_steps.append("outline")

        # ... load other artifacts

        return article
```

### 3.2 Value Objects

#### Outline

```python
@dataclass(frozen=True)
class OutlineSection:
    """Single section in outline"""
    level: int  # 2, 3, 4 (H2, H3, H4)
    title: str
    key_points: List[str]

@dataclass(frozen=True)
class Outline:
    """Article outline"""
    sections: List[OutlineSection]
    has_checklist: bool
    has_faq: bool

    def to_markdown(self) -> str:
        """Export to markdown"""
        lines = []
        for section in self.sections:
            prefix = "#" * section.level
            lines.append(f"{prefix} {section.title}")
            for point in section.key_points:
                lines.append(f"- {point}")
        return "\n\n".join(lines)

    @classmethod
    def from_markdown(cls, content: str) -> 'Outline':
        """Parse from markdown"""
        # Implementation: parse markdown structure
        pass
```

#### SEOData

```python
@dataclass(frozen=True)
class SEOData:
    """SEO metadata"""
    meta_title: str  # max 60 chars
    meta_description: str  # max 160 chars
    keywords: List[str]

    def __post_init__(self):
        """Validate on creation"""
        if len(self.meta_title) > 60:
            raise ValueError("meta_title too long")
        if len(self.meta_description) > 160:
            raise ValueError("meta_description too long")
        if len(self.keywords) < 3:
            raise ValueError("need at least 3 keywords")
```

#### Summary

```python
@dataclass(frozen=True)
class SummaryPoint:
    """Single point in summary"""
    bold_phrase: str  # 2-4 words
    description: str  # 1 sentence

@dataclass(frozen=True)
class Summary:
    """'Co znajdziesz w artykule?' summary"""
    points: List[SummaryPoint]  # 3-5 points

    def __post_init__(self):
        if not (3 <= len(self.points) <= 5):
            raise ValueError("Summary must have 3-5 points")

    def to_markdown(self) -> str:
        lines = ["## Co znajdziesz w artykule?\n"]
        for point in self.points:
            lines.append(f"- **{point.bold_phrase}** - {point.description}")
        return "\n".join(lines)

    @classmethod
    def from_markdown(cls, content: str) -> 'Summary':
        """Parse from markdown"""
        # Parse markdown list with bold phrases
        pass
```

#### BusinessMetadata

```python
from enum import Enum

class InvestmentLevel(Enum):
    NONE = "none"
    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"
    VERY_HIGH = "very_high"

@dataclass(frozen=True)
class BusinessMetadata:
    """Business metadata for entrepreneurs"""
    target_business: List[str]  # ["startup", "scale-up", "enterprise"]
    industry: List[str]  # ["ecommerce", "saas", etc.]
    project_phase: List[str]  # ["planowanie", "wdrożenie", etc.]
    investment: dict  # {level, range, breakdown}
    timeline: dict  # {estimate, phases}
    complexity: dict  # {technical, organizational}
    team_requirements: dict  # {size, roles}
    roi: Optional[dict]  # {breakeven, savings, factors}

    def to_yaml(self) -> str:
        """Export to YAML"""
        import yaml
        return yaml.dump(self.__dict__, allow_unicode=True, default_flow_style=False)

    @classmethod
    def from_yaml(cls, content: str) -> 'BusinessMetadata':
        """Load from YAML"""
        import yaml
        data = yaml.safe_load(content)
        return cls(**data)
```

---

## 4. Workflow Engine

### 4.1 Workflow Engine (Orchestrator)

```python
from typing import Callable, List, Dict, Any
from dataclasses import dataclass

# Type alias
StepFunction = Callable[[Article, Dict[str, Any], Dict[str, Any]], Article]

@dataclass
class WorkflowStep:
    """
    Lightweight step definition (configuration + callable)

    Nie klasa implementująca logikę, tylko config wskazujący na funkcję
    """
    name: str
    function: StepFunction  # Callable function
    prompt_path: Optional[str] = None
    git_commit: bool = False
    commit_message: Optional[str] = None
    config: Dict[str, Any] = field(default_factory=dict)

    def execute(self, article: Article, dependencies: Dict[str, Any]) -> Article:
        """Execute step function with dependencies"""
        return self.function(article, dependencies, self.config)


class WorkflowEngine:
    """
    Lightweight orchestrator

    Single Responsibility: execute steps in order
    Open/Closed: add new steps without modifying engine
    """

    def __init__(self, steps: List[WorkflowStep]):
        self.steps = steps

    def execute(
        self,
        article: Article,
        dependencies: Dict[str, Any],
        start_from: Optional[str] = None,
        stop_at: Optional[str] = None
    ) -> Article:
        """
        Execute workflow steps

        Args:
            article: Article aggregate
            dependencies: Injected dependencies (ai, git, storage, prompts, etc.)
            start_from: Resume from step (for partial execution)
            stop_at: Stop before step (for testing)

        Returns:
            Updated article
        """
        started = start_from is None

        for step in self.steps:
            # Skip until we reach start_from
            if not started:
                if step.name == start_from:
                    started = True
                else:
                    print(f"⏭️  Skipping {step.name} (starting from {start_from})")
                    continue

            # Stop if reached stop_at
            if stop_at and step.name == stop_at:
                print(f"⏹️  Stopping before {step.name}")
                break

            # Skip if already completed (resume capability)
            if article.is_step_completed(step.name):
                print(f"⏭️  Skipping {step.name} (already completed)")
                continue

            # Execute step
            print(f"🔄 Executing {step.name}...")

            try:
                article = step.execute(article, dependencies)
                article.complete_step(step.name)
                article.save_to_disk()

                # Git commit if configured
                if step.git_commit:
                    git = dependencies['git']
                    msg = step.commit_message or f"{step.name} completed"
                    git.commit(article.path, msg)

                print(f"✅ Completed {step.name}")

            except Exception as e:
                print(f"❌ Error in {step.name}: {e}")
                raise

        return article
```

### 4.2 Step Functions (Callables)

**Pattern: każdy step to funkcja z sygnaturą:**

```python
def execute_step(
    article: Article,
    deps: Dict[str, Any],
    config: Dict[str, Any]
) -> Article:
    """
    Step function pattern

    Args:
        article: Current article state (Aggregate Root)
        deps: Injected dependencies (ai, git, prompts, storage)
        config: Step-specific config from workflow.yaml

    Returns:
        Updated article
    """
    pass
```

**Example: Step 1 - Outline**

```python
# core/steps/step_01_outline.py

from core.domain.article import Article
from core.domain.value_objects.outline import Outline
from typing import Dict, Any

def execute_outline(
    article: Article,
    deps: Dict[str, Any],
    config: Dict[str, Any]
) -> Article:
    """
    Generate article outline

    Inputs:
    - article.config.title
    - article.config.target_audience
    - article.config.tone

    Outputs:
    - article.outline (Outline VO)
    - article.seo_data (SEOData VO)
    """
    ai = deps['ai']
    prompts = deps['prompts']

    # Load & render prompt
    prompt = prompts.load_and_render(
        "konspekt/prompt_konspekt_artykulu.md",
        {
            "TEMAT_ARTYKULU": article.config.title,
            "TARGET_AUDIENCE": article.config.target_audience,
            "TONE": article.config.tone,
            "URL_ARTYKULU": f"/artykuly/{article.config.series}/{article.config.silo}/{article.config.slug}"
        }
    )

    # Generate with AI
    response = ai.generate(prompt)

    # Parse response to Value Objects
    outline = Outline.from_markdown(response)
    seo_data = SEOData.from_markdown(response)  # AI generates both in one call

    # Update article (domain operations)
    article.set_outline(outline)
    article.set_seo_data(seo_data)

    return article
```

**Example: Step 5 - Write Sections (loop)**

```python
# core/steps/step_05_write_sections.py

def execute_write_sections(
    article: Article,
    deps: Dict[str, Any],
    config: Dict[str, Any]
) -> Article:
    """
    Write all remaining sections (loop)

    Loops through outline sections 2-N
    Reviews each section with AI review service
    """
    ai = deps['ai']
    prompts = deps['prompts']
    review_service = deps['review']

    # Get sections from outline (skip intro, already done)
    sections_to_write = article.outline.sections[1:]

    for i, section in enumerate(sections_to_write, start=2):
        print(f"  Writing section {i}/{len(sections_to_write)+1}: {section.title}")

        # Render prompt
        prompt = prompts.load_and_render(
            "articles/prompt_artykul_kontynuacja.md",
            {
                "KONSPEKT_TRESC": article.outline.to_markdown(),
                "SEKCJA_TYTUL": section.title,
                "SEKCJA_PUNKTY": "\n".join(f"- {p}" for p in section.key_points),
                "OSTATNIA_SEKCJA": article.sections[-1] if article.sections else "",
                "WYTYCZNE_WSPOLNE": prompts.load("articles/prompt_artykul_common.md"),
                "RELATED_ARTICLES": article.related_articles  # For contextual links
            }
        )

        # Generate section
        section_content = ai.generate(prompt)

        # Review (with auto-fix if needed)
        section_content = review_service.review_and_fix(
            section_content,
            criteria={
                "min_words": config.get('min_words', 300),
                "max_words": config.get('max_words', 400),
                "flesch_min": 40,
                "flesch_max": 60
            },
            max_retries=2
        )

        # Add to article
        article.add_section(section_content)

    return article
```

---

## 5. Infrastructure Layer

### 5.1 AI Provider (Protocol)

```python
# infrastructure/ai/base.py

from typing import Protocol, Dict, Any

class AIProvider(Protocol):
    """
    Protocol for AI providers

    Benefits:
    - Duck typing (no ABC overhead)
    - Easy to swap implementations (Claude ↔ OpenAI)
    - Dependency Inversion Principle
    """

    def generate(
        self,
        prompt: str,
        system_prompt: str = None,
        **kwargs
    ) -> str:
        """Generate text from prompt"""
        ...

    def generate_json(
        self,
        prompt: str,
        schema: Dict[str, Any] = None,
        **kwargs
    ) -> Dict[str, Any]:
        """Generate structured JSON output"""
        ...
```

**Claude Implementation:**

```python
# infrastructure/ai/claude_provider.py

from anthropic import Anthropic

class ClaudeProvider:
    """Claude AI provider implementation"""

    def __init__(self, api_key: str, model: str = "claude-sonnet-4-20250514"):
        self.client = Anthropic(api_key=api_key)
        self.model = model

    def generate(self, prompt: str, system_prompt: str = None, **kwargs) -> str:
        """Generate text"""
        messages = [{"role": "user", "content": prompt}]

        response = self.client.messages.create(
            model=self.model,
            messages=messages,
            system=system_prompt,
            max_tokens=kwargs.get('max_tokens', 4096),
            temperature=kwargs.get('temperature', 0.7)
        )

        return response.content[0].text

    def generate_json(self, prompt: str, schema: Dict = None, **kwargs) -> Dict:
        """Generate JSON (with schema validation)"""
        response = self.generate(
            prompt + "\n\nOutput as JSON.",
            **kwargs
        )

        import json
        return json.loads(response)
```

### 5.2 Git Operations

```python
# infrastructure/git/git_ops.py

import subprocess
from pathlib import Path

class GitOperations:
    """
    Git operations wrapper

    Benefits:
    - Centralized git logic
    - Easy to mock for testing
    - Consistent commit format
    """

    def __init__(self, repo_root: Path, commit_format: str = "[{path}] {action}"):
        self.repo_root = repo_root
        self.commit_format = commit_format

    def commit(self, article_path: Path, message: str) -> None:
        """
        Commit changes for article

        Args:
            article_path: Path to article folder
            message: Commit message
        """
        # Get relative path for commit message
        rel_path = article_path.relative_to(self.repo_root / "artykuly")
        series, silo, slug = rel_path.parts

        # Format commit message
        formatted_msg = self.commit_format.format(
            path=f"{series}/{silo}/{slug}",
            action=message
        )

        # Git add + commit
        subprocess.run(
            ["git", "add", str(article_path)],
            cwd=self.repo_root,
            check=True
        )

        subprocess.run(
            ["git", "commit", "-m", formatted_msg],
            cwd=self.repo_root,
            check=True
        )

    def status(self) -> str:
        """Get git status"""
        result = subprocess.run(
            ["git", "status", "--short"],
            cwd=self.repo_root,
            capture_output=True,
            text=True
        )
        return result.stdout
```

### 5.3 Payload CMS Adapter (Markdown-based)

```python
# infrastructure/cms/payload_adapter.py

import requests
from typing import Dict, Any

class PayloadAdapter:
    """
    Payload CMS v3 API adapter

    Używa Markdown (nie Lexical JSON) - Payload potrafi parsować markdown
    """

    def __init__(self, api_url: str, api_key: str):
        self.api_url = api_url
        self.api_key = api_key
        self.headers = {
            "Authorization": f"Bearer {api_key}",
            "Content-Type": "application/json"
        }

    def create_article(self, payload_data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Create article in Payload CMS

        Args:
            payload_data: Article data in Payload format

        Returns:
            Created article response (with ID)
        """
        response = requests.post(
            f"{self.api_url}/api/articles",
            json=payload_data,
            headers=self.headers
        )
        response.raise_for_status()
        return response.json()

    def update_article(self, article_id: str, payload_data: Dict[str, Any]) -> Dict[str, Any]:
        """Update existing article"""
        response = requests.patch(
            f"{self.api_url}/api/articles/{article_id}",
            json=payload_data,
            headers=self.headers
        )
        response.raise_for_status()
        return response.json()

    def publish_article(self, article_id: str) -> Dict[str, Any]:
        """Change status: draft → published"""
        return self.update_article(article_id, {"status": "published"})
```

**Payload Transformer (Markdown-based):**

```python
# adapters/payload/transformer.py

from core.domain.article import Article
from typing import Dict, Any, List
import re

class PayloadTransformer:
    """
    Transform Article → Payload CMS format

    Używa Markdown (nie Lexical) - prostsze i bardziej maintainable
    Payload CMS v3 potrafi parsować markdown do rich text
    """

    def transform(self, article: Article) -> Dict[str, Any]:
        """
        Transform article to Payload CMS JSON

        Returns:
            Payload-compatible JSON ready for API
        """
        # Parse markdown into sections and blocks
        sections = self._parse_sections(article.final_content)

        # Build blocks list
        blocks = []

        # Main content block (markdown)
        blocks.append({
            "blockType": "richText",
            "content": sections['main']  # Markdown string
        })

        # FAQ block (if exists)
        if sections.get('faq'):
            blocks.append({
                "blockType": "faq",
                "questions": self._parse_faq(sections['faq'])
            })

        # Checklist block (if exists)
        if sections.get('checklist'):
            blocks.append({
                "blockType": "checklist",
                "title": "Checklist",
                "items": self._parse_checklist(sections['checklist'])
            })

        # CTA block ("Co dalej?")
        if sections.get('cta'):
            blocks.append({
                "blockType": "cta",
                "content": sections['cta']  # Markdown
            })

        # Related articles block
        if article.related_articles:
            blocks.append({
                "blockType": "relatedArticles",
                "articles": [
                    {
                        "title": ra['title'],
                        "slug": ra['slug'],
                        "description": ra.get('description', '')
                    }
                    for ra in article.related_articles
                    if not ra.get('contextual', False)  # Only end-section links
                ]
            })

        # Build Payload structure
        payload_data = {
            "title": article.config.title,
            "slug": article.config.slug,

            # Meta
            "meta": {
                "title": article.seo_data.meta_title,
                "description": article.seo_data.meta_description,
                "keywords": article.seo_data.keywords
            },

            # Blocks (layout)
            "blocks": blocks,

            # Taxonomy
            "categories": article.categories,
            "series": article.config.series,
            "silo": article.config.silo,

            # Business metadata (dla filtrowania)
            "businessMetadata": article.business_metadata.__dict__ if article.business_metadata else None,

            # Schema.org (dla SEO)
            "schema": article.schema_json,

            # Multimedia suggestions (dla editora)
            "multimedia": article.multimedia,

            # Status
            "status": "draft",
            "publishedAt": article.updated_at.isoformat()
        }

        return payload_data

    def _parse_sections(self, markdown: str) -> Dict[str, str]:
        """
        Parse markdown into sections

        Returns:
            {
                'main': main content,
                'faq': FAQ section (if exists),
                'checklist': Checklist section (if exists),
                'cta': "Co dalej?" section (if exists)
            }
        """
        sections = {}

        # Split by H2 headers
        parts = re.split(r'\n## ', markdown)

        main_parts = []

        for part in parts:
            if part.startswith('Najczęściej zadawane pytania') or part.startswith('FAQ'):
                sections['faq'] = '## ' + part
            elif part.startswith('Checklist'):
                sections['checklist'] = '## ' + part
            elif part.startswith('Co dalej?'):
                sections['cta'] = '## ' + part
            elif part.startswith('Powiązane artykuły'):
                # Skip - handled separately by related_articles
                pass
            else:
                main_parts.append(part)

        sections['main'] = '\n## '.join(main_parts).strip()

        return sections

    def _parse_faq(self, faq_markdown: str) -> List[Dict[str, str]]:
        """
        Parse FAQ markdown into structured list

        Example input:
        ## FAQ
        ### 1. Pytanie pierwsze?
        Odpowiedź...

        Returns:
        [{"question": "Pytanie pierwsze?", "answer": "Odpowiedź..."}]
        """
        questions = []

        # Split by H3 (FAQ questions)
        parts = re.split(r'\n### \d+\. ', faq_markdown)

        for part in parts[1:]:  # Skip first empty part
            lines = part.strip().split('\n', 1)
            if len(lines) == 2:
                question = lines[0].strip('?') + '?'
                answer = lines[1].strip()
                questions.append({
                    "question": question,
                    "answer": answer
                })

        return questions

    def _parse_checklist(self, checklist_markdown: str) -> List[str]:
        """
        Parse checklist markdown into list of items

        Example:
        - [ ] Item 1
        - [ ] Item 2

        Returns:
        ["Item 1", "Item 2"]
        """
        lines = checklist_markdown.split('\n')
        items = []

        for line in lines:
            match = re.match(r'^- \[ \] (.+)$', line.strip())
            if match:
                items.append(match.group(1))

        return items
```

---

## 6. Configuration (YAML)

### 6.1 workflow.yaml - Workflow Definition

```yaml
# config/workflow.yaml

workflow:
  name: "article_generation"
  version: "1.0"

  steps:
    - name: outline
      function: core.steps.step_01_outline.execute_outline
      prompt: konspekt/prompt_konspekt_artykulu.md
      git_commit: true
      commit_message: "Create outline"

    - name: summary
      function: core.steps.step_02_summary.execute_summary
      prompt: articles/prompt_streszczenie_artykulu.md
      git_commit: false

    - name: internal_linking
      function: core.steps.step_03_linking.execute_linking
      prompt: articles/prompt_linkowanie_wewnetrzne.md
      git_commit: false
      config:
        min_links: 5
        max_links: 8
        same_silo_ratio: 0.6

    - name: write_intro
      function: core.steps.step_04_write_intro.execute_write_intro
      prompt: articles/prompt_artykul_start.md
      git_commit: false
      config:
        min_words: 300
        max_words: 400

    - name: write_sections
      function: core.steps.step_05_write_sections.execute_write_sections
      prompt: articles/prompt_artykul_kontynuacja.md
      git_commit: false
      config:
        min_words: 300
        max_words: 400
        review_enabled: true

    - name: draft
      function: core.steps.step_06_draft.execute_draft
      git_commit: true
      commit_message: "Complete draft"

    - name: seo_review
      function: core.steps.step_07_seo_review.execute_seo_review
      prompt: audyt/prompt_sprawdz_naglowki.md
      git_commit: false

    - name: humanize
      function: core.steps.step_08_humanize.execute_humanize
      prompt: audyt/prompt_sprawdz_styl.md
      git_commit: false

    - name: multimedia
      function: core.steps.step_09_multimedia.execute_multimedia
      prompt: articles/prompt_multimedia_suggestions.md
      git_commit: false
      config:
        min_suggestions: 4
        max_suggestions: 9

    - name: business_metadata
      function: core.steps.step_10_business_metadata.execute_business_metadata
      prompt: metadata/prompt_business_metadata.md
      git_commit: false

    - name: cta
      function: core.steps.step_11_cta.execute_cta
      prompt: articles/prompt_cta_next_steps.md
      git_commit: false

    - name: publish
      function: core.steps.step_12_publish.execute_publish
      git_commit: true
      commit_message: "Publish article"

    - name: schema
      function: core.steps.step_13_schema.execute_schema
      prompt: metadata/prompt_schema_markup.md
      git_commit: false

    - name: categories
      function: core.steps.step_14_categories.execute_categories
      git_commit: true
      commit_message: "Assign categories"
```

### 6.2 providers.yaml - AI Providers

```yaml
# config/providers.yaml

providers:
  default: claude

  claude:
    class: infrastructure.ai.claude_provider.ClaudeProvider
    api_key_env: ANTHROPIC_API_KEY
    model: claude-sonnet-4-20250514
    max_tokens: 4096
    temperature: 0.7

  openai:
    class: infrastructure.ai.openai_provider.OpenAIProvider
    api_key_env: OPENAI_API_KEY
    model: gpt-4-turbo
    max_tokens: 4096
    temperature: 0.7
```

### 6.3 payload.yaml - Payload CMS Config

```yaml
# config/payload.yaml

payload:
  api_url: https://cms.digitalvantage.pl
  api_key_env: PAYLOAD_API_KEY

  # Collection name in Payload
  collection: articles

  # Auto-publish after generation
  auto_publish: false

  # Block types mapping
  blocks:
    richText: enabled
    faq: enabled
    checklist: enabled
    cta: enabled
    relatedArticles: enabled
```

---

## 7. Dependency Injection & Factory

```python
# core/factory.py

import yaml
import os
from pathlib import Path
from typing import Dict, Any
from importlib import import_module

from core.workflow import WorkflowEngine, WorkflowStep
from infrastructure.ai.base import AIProvider
from infrastructure.git.git_ops import GitOperations
from core.services.prompt_loader import PromptLoader

class ServiceFactory:
    """
    Service factory with dependency injection

    Responsibilities:
    - Load configuration from YAML
    - Create and wire dependencies
    - Build workflow engine with all steps

    Benefits:
    - Centralized dependency management
    - Easy testing (mock dependencies)
    - Configuration-driven (YAML)
    """

    def __init__(self, config_dir: Path = Path("config")):
        self.config_dir = config_dir
        self.config = self._load_config()

    def _load_config(self) -> Dict[str, Any]:
        """Load all config files"""
        config = {}

        for yaml_file in self.config_dir.glob("*.yaml"):
            with open(yaml_file) as f:
                data = yaml.safe_load(f)
                config.update(data)

        return config

    def create_ai_provider(self, provider_name: str = None) -> AIProvider:
        """
        Create AI provider from config

        Example:
            provider = factory.create_ai_provider("claude")
        """
        if provider_name is None:
            provider_name = self.config['providers']['default']

        provider_config = self.config['providers'][provider_name]

        # Import provider class dynamically
        module_path, class_name = provider_config['class'].rsplit('.', 1)
        module = import_module(module_path)
        provider_class = getattr(module, class_name)

        # Get API key from environment
        api_key = os.getenv(provider_config['api_key_env'])
        if not api_key:
            raise ValueError(f"Missing {provider_config['api_key_env']} environment variable")

        # Create provider
        return provider_class(
            api_key=api_key,
            model=provider_config['model']
        )

    def create_git_ops(self) -> GitOperations:
        """Create git operations wrapper"""
        return GitOperations(
            repo_root=Path.cwd(),
            commit_format=self.config.get('git', {}).get('commit_format', "[{path}] {action}")
        )

    def create_prompt_loader(self) -> PromptLoader:
        """Create prompt loader service"""
        return PromptLoader(prompts_dir=Path("prompts"))

    def create_dependencies(self) -> Dict[str, Any]:
        """
        Create all dependencies for workflow

        Returns:
            Dict with all services (ai, git, prompts, storage, etc.)
        """
        return {
            'ai': self.create_ai_provider(),
            'git': self.create_git_ops(),
            'prompts': self.create_prompt_loader(),
            'review': self.create_review_service(),
            'categories': self.create_category_matcher(),
            'storage': self.create_storage(),
        }

    def create_workflow_engine(self) -> WorkflowEngine:
        """
        Create workflow engine with all steps from config

        Returns:
            Configured WorkflowEngine
        """
        workflow_config = self.config['workflow']

        # Build steps from config
        steps = []
        for step_config in workflow_config['steps']:
            # Import step function dynamically
            module_path, func_name = step_config['function'].rsplit('.', 1)
            module = import_module(module_path)
            step_function = getattr(module, func_name)

            # Create WorkflowStep
            step = WorkflowStep(
                name=step_config['name'],
                function=step_function,
                prompt_path=step_config.get('prompt'),
                git_commit=step_config.get('git_commit', False),
                commit_message=step_config.get('commit_message'),
                config=step_config.get('config', {})
            )
            steps.append(step)

        return WorkflowEngine(steps)

    # ... more factory methods
```

---

## 8. CLI (Entry Point)

```python
# cli.py

import click
from pathlib import Path
from core.factory import ServiceFactory
from core.domain.article import Article, ArticleConfig
from adapters.payload.transformer import PayloadTransformer
from infrastructure.cms.payload_adapter import PayloadAdapter

@click.group()
def cli():
    """Blog Agent - Automated article generation"""
    pass

@cli.command()
@click.option('--config', type=click.Path(exists=True), required=True, help="Path to article config.yaml")
@click.option('--start-from', default=None, help="Resume from step")
@click.option('--stop-at', default=None, help="Stop before step")
@click.option('--publish-to-cms', is_flag=True, help="Publish to Payload CMS")
def create(config, start_from, stop_at, publish_to_cms):
    """Generate article from config"""

    # Load article config
    config_path = Path(config)
    article_config = ArticleConfig.from_yaml(config_path)
    article_path = config_path.parent

    # Create or load article
    if (article_path / "article.md").exists():
        click.echo("📂 Loading existing article...")
        article = Article.load_from_disk(article_path)
    else:
        click.echo("📝 Creating new article...")
        article = Article(path=article_path, config=article_config)

    # Create factory and dependencies
    factory = ServiceFactory()
    dependencies = factory.create_dependencies()

    # Create workflow engine
    engine = factory.create_workflow_engine()

    # Execute workflow
    try:
        click.echo(f"🚀 Starting workflow...")
        article = engine.execute(
            article,
            dependencies,
            start_from=start_from,
            stop_at=stop_at
        )
        click.echo(f"✅ Article generated: {article.path / 'article.md'}")

        # Publish to CMS if requested
        if publish_to_cms:
            click.echo("📤 Publishing to Payload CMS...")

            # Transform to Payload format
            transformer = PayloadTransformer()
            payload_data = transformer.transform(article)

            # Upload to CMS
            payload = PayloadAdapter(
                api_url=factory.config['payload']['api_url'],
                api_key=os.getenv(factory.config['payload']['api_key_env'])
            )
            result = payload.create_article(payload_data)

            click.echo(f"✅ Published to CMS: {result['id']}")

    except Exception as e:
        click.echo(f"❌ Error: {e}", err=True)
        raise

@cli.command()
@click.option('--series', required=True, help="Series name (e.g., ecommerce)")
@click.option('--silo', required=True, help="Silo name (e.g., operacje)")
@click.option('--slug', required=True, help="Article slug (e.g., bezpieczenstwo-rodo)")
@click.option('--title', required=True, help="Article title")
def init(series, silo, slug, title):
    """Initialize article structure"""

    # Create folder structure
    article_path = Path(f"artykuly/{series}/{silo}/{slug}")
    article_path.mkdir(parents=True, exist_ok=True)

    # Create config.yaml
    config = {
        'title': title,
        'target_audience': '',  # User fills in
        'tone': 'ekspercki, ale naturalny i rozmowny',
        'series': series,
        'silo': silo,
        'slug': slug
    }

    import yaml
    (article_path / "config.yaml").write_text(
        yaml.dump(config, allow_unicode=True, default_flow_style=False)
    )

    click.echo(f"✅ Initialized: {article_path}")
    click.echo(f"📝 Edit config: {article_path / 'config.yaml'}")

@cli.command()
@click.option('--series', default=None, help="Filter by series")
def list(series):
    """List all articles"""

    root = Path("artykuly")

    if series:
        articles = root.glob(f"{series}/*/*/config.yaml")
    else:
        articles = root.glob("*/*/*/config.yaml")

    import yaml
    for config_path in sorted(articles):
        config = yaml.safe_load(config_path.read_text())
        path = config_path.parent

        # Check status
        if (path / "article.md").exists():
            status = "✅ Complete"
        elif (path / "draft.md").exists():
            status = "🚧 Draft"
        elif (path / "outline.md").exists():
            status = "📝 Outline"
        else:
            status = "⚪ Not started"

        click.echo(f"{status} {path} - {config['title']}")

if __name__ == "__main__":
    cli()
```

---

## 9. Example Flow

### 9.1 Creating new article

```bash
# 1. Initialize article structure
python cli.py init \
  --series ecommerce \
  --silo operacje \
  --slug bezpieczenstwo-rodo \
  --title "Bezpieczeństwo i RODO w e-commerce"

# 2. Edit config (user fills target_audience)
vim artykuly/ecommerce/operacje/bezpieczenstwo-rodo/config.yaml

# 3. Generate article
python cli.py create \
  --config artykuly/ecommerce/operacje/bezpieczenstwo-rodo/config.yaml

# 4. (Optional) Resume from specific step
python cli.py create \
  --config artykuly/ecommerce/operacje/bezpieczenstwo-rodo/config.yaml \
  --start-from humanize

# 5. (Optional) Publish to CMS
python cli.py create \
  --config artykuly/ecommerce/operacje/bezpieczenstwo-rodo/config.yaml \
  --publish-to-cms
```

### 9.2 Workflow execution trace

```
🚀 Starting workflow...
🔄 Executing outline...
  ├─ Loading prompt: konspekt/prompt_konspekt_artykulu.md
  ├─ Rendering with: title, target_audience, tone
  ├─ Generating with Claude (30s)
  ├─ Parsing to Outline VO
  ├─ Parsing to SEOData VO
  └─ Git commit: [ecommerce/operacje/bezpieczenstwo-rodo] Create outline
✅ Completed outline

🔄 Executing summary...
  ├─ Loading prompt: articles/prompt_streszczenie_artykulu.md
  ├─ Rendering with: outline, title, target_audience
  ├─ Generating with Claude (15s)
  ├─ Parsing to Summary VO (3-5 points)
  └─ Saved to sections/00-summary.md
✅ Completed summary

🔄 Executing internal_linking...
  ├─ Scanning artykuly/ecommerce/
  ├─ Found 23 articles in series
  ├─ AI selecting 5-8 most related
  ├─ Strategy: 60% same silo, 40% cross-silo
  ├─ Selected: 6 articles (3 contextual, 3 end-section)
  └─ Saved to related_articles.json
✅ Completed internal_linking

🔄 Executing write_intro...
  ├─ Loading prompt: articles/prompt_artykul_start.md
  ├─ Writing intro + first section (2m)
  ├─ AI review: ✅ 350 words, Flesch 52
  └─ Saved to sections/01-intro.md
✅ Completed write_intro

🔄 Executing write_sections...
  ├─ Writing section 2/5: Wymagania RODO (45s)
  ├─ AI review: ✅ 380 words, Flesch 48
  ├─ Writing section 3/5: Certyfikaty SSL (45s)
  ├─ AI review: ✅ 360 words, Flesch 51
  ├─ Writing section 4/5: Polityka prywatności (45s)
  ├─ AI review: ✅ 370 words, Flesch 49
  ├─ Writing section 5/5: Checklist (30s)
  └─ Total: 5 sections written
✅ Completed write_sections

🔄 Executing draft...
  ├─ Assembling: summary + 5 sections
  ├─ Adding "Powiązane artykuły" section
  └─ Git commit: [ecommerce/operacje/bezpieczenstwo-rodo] Complete draft
✅ Completed draft

🔄 Executing seo_review...
  ├─ Checking H1-H4 hierarchy: ✅
  ├─ Checking keywords distribution: ✅
  └─ No fixes needed
✅ Completed seo_review

🔄 Executing humanize...
  ├─ Checking AI tone: ⚠️ found 3 AI-like phrases
  ├─ Auto-fixing...
  ├─ Checking Flesch: ✅ 48 (target: 40-60)
  └─ Saved to article.md
✅ Completed humanize

🔄 Executing multimedia...
  ├─ Analyzing content for multimedia opportunities
  ├─ Suggesting 6 multimedia items:
  │   ├─ 1 hero image
  │   ├─ 2 diagrams
  │   ├─ 2 infographics
  │   └─ 1 screenshot
  ├─ Generated image prompts (DALL-E/MJ)
  └─ Saved to multimedia.json
✅ Completed multimedia

🔄 Executing business_metadata...
  ├─ Analyzing investment: medium (5-30k PLN)
  ├─ Timeline: 3-6 weeks
  ├─ Complexity: technical=low, organizational=medium
  ├─ Team: 2-3 people
  └─ Saved to business_metadata.yaml
✅ Completed business_metadata

🔄 Executing cta...
  ├─ Detected article type: optimization/compliance
  ├─ Generated "Co dalej?" section:
  │   ├─ Self-assessment questions
  │   ├─ Quick wins (3 actions)
  │   └─ Full implementation CTA
  └─ Appended to article.md
✅ Completed cta

🔄 Executing publish...
  ├─ Final article: article.md (3200 words)
  └─ Git commit: [ecommerce/operacje/bezpieczenstwo-rodo] Publish article
✅ Completed publish

🔄 Executing schema...
  ├─ Generating Schema.org JSON-LD:
  │   ├─ Article schema
  │   ├─ HowTo schema (checklist detected)
  │   └─ BreadcrumbList schema
  └─ Saved to schema.json
✅ Completed schema

🔄 Executing categories...
  ├─ Loading categories.yaml (146 categories)
  ├─ AI selecting best matches
  ├─ Selected: E-commerce, Bezpieczeństwo IT, RODO, Strategia IT
  └─ Git commit: [ecommerce/operacje/bezpieczenstwo-rodo] Assign categories
✅ Completed categories

✅ Article generated: artykuly/ecommerce/operacje/bezpieczenstwo-rodo/article.md
📊 Stats: 6min 25s, ~3200 words, 14 steps, 4 git commits

📤 Publishing to Payload CMS...
  ├─ Transforming to Payload format (markdown-based)
  ├─ 5 blocks: richText, checklist, cta, relatedArticles
  ├─ POST /api/articles
  └─ Response: {"id": "67a1b2c3d4e5f6", "status": "draft"}
✅ Published to CMS: 67a1b2c3d4e5f6
```

---

## 10. Testing Strategy

### 10.1 Unit Tests

```python
# tests/unit/test_article.py

def test_article_set_outline():
    """Test setting outline validates VO"""
    article = Article(path=Path("."), config=mock_config)
    outline = Outline(sections=[...], has_checklist=False, has_faq=True)

    article.set_outline(outline)

    assert article.outline == outline
    assert article.updated_at > article.created_at

def test_article_complete_step():
    """Test step completion tracking"""
    article = Article(path=Path("."), config=mock_config)

    article.complete_step("outline")

    assert "outline" in article.completed_steps
    assert article.is_step_completed("outline")
    assert not article.is_step_completed("summary")
```

### 10.2 Integration Tests

```python
# tests/integration/test_workflow.py

def test_full_workflow_execution(tmp_path):
    """Test full workflow end-to-end"""
    # Setup
    factory = ServiceFactory()
    engine = factory.create_workflow_engine()
    article = Article(path=tmp_path, config=mock_config)
    deps = factory.create_dependencies()

    # Execute
    result = engine.execute(article, deps)

    # Assert
    assert (tmp_path / "article.md").exists()
    assert (tmp_path / "outline.md").exists()
    assert len(result.completed_steps) == 14
```

---

## 11. Deployment & Scaling

### 11.1 Local Development

```bash
# Install dependencies
pip install -r requirements.txt

# Run single article
python cli.py create --config artykuly/ecommerce/operacje/test/config.yaml

# Run with specific provider
export ANTHROPIC_API_KEY=xxx
python cli.py create --config ...
```

### 11.2 Batch Processing

```bash
# Generate all pending articles
for config in artykuly/*/*/*/config.yaml; do
  python cli.py create --config "$config"
done

# Or parallel with GNU parallel
find artykuly -name config.yaml | parallel -j 4 python cli.py create --config {}
```

### 11.3 Cron Job

```bash
# crontab -e
0 2 * * * cd /path/to/blog-agent && python cli.py create --config /path/to/config.yaml >> /var/log/blog-agent.log 2>&1
```

---

## 12. Extensibility

### 12.1 Adding New Step

1. Create step function:
```python
# core/steps/step_15_translations.py
def execute_translations(article, deps, config):
    # Implementation
    return article
```

2. Add to `workflow.yaml`:
```yaml
- name: translations
  function: core.steps.step_15_translations.execute_translations
  config:
    languages: [en, de, es]
```

### 12.2 Adding New AI Provider

1. Implement provider:
```python
# infrastructure/ai/gemini_provider.py
class GeminiProvider:
    def generate(self, prompt, **kwargs):
        # Implementation
        pass
```

2. Add to `providers.yaml`:
```yaml
gemini:
  class: infrastructure.ai.gemini_provider.GeminiProvider
  api_key_env: GOOGLE_API_KEY
  model: gemini-pro
```

### 12.3 Adding New Block Type

1. Update transformer:
```python
# adapters/payload/transformer.py
def _create_comparison_block(self, content):
    return {
        "blockType": "comparison",
        "items": self._parse_comparison(content)
    }
```

2. Use in article markdown with special marker.

---

## 13. Next Steps (Implementation)

1. ✅ **Architecture designed** (this document)
2. ⏳ **Setup project structure** (folders, __init__.py)
3. ⏳ **Implement core domain** (Article, Value Objects)
4. ⏳ **Implement infrastructure** (Claude provider, Git ops)
5. ⏳ **Implement step functions** (14 steps)
6. ⏳ **Implement workflow engine**
7. ⏳ **Implement CLI**
8. ⏳ **Testing** (unit + integration)
9. ⏳ **Documentation** (usage examples)
10. ⏳ **Deploy & iterate**

---

**Status:** ✅ Architecture complete, ready for implementation
**Next:** Begin implementation with core domain model
