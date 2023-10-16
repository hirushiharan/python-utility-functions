import pandas as pd

class ExcelReader:
    def __init__(self, file_path, selected_columns=None):
        self.file_path = file_path
        self.df = None
        self.selected_columns = selected_columns

    def read_excel(self):
        # Read the Excel file using the 'openpyxl' engine
        self.df = pd.read_excel(self.file_path, engine='openpyxl')

    def iterate_rows(self):
        if self.df is None:
            print("Error: DataFrame is not initialized. Call read_excel() first.")
            return

        # If selected_columns is not provided, use all columns
        if self.selected_columns is None:
            self.selected_columns = self.df.columns

        # Iterate through each row
        for index, row in self.df.iterrows():
            # Access values in selected columns for the current row
            values = [row[column] for column in self.selected_columns]

            # Print or process the values as needed
            print(values)

# Example usage
excel_reader_5_columns = ExcelReader('sample-debt-upload-data.xlsx', selected_columns=['debtorName', 'debtorType', 'debtorEmail', 'city', 'state'])
excel_reader_5_columns.read_excel()
excel_reader_5_columns.iterate_rows()

excel_reader_4_columns = ExcelReader('sample-debt-upload-data.xlsx', selected_columns=['debtorName', 'debtorType', 'debtorEmail', 'state'])
excel_reader_4_columns.read_excel()
excel_reader_4_columns.iterate_rows()