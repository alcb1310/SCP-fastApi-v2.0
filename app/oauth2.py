from datetime import datetime, timedelta

from fastapi import Depends, status, HTTPException
from fastapi.security import OAuth2PasswordBearer
from jose import JWTError, jwt

from . import schemas
from .config import settings

oauth2_schema = OAuth2PasswordBearer(tokenUrl="login")
# to get a string like this run:
# openssl rand -hex 32
# SECRET_KEY
SECRET_KEY = settings.secret_key
# Algorithm
ALGORITHM = settings.algorithm
# Expiration time
ACCESS_TOKEN_EXPIRE_MINUTES = settings.access_token_expire_minutes


def create_access_token(data: dict):
    to_encode = data.copy()
    expire = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)

    to_encode.update({"exp": expire})

    return jwt.encode(to_encode, SECRET_KEY, ALGORITHM)


def verify_access_token(token: str, credentials_exception):
    try:
        payload = jwt.decode(token, SECRET_KEY, ALGORITHM)

        user_uuid: str = payload.get("user_uuid")
        company_uuid: str = payload.get("company_uuid")

        if user_uuid is None or company_uuid is None:
            raise credentials_exception

        token_data = schemas.TokenData(user_uuid=user_uuid, company_uuid=company_uuid)
        return token_data
    except JWTError:
        raise credentials_exception


def get_current_user(token: str = Depends(oauth2_schema)):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )

    return verify_access_token(token, credentials_exception)
