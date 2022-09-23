import uuid
from typing import List

from fastapi import status, HTTPException, Depends, APIRouter
from sqlalchemy.orm import Session

from ... import schemas, models, oauth2
from ...database import get_db

router = APIRouter(
    prefix="/api/v1.0/budget_items",
    tags=["Budget Items"]
)


@router.get("/", status_code=status.HTTP_200_OK, response_model=List[schemas.BudgetItemResponse])
def get_all_budget_items(db: Session = Depends(get_db), current_user=Depends(oauth2.get_current_user)):
    budget_items = db.query(models.BudgetItems).filter(models.BudgetItems.company_id == current_user.company_uuid).all()

    return budget_items
