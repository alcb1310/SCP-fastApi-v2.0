from fastapi import FastAPI

from . import models
from .database import engine
from .routers.authentication import companies, users, auth
from .routers.Transactions import project

models.Base.metadata.create_all(bind=engine)

app = FastAPI()

app.include_router(auth.router)
app.include_router(companies.router)
app.include_router(project.router)
app.include_router(users.router)
