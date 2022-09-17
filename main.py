from fastapi import FastAPI
from src import root

app = FastAPI()

app.include_router(root.router)
