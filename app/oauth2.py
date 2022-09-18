import uuid
from datetime import datetime, timedelta

from jose import JWTError, jwt
from fastapi import Depends, status, HTTPException
from fastapi.security import OAuth2PasswordBearer

from . import schemas

oauth2_schema = OAuth2PasswordBearer(tokenUrl="login")
# to get a string like this run:
# openssl rand -hex 32
# SECRET_KEY
SECRET_KEY = "669b61ee56369af34403ccccf1db565862612a7759714ad00c3eb8bd89c1d771"
# Algorithm
ALGORITHM = "HS256"
# Expiration time
ACCESS_TOKEN_EXPIRE_MINUTES = 30


def create_access_token(data: dict):
    to_encode = data.copy()
    expire = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)

    to_encode.update({"exp": expire})

    return jwt.encode(to_encode, SECRET_KEY, ALGORITHM)


def verify_access_token(token: str, credentials_exception):
    try:
        payload = jwt.decode(token, SECRET_KEY, ALGORITHM)

        user_uuid: uuid.UUID = payload.get("user_uuid")

        if user_uuid is None:
            raise credentials_exception

        token_data = schemas.TokenData(user_uuid=user_uuid)
        return token_data
    except JWTError as error_data:
        raise credentials_exception


def get_current_user(token: str = Depends(oauth2_schema)):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )

    return verify_access_token(token, credentials_exception)
