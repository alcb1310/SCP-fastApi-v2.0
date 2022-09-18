import uuid
from typing import List

from fastapi import status, HTTPException, Depends, APIRouter
from psycopg2.extras import register_uuid
from sqlalchemy.orm import Session

from ... import schemas, models
from ...database import get_db

router = APIRouter()


@router.get("/api/v1.0/companies/", status_code=status.HTTP_200_OK, response_model=List[schemas.CompanyResponse])
async def get_all_companies(db: Session = Depends(get_db)):
    """
    Returns a list of all the companies registered
    """
    companies = db.query(models.Company).all()

    return companies


@router.get("/api/v1.0/companies/{uuid_str}", status_code=status.HTTP_200_OK, response_model=schemas.CompanyResponse)
async def get_one_company(uuid_str: uuid.UUID, db: Session = Depends(get_db)):
    """
    Given the uuid of a company, returns the company data
    """
    company = db.query(models.Company).filter(models.Company.uuid == uuid_str).one_or_none()
    if not company:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Company with uuid: {uuid_str} not found")

    return company


@router.post("/api/v1.0/companies/", status_code=status.HTTP_201_CREATED, response_model=schemas.CompanyResponse)
async def new_company(company: schemas.CompanyBase, db: Session = Depends(get_db)):
    """
    Creates a new company
    """
    register_uuid()
    uuid_entry = uuid.uuid4()
    company_dict = company.dict()
    company_dict["uuid"] = uuid_entry
    created_company = models.Company(**company_dict)
    try:
        db.add(created_company)
        db.commit()
        db.refresh(created_company)
    except Exception as error:
        print(error)
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail="Company already exists")

    return created_company


@router.put("/api/v1.0/companies/{uuid_str}", status_code=status.HTTP_200_OK, response_model=schemas.CompanyResponse)
async def update_company(uuid_str: uuid.UUID, company: schemas.CompanyBase, db: Session = Depends(get_db)):
    """
    When the user sends an updated company values, it updates the database
    """
    company_query = db.query(models.Company).filter(models.Company.uuid == uuid_str)
    company_to_update = company_query.one_or_none()
    if not company_to_update:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Company with uuid: {uuid_str} not found")

    print(company.dict())
    company_query.update(company.dict())
    db.commit()

    return company_query.one_or_none()
