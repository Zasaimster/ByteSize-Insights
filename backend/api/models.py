from pydantic import BaseModel


class SignUpQuery(BaseModel):
    """Describes POST body for when a user signs up"""

    email: str
    password: str
    firstName: str
    lastName: str
