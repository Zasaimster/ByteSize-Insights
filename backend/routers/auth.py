from datetime import datetime, timedelta
from fastapi import APIRouter, Depends, HTTPException
from fastapi.security import OAuth2PasswordRequestForm, OAuth2PasswordRequestForm
from typing import Annotated


from backend.dependencies import get_mongo_db, AuthHandler
from backend.crud import get_user, insert_user
from backend.models import SignUpQuery

router = APIRouter(prefix="/auth", tags=["auth"])

auth_handler = AuthHandler()


async def get_user_information(
    token: Annotated[str, Depends(auth_handler.get_oauth2_scheme())],
    db=Depends(get_mongo_db),
):
    """Returns user information if they have a valid JWT token."""
    credentials_exception = HTTPException(
        status_code=401,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    print(token)
    username = auth_handler.decode_jwt_token(token)
    print(username)
    if username is None:
        print("username none")
        raise credentials_exception
    user_data = get_user(db, username)
    if user_data is None:
        print("data none")
        raise credentials_exception
    return user_data


@router.post("/signUp")
async def sign_up(user_info: SignUpQuery, db=Depends(get_mongo_db)):
    """Creates a user account in the database"""
    user_data = get_user(db, user_info.email)
    if user_data:
        raise HTTPException(
            status_code=409, detail=f"Account already exists for {user_info.email}"
        )

    # Hash and insert user
    hashed_password = auth_handler.get_password_hash(user_info.password)
    success = insert_user(
        db, user_info.email, hashed_password, user_info.firstName, user_info.lastName
    )
    if not success:
        raise HTTPException(
            status_code=500, detail="Internal server error. Please try again."
        )

    # Make a user sign in again to get their JWT token
    return {"message": "User successfully registered"}


@router.post("/login")
async def login(
    form_data: Annotated[OAuth2PasswordRequestForm, Depends()], db=Depends(get_mongo_db)
):
    """Lets a user login. Once a user logs in, create and return a JWT token."""
    # Check if user exists
    user_data = get_user(db, form_data.username)
    if not user_data:
        raise HTTPException(
            status_code=404,
            detail=f"Account for {form_data.username} not found.",
            headers={"WWW-Authenticate": "Bearer"},
        )

    # Validate password
    valid_password = auth_handler.verify_password(
        form_data.password, user_data["password"]
    )
    if not valid_password:
        raise HTTPException(
            status_code=401,
            detail="Invalid credentials.",
            headers={"WWW-Authenticate": "Bearer"},
        )

    # Create access token
    access_token = auth_handler.create_access_token(data={"sub": user_data["username"]})

    # Follow this format for JWT token
    return {"access_token": access_token, "token_type": "bearer"}


# Returns a User's document
@router.get("/getUser")
async def get_my_info(user=Depends(get_user_information)):
    return user
