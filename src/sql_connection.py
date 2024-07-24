"""
This script establishes a connection to a MySQL database using credentials 
stored in environment variables. It uses the mysql.connector library for 
database operations and the dotenv library to load environment variables 
from a .env file.

Classes:
- DatabaseConnector: Handles the loading of environment variables, establishing 
  a connection to the MySQL database, and managing the connection.

Methods:
- __init__(self): Initializes the DatabaseConnector with the path to the .env file.
- load_env_variables(): Loads environment variables from the .env file using the dotenv library.
- connect_to_mysql(): Establishes a connection to the MySQL database using credentials from environment variables.
- close_connection(): Closes the database connection if it is open.
- main(): Main function to execute the script logic.

Environment Variables:
- MYSQL_ROOT_PASSWORD: Password for the MySQL root user.
- MYSQL_DATABASE: Name of the MySQL database to connect to.
- MYSQL_USER: MySQL username (default is 'root' if not set).
- MYSQL_HOST: MySQL host (default is 'localhost' if not set).
- MYSQL_PORT: MySQL port (default is 3306 if not set).

Usage:
- Ensure the .env file is properly configured with the required environment variables.
- Create an instance of DatabaseConnector and call the connect_to_mysql method to connect to the MySQL database.
- Call the close_connection method to close the database connection when done.
"""

import os
import mysql.connector
from mysql.connector import Error
from dotenv import load_dotenv

class DatabaseConnector:
    """
    A class to handle MySQL database connections using credentials from environment variables.
    
    Attributes:
        log_file (str): Path to the log file.
        max_log_size (int): Maximum size of the log file before rotation (in bytes).
        log_levels (set): A set of log levels that are supported for logging.

    Methods:
        load_env_variables(): Loads environment variables from the .env file.
        connect_to_mysql(): Establishes a connection to the MySQL database.
        close_connection(): Closes the database connection if it is open.
    """

    def __init__(self):
        """
        Initializes the DatabaseConnector and loads environment variables.

        This function sets up the initial configuration and ensures that environment 
        variables are loaded before attempting to connect to the database.
        """
        self.connection = None
        self.load_env_variables()

    def load_env_variables(self):
        """
        Loads environment variables from the .env file using the dotenv library.

        This function should be called before accessing any environment variables
        to ensure they are properly loaded.

        Returns:
            None
        """
        load_dotenv()

    def connect_to_mysql(self):
        """
        Establishes a connection to the MySQL database using credentials from 
        environment variables.

        This function attempts to connect to the MySQL database and prints a 
        success message if connected. If the connection fails, it prints the error 
        message. Finally, it ensures the connection is properly closed.

        Returns:
            None
        """
        # MySQL database credentials
        MYSQL_ROOT_PASSWORD = os.getenv("MYSQL_ROOT_PASSWORD")
        MYSQL_DATABASE = os.getenv("MYSQL_DATABASE")
        MYSQL_USER = os.getenv("MYSQL_USER", "root")
        MYSQL_HOST = os.getenv("MYSQL_HOST", "localhost")
        MYSQL_PORT = int(os.getenv("MYSQL_PORT", 3306))

        try:
            self.connection = mysql.connector.connect(
                host=MYSQL_HOST,
                user=MYSQL_USER,
                password=MYSQL_ROOT_PASSWORD,
                database=MYSQL_DATABASE,
                port=MYSQL_PORT
            )
            if self.connection.is_connected():
                print("SQL Connection Successful")
                cursor = self.connection.cursor()
                # Your database operations here
                cursor.close()
        except Error as err:
            print(f"Error: {err}")

    def close_connection(self):
        """
        Closes the database connection if it is open.

        This function checks if the connection is open and closes it if necessary.
        
        Returns:
            None
        """
        if self.connection and self.connection.is_connected():
            self.connection.close()
            print("MySQL connection is closed")