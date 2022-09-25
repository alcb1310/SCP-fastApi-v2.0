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
    budget_items = db.query(models.BudgetItems).filter(
        models.BudgetItems.company_id == current_user.company_uuid).all()

    return budget_items


@router.get("/{uuid_str}", status_code=status.HTTP_200_OK, response_model=schemas.BudgetItemResponse)
def get_one_budget_item(uuid_str: str, db: Session = Depends(get_db), current_user=Depends(oauth2.get_current_user)):
    budget_item = db.query(models.BudgetItems).filter(
        models.BudgetItems.company_id == current_user.company_uuid).filter(
        models.BudgetItems.uuid == uuid_str).one_or_none()

    if not budget_item:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"Budget item with id {uuid_str} not found")

    return budget_item


@router.post("/", status_code=status.HTTP_201_CREATED, response_model=schemas.BudgetItemResponse)
def create_a_budget_item(
    budget_item: schemas.BudgetItemBase,
    db: Session = Depends(get_db),
    current_user=Depends(oauth2.get_current_user)
):
    uuid_str = str(uuid.uuid4())
    user_uuid = current_user.user_uuid
    company_uuid = current_user.company_uuid
    budget_item_dict = models.BudgetItems(
        uuid=uuid_str,
        user_id=user_uuid,
        company_id=company_uuid,
        code=budget_item.code,
        name=budget_item.name,
        accumulates=budget_item.accumulates,
        level=budget_item.level,
        parent_id=budget_item.parent_id
    )

    db.add(budget_item_dict)
    db.commit()
    db.refresh(budget_item_dict)

    return budget_item_dict


@router.put("/{uuid_str}", status_code=status.HTTP_200_OK, response_model=schemas.BudgetItemResponse)
def update_a_budget_item(
    uuid_str: str,
    budget_item_update_data: schemas.BudgetItemBase,
    db: Session = Depends(get_db),
    current_user=Depends(oauth2.get_current_user)
):
    budget_item_query = db.query(models.BudgetItems).filter(
        models.BudgetItems.company_id == current_user.company_uuid).filter(
        models.BudgetItems.uuid == uuid_str)

    budget_item = budget_item_query.one_or_none()

    if not budget_item:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"Budget item with id {uuid_str} not found")

    budget_item_query.update(budget_item_update_data.dict())
    db.commit()

    return budget_item_query.one_or_none()
