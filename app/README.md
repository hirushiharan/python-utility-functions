# Python Utils

Welcome to the Python Utils repository! This project contains a collection of utility scripts written in Python for various purposes. Each script focuses on specific functionalities that can be reused across different projects. Below is a detailed description of the project's structure and its components.

### Dependancies: 
    
- pandas
- xlsxwriter
- mysql-connector-python
- python-dotenv

## Requirements

Make sure to install the required packages:

    pip install py-utility-scripts

## Components

### [`excel_functions.py`](python_utils/src/excel_functions.py)

This script provides functionalities for reading from and writing to Excel files using the `pandas` and `xlsxwriter` libraries.

#### Classes:
- **ExcelReader**: Reads data from an Excel file.
- **WriteToExcel**: Writes data to an Excel file.

#### Usage:
1. **ExcelReader**: Instantiate with the path to the Excel file and optional columns to select. Use `read_excel()` to read the file and `iterate_rows()` to get the data as a list of dictionaries.
2. **WriteToExcel**: Instantiate with the path to the Excel file. Use `createWorkbook()`, `createWorksheet()`, `defineRowColumn()`, and `closeWorkbook()` to manage and write data to the workbook.

#### Example

    from python_utils import ExcelReader, WriteToExcel

    # Write Score data to example.xlsx Excel file

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

    # Read Score data from example.xlsx Excel file

    excel_reader_6_columns = ExcelReader('example.xlsx', selected_columns=['name', 'score'])
    excel_reader_6_columns.read_excel()
    values = excel_reader_6_columns.iterate_rows()

    for row_data in values:
        print(row_data)

### [`file_functions.py`](python_utils/src/file_functions.py)

This script renames all files in a specified directory to a sequentially numbered format with a user-defined prefix and format.

#### Class:
- **FileRenamer**: Handles the file renaming process within a specified directory.

#### Usage:
- Create an instance of `FileRenamer` with the desired path, prefix, and format. Use `rename_files()` to apply the renaming.

#### Example

    from python_utils import FileRenamer

    prefix = 'desktop-wallpaper'
    count = 0
    path = r'D:\images\Walpapers'

    file_renamer = FileRenamer(path, name_format="{prefix}-{count:03d}")
    file_renamer.rename_files()

### [`log_message.py`](python_utils/src/log_message.py)

This script provides a flexible logging mechanism that supports logging messages with dynamic log levels to both the console and a log file in JSON format. It also includes log file rotation. Check if the current log file exceeds the predefined maximum size. If it does, the function renames the current log file to include a timestamp in its name and retains it as an old log file. The timestamp format used is 'YYYYMMDD_HHMMSS' to ensure uniqueness and chronological sorting of old log files.

#### Class:
- **Logger**: Handles logging messages with support for dynamic log levels and file rotation.

#### Usage:
- Create an instance of `Logger` and use `log()` to log messages. Use `add_log_level()` and `remove_log_level()` to manage log levels.

#### Example

    from python_utils import Logger

    # Constants for log levels
    INFO = "INFO"
    WARNING = "WARNING"
    ERROR = "ERROR"

    logger = Logger()
    logger.log("This is an info message.", INFO)
    logger.log("This is a warning message.", WARNING)
    logger.log("This is an error message.", ERROR)
    
    # Add a new log level and log a message with it
    logger.add_log_level("DEBUG")
    logger.log("This is a debug message.", "DEBUG")

    # Remove an existing log level
    logger.remove_log_level("DEBUG")

### [`sql_connection.py`](python_utils/src/sql_connection.py)

This script establishes a connection to a MySQL database using credentials stored in environment variables. It uses the `mysql.connector` library for database operations.

#### Class:
- **DatabaseConnector**: Handles loading environment variables, establishing a connection to the MySQL database, and managing the connection.

#### Usage:
- Ensure the `.env` file is properly configured. Create an instance of `DatabaseConnector`, call `connect_to_mysql()` to connect to the database, and `close_connection()` to close it.

#### Configuration

Create a .env file in the root directory of the project with the following format:

    # Database configuration
    DB_HOST=your_db_host
    DB_USER=your_db_user
    DB_PASSWORD=your_db_password
    DB_NAME=your_db_name

#### Example

    from python_utils import DatabaseConnector

    db_connector = DatabaseConnector()
    db_connector.connect_to_mysql()
    db_connector.close_connection()
            