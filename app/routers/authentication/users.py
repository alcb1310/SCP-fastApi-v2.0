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
    print(current_user)
    users = db.query(models.User).all()

    return users


@router.get("/{uuid_str}", status_code=status.HTTP_200_OK, response_model=schemas.UserResponse)
async def get_one_user(uuid_str: uuid.UUID, db: Session = Depends(get_db)):
    """
    Get the information of one user
    """
    user = db.query(models.User).filter(models.User.uuid == uuid_str).one_or_none()

    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"User with uuid {uuid_str} not found")

    return user


@router.post("/", status_code=status.HTTP_201_CREATED, response_model=schemas.UserResponse)
async def create_user(user: schemas.UserCreate, db: Session = Depends(get_db)):
    """
    Creates a new user
    """

    # hash the password
    hashed_password = utils.hash_password(user.password)
    user.password = hashed_password
    register_uuid()
    uuid_entry = uuid.uuid4()
    user_dict = user.dict()
    user_dict["uuid"] = uuid_entry
    created_user = models.User(**user_dict)
    try:
        db.add(created_user)
        db.commit()
        db.refresh(created_user)
    except Exception as error:
        print(error)
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail="User already exists")

    return created_user
