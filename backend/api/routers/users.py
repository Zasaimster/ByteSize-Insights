from fastapi import APIRouter, Depends, HTTPException

from ..crud import get_repo_by_url, get_user_repos, subscribe_user_to_repo, get_all_repos
from .auth import get_user_information
from ..dependencies import get_mongo_db


router = APIRouter(prefix="/user", tags=["user"])


@router.post("/subscribeToRepo")
async def subscribe_to_repo(repo_url: str, db=Depends(get_mongo_db), user=Depends(get_user_information)):
    """Subscribe a User to a Repository via the URL"""
    print("USER ID")
    print(user["_id"]['$oid'])
    repo = subscribe_user_to_repo(
        db,
        user["_id"]['$oid'],
        repo_url,
    )
    if not repo:
        raise HTTPException(status_code=404, detail="Repository not found")

    return {"message": repo}


@router.get("/getSubbedRepos")
async def get_repos(db=Depends(get_mongo_db), user=Depends(get_user_information)):
    """List a User's repositories"""
    repositories = get_user_repos(db, user["subscriptions"])

    return repositories

@router.get("/getAllRepos")
async def get_repos(db=Depends(get_mongo_db)):
    repositories = get_all_repos(db)

    return repositories


@router.get("/getRepoInfo")
async def get_repo(repo_url: str, db=Depends(get_mongo_db)):
    """Get a Repository's information"""
    repository = get_repo_by_url(db, repo_url)

    return repository
