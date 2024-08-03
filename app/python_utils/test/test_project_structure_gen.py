import os
import unittest
from app.python_utils.src.project_structure_gen import ProjectStructure

class TestSqlFunctions(unittest.TestCase):
    def test_sql_functions(self):
        root_path = r'D:\repos\python-utility-functions'
        gitignore_file = os.path.join(root_path, '.gitignore')
        structure_path = os.path.join(root_path, r'app\python_utils\src\local_test\structure.md')

        project_structure = ProjectStructure(root_path, gitignore_file, structure_path)
        project_structure.generate()
        pass

if __name__ == '__main__':
    unittest.main()