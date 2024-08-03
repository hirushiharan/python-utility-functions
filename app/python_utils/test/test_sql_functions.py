import unittest
from unittest.mock import patch, AsyncMock
from fastapi import HTTPException, status
from fastapi.responses import JSONResponse
from app.python_utils.src.sql_functions import SqlHandler

class TestSqlHandler(unittest.TestCase):

    @patch('app.python_utils.src.sql_functions.SqlResponse')  # Mock SqlResponse if necessary
    async def test_execute_with_handling_success(self, mock_json_response, mock_sql_response):
        """
        Test the execute_with_handling method for a successful execution.
        """
        # Create a mock function that returns a successful result
        mock_func = AsyncMock(return_value=JSONResponse(content={"success": True}, status_code=status.HTTP_200_OK))
        
        # Initialize SqlHandler
        sql_handler = SqlHandler()
        
        # Call the method
        result = await sql_handler.execute_with_handling(mock_func)
        
        # Assertions
        self.assertEqual(result.status_code, status.HTTP_200_OK)
        self.assertEqual(result.json(), {"success": True})

    @patch('app.python_utils.src.sql_functions.SqlResponse')
    async def test_execute_with_handling_http_exception(self, mock_json_response, mock_sql_response):
        """
        Test the execute_with_handling method for an HTTPException.
        """
        # Create a mock function that raises an HTTPException
        mock_func = AsyncMock(side_effect=HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Bad Request"))
        
        # Initialize SqlHandler
        sql_handler = SqlHandler()
        
        # Call the method
        result = await sql_handler.execute_with_handling(mock_func)
        
        # Assertions
        self.assertEqual(result.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(result.json(), {"message": "Bad Request"})

    @patch('app.python_utils.src.sql_functions.SqlResponse')
    async def test_execute_with_handling_generic_exception(self, mock_json_response, mock_sql_response):
        """
        Test the execute_with_handling method for a generic exception.
        """
        # Create a mock function that raises a generic exception
        mock_func = AsyncMock(side_effect=Exception("An unexpected error occurred"))
        
        # Initialize SqlHandler
        sql_handler = SqlHandler()
        
        # Call the method
        result = await sql_handler.execute_with_handling(mock_func)
        
        # Assertions
        self.assertEqual(result.status_code, status.HTTP_500_INTERNAL_SERVER_ERROR)
        self.assertEqual(result.json(), {"message": "An unexpected error occurred"})

if __name__ == '__main__':
    unittest.main()
