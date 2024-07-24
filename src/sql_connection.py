import os
import mysql.connector
from mysql.connector import Error
from dotenv import load_dotenv

# Load environment variables from the .env file
load_dotenv()

# MySQL database credentials
MYSQL_ROOT_PASSWORD = os.getenv("MYSQL_ROOT_PASSWORD")
MYSQL_DATABASE = os.getenv("MYSQL_DATABASE")
MYSQL_USER = os.getenv("MYSQL_USER", "root")  # Default to root if not set
MYSQL_HOST = os.getenv("MYSQL_HOST", "localhost")  # Default to localhost if not set
MYSQL_PORT = int(os.getenv("MYSQL_PORT", 3306))  # Default to 3306 if not set

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
except Error as err:
    print(f"Error: {err}")
finally:
    if connection and connection.is_connected():
        cursor.close()
        connection.close()
        print("MySQL connection is closed")
