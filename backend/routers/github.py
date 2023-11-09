from fastapi import APIRouter

router = APIRouter(prefix="/github", tags=["github"])


@router.get("/")
async def github_test():
    return {"message": "github"}
