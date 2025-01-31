"""
Module: excel_functions.py

Description:
    This module provides functionalities for reading from and writing to Excel files using 
    the pandas and xlsxwriter libraries. It includes two primary classes:

1. **ExcelReader**: A utility class for reading data from an Excel file. It supports reading  
       specific columns and returning data as a list of dictionaries.
2. **WriteToExcel**: A utility class for creating new Excel workbooks and worksheets, 
       writing data to them, and managing workbook operations.
    
Imports:
    - `pandas`: For reading Excel files into a DataFrame.
    - `xlsxwriter`: For creating and writing to Excel workbooks and worksheets.
    - `Logger`: For logging operations and errors (imported from the log_message module).
"""

import pandas as pd
import xlsxwriter
import logging

# Set up logging for this module
logger = logging.getLogger(__name__)

class ExcelReader:
    """
    A class to read data from an Excel file.

    Attributes:
        file_path (str): Path to the Excel file.
        df (pandas.DataFrame): DataFrame to store the Excel data.
        selected_columns (list, optional): List of columns to read from the Excel file.

    Methods:
        __init__(file_path, selected_columns=None): Initializes the ExcelReader with the file path and optional selected columns.
        read_excel(): Reads the Excel file using the 'openpyxl' engine and stores it in a DataFrame.
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
        try:
            self.df = pd.read_excel(self.file_path, engine='openpyxl')
            logger.info("Excel file read successfully.")
        except Exception as e:
            logger.error(f"Failed to read the Excel file: {e}")
            raise SystemError("Failed to read the Excel file.")

    def iterate_rows(self):
        """
        Iterates through the rows of the DataFrame and returns a list of dictionaries.
        Each dictionary contains the data for one row, with keys as column names.

        Returns:
            list: A list of dictionaries, each representing a row of data.

        Raises:
            ValueError: If the DataFrame is not initialized.
        """
        if self.df is None:
            logger.error("DataFrame is not initialized. Ensure read_excel() is called first.")
            raise ValueError("DataFrame is not initialized")

        if self.selected_columns is None:
            self.selected_columns = self.df.columns.tolist()

        rows_data = []
        for _, row in self.df.iterrows():
            row_data = {column: row[column] for column in self.selected_columns}
            rows_data.append(row_data)

        logger.info("Rows iterated and data extracted successfully.")
        return rows_data


class WriteToExcel:
    """
    A class to write data to an Excel file.

    Attributes:
        file_name (str): Path to the Excel file.
        workbook (xlsxwriter.Workbook, optional): The workbook object for writing data.

    Methods:
        __init__(file_name): Initializes the WriteToExcel with the file path.
        createWorkbook(): Creates a new Excel workbook.
        closeWorkbook(): Closes the opened workbook.
        createWorksheet(sheet_name): Creates a new worksheet in the workbook.
        write_data_to_excel(sheet_name, headers, data): Writes data to an Excel file, including headers and rows.
    """
    
    def __init__(self, file_name) -> None:
        """
        Initializes the WriteToExcel with the file path.

        Parameters:
            file_name (str): Path to the Excel file.
        """
        self.file_name = file_name
        self.workbook = None

    def createWorkbook(self):
        """
        Creates a new Excel workbook.

        Returns:
            xlsxwriter.Workbook: The created workbook object.

        Raises:
            Exception: If the workbook creation fails.
        """
        try:
            self.workbook = xlsxwriter.Workbook(self.file_name)
            logger.info("Excel workbook created successfully.")
        except Exception as e:
            logger.error(f"Failed to create Excel workbook: {e}")
            raise SystemError("Failed to create Excel workbook.")
        return self.workbook
    
    def closeWorkbook(self):
        """
        Closes the opened workbook.

        Returns:
            None
        """
        if self.workbook:
            self.workbook.close()
            logger.info("Excel workbook closed successfully.")

    def createWorksheet(self, sheet_name):
        """
        Creates a new worksheet in the workbook.

        Parameters:
            sheet_name (str): Name of the new worksheet.

        Returns:
            xlsxwriter.Workbook.worksheet: The created worksheet object.

        Raises:
            ValueError: If the workbook is not created.
            Exception: If the worksheet creation fails.
        """
        if not self.workbook:
            logger.error("Workbook must be created before adding a worksheet.")
            raise ValueError("Workbook must be created before adding a worksheet.")
        
        try:
            worksheet = self.workbook.add_worksheet(sheet_name)
            logger.info(f"Worksheet '{sheet_name}' created successfully.")
        except Exception as e:
            logger.error(f"Failed to create worksheet '{sheet_name}': {e}")
            raise SystemError("Failed to create worksheet '{sheet_name}'.")
        return worksheet

    def write_data_to_excel(self, sheet_name, headers, data):
        """
        Writes data to an Excel file, including headers and data rows.

        Parameters:
            sheet_name (str): The name of the Excel worksheet to write data to.
            headers (list): A list of column headers.
            data (list): A list of dictionaries containing the data to write.

        Returns:
            None

        Raises:
            Exception: If writing data to the Excel file fails.
        """
        try:
            self.createWorkbook()
            worksheet = self.createWorksheet(sheet_name)

            # Write the column headers
            for col_num, header in enumerate(headers):
                worksheet.write(0, col_num, header)

            # Write the data rows
            for row_num, row_data in enumerate(data, start=1):
                if isinstance(row_data, dict):  # Validate row_data type
                    for col_num, header in enumerate(headers):
                        worksheet.write(row_num, col_num, row_data.get(header, ""))  # Default to empty string if key is missing
                else:
                    logger.error(f"Invalid data format in row {row_num}: Expected dict, got {type(row_data)}")
                    raise ValueError(f"Invalid data format in row {row_num}: Expected dict, got {type(row_data)}")
                
            self.closeWorkbook()
            logger.info("Data written to Excel file successfully.")
        except Exception as e:
            logger.error(f"Failed to write data to Excel: {e}")
            raise SystemError("Failed to write data to Excel.")
