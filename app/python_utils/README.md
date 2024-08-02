# Python Utils

Welcome to the Python Utils repository! This project contains a collection of utility scripts written in Python for various purposes. Each script focuses on specific functionalities that can be reused across different projects. Below is a detailed description of the project's structure and its components.

Refer [`CHANGLOG.md`](../../CHANGELOG.md) for the release updates.

## Project Structure

The project structure is as follows:

    python-utility-functions/
    │
    ├── .gitignore
    ├── .env
    ├── src/
    │   ├── __init__.py
    │   ├── excel_functions.py
    │   ├── file_functions.py
    │   ├── log_message.py
    │   └── project_structure_generator.py
    ├── tests/
    │   ├── test_excel_functions.py
    │   ├── test_file_functions.py
    │   ├── test_log_message.py
    │   └── test_project_structure_generator.py
    ├── requirements.txt
    ├── README.md
    └── LICENSE 

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

### [`src/project_structure_generator.py`](src/project_structure_generator.py)

This script provides a project structure generatoe mechanism to print the given path directory structure.

#### Class:
- **ProjectStructure**: Handles generating project structure for a given directory.

#### Usage:
- Create an instance of `ProjectStructure` and use `generate()` to generate the project structure of a given directory.

## Requirements

Make sure to install the required packages listed in `requirements.txt`:

- pandas
- xlsxwriter
- python-dotenv

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

Contributions are welcome! Please open an issue or submit a pull request if you have suggestions or improvements.

## Authors

- For any questions or inquiries, please contact Hirushiharan Thevendran 
    --[LinkedIn](https://www.linkedin.com/in/hirushiharan-thevendran-a08a82152?lipi=urn%3Ali%3Apage%3Ad_flagship3_profile_view_base_contact_details%3B54o2t%2B3cRw6IQKiNxmk27A%3D%3D)
    --[Email](hirushiharant@gmail.com)

## License

This project is licensed under the Apache License. - see the [LICENSE](LICENSE) file for details.

Feel free to adjust any sections as needed!