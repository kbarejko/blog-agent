"""
Article - Aggregate Root

Main domain entity representing a blog article.
"""
from dataclasses import dataclass, field
from typing import Optional, List, Dict, Any
from pathlib import Path
from datetime import datetime

from .config import ArticleConfig
from .value_objects import (
    Outline,
    SEOData,
    Summary,
    BusinessMetadata,
    InternalLinks,
    MultimediaSuggestion,
    CTASection,
    SchemaMarkup
)


@dataclass
class Article:
    """
    Article Aggregate Root

    Represents a blog article with all its components.
    Enforces invariants and provides methods for state transitions.
    """
    path: Path
    config: ArticleConfig

    # Value Objects (immutable)
    outline: Optional[Outline] = None
    seo_data: Optional[SEOData] = None
    summary: Optional[Summary] = None
    business_metadata: Optional[BusinessMetadata] = None
    internal_links: Optional[InternalLinks] = None
    multimedia: Optional[MultimediaSuggestion] = None
    cta_section: Optional[CTASection] = None
    schema_markup: Optional[SchemaMarkup] = None

    # Content files
    sections: List[str] = field(default_factory=list)  # Section markdown content
    draft_content: Optional[str] = None
    final_content: Optional[str] = None

    # Categories
    categories: List[str] = field(default_factory=list)

    # Metadata
    created_at: datetime = field(default_factory=datetime.now)
    updated_at: datetime = field(default_factory=datetime.now)
    status: str = "initialized"  # initialized, outline_created, writing, draft_ready, seo_reviewed, humanized, published

    def _mark_updated(self) -> None:
        """Mark article as updated"""
        self.updated_at = datetime.now()

    # === Outline ===

    def set_outline(self, outline: Outline) -> None:
        """Set outline with validation"""
        if not isinstance(outline, Outline):
            raise ValueError("Must be Outline value object")
        self.outline = outline
        self.status = "outline_created"
        self._mark_updated()

    def has_outline(self) -> bool:
        """Check if outline exists"""
        return self.outline is not None

    # === Summary ===

    def set_summary(self, summary: Summary) -> None:
        """Set summary with validation"""
        if not isinstance(summary, Summary):
            raise ValueError("Must be Summary value object")

        issues = summary.validate()
        if issues:
            raise ValueError(f"Invalid summary: {', '.join(issues)}")

        self.summary = summary
        self._mark_updated()

    # === SEO ===

    def set_seo_data(self, seo_data: SEOData) -> None:
        """Set SEO data with validation"""
        if not isinstance(seo_data, SEOData):
            raise ValueError("Must be SEOData value object")

        issues = seo_data.validate()
        if issues:
            raise ValueError(f"Invalid SEO data: {', '.join(issues)}")

        self.seo_data = seo_data
        self.config.meta_title = seo_data.meta_title
        self.config.meta_description = seo_data.meta_description
        self._mark_updated()

    # === Business Metadata ===

    def set_business_metadata(self, metadata: BusinessMetadata) -> None:
        """Set business metadata"""
        if not isinstance(metadata, BusinessMetadata):
            raise ValueError("Must be BusinessMetadata value object")
        self.business_metadata = metadata
        self._mark_updated()

    # === Internal Links ===

    def set_internal_links(self, links: InternalLinks) -> None:
        """Set internal links"""
        if not isinstance(links, InternalLinks):
            raise ValueError("Must be InternalLinks value object")
        self.internal_links = links
        self._mark_updated()

    # === Multimedia ===

    def set_multimedia(self, multimedia: MultimediaSuggestion) -> None:
        """Set multimedia suggestions"""
        if not isinstance(multimedia, MultimediaSuggestion):
            raise ValueError("Must be MultimediaSuggestion value object")
        self.multimedia = multimedia
        self._mark_updated()

    # === CTA ===

    def set_cta_section(self, cta: CTASection) -> None:
        """Set CTA section"""
        if not isinstance(cta, CTASection):
            raise ValueError("Must be CTASection value object")
        self.cta_section = cta
        self._mark_updated()

    # === Schema Markup ===

    def set_schema_markup(self, schema: SchemaMarkup) -> None:
        """Set schema markup"""
        if not isinstance(schema, SchemaMarkup):
            raise ValueError("Must be SchemaMarkup value object")
        self.schema_markup = schema
        self._mark_updated()

    # === Sections ===

    def add_section(self, content: str) -> None:
        """Add a section to the article"""
        self.sections.append(content)
        self.status = "writing"
        self._mark_updated()

    def get_sections_count(self) -> int:
        """Get number of sections"""
        return len(self.sections)

    # === Draft ===

    def create_draft(self) -> str:
        """Create draft by combining summary + sections"""
        if not self.summary:
            raise ValueError("Summary must be set before creating draft")
        if not self.sections:
            raise ValueError("At least one section must be written")

        parts = [self.summary.to_markdown()]
        parts.extend(self.sections)

        self.draft_content = "\n\n".join(parts)
        self.status = "draft_ready"
        self._mark_updated()

        return self.draft_content

    # === Final Content ===

    def set_final_content(self, content: str) -> None:
        """Set final article content after humanization"""
        self.final_content = content
        self.status = "humanized"
        self._mark_updated()

    def add_cta_to_final(self) -> None:
        """Add CTA section to final content"""
        if not self.final_content:
            raise ValueError("Final content must exist before adding CTA")
        if not self.cta_section:
            raise ValueError("CTA section must be set")

        self.final_content = self.final_content.rstrip() + "\n\n" + self.cta_section.to_markdown()
        self._mark_updated()

    def publish(self) -> None:
        """Mark article as published"""
        if not self.final_content:
            raise ValueError("Final content must exist before publishing")

        self.status = "published"
        self._mark_updated()

    # === Categories ===

    def set_categories(self, categories: List[str]) -> None:
        """Set article categories"""
        if not categories:
            raise ValueError("At least one category must be assigned")
        if len(categories) > 5:
            raise ValueError("Maximum 5 categories allowed")

        self.categories = categories
        self._mark_updated()

    # === Path Helpers ===

    def get_config_path(self) -> Path:
        """Get path to config.yaml"""
        return self.path / "config.yaml"

    def get_outline_path(self) -> Path:
        """Get path to outline.md"""
        return self.path / "outline.md"

    def get_sections_dir(self) -> Path:
        """Get path to sections directory"""
        return self.path / "sections"

    def get_section_path(self, index: int) -> Path:
        """Get path to specific section file"""
        return self.get_sections_dir() / f"{index:02d}-section.md"

    def get_draft_path(self) -> Path:
        """Get path to draft.md"""
        return self.path / "draft.md"

    def get_article_path(self) -> Path:
        """Get path to article.md (final)"""
        return self.path / "article.md"

    def get_categories_path(self) -> Path:
        """Get path to categories.yaml"""
        return self.path / "categories.yaml"

    def get_business_metadata_path(self) -> Path:
        """Get path to business_metadata.yaml"""
        return self.path / "business_metadata.yaml"

    def get_multimedia_path(self) -> Path:
        """Get path to multimedia.json"""
        return self.path / "multimedia.json"

    def get_schema_path(self) -> Path:
        """Get path to schema.json"""
        return self.path / "schema.json"

    # === URL Helpers ===

    def get_url_path(self, base_url: str = "https://www.digitalvantage.pl") -> str:
        """
        Get full URL for article based on folder structure

        Example:
        Path: artykuly/ecommerce/operacje/bezpieczenstwo-rodo/
        URL: https://www.digitalvantage.pl/artykuly/ecommerce/operacje/bezpieczenstwo-rodo/
        """
        # Get relative path from project root
        relative_path = str(self.path).replace(str(Path.cwd()), "").lstrip("/")
        return f"{base_url}/{relative_path}/"

    def get_series_silo_slug(self) -> tuple[str, str, str]:
        """
        Extract series, silo, and slug from path

        Returns: (series, silo, slug)
        Example: ('ecommerce', 'operacje', 'bezpieczenstwo-rodo')
        """
        parts = self.path.parts
        # Assume structure: artykuly/[series]/[silo]/[slug]
        if len(parts) >= 4 and parts[-4] == "artykuly":
            return parts[-3], parts[-2], parts[-1]
        raise ValueError(f"Invalid article path structure: {self.path}")

    # === Validation ===

    def validate_for_publication(self) -> List[str]:
        """Validate article is ready for publication"""
        issues = []

        if not self.outline:
            issues.append("Outline not created")
        if not self.summary:
            issues.append("Summary not created")
        if not self.sections:
            issues.append("No sections written")
        if not self.draft_content:
            issues.append("Draft not created")
        if not self.final_content:
            issues.append("Final content not created")
        if not self.seo_data:
            issues.append("SEO data not set")
        if not self.categories:
            issues.append("Categories not assigned")

        return issues

    def is_ready_for_publication(self) -> bool:
        """Check if article is ready for publication"""
        return len(self.validate_for_publication()) == 0

    def __repr__(self) -> str:
        """String representation"""
        return f"Article(path={self.path}, status={self.status}, sections={len(self.sections)})"
