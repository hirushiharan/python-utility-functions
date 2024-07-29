import mysql.connector
from mysql.connector import Error

class DatabaseConnector:
    """
    A class to handle MySQL database connections using credentials from environment variables.
    
    Attributes:
        connection (mysql.connector.connection.MySQLConnection): The MySQL database connection object.
        host (str): The hostname of the MySQL server.
        port (int): The port number of the MySQL server.
        user (str): The username for connecting to the MySQL server.
        password (str): The password for the MySQL user.
        database (str): The name of the database to connect to.

    Methods:
        connect_to_mysql(): Establishes a connection to the MySQL database.
        close_connection(): Closes the database connection if it is open.
    """

    def __init__(self, host, port, user, password, database):
        """
        Initializes the DatabaseConnector with connection parameters.

        Parameters:
            host (str): The hostname of the MySQL server.
            port (int): The port number of the MySQL server.
            user (str): The username for connecting to the MySQL server.
            password (str): The password for the MySQL user.
            database (str): The name of the database to connect to.
        """
        self.connection = None
        self.host = host
        self.port = port
        self.user = user
        self.password = password
        self.database = database

    def connect_to_mysql(self):
        """
        Establishes a connection to the MySQL database using credentials from environment variables.

        This function attempts to connect to the MySQL database and prints a success message if connected. 
        If the connection fails, it prints the error message. Finally, it ensures the connection is properly closed.

        Returns:
            None
        """
        print(f'Host: {self.host}')
        try:
            self.connection = mysql.connector.connect(
                host=self.host,
                user=self.user,
                password=self.password,
                database=self.database,
                port=self.port
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
