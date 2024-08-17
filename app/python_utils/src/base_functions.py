"""
Module: base_functions.py
Description: Provides utility classes and functions for environment variable configuration, secret generation, password management, and email functionality.

This module includes:

1. **Settings**: A configuration class that uses Pydantic's BaseSettings to load environment variables.
2. **BaseFunctions**: A utility class for generating secure random secrets.
3. **PasswordFunctions**: A class for hashing and verifying passwords, and generating temporary passwords.
4. **EmailFunction**: A class for sending emails via an SMTP server with validation and logging.

Imports:
- `pydantic_settings.BaseSettings`: For loading configuration from environment variables.
- `pydantic.ConfigDict`: For defining the configuration settings and environment file location.
- `secrets`: For generating secure random strings.
- `passlib.context.CryptContext`: For hashing and verifying passwords using the bcrypt algorithm.
- `random`, `string`: For generating random temporary passwords.
- `smtplib`: For sending emails using the SMTP protocol.
- `email.mime.multipart.MIMEMultipart`, `email.mime.text.MIMEText`: For creating and structuring email messages.
- `email_validator.validate_email`: For validating email addresses.
- `email_validator.EmailNotValidError`: For handling email validation errors.

Note:
- Ensure that environment variables for database configuration are set in the `.env` file as specified in the `Settings` class.
- Logging should be managed through the Logger class defined in `log_message.py`.
"""

from pydantic_settings import BaseSettings
from pydantic import ConfigDict
import secrets
from passlib.context import CryptContext
import random
import string
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email_validator import validate_email, EmailNotValidError
from .log_message import Logger
from typing import ClassVar
import os

# Constants for log levels
INFO = "INFO"
ERROR = "ERROR"

# Initialize the logger
logger = Logger()

class Settings(BaseSettings):
    """
    Configuration class for loading settings from environment variables.

    Uses Pydantic's BaseSettings to automatically load environment variables.

    Attributes:
        MYSQL_PASSWORD (str): The root password for MySQL.
        MYSQL_DATABASE (str): The name of the MySQL database.
        MYSQL_USER (str): The MySQL user.
        MYSQL_HOST (str): The MySQL host.
        MYSQL_PORT (int): The port for MySQL connection.
    """

    MYSQL_PASSWORD: str
    MYSQL_DATABASE: str
    MYSQL_USER: str
    MYSQL_HOST: str
    MYSQL_PORT: int

    ENV_VAR_MAP: ClassVar[dict] = {
        'MYSQL_PASSWORD': 'MYSQL_PASSWORD',
        'MYSQL_DATABASE': 'MYSQL_DATABASE',
        'MYSQL_USER': 'MYSQL_USER',
        'MYSQL_HOST': 'MYSQL_HOST',
        'MYSQL_PORT': 'MYSQL_PORT'
    }

    class Config:
        """
        Pydantic configuration class.
        """
        env_file = ".env"
        extra = "allow"  # Allow extra fields not defined in the model

    @classmethod
    def config(cls) -> ConfigDict:
        """
        Specifies the environment file to load settings from.

        Returns:
            ConfigDict: Configuration dictionary with the environment file.
        """
        logger.log("Loading environment variables from the .env file.", INFO)
        return ConfigDict(env_file=".env")

    @classmethod
    def _generate_env_vars(cls) -> dict:
        """
        Generates environment variable values based on the current mapping.

        Returns:
            dict: A dictionary with internal names as keys and environment variable values as values.
        """
        env_vars = {}
        for key, env_name in cls.ENV_VAR_MAP.items():
            env_vars[key] = os.getenv(env_name)
        return env_vars

    @classmethod
    def from_env(cls) -> 'Settings':
        """
        Creates an instance of Settings with values loaded from environment variables.

        Returns:
            Settings: An instance of the Settings class with environment variable values.
        """
        env_vars = cls._generate_env_vars()
        return cls(**env_vars)

    @classmethod
    def add_env_var(cls, internal_name: str, env_name: str):
        """
        Adds or updates the mapping of an internal variable name to an environment variable name.

        Args:
            internal_name (str): The internal name to be used in the class.
            env_name (str): The environment variable name.
        """
        cls.ENV_VAR_MAP[internal_name] = env_name
        logger.log(f"Added/Updated environment variable mapping: {internal_name} -> {env_name}", INFO)


class BaseFunctions:
    """
    Utility class for generating secure random secrets.
    """

    @staticmethod
    def gen_secrets(hex_count: int) -> str:
        """
        Generates a secure random hexadecimal string.

        Args:
            hex_count (int): The number of hexadecimal characters in the generated string.

        Returns:
            str: A secure random hexadecimal string.
        """
        secret = secrets.token_hex(hex_count)
        logger.log(f"Generated a secure secret key of {hex_count} hexadecimal characters.", INFO)
        return secret


class PasswordFunctions:
    """
    A class for handling password-related operations, including hashing, verification, and generating temporary passwords.

    Attributes:
        plain_password (str): The plaintext password.
        hashed_password (str): The hashed password.
        temp_password_length (int): The length of the temporary password.
    """

    def __init__(self, plain_password: str = None, hashed_password: str = None, temp_password_length: int = 12) -> None:
        """
        Initializes the PasswordFunctions class with optional parameters.

        Args:
            plain_password (str, optional): The plaintext password. Defaults to None.
            hashed_password (str, optional): The hashed password. Defaults to None.
            temp_password_length (int, optional): The length of the temporary password. Defaults to 12.
        """
        self.pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
        self.plain_password = plain_password
        self.hashed_password = hashed_password
        self.temp_password_length = temp_password_length

    def hash_password(self) -> str:
        """
        Hashes a plaintext password using the bcrypt algorithm.

        Returns:
            str: The hashed password.

        Raises:
            ValueError: If the plain_password attribute is not set.
        """
        if not self.plain_password:
            logger.log("Failed to hash password: Plaintext password is missing.", ERROR)
            raise ValueError("Plaintext password must be provided for hashing.")
        
        try:
            hashed = self.pwd_context.hash(self.plain_password)
            logger.log("Password hashed successfully.", INFO)
            return hashed
        except Exception as e:
            logger.log(f"Exception occurred during password hashing: {str(e)}", ERROR)
            raise

    def verify_password(self) -> bool:
        """
        Verifies a plaintext password against a hashed password.

        Returns:
            bool: True if the plaintext password matches the hashed password, False otherwise.

        Raises:
            ValueError: If either the plain_password or hashed_password attribute is not set.
        """
        if not self.plain_password or not self.hashed_password:
            logger.log("Failed to verify password: Missing plaintext or hashed password.", ERROR)
            raise ValueError("Both plaintext and hashed passwords must be provided for verification.")
        
        try:
            is_valid = self.pwd_context.verify(self.plain_password, self.hashed_password)
            logger.log(f"Password verification {'succeeded' if is_valid else 'failed'}.", INFO)
            return is_valid
        except Exception as e:
            logger.log(f"Exception occurred during password verification: {str(e)}", ERROR)
            raise

    def generate_temp_password(self) -> str:
        """
        Generates a random temporary password.

        Returns:
            str: A randomly generated temporary password.
        """
        characters = string.ascii_letters + string.digits + "!@#$%^&*()"
        try:
            temp_password = ''.join(random.choice(characters) for _ in range(self.temp_password_length))
            logger.log(f"Generated a temporary password of length {self.temp_password_length}.", INFO)
            return temp_password
        except Exception as e:
            logger.log(f"Exception occurred while generating temporary password: {str(e)}", ERROR)
            raise


class EmailFunction:
    """
    A class for sending emails via an SMTP server.

    Attributes:
        smtp_server (str): SMTP server address.
        smtp_port (int): Port to connect to the SMTP server.
        smtp_username (str): SMTP server username.
        smtp_password (str): SMTP server password.
        sender_email (str): Email address of the sender.
        recipient_email (str): Email address of the recipient.
        subject (str): Subject of the email.
        body (str): Body content of the email.
        body_type (str): Type of the email body, either 'plain' or 'html'.
        server (smtplib.SMTP): An instance of the SMTP connection.
    """

    def __init__(self, smtp_server: str, smtp_port: int, smtp_username: str, smtp_password: str,
                 sender_email: str, recipient_email: str, subject: str, body: str, body_type: str = 'plain') -> None:
        """
        Initializes the EmailFunction class with SMTP configuration and email details.

        Args:
            smtp_server (str): SMTP server address.
            smtp_port (int): Port to connect to the SMTP server.
            smtp_username (str): SMTP server username.
            smtp_password (str): SMTP server password.
            sender_email (str): Email address of the sender.
            recipient_email (str): Email address of the recipient.
            subject (str): Subject of the email.
            body (str): Body content of the email.
            body_type (str, optional): Type of the email body, either 'plain' or 'html'. Defaults to 'plain'.
        """
        self.smtp_server = smtp_server
        self.smtp_port = smtp_port
        self.smtp_username = smtp_username
        self.smtp_password = smtp_password
        self.sender_email = sender_email
        self.recipient_email = recipient_email
        self.subject = subject
        self.body = body
        self.body_type = body_type
        self.server = None

    def validate_email(self, email: str) -> bool:
        """
        Validates an email address.

        Args:
            email (str): Email address to be validated.

        Returns:
            bool: True if the email is valid, False otherwise.
        """
        try:
            validate_email(email)
            logger.log(f"Email address '{email}' is valid.", INFO)
            return True
        except EmailNotValidError as e:
            logger.log(f"Email validation failed for '{email}': {str(e)}", ERROR)
            return False

    def send_email(self) -> None:
        """
        Sends an email using the configured SMTP server.

        Raises:
            ValueError: If the email addresses are invalid.
        """
        if not self.validate_email(self.sender_email) or not self.validate_email(self.recipient_email):
            logger.log("Failed to send email due to invalid sender or recipient email address.", ERROR)
            raise ValueError("Invalid sender or recipient email address.")
        
        try:
            # Create email message
            message = MIMEMultipart()
            message['From'] = self.sender_email
            message['To'] = self.recipient_email
            message['Subject'] = self.subject

            # Attach the body with the MIME
            body_part = MIMEText(self.body, self.body_type)
            message.attach(body_part)

            # Connect to SMTP server and send email
            self.server = smtplib.SMTP(self.smtp_server, self.smtp_port)
            self.server.starttls()
            self.server.login(self.smtp_username, self.smtp_password)
            self.server.send_message(message)
            logger.log(f"Email sent successfully to {self.recipient_email}.", INFO)
        except Exception as e:
            logger.log(f"Exception occurred while sending email: {str(e)}", ERROR)
        finally:
            if self.server:
                self.server.quit()
                logger.log("SMTP server connection closed.", INFO)
