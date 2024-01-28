from fastapi import APIRouter

router = APIRouter(prefix="/creators")

@router.get("/")
def get_creators():
    return