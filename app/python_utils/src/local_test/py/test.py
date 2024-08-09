from project_structure_gen import ProjectStructure
import os

# Define the root directory of your project
root_path = r'D:\repos\current\python-utility-functions'

# Specify the .gitignore file to exclude certain files or directories
gitignore_file = os.path.join(root_path, '.gitignore')

# Define the output path for the generated Markdown file
md_file = r'output\structure.md'

# Initialize the ProjectStructure object
project_structure = ProjectStructure(root_path, gitignore_file, md_file)

# Generate the directory structure and save it as a Markdown file
project_structure.generate()