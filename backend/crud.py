import json
from bson import json_util
from bson.objectid import ObjectId


def parse_json(data):
    return json.loads(json_util.dumps(data))


def get_summary(repo: str, id: int):
    print(f"get pr summary with a given repo and id: {repo} {id}")


def insert_user(
    db, username: str, hashed_password: str, first_name: str, last_name: str
):
    result = db.users.insert_one(
        {
            "username": username,
            "password": hashed_password,
            "firstName": first_name,
            "lastName": last_name,
        }
    )

    return result


def get_user(db, username: str):
    col = db["users"]
    user_data = col.find_one({"username": username})

    return parse_json(user_data)


def subscribe_user_to_repo(db, user_id: int, repo_id: int):
    col = db["users"]
    repo = col.find_one_and_update(
        {"_id": ObjectId(repo_id)}, {"$push": {"subscribers": user_id}}
    )

    return parse_json(repo)
