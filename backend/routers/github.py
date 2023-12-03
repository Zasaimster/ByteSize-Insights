from datetime import datetime
import json
from fastapi import APIRouter, Depends
import requests

from crud import get_all_repos, get_repo_by_id
from dependencies import get_mongo_db, GITHUB_TOKEN, OPENAI_TOKEN, GITHUB_API_URL
from datetime import timedelta

github_header = {
    "Accept": "application/vnd.github+json",
    "Authorization": f"Bearer {GITHUB_TOKEN}",
}

openai_header = {"Authorization": f"Bearer {OPENAI_TOKEN}"}

router = APIRouter(prefix="/github", tags=["github"])


@router.get("/getAllRepos")
async def get_repos(db=Depends(get_mongo_db)):
    repositories = get_all_repos(db)

    return repositories


@router.get("/getRepo")
async def get_repo(repo_id: str, db=Depends(get_mongo_db)):
    repository = get_repo_by_id(db, repo_id)

    return repository


@router.post("/registerNewRepository")
async def register_repo(repo_url: str, db=Depends(get_mongo_db)):
    # TODO
    print(f"Registering new repo: {repo_url}")


async def get_last_week_prs(repo):
    print(f"Getting PRs for:", {repo["url"]})
    curr_page, prs_older_than_week = 1, False
    last_week_prs = []

    while not prs_older_than_week:
        print(f"Page: {curr_page}")
        get_prs_url = f"{GITHUB_API_URL}/repos/{repo['owner']}/{repo['name']}/pulls?per_page=10&page={curr_page}"
        response = requests.get(get_prs_url, headers=github_header)
        prs = response.json()
        for pr in prs:
            print(f"ID: {pr['id']}, curr_page: {curr_page}")
            created_at = datetime.strptime(pr["created_at"], "%Y-%m-%dT%H:%M:%SZ")
            curr_time = datetime.now()
            if curr_time - created_at < timedelta(days=7):
                last_week_prs.append(
                    {
                        k: pr[k]
                        for k in [
                            "url",
                            "number",
                            "diff_url",
                            "state",
                            "title",
                            "body",
                            "created_at",
                            "updated_at",
                            "closed_at",
                            "merged_at",
                        ]
                    }
                )
            else:
                prs_older_than_week = True
                break
        if prs_older_than_week:
            break
        curr_page += 1

    return last_week_prs


async def get_diff_text(diff_url):
    print(f"Getting diff {diff_url}")
    response = requests.get(diff_url)
    if response.status_code != 200:
        print(f"Error getting diff: {diff_url}")
        return ""

    return response.text


# Called by Cron job running via AWS Lambda
# https://github.com/settings/tokens use this to make a personal
# access token and add to your .env file
@router.post("/summarizeAllPullRequests")
async def summarize_all_recent_pull_requests(db=Depends(get_mongo_db)):
    print("Summarizing All PRs...")

    pr_information = {}
    repositories = get_all_repos(db)

    # get pr information
    for repo in repositories:
        repo_id = repo["_id"]["$oid"]
        pr_information[repo_id] = await get_last_week_prs(repo)

    # get diff text from the diff_url field
    for pr_summaries in pr_information.values():
        for summary in pr_summaries:
            diff_text = await get_diff_text(summary["diff_url"])
            summary["diff"] = diff_text

    # call gpt wrapper for each pr and add summary to object

    return pr_information
    # call gpt wrapper for each one

    # use the patch url??
