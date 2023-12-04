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
    col = db["repositories"]
    repos = col.find_one_and_update(
        {"_id": ObjectId(repo_id)}, {"$push": {"subscribers": user_id}}
    )

    return parse_json(repos)


def get_all_repos(db):
    col = db["repositories"]
    data = [repo for repo in col.find()]

    return parse_json(data)


def get_repo_by_id(db, repo_id):
    col = db["repositories"]
    repo = col.find_one({"_id": ObjectId(repo_id)})

    return parse_json(repo)


def create_new_prs(db, repo_id, prs):
    if len(prs) == 0:
        print("No PRs included for repository")
        return None

    pr_col = db["pull-requests"]
    prs_to_include = []
    for pr in prs:
        # include PRs that haven't been added already (for when running the API frequently)
        existing_pr = pr_col.find_one({"url": pr["url"]})
        print(existing_pr)
        if not existing_pr:
            prs_to_include.append(pr)
            print("does not exist. adding", len(prs_to_include))

    if len(prs_to_include) == 0:
        print("No new PRs to add")
        return None

    insert_all_prs_res = pr_col.insert_many(prs_to_include)

    if not insert_all_prs_res:
        print("Error inserting PRs ", insert_all_prs_res)
        return None

    # Append PRs to repository.pullRequests
    repo_col = db["repositories"]
    pr_ids = [str(pr["_id"]) for pr_id in insert_all_prs_res.inserted_ids]

    updated_repo = repo_col.find_one_and_update(
        {"_id": ObjectId(repo_id)},
        {"$push": {"pullRequests": {"$each": pr_ids}}},
        return_document=ReturnDocument.AFTER,
    )

    return parse_json(updated_repo)["pullRequests"]
