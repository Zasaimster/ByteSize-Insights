from fastapi import APIRouter, Depends
from bson import json_util
from bson.objectid import ObjectId
import json

from dependencies import get_mongo_db


def parse_json(data):
    return json.loads(json_util.dumps(data))


router = APIRouter(prefix="/github", tags=["github"])


# todo: move this functionality to crud.py
@router.get("/getAllRepos")
async def get_all_repos(db=Depends(get_mongo_db)):
    col = db["repositories"]
    data = [x for x in col.find()]
    return {"message": parse_json(data)}


@router.get("/getRepo")
async def get_repo(repo_id: str, db=Depends(get_mongo_db)):
    col = db["repositories"]
    data = col.find_one({"_id": ObjectId(repo_id)})
    return {"message": parse_json(data)}


@router.post("/summarizePullRequest")
async def summarize_pr(repo_id: str, pr_id: int):
    print("summarizing pr")
