"""
Step 6: Create Draft

Combines summary + sections into draft.md.
"""
from typing import Dict, Any

from ...domain.article import Article


def execute_create_draft(
    article: Article,
    deps: Dict[str, Any],
    config: Dict[str, Any]
) -> Article:
    """
    Create article draft

    Combines:
    - Summary ("Co znajdziesz w artykule?")
    - All sections

    Into draft.md file and git commits.

    Args:
        article: Article (must have summary and sections)
        deps: Dependencies (storage, git, review)
        config: Step configuration

    Returns:
        Article with draft_content set
    """
    if not article.summary:
        raise ValueError("Summary must exist before creating draft")
    if not article.sections:
        raise ValueError("Sections must be written before creating draft")

    storage = deps['storage']
    git = deps['git']
    review = deps['review']

    print("🔄 Creating draft...")

    # Create draft (handled by Article)
    draft_content = article.create_draft()

    # Save draft.md
    draft_path = article.get_draft_path()
    storage.write_file(draft_path, draft_content)

    # Review draft
    draft_review = review.review_article_draft(draft_content)
    print(f"✅ Draft created:")
    print(f"   - Total words: {draft_review['total_words']}")
    print(f"   - Flesch score: {draft_review['flesch_score']:.1f}")
    print(f"   - Sections: {len(article.sections)}")

    # Git commit
    series, silo, slug = article.get_series_silo_slug()
    git.commit_article_stage(
        article.path,
        "draft",
        f"Create draft ({draft_review['total_words']} words, {len(article.sections)} sections)"
    )

    return article
