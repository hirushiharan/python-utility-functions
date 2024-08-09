# Python Utils

Welcome to the Python Utils repository! This project contains a collection of utility scripts written in Python for various purposes. Each script focuses on specific functionalities that can be reused across different projects. Below is a detailed description of the project's structure and its components.

Refer [`CHANGLOG.md`](../../CHANGELOG.md) for the release updates.

## Components

### [`src/excel_functions.py`](src/excel_functions.py)

This script provides functionalities for reading from and writing to Excel files using the `pandas` and `xlsxwriter` libraries.

#### Classes:
- **ExcelReader**: Reads data from an Excel file.
- **WriteToExcel**: Writes data to an Excel file.

#### Usage:
1. **ExcelReader**: Instantiate with the path to the Excel file and optional columns to select. Use `read_excel()` to read the file and `iterate_rows()` to get the data as a list of dictionaries.
2. **WriteToExcel**: Instantiate with the path to the Excel file. Use `createWorkbook()`, `createWorksheet()`, `defineRowColumn()`, and `closeWorkbook()` to manage and write data to the workbook.

### [`src/file_functions.py`](src/file_functions.py)

This script renames all files in a specified directory to a sequentially numbered format with a user-defined prefix and format.

#### Class:
- **FileRenamer**: Handles the file renaming process within a specified directory.

#### Usage:
- Create an instance of `FileRenamer` with the desired path, prefix, and format. Use `rename_files()` to apply the renaming.

### [`src/log_message.py`](src/log_message.py)

This script provides a flexible logging mechanism that supports logging messages with dynamic log levels to both the console and a log file in JSON format. It also includes log file rotation.

#### Class:
- **Logger**: Handles logging messages with support for dynamic log levels and file rotation.

#### Usage:
- Create an instance of `Logger` and use `log()` to log messages. Use `add_log_level()` and `remove_log_level()` to manage log levels.

### [`src/project_structure_gen.py`](src/project_structure_gen.py)

This script provides a project structure generatoe mechanism to print the given path directory structure.

#### Class:
- **ProjectStructure**: Handles generating project structure for a given directory.

#### Usage:
- Create an instance of `ProjectStructure` and use `generate()` to generate the project structure of a given directory.

### [`src/mysql_connection.py`](src/mysql_connection.py)

This script handles the loading of environment variables and the establishment of connections to a MySQL database. It includes methods for managing the database connection and executing MySQL queries.

#### Classes:
- **LoggingMiddleware**: A middleware class for logging HTTP request and response details. This class logs information about incoming HTTP requests and outgoing responses, which is valuable for monitoring and debugging purposes.
- **Settings**: A configuration class for loading environment variables required for MySQL database configuration. It utilizes Pydantic's `BaseSettings` to load configuration details from environment variables, ensuring secure and configurable database connections.
- **MySqlConnection**: Provides a robust mechanism for managing database connections, including retry logic and connection pooling.
- **MySqlResponse**: Standardizes the response format for MySQL operations, ensuring consistent handling of success and error cases.
- **MySqlExecution**: Encapsulates the logic for executing MySQL queries and managing transactions, simplifying database interactions.
- **MySqlHandler**: Manages asynchronous function execution with standardized exception handling. It ensures consistent error handling and response formatting for asynchronous operations, enhancing the application's reliability.

#### Usage:
- This module can be used in a FastAPI application to manage MySQL database connections and execute MySQL queries with robust error handling. The middleware and utility functions provided streamline logging and response formatting, making the application more maintainable and easier to debug.
- Create a `.env` file to store MySQL credentials. Below is an example `.env` file:

        MYSQL_PASSWORD='<MySQL_PASSWORD>'
        MYSQL_DATABASE='<MySQL_DATABASE>'
        MYSQL_USER='<MySQL_USER>'
        MYSQL_HOST='<MySQL_HOST>'
        MYSQL_PORT='<MySQL_PORT>'

- Instantiate `LoggingMiddleware` to log details about incoming HTTP requests and outgoing responses, which aids in monitoring and debugging.
- Instantiate `MySqlConnection`, `MySqlResponse`, `MySqlExecution`, and `MySqlHandler` to integrate with FastAPI APIs.
 

## Requirements

Make sure to install the required packages listed in `requirements.txt`:

- Excel Class Dependancies
    - xlsxwriter
    - python-dotenv

- Environment Variables Dependancies
    - python-dotenv

- MySQL Dependancies
    - pydantic-settings
    - mysql-connector-python

- API Dependancies
    - fastapi

## Installation

1. Clone the repository:
   ```bash
   git clone https://github.com/hirushiharan/python-utility-functions.git
   ```
2. Navigate to the project directory:
    ```
    cd python-utils
    ```
3. Install the dependencies:
    ```bash
    pip install -r requirements.txt
    ```    

## Python Library

This project is available as a Python library on PyPI. You can find it [utility-lib-python](https://pypi.org/project/py-utility-scripts/).

## Contributing

This code is packaged for personal use and to assist other developers. Contributions are welcome! Please submit a pull request or open an issue to discuss any changes.

## Authors

- For any questions or inquiries, please contact Hirushiharan Thevendran 
    --[LinkedIn](https://www.linkedin.com/in/hirushiharan-thevendran-a08a82152?lipi=urn%3Ali%3Apage%3Ad_flagship3_profile_view_base_contact_details%3B54o2t%2B3cRw6IQKiNxmk27A%3D%3D)
    --[Email](hirushiharant@gmail.com)

## License

This project is licensed under the Apache License. - see the [LICENSE](LICENSE) file for details.