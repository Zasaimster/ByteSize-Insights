from fastapi import APIRouter

router = APIRouter(prefix="/pr", tags=["pr"])


@router.get("/process")
async def process_pr(pr_id: int):
    print("TODO: call github api to get pr data. store in mongodb")

    return {"message": "pr/process"}
