"""
This script renames all files in a specified directory to a sequentially 
numbered format with the prefix .

Functions:
- get_paths(path): Returns a list of files and directories in the given path.
- rename_file(old_name, new_name): Renames a file or folder.
- main(): Main function to rename all files in the specified directory.

Usage:
- Ensure the 'path' variable in the main function is set to the target directory.
- Run the script to rename files as '<PREFIX>-1', '<PREFIX>-2', etc., based on their original order.

Note:
- This script does not handle subdirectories; it processes files in the specified directory only.
- Ensure appropriate permissions and backups before running the script.
"""

import os

def get_paths(path):
    """
    Returns all the files and directories in the given path.

    Parameters:
    path (str): The path to the directory to list files from.

    Returns:
    list: A list of files and directories in the specified path.
    """
    return os.listdir(path)

def rename_file(old_name, new_name):
    """
    Renames a file or folder from old_name to new_name.

    Parameters:
    old_name (str): The current name of the file or folder.
    new_name (str): The new name for the file or folder.
    """
    os.rename(old_name, new_name)

def main():
    """
    Main function to rename all files in the specified directory to a 
    sequentially numbered format with the prefix.

    The function will:
    1. Retrieve all files from the given directory.
    2. Iterate through each file, generating a new name in the format '<PREFIX>-X.extension'.
    3. Rename each file to the new name.

    Notes:
    - This function does not handle subdirectories; it processes files in the specified directory only.
    - Ensure the specified path is correct and you have appropriate permissions.
    """
    path = r'D:\images\Walpapers'
    files = get_paths(path)
    count = 0
    prefix = "wallpaper"
    name_format = f"{prefix}-{count}"

    for file in files:
        extension = file.split(".")[-1]
        count += 1
        new_name = f"{name_format}.{extension}"
        old_path = os.path.join(path, file)
        new_path = os.path.join(path, new_name)
        rename_file(old_path, new_path)

if __name__ == "__main__":
    main()
