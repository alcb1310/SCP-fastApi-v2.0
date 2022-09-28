from fastapi import FastAPI

from . import models
from .database import engine
from .routers.authentication import companies, users, auth
from .routers.transactions import project, project_budget
from .routers.parameters import suppliers, budget_items
from .config import settings

models.Base.metadata.create_all(bind=engine)

app = FastAPI(
    title=settings.project_name,
    version=settings.project_version,
    description=settings.project_description
)

app.include_router(auth.router)
app.include_router(budget_items.router)
app.include_router(companies.router)
app.include_router(project.router)
app.include_router(project_budget.router)
app.include_router(suppliers.router)
app.include_router(users.router)
