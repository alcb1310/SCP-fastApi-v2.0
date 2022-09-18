from datetime import datetime, timedelta
from jose import JWTError, jwt

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
    expire = datetime.now() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)

    to_encode.update({"exp": expire})

    return jwt.encode(to_encode, SECRET_KEY, ALGORITHM)
