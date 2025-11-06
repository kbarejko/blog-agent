"""
Git Operations

Wrapper for git commands to ensure consistency.
"""
import subprocess
from pathlib import Path
from typing import Optional, List


class GitOperations:
    """Git operations wrapper"""

    def __init__(self, repo_path: Path):
        """
        Initialize git operations

        Args:
            repo_path: Path to git repository
        """
        self.repo_path = repo_path

    def _run_command(self, command: List[str]) -> tuple[int, str, str]:
        """
        Run git command

        Args:
            command: Command parts (e.g., ['git', 'status'])

        Returns:
            (return_code, stdout, stderr)
        """
        result = subprocess.run(
            command,
            cwd=self.repo_path,
            capture_output=True,
            text=True
        )
        return result.returncode, result.stdout, result.stderr

    def is_git_repo(self) -> bool:
        """Check if directory is a git repository"""
        git_dir = self.repo_path / ".git"
        return git_dir.exists() and git_dir.is_dir()

    def init(self) -> bool:
        """
        Initialize git repository

        Returns:
            True if successful
        """
        returncode, stdout, stderr = self._run_command(['git', 'init'])
        return returncode == 0

    def add(self, paths: List[Path]) -> bool:
        """
        Add files to staging

        Args:
            paths: List of file paths to add

        Returns:
            True if successful
        """
        # Convert paths to relative paths from repo root
        relative_paths = [str(p.relative_to(self.repo_path)) for p in paths]
        command = ['git', 'add'] + relative_paths
        returncode, stdout, stderr = self._run_command(command)
        return returncode == 0

    def commit(self, message: str, author: Optional[str] = None) -> bool:
        """
        Create git commit

        Args:
            message: Commit message
            author: Optional author string

        Returns:
            True if successful
        """
        command = ['git', 'commit', '-m', message]

        if author:
            command.extend(['--author', author])

        returncode, stdout, stderr = self._run_command(command)
        return returncode == 0

    def status(self) -> str:
        """
        Get git status

        Returns:
            Git status output
        """
        returncode, stdout, stderr = self._run_command(['git', 'status'])
        return stdout

    def get_current_branch(self) -> Optional[str]:
        """
        Get current branch name

        Returns:
            Branch name or None if not in a repo
        """
        returncode, stdout, stderr = self._run_command(['git', 'rev-parse', '--abbrev-ref', 'HEAD'])
        if returncode == 0:
            return stdout.strip()
        return None

    def has_changes(self) -> bool:
        """
        Check if there are uncommitted changes

        Returns:
            True if there are changes
        """
        returncode, stdout, stderr = self._run_command(['git', 'status', '--porcelain'])
        return bool(stdout.strip())

    def get_last_commit_message(self) -> Optional[str]:
        """
        Get last commit message

        Returns:
            Commit message or None
        """
        returncode, stdout, stderr = self._run_command(['git', 'log', '-1', '--pretty=%B'])
        if returncode == 0:
            return stdout.strip()
        return None

    def commit_article_stage(
        self,
        article_path: Path,
        stage_name: str,
        description: str
    ) -> bool:
        """
        Commit article at specific stage

        Args:
            article_path: Path to article directory
            stage_name: Stage name (outline, draft, publication, categories)
            description: Additional description

        Returns:
            True if successful
        """
        # Get series/silo/slug from path
        parts = article_path.parts
        if len(parts) >= 4 and parts[-4] == "artykuly":
            series = parts[-3]
            silo = parts[-2]
            slug = parts[-1]
            prefix = f"[{series}/{silo}/{slug}]"
        else:
            prefix = f"[{article_path.name}]"

        # Create commit message
        message = f"{prefix} {description}\n\n🤖 Generated with [Claude Code](https://claude.com/claude-code)\n\nCo-Authored-By: Claude <noreply@anthropic.com>"

        # Add all files in article directory
        files_to_add = list(article_path.glob("**/*"))
        files_to_add = [f for f in files_to_add if f.is_file()]

        if not files_to_add:
            return False

        # Add and commit
        if not self.add(files_to_add):
            return False

        return self.commit(message)
