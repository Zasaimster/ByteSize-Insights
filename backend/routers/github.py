from fastapi import APIRouter
from datetime import date
from bson import json_util
from bson.objectid import ObjectId
import pymongo
import json

def parse_json(data):
    return json.loads(json_util.dumps(data))

router = APIRouter(prefix="/github", tags=["github"])

URI = "mongodb+srv://cs130:7SBYtWrVqif1EzoR@cluster0.miyegq5.mongodb.net/?retryWrites=true&w=majority"
client = pymongo.MongoClient(URI)
db = client["ByteSize-Insights"]
col = db["repositories"]

@router.get("/getAllRepos")
async def get_all_repos():
    data = [x for x in col.find()]
    return {"message": parse_json(data)}

@router.get("/getRepo")
async def get_repo(
    repo_id: str,
    start_time: date = None,
    end_time: date = None
):
    data = col.find({"_id": ObjectId(repo_id)})
    return {"message": parse_json(data)}