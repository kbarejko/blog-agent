"""
Dependency Factory

Creates and wires up all dependencies for workflow execution.
"""
from typing import Dict, Any
from pathlib import Path
import yaml
import os
import re

from .services.prompt_loader import PromptLoader
from .services.review_service import ReviewService
from .services.category_matcher import CategoryMatcher
from ..infrastructure.ai.provider_registry import ProviderRegistry
from ..infrastructure.storage.file_storage import FileStorage
from ..infrastructure.git.git_ops import GitOperations
from ..infrastructure.yaml.category_reader import CategoryReader
from ..infrastructure.cms.payload_adapter import PayloadAdapter
from ..infrastructure.images.image_generator import ImageGenerator, ImageProviderFactory


class DependencyFactory:
    """
    Factory for creating workflow dependencies

    Handles loading configurations and creating instances.
    """

    def __init__(self, project_root: Path):
        """
        Initialize factory

        Args:
            project_root: Project root directory
        """
        self.project_root = project_root
        self.config_dir = project_root / "blog_agent" / "config"
        self.prompts_dir = project_root / "prompts"
        self.categories_path = project_root / "categories.yaml"

    def create_deps(self, provider_name: str = "claude") -> Dict[str, Any]:
        """
        Create full dependencies dict

        Args:
            provider_name: AI provider to use (default: claude)

        Returns:
            Dependencies dict for workflow
        """
        # Load provider config
        provider_config = self._load_provider_config(provider_name)

        # Create AI provider
        ai_provider = ProviderRegistry.create(provider_name, provider_config)

        # Create infrastructure
        storage = FileStorage()
        git = GitOperations(self.project_root)

        # Create category reader
        category_reader = CategoryReader(self.categories_path)
        category_reader.load()

        # Create services
        prompts = PromptLoader(self.prompts_dir)
        review_config = self._load_review_config()
        review = ReviewService(review_config)
        category_matcher = CategoryMatcher(category_reader)

        # Optional: Payload CMS (if configured)
        payload = None
        try:
            payload_config = self._load_payload_config()
            payload = PayloadAdapter(payload_config)
        except:
            pass  # Payload not configured

        # Optional: Image generator (auto-detect based on API keys)
        # Checks for OPENAI_API_KEY or STABILITY_API_KEY
        image_generator = None
        try:
            image_generator = ImageProviderFactory.auto_detect()
        except:
            pass  # Image generator not available

        return {
            'ai': ai_provider,
            'storage': storage,
            'git': git,
            'prompts': prompts,
            'review': review,
            'category_matcher': category_matcher,
            'payload': payload,
            'image_generator': image_generator,
        }

    def _load_provider_config(self, provider_name: str) -> Dict[str, Any]:
        """
        Load AI provider configuration

        Args:
            provider_name: Provider name

        Returns:
            Provider config dict
        """
        config_path = self.config_dir / "providers.yaml"

        if not config_path.exists():
            # Return default config (will need API key from env)
            return {
                'api_key': os.getenv('ANTHROPIC_API_KEY', ''),
                'model': 'claude-sonnet-4-20250514',
                'max_tokens': 4000,
                'temperature': 1.0
            }

        with open(config_path, 'r', encoding='utf-8') as f:
            config = yaml.safe_load(f)

        providers = config.get('providers', {})
        if provider_name not in providers:
            raise ValueError(f"Provider '{provider_name}' not configured")

        provider_config = providers[provider_name]
        # Replace environment variables in config
        return self._replace_env_vars(provider_config)

    def _load_review_config(self) -> Dict[str, Any]:
        """
        Load review service configuration from workflow.yaml

        Returns:
            Review config dict with min_words, max_words, min_flesch, max_flesch
        """
        workflow_path = self.config_dir / "workflow.yaml"

        if not workflow_path.exists():
            # Return default config
            return {
                'min_words': 300,
                'max_words': 400,
                'min_flesch': 40,
                'max_flesch': 60
            }

        with open(workflow_path, 'r', encoding='utf-8') as f:
            config = yaml.safe_load(f)

        # Get review section, fallback to defaults
        review_config = config.get('review', {})
        return {
            'min_words': review_config.get('min_words', 300),
            'max_words': review_config.get('max_words', 400),
            'min_flesch': review_config.get('min_flesch', 40),
            'max_flesch': review_config.get('max_flesch', 60)
        }

    def _load_payload_config(self) -> Dict[str, Any]:
        """
        Load Payload CMS configuration

        Returns:
            Payload config dict
        """
        config_path = self.config_dir / "payload.yaml"

        with open(config_path, 'r', encoding='utf-8') as f:
            config = yaml.safe_load(f)

        # Replace environment variables in config
        return self._replace_env_vars(config)

    def _replace_env_vars(self, config: Any) -> Any:
        """
        Replace environment variables in config values
        
        Replaces ${VARIABLE_NAME} with values from os.getenv().
        Works recursively for nested dicts and lists.
        
        Args:
            config: Configuration dict, list, or value
            
        Returns:
            Config with environment variables replaced
        """
        if isinstance(config, dict):
            return {key: self._replace_env_vars(value) for key, value in config.items()}
        elif isinstance(config, list):
            return [self._replace_env_vars(item) for item in config]
        elif isinstance(config, str):
            # Check if string matches ${VARIABLE_NAME} pattern
            pattern = r'\$\{([A-Z_][A-Z0-9_]*)\}'
            match = re.fullmatch(pattern, config)
            if match:
                var_name = match.group(1)
                env_value = os.getenv(var_name)
                if env_value is None:
                    raise ValueError(f"Environment variable '{var_name}' not set")
                return env_value
            # Replace inline variables like "prefix ${VAR} suffix"
            def replace_var(m):
                var_name = m.group(1)
                env_value = os.getenv(var_name)
                if env_value is None:
                    raise ValueError(f"Environment variable '{var_name}' not set")
                return env_value
            return re.sub(pattern, replace_var, config)
        else:
            return config

    def get_workflow_config_path(self) -> Path:
        """Get path to workflow.yaml"""
        return self.config_dir / "workflow.yaml"
