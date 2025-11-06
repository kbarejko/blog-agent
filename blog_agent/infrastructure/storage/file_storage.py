"""
File Storage

Handles reading/writing files for articles.
"""
from pathlib import Path
from typing import Optional, List
import json
import yaml


class FileStorage:
    """File system operations for articles"""

    @staticmethod
    def read_file(path: Path) -> str:
        """
        Read file content

        Args:
            path: File path

        Returns:
            File content as string
        """
        with open(path, 'r', encoding='utf-8') as f:
            return f.read()

    @staticmethod
    def write_file(path: Path, content: str, create_dirs: bool = True) -> None:
        """
        Write content to file

        Args:
            path: File path
            content: Content to write
            create_dirs: Create parent directories if they don't exist
        """
        if create_dirs:
            path.parent.mkdir(parents=True, exist_ok=True)

        with open(path, 'w', encoding='utf-8') as f:
            f.write(content)

    @staticmethod
    def read_yaml(path: Path) -> dict:
        """
        Read YAML file

        Args:
            path: YAML file path

        Returns:
            Parsed YAML as dict
        """
        with open(path, 'r', encoding='utf-8') as f:
            return yaml.safe_load(f)

    @staticmethod
    def write_yaml(path: Path, data: dict, create_dirs: bool = True) -> None:
        """
        Write dict to YAML file

        Args:
            path: YAML file path
            data: Data to write
            create_dirs: Create parent directories
        """
        if create_dirs:
            path.parent.mkdir(parents=True, exist_ok=True)

        with open(path, 'w', encoding='utf-8') as f:
            yaml.dump(
                data,
                f,
                allow_unicode=True,
                default_flow_style=False,
                sort_keys=False,
                indent=2
            )

    @staticmethod
    def read_json(path: Path) -> dict:
        """
        Read JSON file

        Args:
            path: JSON file path

        Returns:
            Parsed JSON as dict
        """
        with open(path, 'r', encoding='utf-8') as f:
            return json.load(f)

    @staticmethod
    def write_json(path: Path, data: dict, create_dirs: bool = True, indent: int = 2) -> None:
        """
        Write dict to JSON file

        Args:
            path: JSON file path
            data: Data to write
            create_dirs: Create parent directories
            indent: JSON indentation
        """
        if create_dirs:
            path.parent.mkdir(parents=True, exist_ok=True)

        with open(path, 'w', encoding='utf-8') as f:
            json.dump(data, f, ensure_ascii=False, indent=indent)

    @staticmethod
    def file_exists(path: Path) -> bool:
        """Check if file exists"""
        return path.exists() and path.is_file()

    @staticmethod
    def dir_exists(path: Path) -> bool:
        """Check if directory exists"""
        return path.exists() and path.is_dir()

    @staticmethod
    def create_dir(path: Path, parents: bool = True) -> None:
        """
        Create directory

        Args:
            path: Directory path
            parents: Create parent directories
        """
        path.mkdir(parents=parents, exist_ok=True)

    @staticmethod
    def list_files(path: Path, pattern: str = "*") -> List[Path]:
        """
        List files in directory

        Args:
            path: Directory path
            pattern: Glob pattern (default: all files)

        Returns:
            List of file paths
        """
        if not path.is_dir():
            return []
        return sorted([p for p in path.glob(pattern) if p.is_file()])

    @staticmethod
    def list_dirs(path: Path) -> List[Path]:
        """
        List subdirectories

        Args:
            path: Directory path

        Returns:
            List of directory paths
        """
        if not path.is_dir():
            return []
        return sorted([p for p in path.iterdir() if p.is_dir()])
