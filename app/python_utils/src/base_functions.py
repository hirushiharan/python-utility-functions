"""
Module: base_functions.py
Description: Provides utility classes and functions for MySQL configuration, secret generation, and email functionality.

This module includes:

1. **Settings**: A configuration class that uses Pydantic's BaseSettings to load environment variables for MySQL database configuration.
2. **BaseFunctions**: A utility class for generating secrets.
3. **EmailFunction**: A class for sending emails via an SMTP server.

Imports:
- `pydantic_settings.BaseSettings`: For loading configuration from environment variables.
- `secrets`: For generating secure random strings.
- `smtplib`: For sending emails using the SMTP protocol.
- `email.mime.multipart.MIMEMultipart`: For creating email messages.
- `email.mime.text.MIMEText`: For attaching text content to emails.
- `email_validator.validate_email`: For validating email addresses.

Note:
- Ensure that environment variables for database configuration are set in the `.env` file as specified in the `Settings` class.
- Logging should be managed through the Logger class defined in `log_message.py`.
"""

from pydantic_settings import BaseSettings
from pydantic import ConfigDict
import secrets
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
        return ConfigDict(env_file=".env")

class BaseFunctions:
    """
    Utility class for basic functions.
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
    """

    def __init__(self, server, smtp_server, smtp_port, smtp_username, smtp_password, sender_email, recipient_email, subject, body, body_type='plain') -> None:
        self.smtp_server = smtp_server
        self.smtp_port = smtp_port
        self.smtp_username = smtp_username
        self.smtp_password = smtp_password
        self.sender_email = sender_email
        self.recipient_email = recipient_email
        self.subject = subject
        self.body = body
        self.body_type = body_type
        self.server = server

    def connect_smtp_server(self):
        """
        Connects to the SMTP server and logs in.

        Returns:
            smtplib.SMTP: An instance of the SMTP connection.

        Raises:
            Exception: If there is a failure in connecting or logging in to the SMTP server.
        """
        try:
            # Connect to the SMTP server
            server = smtplib.SMTP(self.smtp_server, self.smtp_port)
            server.starttls()  # Secure the connection
            server.login(self.smtp_username, self.smtp_password)
            self.server = server
        except smtplib.SMTPException as e:
            print(f"Failed to connect to the SMTP server: {str(e)}")
            raise

    def send_email(self):
        """
        Sends an email using the SMTP server connection.

        Raises:
            EmailNotValidError: If the recipient email address is not valid.
            Exception: If there is a failure in sending the email.
        """
        try:
            # Validate the recipient email address
            validate_email(self.recipient_email)

            # Create the email
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
            print(f"Email sent to {self.recipient_email}")

        except EmailNotValidError as e:
            print(f"Invalid email address: {str(e)}")
        except Exception as e:
            print(f"Failed to send email: {str(e)}")
        finally:
            if self.server:
                self.server.quit()

