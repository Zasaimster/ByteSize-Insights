from fastapi import APIRouter, Depends, HTTPException
from bson.objectid import ObjectId

from dependencies import get_mongo_db
from crud import subscribe_user_to_repo


router = APIRouter(prefix="/user", tags=["user"])


@router.post("/subscribeToRepo")
async def subscribe_to_repo(user_id: int, repo_id: int, db=Depends(get_mongo_db)):
    repo = subscribe_user_to_repo(
        db,
        user_id,
        repo_id,
    )
    if not repo:
        raise HTTPException(status_code=404, detail="Repository not found")

    return {"message": repo}
