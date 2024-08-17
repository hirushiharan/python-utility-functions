"""
File: auth_functions.py

Description:
    This module provides utility functions for handling JWT (JSON Web Token) 
    operations, including the generation and decoding of JWT tokens. These tokens 
    are typically used for authentication and authorization purposes in web 
    applications. The module includes error handling and logging capabilities 
    to ensure smooth operation and traceability of the token management process.

This module includes:

**JwtAuthFunctions**: A utility class for generating and decoding JWT tokens, with options 
        for setting expiration durations and using specific cryptographic 
        algorithms. Includes methods for secure token management.

    Methods:
        __init__:
            Initializes the JwtAuthFunctions class with the provided configurations 
            for secret key, algorithm, auth_email, and token expiration duration.

        generate_jwt_token:
            Generates a JWT token based on the provided email and optional 
            expiration duration. Logs the token creation process and handles errors.

        decode_jwt_token:
            Decodes a provided JWT token and returns its payload. Handles expired 
            and invalid tokens with appropriate error responses.

Imports:
    - datetime, timedelta, timezone: For handling token expiration times.
    - fastapi.status, HTTPException: For raising appropriate HTTP errors.
    - typing.Dict: For type hinting the decoded JWT payload.
    - jwt: For encoding and decoding JWT tokens.
    - log_message.Logger: For logging messages.

Note:
    - Ensure that the `secret_key` is securely stored and not hard-coded in the 
      application. It should be loaded from a secure environment variable or 
      configuration file.
    - The `algorithm` should be a robust cryptographic algorithm suitable for 
      your application's security requirements.
    - This module is designed to be used in web applications where JWT tokens 
      are a part of the authentication and authorization mechanism.
"""

from datetime import datetime, timedelta, timezone
from fastapi import status, HTTPException
from typing import Dict
import jwt
from .log_message import Logger

# Constants for log levels
INFO = "INFO"
ERROR = "ERROR"

# Initialize the logger
logger = Logger()

class JwtAuthFunctions:
    """
    A utility class for handling JWT token operations including generation and 
    decoding of tokens.

    Attributes:
        secret_key (str): The secret key used for signing the JWT tokens.
        algorithm (str): The algorithm used for encoding the JWT tokens.
        auth_email (str): The email address used as a payload for generating the JWT token.
        expiration_duration (int): The token's expiration duration in hours.
    """

    def __init__(self, 
                 auth_email: str = None, 
                 expiration_duration: int = 1, 
                 secret_key: str = None, 
                 algorithm: str = "HS256"
                 ) -> None:
        """
        Initializes the JwtAuthFunctions class with the provided configurations.

        Args:
            auth_email (str): The email address to be included in the JWT payload.
            expiration_duration (int): The duration in hours before the token expires.
            secret_key (str): The secret key used for signing the JWT tokens.
            algorithm (str): The algorithm used for encoding the JWT tokens.
        """
        self.secret_key = secret_key
        self.algorithm = algorithm
        self.auth_email = auth_email
        self.expiration_duration = expiration_duration

    def generate_jwt_token(self) -> str:
        """
        Generates a JWT token with or without an expiration time.

        Returns:
            str: The encoded JWT token.

        Raises:
            ValueError: If the email is not provided.
            Exception: If there is an error in token generation.
        """
        if not self.auth_email:
            logger.log("Email is not provided.", ERROR)
            raise ValueError("Email must be provided to generate a JWT token.")
        
        try:
            payload = {"email": self.auth_email}

            if self.expiration_duration:
                expiration = datetime.now(timezone.utc) + timedelta(hours=self.expiration_duration)
                payload["exp"] = expiration
                logger.log(f"JWT token generated successfully. Token will expire in {self.expiration_duration} hours.", INFO)
            
            token = jwt.encode(payload, self.secret_key, algorithm=self.algorithm)
            return token

        except Exception as e:
            logger.log(f"Error generating JWT token: {e}", ERROR)
            raise Exception("An error occurred while generating the JWT token.")

    def decode_jwt_token(self, token: str) -> Dict[str, str]:
        """
        Decodes a JWT token and returns the payload.

        Args:
            token (str): The JWT token to be decoded.

        Returns:
            Dict[str, str]: The decoded token payload.

        Raises:
            ValueError: If the token is not provided.
            HTTPException: If the token is expired or invalid.
        """
        if not token:
            logger.log("Token is not provided.", ERROR)
            raise ValueError("Token must be provided to decode a JWT token.")
        
        try:
            payload = jwt.decode(token, self.secret_key, algorithms=[self.algorithm])
            logger.log("JWT token decoded successfully.", INFO)
            return payload

        except jwt.ExpiredSignatureError:
            logger.log("Token has expired.", ERROR)
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED, detail="Token has expired"
            )

        except jwt.InvalidTokenError:
            logger.log("Invalid token.", ERROR)
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid token"
            )

        except Exception as e:
            logger.log(f"Error decoding JWT token: {e}", ERROR)
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="An error occurred while decoding the JWT token."
            )
