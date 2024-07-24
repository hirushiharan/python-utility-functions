"""
This script establishes a connection to a MySQL database using credentials 
stored in environment variables. It uses the mysql.connector library for 
database operations and the dotenv library to load environment variables 
from a .env file.

Functions:
- load_env_variables(): Loads environment variables from the .env file.
- connect_to_mysql(): Establishes a connection to the MySQL database.
- main(): Main function to execute the script logic.

Environment Variables:
- MYSQL_ROOT_PASSWORD: Password for the MySQL root user.
- MYSQL_DATABASE: Name of the MySQL database to connect to.
- MYSQL_USER: MySQL username (default is 'root' if not set).
- MYSQL_HOST: MySQL host (default is 'localhost' if not set).
- MYSQL_PORT: MySQL port (default is 3306 if not set).

Usage:
- Ensure the .env file is properly configured with the required environment variables.
- Run the script to connect to the MySQL database and perform operations.
"""

import os
import mysql.connector
from mysql.connector import Error
from dotenv import load_dotenv

def load_env_variables():
    """
    Loads environment variables from the .env file using the dotenv library.
    
    This function should be called before accessing any environment variables
    to ensure they are properly loaded.

    Returns:
        None
    """
    load_dotenv()

def connect_to_mysql():
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

    connection = None
    try:
        connection = mysql.connector.connect(
            host=MYSQL_HOST,
            user=MYSQL_USER,
            password=MYSQL_ROOT_PASSWORD,
            database=MYSQL_DATABASE,
            port=MYSQL_PORT
        )
        if connection.is_connected():
            print("SQL Connection Successful")
            cursor = connection.cursor()
            # Your database operations here
            cursor.close()
    except Error as err:
        print(f"Error: {err}")
    finally:
        if connection and connection.is_connected():
            connection.close()
            print("MySQL connection is closed")

def main():
    """
    Main function to execute the script logic.

    This function loads the environment variables and establishes a connection
    to the MySQL database.

    Returns:
        None
    """
    load_env_variables()
    connect_to_mysql()

if __name__ == "__main__":
    main()
