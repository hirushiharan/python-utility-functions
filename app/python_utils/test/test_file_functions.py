import unittest
from app.python_utils.src.file_functions import FileRenamer

class TestFileFunctions(unittest.TestCase):
    def test_excel_reader(self):
        prefix = 'desktop-wallpaper'
        count = 0
        path = r'D:\repos\python-utility-functions\app\python_utils\src\local_test\Walpapers'

        file_renamer = FileRenamer(path, prefix=prefix, name_format="{prefix}-{count:03d}")
        file_renamer.rename_files()
        pass

if __name__ == '__main__':
    unittest.main()