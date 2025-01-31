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
from fastapi import status
from fastapi.responses import JSONResponse
from typing import Dict, Any, Optional

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
