# Python Utils

Welcome to the Python Utils repository! This project contains a collection of utility scripts written in Python for various purposes. Each script focuses on specific functionalities that can be reused across different projects. Below is a detailed description of the project's structure and its components.

### Dependancies: 
    
- Excel Class Dependancies
    - xlsxwriter
    - python-dotenv
    - pandas

- Environment Variables Dependancies
    - python-dotenv

- MySQL Dependancies
    - pydantic-settings
    - mysql-connector-python

- API Dependancies
    - fastapi
    -uvicorn

- Authentication
    - PyJWT

- Email
    - email-validator

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
    
    file_path = "example.xlsx"
    
    # Define headers and data
    headers = ['name','age', 'score']
    scores = [
        ['ankit',12, 1000],
        ['rahul',13, 100],
        ['priya',12, 300],
        ['harshita',12, 50],
    ]

    # Create an instance of WriteToExcel
    excel = WriteToExcel(file_path)

    # Write data to the Excel file
    excel.write_data_to_excel(file_path, "sheet_1", 0, 0, headers, scores)
    

    # Read Score data from example.xlsx Excel file

    excel_columns = ExcelReader('example.xlsx', selected_columns=['name', 'score'])
    excel_columns.read_excel()
    values = excel_columns.iterate_rows()

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

    file_renamer = FileRenamer(path, prefix=prefix, count=count, name_format="{prefix}-{count:03d}")
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

### [`mysql_functions.py`](python_utils/src/mysql_functions.py)

This script provides functionalities for establishing a connection to a MySQL database, executing MySQL queries, and managing the database connection. It uses the mysql-connector-python library and supports environment variable management using the python-dotenv library.

#### Class:
- **LoggingMiddleware**: Middleware for logging HTTP request and response details. This class logs details about incoming HTTP requests and outgoing responses, which is helpful for monitoring and debugging purposes.
- **Settings**: A configuration class for loading environment variables for MySQL database configuration. Uses Pydantic's BaseSettings to load configuration details from environment variables, ensuring secure and configurable database connections.
- **MySqlConnection**: Provides a robust mechanism for managing database connections, including retry logic and connection pooling.
- **MySqlResponse**: Standardizes the response format for MySQL operations, ensuring consistent handling of success and error cases.
- **MySqlExecution**: Encapsulates the logic for executing MySQL queries and managing transactions, which simplifies database interactions.
- **MySqlHandler**: Handles asynchronous function execution with standard exception handling. Ensures consistent error handling and response formatting for asynchronous operations, enhancing the reliability of the application.

#### Usage:
- The module can be used in a FastAPI application to manage MySQL database connections and execute MySQL queries with robust error handling. The middleware and utility functions provided streamline logging and response formatting, making the application more maintainable and easier to debug.

#### Example

    from python_utils import LoggingMiddleware, MySqlConnection, MySqlExecution, MySqlHandler, Logger
    from fastapi import HTTPException, status, Query
    from fastapi import FastAPI, Depends
    from fastapi.responses import JSONResponse
    import uvicorn

    # Constants for log levels
    INFO = "INFO"
    WARNING = "WARNING"
    ERROR = "ERROR"

    logger = Logger()

    def fetch_user_by_email(email: str, db_conn) -> dict:
        try:
            query = "SELECT * FROM user WHERE email = %s"
            result = MySqlExecution.execute_single_query(db_conn, query, (email,))
            if not result:
                raise HTTPException(status_code=404, detail="User not found")
            logger.log(f"Fetched data for '{email}' from user table", INFO)
            return result
        except Exception as e:
            logger.log(f"Error fetching user by email '{email}': {str(e)}", ERROR)
            raise HTTPException(status_code=500, detail="Error fetching user")

    # Initialize FastAPI app
    app = FastAPI()
    app.add_middleware(LoggingMiddleware)

    # Fetch User
    async def get_user_handler(email: str, db_conn) -> JSONResponse:
        data = fetch_user_by_email(email, db_conn)
        return JSONResponse(content=data, status_code=status.HTTP_200_OK)

    @app.get("/user", response_description="Retrieve user data by email")
    async def get_user(email: str = Query(...), db_conn=Depends(MySqlConnection().get_db_connection)) -> JSONResponse:
        return await MySqlHandler.execute_with_handling(get_user_handler, email, db_conn)

    def main():
        try:
            # Run the Uvicorn server
            uvicorn.run('main:app', host='0.0.0.0', port=8000)
        except Exception as e:
            logger.log(f"Error running the application: {e}", level=ERROR)
            raise

    if __name__ == '__main__':
        main()

### [`project_structure_gen.py`](python_utils/src/project_structure_gen.py)

This script is designed to facilitate the creation of a comprehensive directory structure for your projects, with the added ability to generate a Markdown file documenting this structure. Utilizing the mysql-connector-python library, it also supports database interactions, and environment variables can be managed efficiently using the python-dotenv library.

#### Class:
- **ProjectStructure**: A class that handles the generation of the project's directory structure and the creation of a corresponding Markdown file.

    ***Attributes:***
        - `root_dir` (str): The root path for the directory.
        - `gitignore_file` (str): Path of the gitignore file.
        - `custom_patterns` (str): List of custom patterns to ignore.
        - `md_file` (str): Path of the generated Markdown file.

    ***Methods:***
    - `read_gitignore_patterns() -> None`: Reads the .gitignore file and returns a list of patterns.
    - `is_ignored() -> Bool`: Checks if a given path matches any of the .gitignore patterns.
    - `get_project_structure() -> List`: Generates the directory structure of the project, excluding ignored files and directories.
    - `format_structure(structure: list) -> str`: Formats the project structure into a hierarchical text format.
    - `add_path(formatted: List, path: str, depth: int) -> None`: Adds paths to the formatted list with correct indentation.
    - `create_md_file() -> None`: Ensures the Markdown file exists. If it does not exist, creates an empty file.
    - `generate() -> None`: Generates the project structure and writes it to the Markdown file.

#### Usage:
- The script can be seamlessly integrated into any project where there's a need to generate and document the project's directory structure in Markdown format.

#### Example

    from python_utils import ProjectStructure
    import os

    # Define the root directory of your project
    root_path = r'D:\repos\current\python-utility-functions'

    # Specify the .gitignore file to exclude certain files or directories
    gitignore_file = os.path.join(root_path, '.gitignore')

    # Define the output path for the generated Markdown file
    md_file = r'output\structure.md'

    # Initialize the ProjectStructure object
    project_structure = ProjectStructure(root_path, gitignore_file, md_file)

    # Generate the directory structure and save it as a Markdown file
    project_structure.generate()


### [`base_functions.py`](python_utils/src/base_functions.py)

This script is designed to provides utility classes and functions essential for environment variables configuration, secure secret key generation, password management, and email functionality. These utilities can be reused across various projects to streamline common tasks such as configuration management and secure operations.


#### Class:
- **Settings**: A configuration class that uses Pydantic's `BaseSettings` to load environment variables for MySQL database configuration. It automatically reads from a `.env` file, making it easier to manage environment-specific configurations.

    ***Attributes:***
    - `MYSQL_PASSWORD` (str): The root password for MySQL.
    - `MYSQL_DATABASE` (str): The name of the MySQL database.
    - `MYSQL_USER` (str): The MySQL user.
    - `MYSQL_HOST` (str): The MySQL host.
    - `MYSQL_PORT` (int): The port for MySQL connection.
    - `SECRET_KEY` (str): Secret key for JWT authentication.
    - `ALGORITHM` (str): Secret key algorithm for JWT authentication.

    ***Methods:***
    - `config(cls) -> ConfigDict`: Specifies the environment file (`.env`) to load settings from.


- **BaseFunctions**: A class includes basic utility functions, such as generating secure secrets.

    ***Methods:***
    - `gen_secrets(hex_count: int) -> str`: Generates a secure random hexadecimal string of the specified length.


- **PasswordFunctions**: Class handles password-related operations such as hashing, verification, and generating temporary passwords. It leverages the `passlib` library for secure password management.
    ***Attributes:***
    - `plain_password` (str): The plaintext password.
    - `hashed_password` (str): The hashed password.
    - `temp_password_length` (int): The length of the temporary password.

    ***Methods:***
    - `hash_password() -> str`: Hashes a plaintext password using the bcrypt algorithm.
    - `verify_password() -> bool`: Verifies a plaintext password against a hashed password.
    - `generate_temp_password() -> str`: Generates a secure random temporary password of a specified length.


- **EmailFunction**: Class simplifies the process of sending emails via an SMTP server. It handles the creation and structuring of email messages using the `email.mime` library.

    ***Methods:***
    - `send_email(subject: str, body: str, to_email: str, from_email: str, smtp_server: str, smtp_port: int, smtp_user: str, smtp_password: str) -> None`: Sends an email with the specified subject and body to a given recipient.


#### Usage:
- The script can be seamlessly integrated into any project where there's a need to configure environment varibales, authentication and send email.
- Ensure that environment variables for database configuration are set in the `.env` file as specified in the `Settings` class.
- Logging should be managed through the `Logger` class defined in `log_message.py`.

#### Example

    from python_utils import Settings, BaseFunctions, PasswordFunctions, EmailFunction

    # 1. Using the Settings class to load environment variables for MySQL configuration
    settings = Settings()
    print(f"MySQL User: {settings.MYSQL_USER}")
    print(f"MySQL Host: {settings.MYSQL_HOST}")

    # 2. Using BaseFunctions to generate a secure random secret
    secure_secret = BaseFunctions.gen_secrets(hex_count=32)
    print(f"Generated Secure Secret: {secure_secret}")

    # 3. Using PasswordFunctions for password management
    plain_password = "MySecurePassword"
    password_func = PasswordFunctions(plain_password=plain_password)

    # Hash the password
    hashed_password = password_func.hash_password()
    print(f"Hashed Password: {hashed_password}")

    # Verify the password
    is_password_correct = password_func.verify_password()
    print(f"Is the password correct? {'Yes' if is_password_correct else 'No'}")

    # Generate a temporary password
    temp_password = password_func.generate_temp_password()
    print(f"Generated Temporary Password: {temp_password}")

    # 4. Using EmailFunction to send an email
    email_func = EmailFunction()

    subject = "Test Email"
    body = "This is a test email sent from the base_functions module."
    to_email = "recipient@example.com"
    from_email = "sender@example.com"
    smtp_server = "smtp.example.com"
    smtp_port = 587
    smtp_user = "smtp_user"
    smtp_password = "smtp_password"

    # Send the email
    email_func.send_email(
        subject=subject,
        body=body,
        to_email=to_email,
        from_email=from_email,
        smtp_server=smtp_server,
        smtp_port=smtp_port,
        smtp_user=smtp_user,
        smtp_password=smtp_password
    )

    print("Email sent successfully!")

### [`auth_functions.py`](python_utils/src/auth_functions.py)

This script is designed to provides utility functions for generating and decoding JWT tokens, crucial for authentication purposes. It also includes error handling and logging for better traceability and debugging.

#### Class:
- **JwtAuthFunctions**: A utility class for handling JWT token operations including generation and decoding of tokens.


    ***Attributes:***
    - `secret_key (str)`: The secret key used for signing the JWT tokens.
    - `algorithm (str)`: The algorithm used for encoding the JWT tokens (default is `"HS256"`).
    - `auth_email (str)`: The email address used as a payload for generating the JWT token.
    - `expiration_duration (int)`: The token's expiration duration in hours (default is `1` hour).

    ***methods:***
    - `generate_jwt_token() -> str`: Generates a JWT token based on the provided email and optional expiration duration and returns the encoded JWT token.
    - `decode_jwt_token(token: str) -> Dict[str, str]`: Decodes a provided JWT token and returns its payload.

#### Usage:
- The script can be seamlessly integrated into any project where there's a need to provide authentication functions.

#### Example

    from python_utils import Settings, BaseFunctions, PasswordFunctions, EmailFunction

    # Initialize JwtAuthFunctions with email and secret key
    jwt_auth = JwtAuthFunctions(auth_email="user@example.com", secret_key="your_secret_key")

    # Generate JWT Token
    token = jwt_auth.generate_jwt_token()
    print(f"Generated Token: {token}")

    # Decode JWT Token
    decoded_payload = jwt_auth.decode_jwt_token(token)
    print(f"Decoded Payload: {decoded_payload}")