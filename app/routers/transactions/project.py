import uuid
from typing import List

from fastapi import status, HTTPException, Depends, APIRouter
from sqlalchemy.orm import Session

from ... import schemas, models, oauth2
from ...database import get_db

router = APIRouter(
    prefix="/api/v1.0/projects",
    tags=["Projects"]
)


@router.get("/", response_model=List[schemas.ProjectResponse], status_code=status.HTTP_200_OK)
def get_all_projects(db: Session = Depends(get_db), current_user=Depends(oauth2.get_current_user)):
    projects = db.query(models.Project).filter(models.Project.company_id == current_user.company_uuid).all()

    return projects


@router.get("/{uuid_str}", response_model=schemas.ProjectResponse, status_code=status.HTTP_200_OK)
def get_one_project(uuid_str: str, db: Session = Depends(get_db), current_user=Depends(oauth2.get_current_user)):
    project = db.query(models.Project). \
        filter(models.Project.company_id == current_user.company_uuid). \
        filter(models.Project.uuid == uuid_str). \
        one_or_none()

    if not project:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Project with id: {uuid_str} doesn't exist")

    return project


@router.post("/", response_model=schemas.ProjectResponse, status_code=status.HTTP_201_CREATED)
def create_a_project(project: schemas.ProjectBase, db: Session = Depends(get_db),
                     current_user=Depends(oauth2.get_current_user)
                     ):
    uuid_str = str(uuid.uuid4())

    project_dict = models.Project(
        name=project.name,
        uuid=uuid_str,
        user_id=current_user.user_uuid,
        company_id=current_user.company_uuid
    )

    try:
        db.add(project_dict)
        db.commit()
        db.refresh(project_dict)
    except Exception as error:
        print(error)
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail=f"Project {project.name} already exists")

    return project_dict


@router.put("/{uuid_str}", response_model=schemas.ProjectResponse, status_code=status.HTTP_200_OK)
def update_a_project(uuid_str: str, project: schemas.ProjectBase, db: Session = Depends(get_db),
                     current_user=Depends(oauth2.get_current_user)):
    project_query = db.query(models.Project). \
        filter(models.Project.company_id == current_user.company_uuid). \
        filter(models.Project.uuid == uuid_str)

    project_data = project_query.one_or_none()

    if not project_data:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Project with id: {uuid_str} doesn't exist")

    project_query.update(project.dict())
    db.commit()

    return project_query.one_or_none()
