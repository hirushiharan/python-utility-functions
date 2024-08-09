from fastapi import FastAPI, Depends, Request, HTTPException, status
from fastapi.responses import JSONResponse
import uvicorn
from app.python_utils.src.mysql_functions import SqlConnection, SqlHandler, SqlResponse
from typing import Callable
from jwt_authentication_functions import AuthHandler, auth_router

# Initialize FastAPI app
app = FastAPI()


async def execute_with_handling(func: Callable, *args, **kwargs) -> JSONResponse:
    """
    Execute a function with standard exception handling.

    Args:
        func (Callable): The function to execute.
        *args: Positional arguments for the function.
        **kwargs: Keyword arguments for the function.

    Returns:
        JSONResponse: The response from the function or an error response.
    """
    try:
        return await func(*args, **kwargs)
    except HTTPException as e:
        error_response = JSONResponse(
            content={"message": str(e.detail)},
            status_code=e.status_code
        )
        formatted_response = SqlResponse.format_response(
            success=False,
            result=None,
            status_code=e.status_code,
            response=error_response,
            error=str(e.detail)
        )
        return JSONResponse(content=formatted_response, status_code=e.status_code)
    except Exception as e:
        error_response = JSONResponse(
            content={"message": str(e)},
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR
        )
        formatted_response = SqlResponse.format_response(
            success=False,
            result=None,
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            response=error_response,
            error=str(e)
        )
        return JSONResponse(content=formatted_response, status_code=status.HTTP_500_INTERNAL_SERVER_ERROR)


async def root_handler(request: Request) -> JSONResponse:
    """
    Root endpoint to check if the app is running.

    Args:
        request (Request): The HTTP request object.

    Returns:
        JSONResponse: A JSON response indicating the application is running along with the API description.
    """
    response_content = {
        "message": "App is running..."
    }
    return JSONResponse(content=response_content, status_code=status.HTTP_200_OK)

# Verify API


@app.get("/", response_description="Check if the application is running")
async def root(request: Request) -> JSONResponse:
    """
    Endpoint to verify if the application is up and running.
    """
    return await SqlHandler.execute_with_handling(root_handler, request)
    
@app.post("/auth_login", response_description="Authenticate user and get JWT token")
async def login_user(request: Request, db_conn=Depends(SqlConnection.get_db_connection)) -> JSONResponse:
    """
    Endpoint to authenticate a user and return a JWT token.

    Args:
        request (LoginRequest): The request body containing the login data.

    Returns:
        JSONResponse: The response containing the JWT token or an error message.
    """
    print(f'Request============================={request}')
    return await execute_with_handling(AuthHandler.login_user_handler(request, db_conn))
    

@app.get("/protected", response_description="Protected route")
async def protected_route(current_user: str = Depends(AuthHandler.get_current_user)) -> JSONResponse:
    """
    Protected endpoint that requires authentication.

    Args:
        current_user (str): The email of the current user.

    Returns:
        JSONResponse: A JSON response with a welcome message.
    """
    response_content = {"success": True, "body": {"message": f"Hello, {current_user}"}, "error": None}
    return JSONResponse(content=response_content, status_code=status.HTTP_200_OK)

def main():
    try:
        # Run the Uvicorn server
        uvicorn.run("main_test:app", host="0.0.0.0", port=8000)
    except Exception as e:
        print(f"Error running the application: {e}")

if __name__ == "__main__":
    main()
