"""
Value Objects for Article domain

Immutable data structures representing article components.
"""
from dataclasses import dataclass, field
from typing import List, Optional, Dict, Any
from datetime import datetime


@dataclass(frozen=True)
class Outline:
    """Article outline with sections (FAQ and Checklist always included)"""
    sections: List[Dict[str, str]]  # [{"title": "...", "description": "..."}]
    estimated_word_count: int = 0

    @classmethod
    def from_markdown(cls, content: str) -> 'Outline':
        """Parse outline from markdown format"""
        # Will be implemented with actual parsing logic
        return cls(sections=[])

    def to_markdown(self) -> str:
        """Convert outline to markdown format"""
        lines = ["# Konspekt artykułu\n"]

        for i, section in enumerate(self.sections, 1):
            lines.append(f"## {i}. {section['title']}")
            if section.get('description'):
                lines.append(f"{section['description']}\n")

        return "\n".join(lines)


@dataclass(frozen=True)
class SEOData:
    """SEO metadata for article"""
    meta_title: str
    meta_description: str
    focus_keyword: Optional[str] = None
    additional_keywords: List[str] = field(default_factory=list)

    def validate(self) -> List[str]:
        """Validate SEO data and return list of issues"""
        issues = []

        if len(self.meta_title) > 60:
            issues.append(f"Meta title too long: {len(self.meta_title)} chars (max 60)")
        if len(self.meta_description) > 160:
            issues.append(f"Meta description too long: {len(self.meta_description)} chars (max 160)")
        if len(self.meta_description) < 120:
            issues.append(f"Meta description too short: {len(self.meta_description)} chars (min 120)")

        return issues


@dataclass(frozen=True)
class Summary:
    """Article summary - 'Co znajdziesz w artykule?'"""
    points: List[str]  # 3-5 konkretnych punktów wartości

    def to_markdown(self) -> str:
        """Convert summary to markdown"""
        lines = ["## Co znajdziesz w artykule?\n"]
        for point in self.points:
            lines.append(f"- {point}")
        return "\n".join(lines) + "\n"

    def validate(self) -> List[str]:
        """Validate summary"""
        issues = []
        if len(self.points) < 3:
            issues.append(f"Too few summary points: {len(self.points)} (min 3)")
        if len(self.points) > 5:
            issues.append(f"Too many summary points: {len(self.points)} (max 5)")
        return issues


@dataclass(frozen=True)
class BusinessMetadata:
    """Business metadata for entrepreneurs"""
    target_business: List[str]  # startup, scale-up, enterprise
    industry: List[str]  # ecommerce, saas, fintech, etc.
    project_phase: str  # planowanie, wdrożenie, optymalizacja, migracja

    # Investment
    investment_level: str  # low, medium, high, very_high
    investment_range: str  # "5,000-15,000 PLN"
    investment_breakdown: Dict[str, str]  # {"oprogramowanie": "3,000-5,000 PLN", ...}

    # Timeline
    timeline_estimate: str  # "2-3 miesiące"
    timeline_phases: List[Dict[str, str]]  # [{"phase": "...", "duration": "..."}]

    # Complexity
    complexity_technical: str  # low, medium, high
    complexity_organizational: str  # low, medium, high
    complexity_factors: List[str]  # ["integracje z systemami", ...]

    # Team
    team_size: str  # "2-3 osoby"
    team_roles: List[str]  # ["developer", "project manager", ...]

    # ROI (optional)
    roi_breakeven: Optional[str] = None  # "6-12 miesięcy"
    roi_savings: Optional[str] = None  # "20-30% kosztów operacyjnych"
    roi_factors: List[str] = field(default_factory=list)


@dataclass(frozen=True)
class InternalLinks:
    """Internal linking suggestions"""
    contextual_links: List[Dict[str, str]]  # [{"anchor": "...", "url": "...", "context": "..."}]
    related_articles: List[Dict[str, str]]  # [{"title": "...", "url": "...", "description": "..."}]

    def get_total_count(self) -> int:
        """Get total number of links"""
        return len(self.contextual_links) + len(self.related_articles)


@dataclass(frozen=True)
class MultimediaSuggestion:
    """Multimedia suggestions for article"""
    hero_image: Dict[str, str]  # {"type": "photo", "description": "...", "prompt": "..."}
    section_media: List[Dict[str, Any]]  # [{"section": "...", "type": "...", "description": "...", "prompt": "..."}]

    def get_total_count(self) -> int:
        """Get total number of multimedia elements"""
        return 1 + len(self.section_media)  # hero + sections


@dataclass(frozen=True)
class CTASection:
    """CTA/Next Steps section"""
    variant: str  # practical, theoretical, optimization
    content: str  # Markdown content

    def to_markdown(self) -> str:
        """Convert CTA to markdown"""
        return self.content


@dataclass(frozen=True)
class SchemaMarkup:
    """Schema.org structured data"""
    schemas: List[Dict[str, Any]]  # List of schema objects (Article, FAQPage, HowTo, BreadcrumbList)

    def to_json_ld(self) -> List[Dict[str, Any]]:
        """Get JSON-LD format for embedding"""
        return self.schemas

    def get_schema_types(self) -> List[str]:
        """Get list of schema types"""
        return [schema.get('@type', 'Unknown') for schema in self.schemas]
