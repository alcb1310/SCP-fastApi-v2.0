import uuid
from typing import List

from fastapi import status, HTTPException, Depends, APIRouter
from psycopg2.extras import register_uuid
from sqlalchemy.orm import Session

from ... import schemas, models, utils, oauth2
from ...database import get_db

router = APIRouter(
    prefix="/api/v1.0/users",
    tags=["Users"]
)


@router.get("/", status_code=status.HTTP_200_OK, response_model=List[schemas.UserResponse])
async def get_all_users(db: Session = Depends(get_db), current_user=Depends(oauth2.get_current_user)):
    """
    Retrieves all the users
    """
    users = db.query(models.User).filter(models.User.company_id == current_user.company_uuid).all()

    return users


@router.get("/{uuid_str}", status_code=status.HTTP_200_OK, response_model=schemas.UserResponse)
async def get_one_user(uuid_str: str, db: Session = Depends(get_db), current_user=Depends(oauth2.get_current_user)):
    """
    Get the information of one user
    """
    user = db.query(models.User).filter(models.User.company_id == current_user.company_uuid).filter(models.User.uuid == uuid_str).one_or_none()

    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"User with uuid {uuid_str} not found")

    return user


@router.post("/", status_code=status.HTTP_201_CREATED, response_model=schemas.UserResponse)
async def create_user(user: schemas.UserPost, db: Session = Depends(get_db), current_user=Depends(oauth2.get_current_user)):
    """
    Creates a new user
    """
    company = db.query(models.Company).filter(models.Company.uuid == current_user.company_uuid).one_or_none()
    all_users = db.query(models.User).filter(models.User.company_id == current_user.company_uuid)
    # print(all_users.count())
    if all_users.count() == company.employees:
        raise HTTPException(status_code=status.HTTP_402_PAYMENT_REQUIRED, detail=f"Have reached the maximum amount({company.employees}) of user accounts")
    # hash the password
    
    hashed_password = utils.hash_password(user.password)
    user.password = hashed_password
    register_uuid()
    uuid_entry = str(uuid.uuid4())
    user_dict = user.dict()
    user_dict["uuid"] = uuid_entry
    user_dict["company_id"] = current_user.company_uuid
    created_user = models.User(**user_dict)
    try:
        db.add(created_user)
        db.commit()
        db.refresh(created_user)
    except Exception as error:
        print(error)
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail="User already exists")

    return created_user
