from fastapi import APIRouter
from bson import json_util
from bson.objectid import ObjectId
import pymongo


def parse_json(data):
    return json.loads(json_util.dumps(data))


router = APIRouter(prefix="/user", tags=["user"])

URI = "mongodb+srv://cs130:7SBYtWrVqif1EzoR@cluster0.miyegq5.mongodb.net/?retryWrites=true&w=majority"
client = pymongo.MongoClient(URI)
db = client["ByteSize-Insights"]
col = db["users"]


@router.get("/getUser")
async def get_user(user_id: int):
    data = col.find({"_id": ObjectId(user_id)})
    return {"message": parse_json(data)}


@router.get("/subscribeToRepo")
async def subscribe_to_repo(user_id: int, repo_id: int):
    repo = col.find_one_and_update(
        {"_id": ObjectId(repo_id)}, {"$push": {"subscribers": user_id}}
    )
    return {"message": "pr/subscribeToRepo"}
