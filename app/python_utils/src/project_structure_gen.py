"""
Module: project_structure_gen.py

Description:
    This module provides functionality to generate and format the directory structure
    of a project, excluding files and directories specified in a .gitignore file.
    It also writes the formatted project structure to a Markdown (.md) file.

Classes:
    ProjectStructure: A class to handle the reading of .gitignore patterns, 
                      generation of project structure, and creation of Markdown files.

Usage:
    Create an instance of the ProjectStructure class with the root directory of
    the project and the path to the .gitignore file. Call the generate() method
    to produce the Markdown file with the project's directory structure.
"""

import os
import fnmatch
from pathlib import Path
from log_message import Logger

# Constants for log levels
INFO = "INFO"
ERROR = "ERROR"

# Initialize the logger
logger = Logger()

class ProjectStructure:
    def __init__(self, root_dir, gitignore_file, custom_patterns, md_file='project_structure.md'):
        """
        Initializes the ProjectStructure instance.

        Args:
            root_dir (str): The root directory of the project.
            gitignore_file (str): The path to the .gitignore file.
            custom_patterns (list): List of custom patterns to ignore.
            md_file (str): The path to the Markdown file where the structure will be saved. Default is 'project_structure.md'.
        """
        self.root_dir = root_dir
        self.gitignore_file = gitignore_file
        self.md_file = md_file
        self.custom_patterns = custom_patterns
        self.gitignore_patterns = self.read_gitignore_patterns()

    def read_gitignore_patterns(self):
        """
        Reads the .gitignore file and returns a list of patterns.

        Returns:
            list: A list of patterns read from the .gitignore file.
        """
        patterns = []
        try:
            with open(self.gitignore_file, 'r') as file:
                for line in file:
                    line = line.strip()
                    if line and not line.startswith('#'):
                        patterns.append(line)
            logger.log("Gitignore patterns captured successfully.", INFO)
        except FileNotFoundError:
            logger.log(f"Error: The file {self.gitignore_file} was not found.", ERROR)
        except IOError as e:
            logger.log(f"Error: An IOError occurred while reading the file: {e}", ERROR)
        
        patterns.extend(self.custom_patterns)
        return patterns

    def is_ignored(self, path):
        """
        Checks if a given path matches any of the .gitignore patterns.

        Args:
            path (str): The path to check.

        Returns:
            bool: True if the path is ignored by any pattern, False otherwise.
        """
        path = path.replace('\\', '/')
        for pattern in self.gitignore_patterns:
            pattern = pattern.replace('\\', '/')
            if fnmatch.fnmatch(path, pattern.rstrip('/') + '/*') or fnmatch.fnmatch(path, pattern.rstrip('/')):
                return True
        return False

    def get_project_structure(self):
        """
        Generates the directory structure of the project, excluding ignored files and directories.

        Returns:
            list: List of paths that are not ignored.
        """
        structure = []
        try:
            for dirpath, dirnames, filenames in os.walk(self.root_dir):
                rel_path = os.path.relpath(dirpath, self.root_dir).replace('\\', '/')
                
                if self.is_ignored(rel_path):
                    dirnames[:] = []  # Don't recurse into ignored directories
                    continue
                
                if rel_path == '.':
                    rel_path = ''
                
                for dirname in dirnames:
                    full_path = os.path.join(rel_path, dirname).replace('\\', '/')
                    if not self.is_ignored(full_path):
                        structure.append(full_path + '/')
                    else:
                        dirnames.remove(dirname)  # Remove ignored directories from the list

                for filename in filenames:
                    full_path = os.path.join(rel_path, filename).replace('\\', '/')
                    if not self.is_ignored(full_path):
                        structure.append(full_path)
        except Exception as e:
            logger.log(f"Error: An exception occurred while generating project structure: {e}", ERROR)
        
        return structure

    def format_structure(self, structure):
        """
        Formats the project structure into a hierarchical text format.

        Args:
            structure (list): List of paths in the project structure.

        Returns:
            str: Formatted project structure.
        """
        formatted = []
        indent = '    '
        
        path_map = {}
        
        for path in structure:
            parts = path.split('/')
            for i in range(len(parts) - 1):
                parent = '/'.join(parts[:i + 1])
                if parent not in path_map:
                    path_map[parent] = []
                if i + 1 < len(parts):
                    child = parts[i + 1]
                    if child not in path_map[parent]:
                        path_map[parent].append(child)
        
        def build_tree(path, level):
            if path in path_map:
                for item in sorted(path_map[path]):
                    formatted.append(f'{indent * level}├── {item}')
                    build_tree(f'{path}/{item}', level + 1)
        
        build_tree('', 0)
        
        return '\n'.join(formatted)

    def add_path(self, formatted, path, depth=1):
        """
        Adds paths to the formatted list with correct indentation.

        Args:
            formatted (list): List of formatted paths.
            path (str): The path to format.
            depth (int): The depth level for indentation.
        """
        parts = path.strip('/').split('/')
        for i, part in enumerate(parts):
            indentation = '│   ' * (depth + i - 1)
            if i == len(parts) - 1:
                if part.endswith('/'):
                    formatted.append(f'{indentation}├── {part.strip("/")}/')
                else:
                    if part == parts[-1] and len(parts) == depth:
                        formatted.append(f'{indentation}└── {part}')
                    else:
                        formatted.append(f'{indentation}├── {part}')
            else:
                if f'{indentation}├── {part}/' not in formatted:
                    formatted.append(f'{indentation}├── {part}/')

    def create_md_file(self):
        """
        Ensures the Markdown file exists. If it does not exist, creates an empty file.

        Returns:
            None
        """
        path = Path(self.md_file)
        try:
            if not path.parent.exists():
                path.parent.mkdir(parents=True, exist_ok=True)
            if not path.exists():
                with open(self.md_file, "w", encoding="utf-8") as file:
                    pass  # Create an empty file
        except IOError as e:
            logger.log(f"Error: An IOError occurred while creating the Markdown file: {e}", ERROR)

    def generate(self):
        """
        Generates the project structure and writes it to the Markdown file.

        Returns:
            None
        """
        try:
            structures = self.get_project_structure()

            patterns_to_remove = ['*/']

            filtered_structure = [structure for structure in structures if not any(fnmatch.fnmatch(structure, pattern) for pattern in patterns_to_remove)]
            
            filtered_structure.sort()
            
            root_folder = self.root_dir.split('\\')[-1] + '/'

            formatted = [root_folder]

            for structure in filtered_structure:
                self.add_path(formatted, structure)

            output = '\n'.join(formatted)

            self.create_md_file()
            with open(self.md_file, "w", encoding="utf-8") as f:
                f.write(output)
        except Exception as e:
            logger.log(f"Error: An exception occurred while generating the Markdown file: {e}", ERROR)
