from pydantic import BaseModel


class SignUpQuery(BaseModel):
    email: str
    password: str
    firstName: str
    lastName: str


class LoginQuery(BaseModel):
    username: str
    password: str
