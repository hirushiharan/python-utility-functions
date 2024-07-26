# Python Utils

Welcome to the Python Utils repository! This project contains a collection of utility scripts written in Python for various purposes. Each script focuses on specific functionalities that can be reused across different projects. Below is a detailed description of the project's structure and its components.

## Components

### [`excel_functions.py`](python_utils/src/excel_functions.py)

This script provides functionalities for reading from and writing to Excel files using the `pandas` and `xlsxwriter` libraries.

#### Classes:
- **ExcelReader**: Reads data from an Excel file.
- **WriteToExcel**: Writes data to an Excel file.

#### Usage:
1. **ExcelReader**: Instantiate with the path to the Excel file and optional columns to select. Use `read_excel()` to read the file and `iterate_rows()` to get the data as a list of dictionaries.
2. **WriteToExcel**: Instantiate with the path to the Excel file. Use `createWorkbook()`, `createWorksheet()`, `defineRowColumn()`, and `closeWorkbook()` to manage and write data to the workbook.

### [`file_functions.py`](python_utils/src/file_functions.py)

This script renames all files in a specified directory to a sequentially numbered format with a user-defined prefix and format.

#### Class:
- **FileRenamer**: Handles the file renaming process within a specified directory.

#### Usage:
- Create an instance of `FileRenamer` with the desired path, prefix, and format. Use `rename_files()` to apply the renaming.

### [`log_message.py`](python_utils/src/log_message.py)

This script provides a flexible logging mechanism that supports logging messages with dynamic log levels to both the console and a log file in JSON format. It also includes log file rotation.

#### Class:
- **Logger**: Handles logging messages with support for dynamic log levels and file rotation.

#### Usage:
- Create an instance of `Logger` and use `log()` to log messages. Use `add_log_level()` and `remove_log_level()` to manage log levels.

### [`ql_connection.py`](python_utils/src/sql_connection.py)

This script establishes a connection to a MySQL database using credentials stored in environment variables. It uses the `mysql.connector` library for database operations.

#### Class:
- **DatabaseConnector**: Handles loading environment variables, establishing a connection to the MySQL database, and managing the connection.

#### Usage:
- Ensure the `.env` file is properly configured. Create an instance of `DatabaseConnector`, call `connect_to_mysql()` to connect to the database, and `close_connection()` to close it.

## Requirements

Make sure to install the required packages listed in `requirements.txt`:

- pandas
- xlsxwriter
- mysql-connector-python
- python-dotenv

## Configuration

Create a .env file in the root directory of the project with the following format:

    # Database configuration
    DB_HOST=your_db_host
    DB_USER=your_db_user
    DB_PASSWORD=your_db_password
    DB_NAME=your_db_name