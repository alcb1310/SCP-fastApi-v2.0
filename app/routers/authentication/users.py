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
    users = db.query(models.User).filter(
        models.User.company_id == current_user.company_uuid).order_by(models.User.name).all()

    return users


@router.post("/me", status_code=status.HTTP_200_OK, response_model=schemas.UserResponse)
async def me(db: Session = Depends(get_db), current_user=Depends(oauth2.get_current_user)):
    user = db.query(models.User).\
        filter(models.User.company_id == current_user.company_uuid).\
        filter(models.User.uuid == current_user.user_uuid).one_or_none()

    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail=f"You are not autorized, please log in"
        )

    return user


@router.get("/{uuid_str}", status_code=status.HTTP_200_OK, response_model=schemas.UserResponse)
async def get_one_user(uuid_str: str, db: Session = Depends(get_db), current_user=Depends(oauth2.get_current_user)):
    """
    Get the information of one user
    """
    user = db.query(models.User).filter(models.User.company_id == current_user.company_uuid).filter(
        models.User.uuid == uuid_str).one_or_none()

    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"User with uuid {uuid_str} not found")

    return user


@router.post("/", status_code=status.HTTP_201_CREATED, response_model=schemas.UserResponse)
async def create_user(user: schemas.UserPost, db: Session = Depends(get_db), current_user=Depends(oauth2.get_current_user)):
    """
    Creates a new user
    """
    company = db.query(models.Company).filter(
        models.Company.uuid == current_user.company_uuid).one_or_none()
    all_users = db.query(models.User).filter(
        models.User.company_id == current_user.company_uuid)

    if all_users.count() == company.employees:
        raise HTTPException(status_code=status.HTTP_402_PAYMENT_REQUIRED,
                            detail=f"Have reached the maximum amount({company.employees}) of user accounts")
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
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT, detail="User already exists")

    return created_user


@router.put(
    "/{uuid_str}",
    response_model=schemas.UserResponse,
    status_code=status.HTTP_200_OK,
    responses={
        401: {
            "detail": "Not authenticated"
        },
        404: {
            "detail": "User not found"
        },
        409:{
            "detail": "Unable to update the user"
        }
    }
)
def update_user(user: schemas.UserBase, uuid_str: str, db: Session = Depends(get_db), current_user=Depends(oauth2.get_current_user)):
    user_query = db.query(models.User).\
        filter(models.User.company_id == current_user.company_uuid).\
        filter(models.User.uuid == uuid_str)
        
    user_data = user_query.one_or_none()

    if not user_data:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"User with id {uuid_str} does not exist")
    
    try:
        user_query.update(user.dict())
        db.commit()
    except:
        db.rollback()
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail="Unable to update the user")
    
    return user_query.one_or_none()