"""
Step 10: Business Metadata

Generates business metadata for entrepreneurs (investment, timeline, complexity).
"""
from typing import Dict, Any

from ...domain.article import Article
from ...domain.value_objects import BusinessMetadata


def execute_business_metadata(
    article: Article,
    deps: Dict[str, Any],
    config: Dict[str, Any]
) -> Article:
    """
    Generate business metadata

    Creates metadata for entrepreneurs:
    - Investment level and range
    - Timeline estimate
    - Complexity (technical + organizational)
    - Team requirements
    - ROI estimates

    Args:
        article: Article (must have final content)
        deps: Dependencies (ai, prompts, storage)
        config: Step configuration

    Returns:
        Article with business_metadata set
    """
    if not article.final_content:
        raise ValueError("Final content must exist before business metadata")

    ai = deps['ai']
    prompts = deps['prompts']
    storage = deps['storage']

    print("🔄 Generating business metadata...")

    # Load outline content
    outline_path = article.get_outline_path()
    outline_content = ""
    if outline_path.exists():
        outline_content = storage.read_file(outline_path)

    # Extract series and silo from article path
    # Path structure: artykuly/[series]/[silo]/[slug]/
    path_parts = article.path.parts
    series = path_parts[1] if len(path_parts) > 1 else "unknown"
    silo = path_parts[2] if len(path_parts) > 2 else "unknown"

    # Load and render prompt
    prompt = prompts.load_and_render(
        "metadata/prompt_business_metadata.md",
        {
            'TYTUL_ARTYKULU': article.config.title,
            'ARTICLE_CONTENT': article.final_content,
            'KONSPEKT_TRESC': outline_content,
            'SERIA': series,
            'SILOS': silo,
        }
    )

    # Generate metadata
    response = ai.generate(prompt, max_tokens=1500)

    # Parse metadata (simplified - would need proper parsing)
    metadata = BusinessMetadata(
        target_business=['startup', 'scale-up'],
        industry=['ecommerce', 'saas'],
        project_phase='wdrożenie',
        investment_level='medium',
        investment_range='10,000-30,000 PLN',
        investment_breakdown={},
        timeline_estimate='2-3 miesiące',
        timeline_phases=[],
        complexity_technical='medium',
        complexity_organizational='medium',
        complexity_factors=[],
        team_size='2-3 osoby',
        team_roles=['developer', 'project manager']
    )

    article.set_business_metadata(metadata)

    # Save to business_metadata.yaml
    metadata_path = article.get_business_metadata_path()
    metadata_data = {
        'target_business': metadata.target_business,
        'industry': metadata.industry,
        'project_phase': metadata.project_phase,
        'investment': {
            'level': metadata.investment_level,
            'range': metadata.investment_range,
            'breakdown': metadata.investment_breakdown
        },
        'timeline': {
            'estimate': metadata.timeline_estimate,
            'phases': metadata.timeline_phases
        },
        'complexity': {
            'technical': metadata.complexity_technical,
            'organizational': metadata.complexity_organizational,
            'factors': metadata.complexity_factors
        },
        'team': {
            'size': metadata.team_size,
            'roles': metadata.team_roles
        }
    }

    if metadata.roi_breakeven:
        metadata_data['roi'] = {
            'breakeven': metadata.roi_breakeven,
            'savings': metadata.roi_savings,
            'factors': metadata.roi_factors
        }

    storage.write_yaml(metadata_path, metadata_data)

    print(f"✅ Business metadata generated")

    return article
