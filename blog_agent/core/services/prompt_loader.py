"""
Prompt Loader

Loads and renders prompt templates with variable substitution.
"""
from pathlib import Path
from typing import Dict, Any
import re


class PromptLoader:
    """Load and render prompt templates"""

    def __init__(self, prompts_dir: Path):
        """
        Initialize prompt loader

        Args:
            prompts_dir: Path to prompts directory
        """
        self.prompts_dir = prompts_dir

    def load(self, prompt_path: str) -> str:
        """
        Load prompt template

        Args:
            prompt_path: Relative path to prompt (e.g., "konspekt/prompt_konspekt_artykulu.md")

        Returns:
            Prompt template content
        """
        full_path = self.prompts_dir / prompt_path
        with open(full_path, 'r', encoding='utf-8') as f:
            return f.read()

    def render(self, template: str, variables: Dict[str, Any]) -> str:
        """
        Render prompt template with variables

        Replaces {{VARIABLE_NAME}} with values from variables dict.

        Args:
            template: Prompt template
            variables: Variable values

        Returns:
            Rendered prompt
        """
        rendered = template

        # Find all variables in template
        pattern = r'\{\{([A-Z_]+)\}\}'
        found_vars = set(re.findall(pattern, template))

        # Replace each variable
        for var_name in found_vars:
            if var_name in variables:
                value = variables[var_name]
                # Convert to string if not already
                if not isinstance(value, str):
                    value = str(value)
                rendered = rendered.replace(f'{{{{{var_name}}}}}', value)
            else:
                # Variable not provided - leave placeholder or raise error
                raise ValueError(f"Variable '{var_name}' not provided for prompt template")

        return rendered

    def load_and_render(self, prompt_path: str, variables: Dict[str, Any]) -> str:
        """
        Load and render prompt in one step

        Args:
            prompt_path: Relative path to prompt
            variables: Variable values

        Returns:
            Rendered prompt
        """
        template = self.load(prompt_path)
        return self.render(template, variables)

    def list_prompts(self, subdir: str = "") -> list[str]:
        """
        List available prompts

        Args:
            subdir: Optional subdirectory (e.g., "konspekt", "articles")

        Returns:
            List of prompt paths
        """
        search_dir = self.prompts_dir / subdir if subdir else self.prompts_dir
        prompts = []

        for prompt_file in search_dir.rglob("*.md"):
            # Get relative path from prompts_dir
            rel_path = prompt_file.relative_to(self.prompts_dir)
            prompts.append(str(rel_path))

        return sorted(prompts)

    def get_common_prompt(self) -> str:
        """
        Load common article prompt (prompt_artykul_common.md)

        Returns:
            Common prompt content
        """
        return self.load("articles/prompt_artykul_common.md")
