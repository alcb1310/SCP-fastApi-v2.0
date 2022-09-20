from fastapi import APIRouter, Depends, status, HTTPException
from fastapi.security.oauth2 import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session

from ... import models, utils, oauth2
from ...database import get_db

router = APIRouter(
    tags=["Authentication"]
)


@router.post("/login")
def login(user_credentials: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    user = db.query(models.User).filter(models.User.email == user_credentials.username).one_or_none()

    if not user or not utils.verify_password(user_credentials.password, user.password):
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid Credentials")

    #create token
    user_uuid = str(user.uuid)
    company_uuid = str(user.company_id)
    token = oauth2.create_access_token({
        "user_uuid": user_uuid,
        "company_uuid": company_uuid
    })

    return {"access_token": token, "token_type": "bearer"}
