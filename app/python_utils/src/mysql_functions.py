"""
Module: mysql_functions.py
Description: Provides utility classes and functions for managing MySQL database operations and middleware in a FastAPI application.

This module includes:

1. **LoggingMiddleware**: Middleware for logging HTTP request and response details, including method, URL, headers, and status codes.

2. **Settings**: A configuration class that uses Pydantic's BaseSettings to load environment variables for MySQL database configuration.

3. **MySqlConnection**: Manages MySQL database connections using a connection pool with retry mechanisms for robustness. It includes methods to create a connection pool and retrieve a connection with retry logic.

4. **MySqlResponse**: Handles the structure and formatting of MySQL operation responses. It provides methods to format successful and error responses for MySQL operations.

5. **MySqlExecution**: Provides methods for executing MySQL queries and transactions. It includes methods to execute single queries and manage transactions, returning responses formatted with success status and error messages if applicable.

6. **MySqlHandler**: A class that executes asynchronous functions with standard exception handling. It formats responses for both successful operations and errors, using the MySqlResponse class to ensure consistent response formatting.

Imports:
- `json`, `time`, `datetime`: Standard libraries for JSON handling, time management, and date-time operations.
- `pydantic_settings.BaseSettings`: For loading configuration from environment variables.
- `mysql.connector`, `mysql.connector.pooling`: For MySQL database connection and pooling.
- `fastapi.Request`, `fastapi.status`, `fastapi.HTTPException`, `fastapi.responses.JSONResponse`: For handling HTTP requests, responses, and exceptions in FastAPI.
- `starlette.middleware.base.BaseHTTPMiddleware`: For creating custom middleware in FastAPI.
- `typing.Dict`, `typing.Any`, `typing.Optional`, `typing.Callable`: For type hints and annotations.

Note:
- Ensure that environment variables for database configuration are set in the `.env` file as specified in the Settings class.
- Logging is managed through the Logger class defined in `log_message.py`.
"""

import json
import time
from datetime import datetime
from pydantic import ValidationError
import mysql.connector
from mysql.connector import Error
from fastapi import Request, status, HTTPException
from fastapi.responses import JSONResponse
from typing import Dict, Any, Optional, Callable
from mysql.connector.pooling import MySQLConnectionPool
from starlette.middleware.base import BaseHTTPMiddleware
from .log_message import Logger
from .base_functions import Settings

# Constants for log levels
INFO = "INFO"
ERROR = "ERROR"

# Initialize the logger
logger = Logger()


class LoggingMiddleware(BaseHTTPMiddleware):
    """
    Middleware for logging HTTP request and response details.

    Logs information about incoming HTTP requests and outgoing responses,
    including timestamp, method, URL, headers, and response status code.

    Methods:
        dispatch(request, call_next): Logs request and response details.
    """

    async def dispatch(self, request: Request, call_next):
        """
        Logs request details before processing and response details after processing.

        Args:
            request (Request): The incoming HTTP request object.
            call_next (Callable): A callable to invoke the next middleware or route handler.

        Returns:
            Response: The HTTP response object.
        """
        # Log request details
        log_message = {
            "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            "method": request.method,
            "url": str(request.url),
            "headers": dict(request.headers)
        }
        logger.log(json.dumps(log_message), INFO)

        # Process the request and get the response
        response = await call_next(request)

        # Log response details
        log_message = {
            "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            "status_code": response.status_code
        }
        logger.log(json.dumps(log_message), INFO)

        return response


class MySqlConnection:
    """
    Manages MySQL database connections using a connection pool.

    Provides methods to create a connection pool and retrieve a connection from the pool
    with retry mechanisms for robustness.

    Attributes:
        retries (int): Number of retry attempts for pool creation and connection acquisition.
        pool_name (str): Name of the connection pool.
        pool_size (int): Size of the connection pool.
        timeout (int): Timeout for establishing a database connection.

    Methods:
        create_connection_pool(): Creates a MySQL connection pool with retries.
        get_db_connection(): Retrieves a MySQL database connection from the pool with retries.
    """

    def __init__(self, retries=3, pool_name='My_App_Pool', pool_size=10, timeout=300):
        """
        Initialize the MySqlConnection with specified parameters.

        Args:
            retries (int, optional): Number of retry attempts. Defaults to 3.
            pool_name (str, optional): Name of the connection pool. Defaults to 'My_App_Pool'.
            pool_size (int, optional): Number of connections in the pool. Defaults to 10.
            timeout (int, optional): Timeout for establishing a database connection. Defaults to 300.
        """
        self.retries = retries
        self.pool_name = pool_name
        self.pool_size = pool_size
        self.timeout = timeout
        self.connection_pool = self.create_connection_pool()  # Initialize the connection pool

    def create_connection_pool(self) -> MySQLConnectionPool:
        """
        Create a MySQL connection pool with retry logic.

        Attempts to create a MySQL connection pool with specified settings. Retries if an error occurs.

        Returns:
            MySQLConnectionPool: A pool of MySQL connections.

        Raises:
            HTTPException: If the connection pool cannot be created after retries.
        """
        # Initialize settings from environment variables
        try:
            settings = Settings()
        except ValidationError as e:
            # Log the detailed validation error for debugging
            logger.log(f"Error loading settings: {e}", ERROR)
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="Failed to load environment variables. Please check your .env file."
            )

        for attempt in range(self.retries):
            try:
                logger.log("Creating connection pool...", INFO)
                return MySQLConnectionPool(
                    pool_name=self.pool_name,
                    pool_size=self.pool_size,
                    pool_reset_session=True,
                    host=settings.MYSQL_HOST,
                    user=settings.MYSQL_USER,
                    password=settings.MYSQL_PASSWORD,
                    database=settings.MYSQL_DATABASE,
                    port=settings.MYSQL_PORT,
                    connection_timeout=self.timeout
                )
            except Error as err:
                logger.log(f"Attempt {attempt + 1}: Error creating connection pool: {err}", ERROR)
                if attempt + 1 == self.retries:
                    raise HTTPException(
                        status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                        detail="Database connection pool creation error"
                    )
                time.sleep(2)  # Wait before retrying

    def get_db_connection(self) -> mysql.connector.MySQLConnection:
        """
        Retrieve a MySQL database connection from the pool with retry logic.

        Attempts to acquire a connection from the pool. Retries if an error occurs or no connection is available.

        Returns:
            MySQLConnection: A MySQL database connection.

        Raises:
            HTTPException: If a connection cannot be acquired after retries.
        """
        for attempt in range(self.retries):
            try:
                connection = self.connection_pool.get_connection()
                if connection.is_connected():
                    logger.log("MySQL Connection Successful", INFO)
                    return connection
            except Error as err:
                logger.log(f"Attempt {attempt + 1}: Error getting connection: {err}", ERROR)
                if attempt + 1 == self.retries:
                    raise HTTPException(
                        status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                        detail="Database connection error"
                    )
                time.sleep(2)  # Wait before retrying


class MySqlResponse:
    """
    Handles the structure and formatting of MySQL operation responses.

    Attributes:
        success (bool): Indicates if the operation was successful.
        result (Any): The result data to be included in the response.
        status_code (int): The HTTP status code of the response.
        response (JSONResponse): The JSON response object.
        error (Optional[str]): An optional error message if the operation failed.

    Methods:
        format_response(): Formats the JSON response for successful operations.
        format_error_response(e): Formats the error response for HTTP exceptions.
    """

    def __init__(self, success: bool, result: Any, status_code: int, response: JSONResponse, 
                 error: Optional[str] = None):
        """
        Initialize the MySqlResponse with the provided parameters.

        Args:
            success (bool): Indicates if the operation was successful.
            result (Any): The result data to be included in the response.
            status_code (int): The HTTP status code of the response.
            response (JSONResponse): The JSON response object.
            error (Optional[str], optional): An optional error message if the operation failed. Defaults to None.
        """
        self.success = success
        self.result = result
        self.status_code = status_code
        self.response = response
        self.error = error

    def format_response(self) -> Dict[str, Any]:
        """
        Format the JSON response for successful operations.

        Returns:
            Dict[str, Any]: The formatted JSON response with success status, result, headers, and optional error message.
        """
        headers = {
            "Content-Length": str(len(str(self.result))),
            "Content-Type": self.response.headers.get("content-type", "application/json"),
            "Server": "MySQL Response Server"
        }
        response_body = {
            "success": self.success,
            "result": self.result,
            "error": self.error
        }
        return {
            "status_code": self.status_code,
            "headers": headers,
            "body": json.dumps(response_body)
        }

    def format_error_response(self, e: Exception) -> JSONResponse:
        """
        Format the error response for HTTP exceptions.

        Args:
            e (Exception): The exception to be included in the response.

        Returns:
            JSONResponse: The JSON response object containing error details.
        """
        return JSONResponse(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            content={"success": False, "error": str(e)}
        )


class MySqlExecution:
    """
    Provides methods for executing MySQL queries and transactions.

    Methods:
        execute_query(query: str, params: Optional[Dict[str, Any]] = None): Executes a single MySQL query and returns the result.
        execute_transaction(queries: Dict[str, Any]): Executes multiple MySQL queries within a transaction and returns the result.
    """

    @staticmethod
    def execute_query(query: str, params: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
        """
        Execute a single MySQL query and return the result.

        Args:
            query (str): The MySQL query to be executed.
            params (Optional[Dict[str, Any]], optional): Optional parameters for the query. Defaults to None.

        Returns:
            Dict[str, Any]: The result of the query execution with success status and result.
        """
        try:
            connection = MySqlConnection().get_db_connection()
            cursor = connection.cursor(dictionary=True)
            cursor.execute(query, params or ())
            result = cursor.fetchall()
            connection.commit()
            cursor.close()
            connection.close()
            return MySqlResponse(
                success=True,
                result=result,
                status_code=status.HTTP_200_OK,
                response=JSONResponse(content={}),
            ).format_response()
        except Error as e:
            logger.log(f"Error executing query: {e}", ERROR)
            return MySqlResponse(
                success=False,
                result={},
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                response=JSONResponse(content={}),
                error=str(e)
            ).format_error_response(e)

    @staticmethod
    def execute_transaction(queries: Dict[str, Any]) -> Dict[str, Any]:
        """
        Execute multiple MySQL queries within a transaction and return the result.

        Args:
            queries (Dict[str, Any]): A dictionary of MySQL queries to be executed with parameters.

        Returns:
            Dict[str, Any]: The result of the transaction with success status and result.
        """
        try:
            connection = MySqlConnection().get_db_connection()
            cursor = connection.cursor(dictionary=True)
            for query, params in queries.items():
                cursor.execute(query, params)
            connection.commit()
            cursor.close()
            connection.close()
            return MySqlResponse(
                success=True,
                result={},
                status_code=status.HTTP_200_OK,
                response=JSONResponse(content={}),
            ).format_response()
        except Error as e:
            logger.log(f"Error executing transaction: {e}", ERROR)
            return MySqlResponse(
                success=False,
                result={},
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                response=JSONResponse(content={}),
                error=str(e)
            ).format_error_response(e)


class MySqlHandler:
    """
    Executes asynchronous functions with standard exception handling and formats responses.

    Methods:
        execute_with_handling(func: Callable[..., Any], *args: Any, **kwargs: Any) -> JSONResponse: Executes a function with exception handling.
    """

    @staticmethod
    async def execute_with_handling(func: Callable[..., Any], *args: Any, **kwargs: Any) -> JSONResponse:
        """
        Executes a function with standard exception handling and formats responses.

        Args:
            func (Callable[..., Any]): The function to be executed.
            *args (Any): Positional arguments for the function.
            **kwargs (Any): Keyword arguments for the function.

        Returns:
            JSONResponse: The JSON response object with success status or error details.
        """
        try:
            result = await func(*args, **kwargs)
            return JSONResponse(
                status_code=status.HTTP_200_OK,
                content={"success": True, "result": result}
            )
        except HTTPException as e:
            logger.log(f"HTTPException: {e.detail}", ERROR)
            return JSONResponse(
                status_code=e.status_code,
                content={"success": False, "error": e.detail}
            )
        except Exception as e:
            logger.log(f"Unhandled exception: {str(e)}", ERROR)
            return JSONResponse(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                content={"success": False, "error": str(e)}
            )
