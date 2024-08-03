import unittest
from app.python_utils.src.excel_functions import ExcelReader, WriteToExcel

class TestExcelFunctions(unittest.TestCase):
    def test_write_and_read_excel(self):
        file_path = "app/python_utils/src/local_test/example.xlsx"
        
        # Define headers and data
        headers = ['name', 'age', 'score']
        scores = [
            ['ankit', 12, 1000],
            ['rahul', 13, 100],
            ['priya', 12, 300],
            ['harshita', 12, 50],
        ]

        # Create an instance of WriteToExcel
        excel = WriteToExcel(file_path)

        # Write data to the Excel file
        excel.write_data_to_excel(file_path, "sheet_1", 0, 0, headers, scores)

        # Read Score data from example.xlsx Excel file
        excel_columns = ExcelReader(file_path, selected_columns=['name', 'score'])
        excel_columns.read_excel()
        values = list(excel_columns.iterate_rows())

        for row_data in values:
            print(row_data)
            # You can add assertions here to validate the output

if __name__ == '__main__':
    unittest.main()
