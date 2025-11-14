"""
Workflow Engine

Orchestrates article generation workflow by executing step functions.
"""
from typing import Dict, Any, Callable, List, Optional
from pathlib import Path
import importlib
import yaml

from ..domain.article import Article
from ..factory import DependencyFactory


class WorkflowEngine:
    """
    Workflow execution engine

    Loads workflow configuration and executes steps in sequence.
    """

    def __init__(self, workflow_config_path: Path, factory: Optional[DependencyFactory] = None):
        """
        Initialize workflow engine

        Args:
            workflow_config_path: Path to workflow.yaml
            factory: Optional DependencyFactory for creating per-step providers
        """
        self.workflow_config_path = workflow_config_path
        self.workflow_config = self._load_workflow_config()
        self.step_registry: Dict[str, Callable] = {}
        self.factory = factory  # For creating per-step AI providers

    def _load_workflow_config(self) -> Dict[str, Any]:
        """Load workflow configuration from YAML"""
        with open(self.workflow_config_path, 'r', encoding='utf-8') as f:
            return yaml.safe_load(f)

    def register_step(self, step_name: str, step_func: Callable) -> None:
        """
        Register a step function

        Args:
            step_name: Step name (e.g., "init", "outline")
            step_func: Step function callable(article, deps, config) -> article
        """
        self.step_registry[step_name] = step_func

    def _auto_detect_provider_from_model(self, model: str) -> str:
        """
        Auto-detect provider name from model string

        Args:
            model: Model name (e.g., "gpt-4o", "gemini-2.5-flash", "claude-sonnet-4")

        Returns:
            Provider name
        """
        model_lower = model.lower()

        # GPT models → openai-gpt*
        if model.startswith('gpt-') or 'gpt' in model_lower:
            # Normalize: gpt-5.1 -> gpt5-1, gpt-4o -> gpt4o
            model_normalized = model.replace('.', '-').replace('gpt-', 'gpt')
            return f'openai-{model_normalized}'

        # Gemini models → gemini
        elif model.startswith('gemini'):
            return 'gemini'

        # Claude models → claude
        elif model.startswith('claude'):
            return 'claude'

        # Default: return as-is (assume it's a provider name)
        return model

    def _get_step_ai_provider(self, step_config: Dict[str, Any], default_ai_provider: Any) -> Any:
        """
        Get AI provider for a specific step

        If step has 'provider' or 'model' config, creates a new AI provider.
        Otherwise returns the default provider.

        Args:
            step_config: Step configuration from workflow.yaml
            default_ai_provider: Default AI provider from deps

        Returns:
            AI provider instance for this step
        """
        # Check if step specifies a provider or model
        step_provider = step_config.get('provider')
        step_model = step_config.get('model')

        # No override - use default
        if not step_provider and not step_model:
            return default_ai_provider

        # Need factory to create new provider
        if not self.factory:
            print(f"   ⚠️  Step specifies provider/model but no factory available - using default")
            return default_ai_provider

        # Auto-detect provider from model if specified
        if step_model and not step_provider:
            step_provider = self._auto_detect_provider_from_model(step_model)
            print(f"   🔄 Auto-detected provider: {step_provider} (from model: {step_model})")

        # Create new AI provider for this step
        try:
            provider_config = self.factory._load_provider_config(step_provider)
            from ..infrastructure.ai.provider_registry import ProviderRegistry
            ai_provider = ProviderRegistry.create(step_provider, provider_config)
            print(f"   🔀 Using step-specific provider: {step_provider}")
            return ai_provider
        except Exception as e:
            print(f"   ⚠️  Failed to create step provider '{step_provider}': {e}")
            print(f"   ⚠️  Falling back to default provider")
            return default_ai_provider

    def _load_step_function(self, step_name: str, module_path: str) -> Callable:
        """
        Dynamically load step function from module

        Args:
            step_name: Step name
            module_path: Python module path (e.g., "blog_agent.core.workflow.steps.step_01_init")

        Returns:
            Step function
        """
        if step_name in self.step_registry:
            return self.step_registry[step_name]

        # Import module
        module = importlib.import_module(module_path)

        # Get execute function (e.g., execute_init, execute_outline)
        func_name = f"execute_{step_name}"
        if not hasattr(module, func_name):
            raise ValueError(f"Module {module_path} missing function {func_name}")

        step_func = getattr(module, func_name)
        self.step_registry[step_name] = step_func

        return step_func

    def execute_workflow(
        self,
        article: Article,
        deps: Dict[str, Any],
        skip_steps: List[str] = None,
        only_steps: List[str] = None
    ) -> Article:
        """
        Execute complete workflow

        Args:
            article: Article to process
            deps: Dependencies dict (ai, prompts, storage, git, etc.)
            skip_steps: Optional list of step names to skip
            only_steps: Optional list of step names to execute (skips all others)

        Returns:
            Processed article
        """
        skip_steps = skip_steps or []
        steps = self.workflow_config.get('steps', [])

        print(f"\n{'='*60}")
        print(f"🚀 Starting workflow: {len(steps)} steps")
        print(f"{'='*60}\n")

        for step_config in steps:
            step_name = step_config['name']
            step_module = step_config['module']
            step_description = step_config.get('description', step_name)
            step_enabled = step_config.get('enabled', True)

            # Check if step should be executed
            if not step_enabled:
                print(f"⏭️  Skipping {step_name} (disabled in config)")
                continue

            if skip_steps and step_name in skip_steps:
                print(f"⏭️  Skipping {step_name} (explicitly skipped)")
                # Try to load existing data when skipping steps
                self._load_existing_data_for_step(article, step_name, deps)
                continue

            if only_steps and step_name not in only_steps:
                print(f"⏭️  Skipping {step_name} (not in only_steps)")
                # Try to load existing data when skipping steps
                self._load_existing_data_for_step(article, step_name, deps)
                continue

            # Execute step
            print(f"\n{'─'*60}")
            print(f"🔄 Step: {step_description}")
            print(f"{'─'*60}")

            try:
                # Load step function
                step_func = self._load_step_function(step_name, step_module)

                # Get step-specific AI provider (if configured)
                step_ai_provider = self._get_step_ai_provider(step_config, deps.get('ai'))

                # Create step-specific deps if provider is different
                step_deps = deps
                if step_ai_provider is not deps.get('ai'):
                    # Shallow copy deps and replace AI provider
                    step_deps = {**deps, 'ai': step_ai_provider}

                # Execute step
                article = step_func(article, step_deps, step_config)

                print(f"✅ Step completed: {step_name}\n")

            except Exception as e:
                print(f"❌ Step failed: {step_name}")
                print(f"   Error: {str(e)}\n")
                raise

        print(f"\n{'='*60}")
        print(f"✅ Workflow completed successfully!")
        print(f"{'='*60}\n")

        return article

    def _load_existing_data_for_step(
        self,
        article: Article,
        step_name: str,
        deps: Dict[str, Any]
    ) -> None:
        """
        Load existing data from files when a step is skipped

        Args:
            article: Article object to load data into
            step_name: Name of the skipped step
            deps: Dependencies (storage, etc.)
        """
        storage = deps.get('storage')
        if not storage:
            return

        try:
            # Load data based on step name
            if step_name == 'outline':
                # Load outline.md if it exists
                outline_path = article.get_outline_path()
                if outline_path.exists():
                    from ..domain.value_objects import Outline
                    import re

                    content = storage.read_file(outline_path)
                    # Parse outline from file (simplified parsing)
                    sections = []
                    lines = content.split('\n')
                    current_section = None

                    for line in lines:
                        line = line.strip()
                        # Look for H2 headings (## Title)
                        match = re.match(r'^##\s+(?:\d+\.\s+)?(.+)$', line)
                        if match:
                            if current_section:
                                sections.append(current_section)
                            current_section = {
                                'title': match.group(1).strip(),
                                'description': ''
                            }
                        elif current_section and line and not line.startswith('#'):
                            if current_section['description']:
                                current_section['description'] += ' '
                            current_section['description'] += line

                    if current_section:
                        sections.append(current_section)

                    outline = Outline(
                        sections=sections,
                        estimated_word_count=len(sections) * 350
                    )
                    article.set_outline(outline)
                    print(f"   📄 Loaded existing outline ({len(sections)} sections)")

            elif step_name == 'create_draft':
                # Load draft.md if it exists
                draft_path = article.get_draft_path()
                if draft_path.exists():
                    content = storage.read_file(draft_path)
                    article.draft_content = content
                    article.status = "draft_ready"
                    print(f"   📄 Loaded existing draft ({len(content)} chars)")

            elif step_name == 'humanize':
                # Load article.md if it exists
                article_path = article.get_article_path()
                if article_path.exists():
                    content = storage.read_file(article_path)
                    article.final_content = content
                    article.status = "humanized"
                    print(f"   📄 Loaded existing article ({len(content)} chars)")

        except Exception as e:
            # Don't fail if loading doesn't work - just skip silently
            pass

    def execute_single_step(
        self,
        step_name: str,
        article: Article,
        deps: Dict[str, Any]
    ) -> Article:
        """
        Execute a single step

        Args:
            step_name: Name of step to execute
            article: Article to process
            deps: Dependencies

        Returns:
            Processed article
        """
        # Find step config
        steps = self.workflow_config.get('steps', [])
        step_config = None

        for config in steps:
            if config['name'] == step_name:
                step_config = config
                break

        if not step_config:
            raise ValueError(f"Step '{step_name}' not found in workflow config")

        # Load and execute
        step_module = step_config['module']
        step_func = self._load_step_function(step_name, step_module)

        print(f"🔄 Executing step: {step_name}")
        article = step_func(article, deps, step_config)
        print(f"✅ Step completed: {step_name}")

        return article

    def list_steps(self) -> List[Dict[str, Any]]:
        """
        List all steps in workflow

        Returns:
            List of step configurations
        """
        return self.workflow_config.get('steps', [])

    def get_step_count(self) -> int:
        """Get total number of steps"""
        return len(self.workflow_config.get('steps', []))
