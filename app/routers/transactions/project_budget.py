import uuid
from typing import List
import sqlalchemy

from fastapi import status, HTTPException, Depends, APIRouter
from sqlalchemy.orm import Session

from ... import schemas, models, oauth2
from ...database import get_db

router = APIRouter(
    prefix="/api/v1.0/project_budgets",
    tags=["Project Budgets"]
)


@router.get(
    "/",
    status_code=status.HTTP_200_OK,
    response_model=List[schemas.ProjectBudgetResponse],
    responses={
        401: {
            "detail": "Not authenticated"
        }
    },
    summary="Get all of the project budget's items",
    response_description="A list of all of the project budget items"
)
def get_all_project_budgets(db: Session = Depends(get_db), current_user=Depends(oauth2.get_current_user)):
    """
    Returns a list of all of the project's budget items

    - **initial_quantity** (float) -> The budgeted initial quantity, can be null on budget items that accumulates
    - **initial_cost** (float) -> The cost of each budget item unit, can be null on budget items that accumulates
    - **initial_total** (float) -> The amount of money of each budget item
    - **spent_quantity** (float) -> The quantity of the budget item that has been spent to date, can be null on budget items that accumulates
    - **spent_total** (float) -> The amount of money that has been spent of the budget item to date
    - **to_spend_quantity** (float) -> The quantity of the budget item that is still to spend, cna be null on budget items that accumulates
    - **to_spend_cost** (float) -> The cost of each budget item unit, can be null on budget items that accumulates
    - **to_spend_total** (float) -> The amount of money that is still to be spend
    - **updated_budget** (float) -> The adjusted amount of money that is required by each budget item
    - It also returns the information about the project and the budget item
    """
    project_budgets = db.query(models.ProjectBudget).\
        join(models.Project).\
        join(models.BudgetItems).\
        filter(models.ProjectBudget.company_id == current_user.company_uuid).\
        order_by(models.Project.name).\
        order_by(models.BudgetItems.code).\
        all()

    return project_budgets


@router.post(
    "/",
    status_code=status.HTTP_201_CREATED,
    response_model=schemas.ProjectBudgetResponse,
    responses={
        401: {
            "detail": "Not authenticated"
        },
        409: {
            "detail": "Budget for project <project_id> with item <budget_item_id> already exists"
        }
    },
    summary="Create a project budget item",
    response_description="The created project budget item"
)
def create_project_budget(
    project_budget: schemas.ProjectBudget,
    db: Session = Depends(get_db),
    current_user=Depends(oauth2.get_current_user)
):
    """
    Creates a budget item within a project, on success it returns 201 Created on Exception it returns 409 Conflict

    - **project_id** (string) Each project budget must be associated to a project
    - **budget_item_id** (string) Each project budget must be associated to a budget item
    - **quantity** (float) Indicates the amount of the budget item is budgeted
    - **cost** (float) Indicates the cost of each unit of the budget item

    """
    total = project_budget.quantity * project_budget.cost

    to_create = models.ProjectBudget(
        uuid=str(uuid.uuid4()),
        user_id=current_user.user_uuid,
        company_id=current_user.company_uuid,
        project_id=project_budget.project_id,
        budget_item_id=project_budget.budget_item_id,
        initial_quantity=project_budget.quantity,
        initial_cost=project_budget.cost,
        initial_total=total,
        spent_quantity=0,
        spent_total=0,
        to_spend_quantity=project_budget.quantity,
        to_spend_cost=project_budget.cost,
        to_spend_total=total,
        updated_budget=total
    )
    try:
        db.add(to_create)
        project_budget_dict = project_budget.dict()
        create_parent_budget(project_budget_dict, db, current_user)
        db.commit()
        db.refresh(to_create)
    except sqlalchemy.exc.IntegrityError:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail=f"Budget for project {project_budget.project_id} with item {project_budget.budget_item_id} already exist"
        )

    return to_create


# Methods that supports the api calls
def create_parent_budget(budget, db: Session, current_user):
    """
    Given a budget dictionary defined by 
    {
        "project_id" the uuid of the project,
        "budget_item_id" the uuid of the budget item,
        "quantity": how much of the item,
        "cost": what is the cost of each item unit
    }
    if it does not exist it creates the budget item in the project and if it exists it updates the parent's total
    """
    budget_item = db.query(models.BudgetItems).filter(models.BudgetItems.company_id == current_user.company_uuid).filter(
        models.BudgetItems.uuid == budget["budget_item_id"]).one()
    parent_id = budget_item.parent_id

    if parent_id == None:
        return

    new_project_budget_query = db.query(models.ProjectBudget).filter(models.ProjectBudget.company_id == current_user.company_uuid).filter(
        models.ProjectBudget.budget_item_id == parent_id).filter(models.ProjectBudget.project_id == budget["project_id"])

    new_project_budget = new_project_budget_query.one_or_none()

    total = budget["quantity"] * budget["cost"]
    if new_project_budget:
        to_update = {
            "initial_total": new_project_budget.initial_total + total,
            "to_spend_total": total + new_project_budget.to_spend_total,
            "updated_budget": total + new_project_budget.updated_budget
        }

        new_project_budget_query.update(to_update)
    else:
        # have to create
        to_create = models.ProjectBudget(
            uuid=str(uuid.uuid4()),
            user_id=current_user.user_uuid,
            company_id=current_user.company_uuid,
            project_id=budget["project_id"],
            budget_item_id=parent_id,
            initial_total=total,
            spent_total=0,
            to_spend_total=total,
            updated_budget=total
        )
        db.add(to_create)

    budget["budget_item_id"] = parent_id
    create_parent_budget(budget, db, current_user)
