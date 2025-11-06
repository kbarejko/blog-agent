"""
Step 12: Publish Article

Marks article as published and commits to git.
"""
from typing import Dict, Any

from ...domain.article import Article


def execute_publish(
    article: Article,
    deps: Dict[str, Any],
    config: Dict[str, Any]
) -> Article:
    """
    Publish article

    Marks article as published and creates git commit.

    Args:
        article: Article (must have final content with CTA)
        deps: Dependencies (git, review)
        config: Step configuration

    Returns:
        Article marked as published
    """
    if not article.final_content:
        raise ValueError("Final content must exist before publishing")

    git = deps['git']
    review = deps['review']

    print("🔄 Publishing article...")

    # Validate article is ready
    issues = article.validate_for_publication()
    if issues:
        print(f"   ⚠️  Article has issues:")
        for issue in issues:
            print(f"      - {issue}")
        print("   Publishing anyway (issues can be fixed later)")

    # Get final stats
    final_review = review.review_article_draft(article.final_content)

    # Mark as published
    article.publish()

    # Git commit
    series, silo, slug = article.get_series_silo_slug()
    git.commit_article_stage(
        article.path,
        "publication",
        f"Publish article ({final_review['total_words']} words)"
    )

    print(f"✅ Article published")
    print(f"   - Total words: {final_review['total_words']}")
    print(f"   - Flesch score: {final_review['flesch_score']:.1f}")
    print(f"   - Status: {article.status}")

    return article
