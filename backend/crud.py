import json
from bson import json_util
from bson.objectid import ObjectId
from pymongo.collection import ReturnDocument


# Parses MongoDB document and converts to a dictionary/json object
def parse_json(data):
    return json.loads(json_util.dumps(data))


# Creates a user in MongoDB
def insert_user(
    db, username: str, hashed_password: str, first_name: str, last_name: str
):
    result = db.users.insert_one(
        {
            "username": username,
            "password": hashed_password,
            "firstName": first_name,
            "lastName": last_name,
            "subscriptions": [],
        }
    )

    return result


# Returns a MongoDB user
def get_user(db, username: str):
    col = db["users"]
    user_data = col.find_one({"username": username})

    return parse_json(user_data)


# Subscribes a user to a repository in MongoDB. Creates 2 way mapping between User and Repository
def subscribe_user_to_repo(db, user_id: str, repo_url: str):
    repo_col = db["repositories"]
    repo_col.find_one_and_update({"url": repo_url}, {"$push": {"subscribers": user_id}})

    users_col = db["users"]
    user = users_col.find_one_and_update(
        {"_id": ObjectId(user_id)}, {"$push": {"subscriptions": repo_url}}
    )

    return parse_json(user)


# Return all Repositories
def get_all_repos(db):
    col = db["repositories"]
    data = [repo for repo in col.find()]

    return parse_json(data)


# Returns a User's repositories
def get_user_repos(db, repo_urls):
    col = db["repositories"]
    user_repos = []
    for repo_url in repo_urls:
        user_repo = col.find_one({"url": repo_url})
        user_repos.append(parse_json(user_repo))

    return user_repos


# Returns a repository based on its URL
def get_repo_by_url(db, repo_url):
    repo_col = db["repositories"]
    repo = repo_col.find_one({"url": repo_url})

    pr_col = db["pull-requests"]
    repo = parse_json(repo)
    prs = []
    for pr_id in repo["pullRequests"]:
        pr = pr_col.find_one({"_id": ObjectId(pr_id)})
        prs.append(parse_json(pr))
    repo["pullRequests"] = prs

    return repo


# Adds list of PRs for a repository
def create_new_prs(db, repo_id, prs):
    if len(prs) == 0:
        print("No PRs included for repository")
        return None

    pr_col = db["pull-requests"]
    prs_to_include = []
    for pr in prs:
        # include PRs that haven't been added already (for when running the API frequently)
        existing_pr = pr_col.find_one({"url": pr["url"]})
        if existing_pr:
            print(f"PR for {pr['url']} exists. Skipping")
        else:
            prs_to_include.append(pr)

    if len(prs_to_include) == 0:
        print("No new PRs to add")
        return None

    insert_all_prs_res = pr_col.insert_many(prs_to_include)

    if not insert_all_prs_res:
        print("Error inserting PRs ", insert_all_prs_res)
        return None

    # Append PRs to repository.pullRequests
    repo_col = db["repositories"]
    pr_ids = [str(pr_id) for pr_id in insert_all_prs_res.inserted_ids]

    updated_repo = repo_col.find_one_and_update(
        {"_id": ObjectId(repo_id)},
        {"$push": {"pullRequests": {"$each": pr_ids}}},
        return_document=ReturnDocument.AFTER,
    )
    return parse_json(updated_repo)["pullRequests"]


# Gets all Users
def get_all_users(db):
    col = db["users"]
    user_lst = col.distinct("username")
    return parse_json(user_lst)


# Gets all PRs for a Repository
def get_all_prs(db):
    col = db["pull-requests"]
    pr_lst = col.distinct("description")
    return parse_json(pr_lst)
