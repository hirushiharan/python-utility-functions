"""
Module: file_functions.py

Description:
    This module provides functionality for renaming files in a specified directory. 
    The FileRenamer class allows users to rename all files within a directory to a 
    sequentially numbered format with a user-defined prefix and naming format. The 
    module is useful for batch renaming files in a consistent and automated manner.

Classes:
    FileRenamer:
        Handles the file renaming process within a specified directory. 
        The class allows customization of the prefix, starting count, 
        and naming format for the renamed files.

Usage:
    - Set the 'path' variable in the main function to the target directory.
    - Create an instance of FileRenamer with the desired path, prefix, and name format.
    - Run the script to rename files based on the specified format.

Note:
    - This script processes only files in the specified directory and does not handle subdirectories.
    - Ensure appropriate permissions and backups before running the script.

Imports:
    - os: For interacting with the operating system, specifically for directory and file operations.
    - Logger: Custom logging class from log_message.py for logging operations.
"""

import os
from .log_message import Logger

# Constants for log levels
INFO = "INFO"
ERROR = "ERROR"

# Initialize the logger
logger = Logger()

class FileRenamer:
    """
    A class to handle renaming files in a specified directory.

    Attributes:
        path (str): The path to the directory containing files to rename.
        prefix (str): The prefix to use for renamed files.
        count (int): The starting number for the file renaming sequence.
        name_format (str): The format string for renaming files.

    Methods:
        get_paths():
            Returns all files and directories in the specified path.

        rename_file(old_name, new_name):
            Renames a file or folder from old_name to new_name.

        rename_files():
            Renames all files in the specified directory to a sequentially 
            numbered format with the prefix.
    """
    
    def __init__(self, path, prefix="file", count=0, name_format="{prefix}-{count}"):
        """
        Initializes the FileRenamer with the target directory path, prefix, 
        starting count, and name format.

        Parameters:
            path (str): The path to the directory containing files to rename.
            prefix (str): The prefix to use for renamed files.
            count (int): The starting number for the file renaming sequence.
            name_format (str): The format string for renaming files.
        """
        self.path = path
        self.prefix = prefix
        self.count = count
        self.name_format = name_format

    def get_paths(self):
        """
        Retrieves all files and directories in the specified path.

        Returns:
            list: A list of files and directories in the specified path.
        """
        return os.listdir(self.path)

    def rename_file(self, old_name, new_name):
        """
        Renames a file or folder from old_name to new_name.

        Parameters:
            old_name (str): The current name of the file or folder.
            new_name (str): The new name for the file or folder.

        Returns:
            None
        """
        try:
            os.rename(old_name, new_name)
            logger.log(f"Renamed '{old_name}' to '{new_name}'", INFO)
        except Exception as e:
            logger.log(f"Error renaming '{old_name}' to '{new_name}': {str(e)}", ERROR)

    def rename_files(self):
        """
        Renames all files in the specified directory to a sequentially numbered 
        format with the prefix.

        The function performs the following:
        1. Retrieves all files from the specified directory.
        2. Iterates through each file, generating a new name in the format 
           '<PREFIX>-X.extension'.
        3. Renames each file to the new name.

        Notes:
            - The function does not handle subdirectories and processes files 
              in the specified directory only.
            - Ensure the specified path is correct and appropriate permissions 
              are granted.

        Returns:
            None
        """
        files = self.get_paths()

        for file in files:
            extension = file.split(".")[-1]
            new_name = self.name_format.format(prefix=self.prefix, count=self.count) + f".{extension}"
            old_path = os.path.join(self.path, file)
            new_path = os.path.join(self.path, new_name)
            self.rename_file(old_path, new_path)
            self.count += 1

        logger.log(f"Renamed all files in {self.path}", INFO)
