"""
Module: base_functions.py
Description: Provides utility classes and functions for MySQL configuration, secret generation, password management, and email functionality.

This module includes:

1. **Settings**: A configuration class that uses Pydantic's BaseSettings to load environment variables for MySQL database configuration.
2. **BaseFunctions**: A utility class for generating secure random secrets.
3. **PasswordFunctions**: A class for hashing and verifying passwords and generating temporary passwords.
4. **EmailFunction**: A class for sending emails via an SMTP server.

Imports:
- `pydantic_settings.BaseSettings`: For loading configuration from environment variables.
- `secrets`: For generating secure random strings.
- `passlib.context.CryptContext`: For hashing and verifying passwords using the bcrypt algorithm.
- `random`, `string`: For generating random temporary passwords.
- `smtplib`: For sending emails using the SMTP protocol.
- `email.mime.multipart.MIMEMultipart`, `email.mime.text.MIMEText`: For creating and structuring email messages.
- `email_validator.validate_email`: For validating email addresses.

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


class Settings(BaseSettings):
    """
    Configuration class for loading settings from environment variables.

    Uses Pydantic's BaseSettings to automatically load environment variables for database configuration.

    Attributes:
        MYSQL_PASSWORD (str): The root password for MySQL.
        MYSQL_DATABASE (str): The name of the MySQL database.
        MYSQL_USER (str): The MySQL user.
        MYSQL_HOST (str): The MySQL host.
        MYSQL_PORT (int): The port for MySQL connection.
        SECRET_KEY (str): Secret key for JWT authentication.
        ALGORITHM (str): Secret key algorithm for JWT authentication.

    Config:
        env_file (str): Specifies the environment file to load settings from.
    """

    MYSQL_PASSWORD: str
    MYSQL_DATABASE: str
    MYSQL_USER: str
    MYSQL_HOST: str
    MYSQL_PORT: int
    SECRET_KEY: str
    ALGORITHM: str

    @classmethod
    def config(cls) -> ConfigDict:
        """
        Specifies the environment file to load settings from.

        Returns:
            ConfigDict: Configuration dictionary with the environment file.
        """
        return ConfigDict(env_file=".env")


class BaseFunctions:
    """
    Utility class for basic functions, such as generating secure secrets.
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
        return secrets.token_hex(hex_count)


class PasswordFunctions:
    """
    A class for handling password-related operations, including hashing, verification, and generating temporary passwords.

    Attributes:
        plain_password (str): The plaintext password.
        hashed_password (str): The hashed password.
        temp_password_length (int): The length of the temporary password.
    """

    def __init__(self, plain_password: str = None, hashed_password: str = None, temp_password_length: int = 12) -> None:
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
            raise ValueError("Plaintext password must be provided for hashing.")
        
        try:
            return self.pwd_context.hash(self.plain_password)
        except Exception as e:
            print(f"Error while hashing the password: {str(e)}")
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
            raise ValueError("Both plaintext and hashed passwords must be provided for verification.")
        
        try:
            return self.pwd_context.verify(self.plain_password, self.hashed_password)
        except Exception as e:
            print(f"Error while verifying the password: {str(e)}")
            raise

    def generate_temp_password(self) -> str:
        """
        Generates a random temporary password.

        Returns:
            str: A randomly generated temporary password.
        """
        characters = string.ascii_letters + string.digits + "!@#$%^&*()"
        try:
            temp_password = ''.join(random.choice(characters) for i in range(self.temp_password_length))
            return temp_password
        except Exception as e:
            print(f"Error while generating a temporary password: {str(e)}")
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

    def connect_smtp_server(self) -> None:
        """
        Connects to the SMTP server and logs in.

        Raises:
            smtplib.SMTPException: If there is a failure in connecting or logging in to the SMTP server.
        """
        try:
            # Connect to the SMTP server
            server = smtplib.SMTP(self.smtp_server, self.smtp_port)
            server.starttls()  # Secure the connection
            server.login(self.smtp_username, self.smtp_password)
            self.server = server
            print("Successfully connected to the SMTP server.")
        except smtplib.SMTPException as e:
            print(f"Failed to connect to the SMTP server: {str(e)}")
            raise

    def send_email(self) -> None:
        """
        Sends an email using the SMTP server connection.

        Raises:
            EmailNotValidError: If the recipient email address is not valid.
            smtplib.SMTPException: If there is a failure in sending the email.
        """
        try:
            # Validate the recipient email address
            validate_email(self.recipient_email)

            # Create the email message
            msg = MIMEMultipart()
            msg['From'] = self.sender_email
            msg['To'] = self.recipient_email
            msg['Subject'] = self.subject

            # Attach the email body
            msg.attach(MIMEText(self.body, self.body_type))

            if not self.server:
                self.connect_smtp_server()

            # Send the email
            self.server.send_message(msg)
            print(f"Email successfully sent to {self.recipient_email}.")

        except EmailNotValidError as e:
            print(f"Invalid email address: {str(e)}")
            raise
        except smtplib.SMTPException as e:
            print(f"Failed to send email: {str(e)}")
            raise
        except Exception as e:
            print(f"An unexpected error occurred while sending the email: {str(e)}")
            raise
        finally:
            if self.server:
                self.server.quit()
                print("SMTP server connection closed.")
