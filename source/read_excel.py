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

        # Initialize an empty list to store dictionaries for each row
        rows_data = []

        # Iterate through each row
        for index, row in self.df.iterrows():
            # Create a dictionary for the current row
            row_data = {column: row[column] for column in self.selected_columns}
            
            # Append the dictionary to the list
            rows_data.append(row_data)

        # Return the list of dictionaries
        return rows_data

# Example usage
excel_reader_6_columns = re.ExcelReader('./assets/sample-debt-upload-data.xlsx', selected_columns=['city', 'state'])
excel_reader_6_columns.read_excel()
values = excel_reader_6_columns.iterate_rows()

# Print the list of dictionaries
for row_data in values:
    print(row_data)