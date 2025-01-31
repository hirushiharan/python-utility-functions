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

import random
import string
import smtplib
import logging
from passlib.context import CryptContext
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email_validator import validate_email, EmailNotValidError

# Set up logging for this module
logger = logging.getLogger(__name__)

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
            logger.warning("Failed to hash password: Plaintext password is missing.")
            raise ValueError("Plaintext password must be provided for hashing.")
        
        try:
            hashed = self.pwd_context.hash(self.plain_password)
            logger.info("Password hashed successfully.")
            return hashed
        except Exception as e:
            logger.error(f"Exception occurred during password hashing: {str(e)}")
            raise SystemError("Exception occurred during password hashing.")

    def verify_password(self) -> bool:
        """
        Verifies a plaintext password against a hashed password.

        Returns:
            bool: True if the plaintext password matches the hashed password, False otherwise.

        Raises:
            ValueError: If either the plain_password or hashed_password attribute is not set.
        """
        if not self.plain_password or not self.hashed_password:
            logger.warning("Failed to verify password: Missing plaintext or hashed password.")
            raise ValueError("Both plaintext and hashed passwords must be provided for verification.")
        
        try:
            is_valid = self.pwd_context.verify(self.plain_password, self.hashed_password)
            logger.info(f"Password verification {'succeeded' if is_valid else 'failed'}.")
            return is_valid
        except Exception as e:
            logger.error(f"Exception occurred during password verification: {str(e)}")
            raise SystemError("Exception occurred during password verification.")

    def generate_temp_password(self) -> str:
        """
        Generates a random temporary password.

        Returns:
            str: A randomly generated temporary password.
        """
        characters = string.ascii_letters + string.digits + "!@#$%^&*()"
        try:
            temp_password = ''.join(random.choice(characters) for _ in range(self.temp_password_length))
            logger.info(f"Generated a temporary password of length {self.temp_password_length}.")
            return temp_password
        except Exception as e:
            logger.error(f"Exception occurred while generating temporary password: {str(e)}")
            raise SystemError("Exception occurred while generating temporary password.")


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

    def send_email(self) -> None:
        """
        Sends an email using the configured SMTP server.

        Raises:
            EmailNotValidError: If the sender or recipient email is not valid.
            Exception: If there is an issue with the SMTP connection or sending the email.
        """
        try:
            # Validate email addresses
            validate_email(self.sender_email)
            validate_email(self.recipient_email)
            logger.info("Email addresses validated successfully.")

            # Prepare the email message
            msg = MIMEMultipart()
            msg['From'] = self.sender_email
            msg['To'] = self.recipient_email
            msg['Subject'] = self.subject

            msg.attach(MIMEText(self.body, self.body_type))
            logger.info("Email message prepared successfully.")

            # Send the email via SMTP server
            with smtplib.SMTP(self.smtp_server, self.smtp_port) as server:
                server.starttls()
                server.login(self.smtp_username, self.smtp_password)
                server.send_message(msg)
                logger.info(f"Email sent successfully to {self.recipient_email}.")

        except EmailNotValidError as e:
            logger.error(f"Invalid email address: {str(e)}")
            raise SystemError("Invalid email address.")
        except Exception as e:
            logger.error(f"Failed to send email: {str(e)}")
            raise SystemError("Failed to send email.")
