from fastapi import APIRouter

router = APIRouter(prefix="/ai", tags=["chatgpt"])


@router.get("/")
async def github_test():
    return {"message": "ai"}
