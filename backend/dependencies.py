from datetime import datetime, timedelta
import os
import pymongo
from jose import jwt
from passlib.context import CryptContext
from fastapi.security import OAuth2PasswordBearer
from dotenv import load_dotenv

load_dotenv()

URI = os.getenv("MONGO_URI")
GITHUB_TOKEN = os.getenv("GITHUB_TOKEN")
OPENAI_TOKEN = os.getenv("OPENAI_TOKEN")
GITHUB_API_URL = "https://api.github.com"


def get_mongo_db():
    client = pymongo.MongoClient(URI)
    db = client["ByteSize-Insights"]

    try:
        yield db
    finally:
        client.close()


class AuthHandler:
    SECRET_KEY = "a6e7e786f3c0532a648e169792583367e6235373f46def643c600f6b8aa449ef"
    ALGORITHM = "HS256"
    ACCESS_TOKEN_EXPIRE_MINS = 60 * 24

    def __init__(self):
        self.password_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
        self.oauth2_scheme = OAuth2PasswordBearer(tokenUrl="auth/login")

    def get_oauth2_scheme(self):
        return self.oauth2_scheme

    def create_access_token(self, data: dict):
        access_token_expires = timedelta(minutes=self.ACCESS_TOKEN_EXPIRE_MINS)
        to_encode = data.copy()

        expire = datetime.utcnow() + access_token_expires

        to_encode.update({"exp": expire})
        encoded_jwt = jwt.encode(to_encode, self.SECRET_KEY, algorithm=self.ALGORITHM)
        return encoded_jwt

    def verify_password(self, plain_password, hashed_password):
        print(plain_password, hashed_password)
        return self.password_context.verify(plain_password, hashed_password)

    def get_password_hash(self, password):
        return self.password_context.hash(password)

    def decode_jwt_token(self, token):
        try:
            payload = jwt.decode(token, self.SECRET_KEY, algorithms=[self.ALGORITHM])
            username = payload.get("sub")
            return username
        except:
            return None
