import pandas as pd
import xlsxwriter

class ExcelHandler:
    """
    A class to handle reading from and writing to Excel files.

    Attributes:
    input_file (str): Path to the input Excel file.
    output_file (str): Path to the output Excel file.
    df (DataFrame): Pandas DataFrame to hold the read data.
    selected_columns (list): List of columns to be selected from the input file.
    workbook (Workbook): XlsxWriter Workbook object.
    sheet (Worksheet): XlsxWriter Worksheet object.
    row (int): Row index for writing data.
    col (int): Column index for writing data.
    """

    def __init__(self, input_file, output_file):
        """
        Initializes the ExcelHandler with input and output file paths.

        Parameters:
        input_file (str): Path to the input Excel file.
        output_file (str): Path to the output Excel file.
        """
        self.input_file = input_file
        self.output_file = output_file
        self.df = None
        self.selected_columns = None
        self.workbook = None
        self.sheet = None
        self.row = 0
        self.col = 0

    def read_excel(self):
        """
        Reads the input Excel file into a Pandas DataFrame.
        """
        self.df = pd.read_excel(self.input_file, engine='openpyxl')

    def iterate_rows(self):
        """
        Iterates through rows of the DataFrame and returns data as a list of dictionaries.

        Returns:
        list: A list of dictionaries, each representing a row.
        """
        if self.df is None:
            print("Error: DataFrame is not initialized. Call read_excel() first.")
            return []

        if self.selected_columns is None:
            self.selected_columns = self.df.columns

        rows_data = []

        for index, row in self.df.iterrows():
            row_data = {column: row[column] for column in self.selected_columns}
            rows_data.append(row_data)

        return rows_data

    def create_workbook(self):
        """
        Creates a new XlsxWriter Workbook.
        """
        self.workbook = xlsxwriter.Workbook(self.output_file)

    def create_worksheet(self, sheet_name):
        """
        Creates a new worksheet in the workbook.

        Parameters:
        sheet_name (str): Name of the worksheet to be created.
        """
        self.sheet = self.workbook.add_worksheet(sheet_name)
        self.row = 0
        self.col = 0

    def write_data(self, data):
        """
        Writes data to the worksheet.

        Parameters:
        data (list): A list of lists, where each sublist represents a row.
        """
        if self.sheet is None:
            print("Error: Worksheet is not initialized. Call create_worksheet() first.")
            return

        for item in data:
            for value in item:
                self.sheet.write(self.row, self.col, value)
                self.col += 1
            self.row += 1
            self.col = 0  # Reset column position for the next row

    def close_workbook(self):
        """
        Closes the XlsxWriter Workbook.
        """
        if self.workbook:
            self.workbook.close()

# Example usage
if __name__ == "__main__":
    # Initialize ExcelHandler for reading and writing
    excel_handler = ExcelHandler(input_file='./assets/sample-debt-upload-data.xlsx', output_file='example.xlsx')

    # Reading from Excel
    excel_handler.read_excel()
    values = excel_handler.iterate_rows()
    print("Read data:")
    for row_data in values:
        print(row_data)

    # Writing to Excel
    excel_handler.create_workbook()
    excel_handler.create_worksheet(sheet_name='my_sheet')

    # Example data to write
    scores = [
        ['ankit', 1000],
        ['rahul', 100],
        ['priya', 300],
        ['harshita', 50],
    ]

    # Write data to the worksheet
    excel_handler.write_data(scores)

    # Close the workbook
    excel_handler.close_workbook()
