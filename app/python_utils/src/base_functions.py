"""
Module: base_functions.py
Description: Provides utility classes and functions.

This module includes:

1. **Settings**: A configuration class that uses Pydantic's BaseSettings to load environment variables for MySQL database configuration.

Imports:
- `pydantic_settings.BaseSettings`: For loading configuration from environment variables.

Note:
- Ensure that environment variables for database configuration are set in the `.env` file as specified in the Settings class.
- Logging is managed through the Logger class defined in `log_message.py`.
"""

from pydantic_settings import BaseSettings
from pydantic import ConfigDict
import secrets


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
        ALGORITHM(str): Secret key algorithm for JWT authentication

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

def gen_secrets(hex_count):
    secret = secrets.token_hex(hex_count)
    return(secret)