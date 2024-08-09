"""
Module: auth_functions.py
Description: This module contains utility functions for generating and decoding 
JWT tokens for authentication purposes. It also includes proper error handling 
and logging for better traceability.
"""

from datetime import datetime, timedelta, timezone
from fastapi import status, HTTPException
from typing import Dict
import jwt
from .log_message import Logger

# Constants for log levels
INFO = "INFO"
WARNING = "WARNING"
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
        Generate a JWT token with or without an expiration time.

        Returns:
            str: The encoded JWT token.

        Raises:
            ValueError: If the email is not provided.
            Exception: If there is an error in token generation.
        """
        if not self.auth_email:
            logger.log("Email must be provided to generate a JWT token.", ERROR)
            raise ValueError("Email must be provided to generate a JWT token.")
        
        try:
            payload = {"email": self.auth_email}

            if self.expiration_duration:
                expiration = datetime.now(timezone.utc) + timedelta(hours=self.expiration_duration)
                payload["exp"] = expiration
                logger.log(f"JWT token generated successfully for email: {self.auth_email}. Token will expire in {self.expiration_duration} hours", INFO)
            else:
                logger.log(f"JWT token generated successfully for email: {self.auth_email} with no expiration", INFO)
            
            token = jwt.encode(payload, self.secret_key, algorithm=self.algorithm)
            return token

        except Exception as e:
            logger.log(f"Error generating JWT token: {e}", ERROR)
            raise Exception("An error occurred while generating the JWT token.")


    def decode_jwt_token(self, token: str) -> Dict[str, str]:
        """
        Decode a JWT token and return the payload.

        Args:
            token (str): The JWT token to be decoded.

        Returns:
            Dict[str, str]: The decoded token payload.

        Raises:
            ValueError: If the token is not provided.
            HTTPException: If the token is expired or invalid.
        """
        if not token:
            logger.log("Token must be provided to decode a JWT token.", ERROR)
            raise ValueError("Token must be provided to decode a JWT token.")
        
        try:
            payload = jwt.decode(token, self.secret_key, algorithms=[self.algorithm])
            logger.log(f"JWT token decoded successfully for email: {payload.get('email')}", INFO)
            return payload
        except jwt.ExpiredSignatureError:
            logger.log("Token has expired.", WARNING)
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED, detail="Token has expired"
            )
        except jwt.InvalidTokenError:
            logger.log("Invalid token.", WARNING)
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid token"
            )
        except Exception as e:
            logger.log(f"Error decoding JWT token: {e}", ERROR)
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="An error occurred while decoding the JWT token."
            )
