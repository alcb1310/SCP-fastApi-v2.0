import uuid
from typing import List

from fastapi import status, HTTPException, Depends, APIRouter
from sqlalchemy.orm import Session

from ... import schemas, models, oauth2
from ...database import get_db

router = APIRouter(
    prefix="/api/v1.0/suppliers",
    tags=["Suppliers"]
)


@router.get("/", status_code=status.HTTP_200_OK, response_model=List[schemas.SupplierResponse])
def get_all_suppliers(db: Session = Depends(get_db), current_user=Depends(oauth2.get_current_user)):
    suppliers = db.query(models.Supplier).filter(models.Supplier.company_id == current_user.company_uuid).all()

    return suppliers


@router.get("/{uuid_str}", status_code=status.HTTP_200_OK, response_model=schemas.SupplierResponse)
def get_one_supplier(uuid_str: str, db: Session = Depends(get_db), current_user=Depends(oauth2.get_current_user)):
    supplier = db.query(models.Supplier).\
        filter(models.Supplier.company_id == current_user.company_uuid).\
        filter(models.Supplier.uuid == uuid_str).\
        one_or_none()

    if not supplier:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Supplier could not be found")

    return supplier


@router.post("/", status_code=status.HTTP_201_CREATED, response_model=schemas.SupplierResponse)
def create_a_supplier(
        supplier: schemas.SupplierBase,
        db: Session = Depends(get_db),
        current_user=Depends(oauth2.get_current_user)
):
    uuid_str = str(uuid.uuid4())
    try:
        supplier_dict = models.Supplier(
            uuid=uuid_str,
            company_id=current_user.company_uuid,
            user_id=current_user.user_uuid,
            supplier_id=supplier.supplier_id,
            name=supplier.name,
            contact_name=supplier.contact_name,
            contact_phone=supplier.contact_phone,
            contact_email=supplier.contact_email
        )
        db.add(supplier_dict)
        db.commit()
        db.refresh(supplier_dict)
    except Exception as error:
        print(error)
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail=f"Supplier {supplier.name} already exists")

    return supplier_dict


@router.put("/{uuid_str}", status_code=status.HTTP_200_OK, response_model=schemas.SupplierResponse)
def update_a_supplier(
        uuid_str: str,
        supplier: schemas.SupplierBase,
        db: Session = Depends(get_db),
        current_user=Depends(oauth2.get_current_user)
):
    supplier_query = db.query(models.Supplier).\
        filter(models.Supplier.company_id == current_user.company_uuid).\
        filter(models.Supplier.uuid == uuid_str)

    supplier_data = supplier_query.one_or_none()

    if not supplier_data:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Supplier could not be found")

    supplier_query.update(supplier.dict())
    db.commit()

    return supplier_query.one_or_none()
