from fastapi import APIRouter, status

router = APIRouter()


#    tags=["Home"],
#    prefix="/"


@router.get("/")
def home_page():
    return {
        "status": status.HTTP_200_OK,
        "data": {
            "message": "Welcome to SCP API"
        }
    }
