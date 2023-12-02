from pydantic import BaseModel


class SignUpQuery(BaseModel):
    email: str
    password: str
    firstName: str
    lastName: str


class LoginQuery(BaseModel):
    email: str
    password: str
