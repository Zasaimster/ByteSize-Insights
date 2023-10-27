from fastapi import APIRouter

router = APIRouter(prefix="/db", tags=["db"])


@router.get("/")
async def github_test():
    return {"message": "db"}
