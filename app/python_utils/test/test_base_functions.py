import unittest
from unittest.mock import patch, MagicMock
from pydantic import ValidationError
from app.python_utils.src.base_functions import Settings, BaseFunctions, PasswordFunctions, EmailFunction
from email_validator import EmailNotValidError
import smtplib

class TestSettings(unittest.TestCase):

    @patch.dict('os.environ', {
        'MYSQL_PASSWORD': 'test_password',
        'MYSQL_DATABASE': 'test_db',
        'MYSQL_USER': 'test_user',
        'MYSQL_HOST': 'localhost',
        'MYSQL_PORT': '3306',
        'SECRET_KEY': 'test_secret_key',
        'ALGORITHM': 'HS256'
    })
    def test_load_settings_from_env(self):
        """Test loading settings from environment variables."""
        settings = Settings()
        self.assertEqual(settings.MYSQL_PASSWORD, 'test_password')
        self.assertEqual(settings.MYSQL_DATABASE, 'test_db')
        self.assertEqual(settings.MYSQL_USER, 'test_user')
        self.assertEqual(settings.MYSQL_HOST, 'localhost')
        self.assertEqual(settings.MYSQL_PORT, 3306)
        self.assertEqual(settings.SECRET_KEY, 'test_secret_key')
        self.assertEqual(settings.ALGORITHM, 'HS256')

    def test_invalid_settings(self):
        """Test invalid settings raise ValidationError."""
        with self.assertRaises(ValidationError):
            Settings(MYSQL_PORT='not_a_port')


class TestBaseFunctions(unittest.TestCase):

    def test_gen_secrets(self):
        """Test generating secure secrets."""
        secret = BaseFunctions.gen_secrets(16)
        self.assertEqual(len(secret), 32)  # 16 hex bytes = 32 characters
        self.assertIsInstance(secret, str)


class TestPasswordFunctions(unittest.TestCase):

    def setUp(self):
        """Set up for password function tests."""
        self.plain_password = "secure_password"
        self.hashed_password = PasswordFunctions(self.plain_password).hash_password()
        self.password_functions = PasswordFunctions(self.plain_password, self.hashed_password)

    def test_hash_password(self):
        """Test hashing a password."""
        hashed_password = self.password_functions.hash_password()
        self.assertNotEqual(self.plain_password, hashed_password)
        self.assertTrue(hashed_password.startswith('$2b$'))

    def test_hash_password_without_plain(self):
        """Test hashing a password without providing plaintext password."""
        password_functions = PasswordFunctions()
        with self.assertRaises(ValueError):
            password_functions.hash_password()

    def test_verify_password(self):
        """Test verifying a hashed password."""
        is_verified = self.password_functions.verify_password()
        self.assertTrue(is_verified)

    def test_verify_password_invalid(self):
        """Test verifying an incorrect password."""
        password_functions = PasswordFunctions("wrong_password", self.hashed_password)
        is_verified = password_functions.verify_password()
        self.assertFalse(is_verified)

    def test_verify_password_without_plain_or_hashed(self):
        """Test verifying a password without providing both plaintext and hashed passwords."""
        password_functions = PasswordFunctions()
        with self.assertRaises(ValueError):
            password_functions.verify_password()

    def test_generate_temp_password(self):
        """Test generating a temporary password."""
        temp_password = self.password_functions.generate_temp_password()
        self.assertEqual(len(temp_password), self.password_functions.temp_password_length)
        self.assertIsInstance(temp_password, str)


class TestEmailFunction(unittest.TestCase):

    def setUp(self):
        """Set up for email function tests."""
        self.email_function = EmailFunction(
            smtp_server='smtp.test.com',
            smtp_port=587,
            smtp_username='test_user',
            smtp_password='test_password',
            sender_email='sender@test.com',
            recipient_email='recipient@test.com',
            subject='Test Subject',
            body='This is a test email.',
            body_type='plain'
        )

    @patch('smtplib.SMTP')
    def test_connect_smtp_server(self, mock_smtp):
        """Test connecting to the SMTP server."""
        mock_server = MagicMock()
        mock_smtp.return_value = mock_server

        self.email_function.connect_smtp_server()
        mock_smtp.assert_called_with('smtp.test.com', 587)
        mock_server.starttls.assert_called_once()
        mock_server.login.assert_called_once_with('test_user', 'test_password')

    @patch('smtplib.SMTP')
    def test_send_email(self, mock_smtp):
        """Test sending an email."""
        mock_server = MagicMock()
        mock_smtp.return_value = mock_server

        self.email_function.connect_smtp_server = MagicMock(return_value=mock_server)
        self.email_function.send_email()

        self.email_function.connect_smtp_server.assert_called_once()
        mock_server.send_message.assert_called_once()
        mock_server.quit.assert_called_once()

    def test_send_email_invalid_address(self):
        """Test sending an email with an invalid recipient address."""
        self.email_function.recipient_email = 'invalid_email'
        with self.assertRaises(EmailNotValidError):
            self.email_function.send_email()

    @patch('smtplib.SMTP')
    def test_send_email_exception(self, mock_smtp):
        """Test sending an email and handling an SMTP exception."""
        mock_server = MagicMock()
        mock_smtp.return_value = mock_server
        mock_server.send_message.side_effect = smtplib.SMTPException("Failed to send email")

        self.email_function.connect_smtp_server = MagicMock(return_value=mock_server)
        with self.assertRaises(smtplib.SMTPException):
            self.email_function.send_email()

        mock_server.quit.assert_called_once()
    
    print('====================Base Function Test Successful.====================\n')


if __name__ == '__main__':
    unittest.main()
