from datetime import datetime
import json
from fastapi import APIRouter, Depends
import requests

from crud import get_all_repos, get_repo_by_url, create_new_prs, parse_json
from routers.auth import get_user_information
from dependencies import (
    get_mongo_db,
    GITHUB_TOKEN,
    OPENAI_TOKEN,
    GITHUB_API_URL,
    OPENAI_API_URL,
)
from datetime import timedelta

github_header = {
    "Accept": "application/vnd.github+json",
    "Authorization": f"Bearer {GITHUB_TOKEN}",
}

openai_header = {
    "Content-Type": "application/json",
    "Authorization": f"Bearer {OPENAI_TOKEN}",
}


router = APIRouter(prefix="/github", tags=["github"])


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


def get_chatgpt_message(pr_info):
    message = "Summarize the information about this pull request with the provided information. Make sure to make your description concise and understandable for non-developers like managers or executives when they read this. Here is all the necessary information you may need. You do not need to include it all. Use absolutely no markdown formatting in the response. Do not reply with a list. Give a brief summary as a paragraph.\n"
    message += f"Title: {pr_info['title']}\n"
    message += f"Body: {pr_info['body']}\n"
    if len(pr_info["diff"]) < 2500:
        message += (
            f"Use this PR's diff as a supplement for your response: {pr_info['diff']}\n"
        )
    message += "Here is other important info about the PR:\n"
    message += f"State: {pr_info['state']}\n"
    message += (
        f"Created at: {pr_info['created_at']}, Updated at: {pr_info['updated_at']}\n"
    )

    return message


async def chat_gpt_summarizer(pr_info):
    print(f"Getting ChatGPT Summary for PR {pr_info['url']}")
    chatgpt_body = {
        "model": "gpt-3.5-turbo",
        "messages": [{"role": "user", "content": get_chatgpt_message(pr_info)}],
    }

    chatgpt_response = requests.post(
        OPENAI_API_URL, headers=openai_header, json=chatgpt_body
    ).json()

    if "error" in chatgpt_response:
        print(chatgpt_response)
        return None
    print(chatgpt_response)

    return chatgpt_response["choices"][0]["message"]["content"]


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

    # TODO: filter out PRs here so that way we use less chatgpt and it runs quicker

    # get diff text and call chatgpt api
    for pr_summaries in pr_information.values():
        for summary in pr_summaries:
            diff_text = await get_diff_text(summary["diff_url"])
            summary["diff"] = diff_text

            chatgpt_summary = await chat_gpt_summarizer(summary)
            if chatgpt_summary is None:
                print("Unable to call ChatGPT")
                continue
            summary["description"] = chatgpt_summary

    print(
        "PR URLs:",
        [summary["url"] for prs in pr_information.values() for summary in prs],
    )

    # Create PRs and add them to repository
    for repo_id, pr_summaries in pr_information.items():
        res = create_new_prs(db, repo_id, pr_summaries)
        if res is None:
            continue
        print("New PR ObjectIds: ", res)

    return parse_json(pr_information)
