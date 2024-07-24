"""
This script provides functionalities for reading from and writing to Excel files using the pandas 
and xlsxwriter libraries. The ExcelReader class reads specified columns from an Excel file and 
returns the data as a list of dictionaries. The WriteToExcel class creates new Excel workbooks 
and worksheets, and writes data to them.

Classes:
- ExcelReader: Reads data from an Excel file.
- WriteToExcel: Writes data to an Excel file.

Usage:
- Instantiate the ExcelReader class with the path to the Excel file and optional selected columns.
- Call the read_excel method to read the file, and iterate_rows to get data as a list of dictionaries.
- Instantiate the WriteToExcel class with the path to the Excel file.
- Use the createWorkbook, closeWorkbook, createWorksheet, and defineRowColumn methods to write data.
"""

import pandas as pd
import xlsxwriter

class ExcelReader:
    """
    A class to read data from an Excel file.

    Attributes:
    file_path (str): Path to the Excel file.
    df (pandas.DataFrame): DataFrame to store the Excel data.
    selected_columns (list): List of columns to read from the Excel file.

    Methods:
    read_excel(): Reads the Excel file using the 'openpyxl' engine.
    iterate_rows(): Iterates through the rows of the DataFrame and returns a list of dictionaries.
    """
    
    def __init__(self, file_path, selected_columns=None):
        """
        Initializes the ExcelReader with the file path and optional selected columns.

        Parameters:
        file_path (str): Path to the Excel file.
        selected_columns (list, optional): List of columns to read. Defaults to None.
        """
        self.file_path = file_path
        self.df = None
        self.selected_columns = selected_columns

    def read_excel(self):
        """
        Reads the Excel file using the 'openpyxl' engine and stores it in a DataFrame.
        
        Returns:
            None
        """
        self.df = pd.read_excel(self.file_path, engine='openpyxl')

    def iterate_rows(self):
        """
        Iterates through the rows of the DataFrame and returns a list of dictionaries.
        Each dictionary contains the data for one row, with keys as column names.

        Returns:
        list: A list of dictionaries, each representing a row of data.
        """
        if self.df is None:
            print("Error: DataFrame is not initialized. Call read_excel() first.")
            return

        if self.selected_columns is None:
            self.selected_columns = self.df.columns

        rows_data = []
        for index, row in self.df.iterrows():
            row_data = {column: row[column] for column in self.selected_columns}
            rows_data.append(row_data)

        return rows_data

class WriteToExcel:
    """
    A class to write data to an Excel file.

    Attributes:
    workbook (str): Path to the Excel file.

    Methods:
    createWorkbook(): Creates a new Excel workbook.
    closeWorkbook(workbook): Closes the opened workbook.
    createWorksheet(workbook, sheet): Creates a new worksheet in the workbook.
    defineRowColumn(rowNum, columnNum): Defines the initial row and column for writing data.
    """
    
    def __init__(self, workbook) -> None:
        """
        Initializes the WriteToExcel with the file path.

        Parameters:
        workbook (str): Path to the Excel file.
        """
        self.workbook = workbook

    def createWorkbook(self):
        """
        Creates a new Excel workbook.

        Returns:
        xlsxwriter.Workbook: The created workbook object.
        """
        file = xlsxwriter.Workbook(self.workbook)
        return file
    
    def closeWorkbook(self, workbook):
        """
        Closes the opened workbook.

        Parameters:
        workbook (xlsxwriter.Workbook): The workbook object to close.

        Returns:
            None
        """
        workbook.close()

    def createWorksheet(self, workbook, sheet):
        """
        Creates a new worksheet in the workbook.

        Parameters:
        workbook (xlsxwriter.Workbook): The workbook object.
        sheet (str): Name of the new worksheet.

        Returns:
        xlsxwriter.Workbook.worksheet: The created worksheet object.
        """
        worksheet = workbook.add_worksheet(sheet)
        return worksheet
    
    def defineRowColumn(self, rowNum, columnNum):
        """
        Defines the initial row and column for writing data.

        Parameters:
        rowNum (int): Initial row number.
        columnNum (int): Initial column number.

        Returns:
        tuple: A tuple containing the initial row and column.
        """
        row = rowNum
        col = columnNum
        return row, col

# Example usage of the classes

# Reading from an Excel file
excel_reader_6_columns = ExcelReader('./assets/sample-debt-upload-data.xlsx', selected_columns=['city', 'state'])
excel_reader_6_columns.read_excel()
values = excel_reader_6_columns.iterate_rows()

for row_data in values:
    print(row_data)

# Writing to an Excel file
excel = WriteToExcel("example.xlsx")
file = excel.createWorkbook()
sheet = excel.createWorksheet(file, "my_sheet")
row, col = excel.defineRowColumn(0, 0)

scores = [
    ['ankit', 1000],
    ['rahul', 100],
    ['priya', 300],
    ['harshita', 50],
]

for name, score in scores:
    sheet.write(row, col, name)
    sheet.write(row, col + 1, score)
    row += 1

excel.closeWorkbook(file)
