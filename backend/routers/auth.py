from datetime import datetime, timedelta
from fastapi import APIRouter, Depends, HTTPException
from fastapi.security import OAuth2PasswordRequestForm, OAuth2PasswordRequestForm
from typing import Annotated


from dependencies import get_mongo_db, AuthHandler
from crud import get_user, insert_user
from models import SignUpQuery

router = APIRouter(prefix="/auth", tags=["auth"])

auth_handler = AuthHandler()


async def get_user_information(
    token: Annotated[str, Depends(auth_handler.get_oauth2_scheme())],
    db=Depends(get_mongo_db),
):
    credentials_exception = HTTPException(
        status_code=401,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )

    username = auth_handler.decode_jwt_token(token)
    if username is None:
        raise credentials_exception
    user_data = get_user(db, username)
    if user_data is None:
        raise credentials_exception
    return user_data


@router.post("/signUp")
async def sign_up(user_info: SignUpQuery, db=Depends(get_mongo_db)):
    user_data = get_user(db, user_info.email)
    if user_data:
        raise HTTPException(
            status_code=409, detail=f"Account already exists for {user_info.email}"
        )

    hashed_password = auth_handler.get_password_hash(user_info.password)
    success = insert_user(
        db, user_info.email, hashed_password, user_info.firstName, user_info.lastName
    )
    if not success:
        raise HTTPException(
            status_code=500, detail="Internal server error. Please try again."
        )

    return {"message": "User successfully registered"}


@router.post("/login")
async def login(
    form_data: Annotated[OAuth2PasswordRequestForm, Depends()], db=Depends(get_mongo_db)
):
    user_data = get_user(db, form_data.username)
    print(user_data)
    if not user_data:
        raise HTTPException(
            status_code=404,
            detail=f"Account for {form_data.username} not found.",
            headers={"WWW-Authenticate": "Bearer"},
        )
    valid_password = auth_handler.verify_password(
        form_data.password, user_data["password"]
    )
    if not valid_password:
        raise HTTPException(
            status_code=401,
            detail="Invalid credentials.",
            headers={"WWW-Authenticate": "Bearer"},
        )

    access_token = auth_handler.create_access_token(data={"sub": user_data["username"]})

    return {"access_token": access_token, "token_type": "bearer"}


@router.get("/getUser")
async def get_my_info(user=Depends(get_user_information)):
    return user
