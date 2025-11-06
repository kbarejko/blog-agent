"""
Payload CMS Adapter

Transforms articles to Payload CMS v3 format and publishes via API.
"""
from typing import Dict, Any, List
from pathlib import Path
import requests

from ...core.domain.article import Article


class PayloadAdapter:
    """
    Payload CMS v3 adapter

    Transforms markdown articles to Payload format and publishes via API.
    """

    def __init__(self, config: Dict[str, Any]):
        """
        Initialize Payload adapter

        Config:
            api_url: Payload API URL
            api_key: API key
            collection: Collection name (default: 'articles')
        """
        self.api_url = config['api_url'].rstrip('/')
        self.api_key = config['api_key']
        self.collection = config.get('collection', 'articles')

    def transform(self, article: Article) -> Dict[str, Any]:
        """
        Transform article to Payload format

        Uses Markdown-based blocks (not Lexical JSON).

        Args:
            article: Article to transform

        Returns:
            Payload document structure
        """
        if not article.final_content:
            raise ValueError("Article must have final content")

        # Get series/silo/slug for URL
        series, silo, slug = article.get_series_silo_slug()

        # Base document
        doc = {
            'title': article.config.title,
            'slug': slug,
            'metaTitle': article.config.meta_title,
            'metaDescription': article.config.meta_description,
            'series': series,
            'silo': silo,
            'targetAudience': article.config.target_audience,
            'tone': article.config.tone,
            'status': 'draft',  # or 'published'
            'blocks': []
        }

        # Main content block (richText with markdown)
        doc['blocks'].append({
            'blockType': 'richText',
            'content': article.final_content
        })

        # FAQ block (if exists)
        if article.outline and article.outline.has_faq:
            # Parse FAQ from final content
            # For now, placeholder - actual parsing can be added later
            doc['blocks'].append({
                'blockType': 'faq',
                'questions': []  # Would be parsed from content
            })

        # Checklist block (if exists)
        if article.outline and article.outline.has_checklist:
            # Parse checklist from final content
            doc['blocks'].append({
                'blockType': 'checklist',
                'items': []  # Would be parsed from content
            })

        # Related articles block (if internal links exist)
        if article.internal_links:
            doc['blocks'].append({
                'blockType': 'relatedArticles',
                'articles': [
                    {
                        'title': link['title'],
                        'url': link['url'],
                        'description': link.get('description', '')
                    }
                    for link in article.internal_links.related_articles
                ]
            })

        # Categories
        if article.categories:
            doc['categories'] = article.categories

        # Business metadata
        if article.business_metadata:
            doc['businessMetadata'] = {
                'targetBusiness': article.business_metadata.target_business,
                'industry': article.business_metadata.industry,
                'projectPhase': article.business_metadata.project_phase,
                'investmentLevel': article.business_metadata.investment_level,
                'investmentRange': article.business_metadata.investment_range,
                'timelineEstimate': article.business_metadata.timeline_estimate,
                'complexityTechnical': article.business_metadata.complexity_technical,
                'complexityOrganizational': article.business_metadata.complexity_organizational,
                'teamSize': article.business_metadata.team_size
            }

        # Schema markup
        if article.schema_markup:
            doc['schemaMarkup'] = article.schema_markup.to_json_ld()

        return doc

    def publish(self, article: Article) -> Dict[str, Any]:
        """
        Publish article to Payload CMS

        Args:
            article: Article to publish

        Returns:
            API response

        Raises:
            requests.HTTPError: If API request fails
        """
        doc = self.transform(article)

        # API endpoint
        url = f"{self.api_url}/api/{self.collection}"

        # Headers
        headers = {
            'Authorization': f'Bearer {self.api_key}',
            'Content-Type': 'application/json'
        }

        # POST request
        response = requests.post(url, json=doc, headers=headers)
        response.raise_for_status()

        return response.json()

    def update(self, article: Article, document_id: str) -> Dict[str, Any]:
        """
        Update existing article in Payload CMS

        Args:
            article: Article to update
            document_id: Payload document ID

        Returns:
            API response

        Raises:
            requests.HTTPError: If API request fails
        """
        doc = self.transform(article)

        # API endpoint
        url = f"{self.api_url}/api/{self.collection}/{document_id}"

        # Headers
        headers = {
            'Authorization': f'Bearer {self.api_key}',
            'Content-Type': 'application/json'
        }

        # PATCH request
        response = requests.patch(url, json=doc, headers=headers)
        response.raise_for_status()

        return response.json()

    def get_by_slug(self, slug: str) -> Dict[str, Any]:
        """
        Get article by slug from Payload CMS

        Args:
            slug: Article slug

        Returns:
            Article document or None if not found

        Raises:
            requests.HTTPError: If API request fails
        """
        url = f"{self.api_url}/api/{self.collection}"

        headers = {
            'Authorization': f'Bearer {self.api_key}'
        }

        params = {
            'where': {'slug': {'equals': slug}}
        }

        response = requests.get(url, headers=headers, params=params)
        response.raise_for_status()

        data = response.json()
        docs = data.get('docs', [])

        return docs[0] if docs else None
