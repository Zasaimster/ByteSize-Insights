from fastapi import FastAPI
import requests

app = FastAPI()


@app.get("/")
async def root():
    return {"message": "Hello World"}

# @app.post("/scrape_repo/{url}")
# def scrape_repo(url):
#     repo_exists = False
