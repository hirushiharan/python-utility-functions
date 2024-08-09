import unittest
from app.python_utils.src.auth_functions import JwtAuthFunctions
from fastapi import HTTPException
import jwt

SECRET_KEY = "test_secret_key"
ALGORITHM = "HS256"
AUTH_EMAIL = "test@example.com"
INVALID_TOKEN = "invalid.token.value"

class TestJwtAuthFunctions(unittest.TestCase):

    def setUp(self):
        """Set up the JwtAuthFunctions instance for testing."""
        self.jwt_auth = JwtAuthFunctions(
            auth_email=AUTH_EMAIL, 
            expiration_duration=1, 
            secret_key=SECRET_KEY, 
            algorithm=ALGORITHM
        )

    def test_generate_jwt_token_with_expiration(self):
        """Test generating a JWT token with expiration time."""
        token = self.jwt_auth.generate_jwt_token()
        self.assertIsNotNone(token)
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        self.assertEqual(payload["email"], AUTH_EMAIL)
        self.assertIn("exp", payload)

    def test_generate_jwt_token_without_expiration(self):
        """Test generating a JWT token without expiration time."""
        self.jwt_auth.expiration_duration = None
        token = self.jwt_auth.generate_jwt_token()
        self.assertIsNotNone(token)
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        self.assertEqual(payload["email"], AUTH_EMAIL)
        self.assertNotIn("exp", payload)

    def test_generate_jwt_token_missing_email(self):
        """Test generating a JWT token without providing an email."""
        jwt_auth = JwtAuthFunctions(secret_key=SECRET_KEY, algorithm=ALGORITHM)
        with self.assertRaises(ValueError) as context:
            jwt_auth.generate_jwt_token()
        self.assertEqual(str(context.exception), "Email must be provided to generate a JWT token.")

    def test_generate_jwt_token_error_handling(self):
        """Test error handling during JWT token generation."""
        def mock_jwt_encode(*args, **kwargs):
            raise Exception("Mocked error")
        
        original_jwt_encode = jwt.encode
        jwt.encode = mock_jwt_encode
        
        with self.assertRaises(Exception) as context:
            self.jwt_auth.generate_jwt_token()
        self.assertEqual(str(context.exception), "An error occurred while generating the JWT token.")
        
        # Restore the original jwt.encode method
        jwt.encode = original_jwt_encode

    def test_decode_jwt_token_valid(self):
        """Test decoding a valid JWT token."""
        token = self.jwt_auth.generate_jwt_token()
        payload = self.jwt_auth.decode_jwt_token(token)
        self.assertEqual(payload["email"], AUTH_EMAIL)

    def test_decode_jwt_token_missing_token(self):
        """Test decoding a JWT token without providing a token."""
        with self.assertRaises(ValueError) as context:
            self.jwt_auth.decode_jwt_token("")
        self.assertEqual(str(context.exception), "Token must be provided to decode a JWT token.")

    def test_decode_jwt_token_expired(self):
        """Test decoding an expired JWT token."""
        self.jwt_auth.expiration_duration = -1  # Set expiration to past time
        token = self.jwt_auth.generate_jwt_token()
        
        with self.assertRaises(HTTPException) as context:
            self.jwt_auth.decode_jwt_token(token)
        self.assertEqual(context.exception.status_code, 401)
        self.assertEqual(context.exception.detail, "Token has expired")

    def test_decode_jwt_token_invalid(self):
        """Test decoding an invalid JWT token."""
        with self.assertRaises(HTTPException) as context:
            self.jwt_auth.decode_jwt_token(INVALID_TOKEN)
        self.assertEqual(context.exception.status_code, 401)
        self.assertEqual(context.exception.detail, "Invalid token")

    def test_decode_jwt_token_error_handling(self):
        """Test error handling during JWT token decoding."""
        def mock_jwt_decode(*args, **kwargs):
            raise Exception("Mocked error")
        
        original_jwt_decode = jwt.decode
        jwt.decode = mock_jwt_decode
        
        token = self.jwt_auth.generate_jwt_token()
        with self.assertRaises(HTTPException) as context:
            self.jwt_auth.decode_jwt_token(token)
        self.assertEqual(context.exception.status_code, 500)
        self.assertEqual(context.exception.detail, "An error occurred while decoding the JWT token.")
        
        # Restore the original jwt.decode method
        jwt.decode = original_jwt_decode

    print('====================Authentication Function Test Successful.====================\n')

if __name__ == '__main__':
    unittest.main()
