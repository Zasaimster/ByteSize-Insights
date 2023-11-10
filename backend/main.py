from backend import chatgpt
from backend.routers import summaries
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from backend.routers import pr

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    # might want to change this to a designated list of allowed origins to limit who can call our endpoints
    # but I doubt this should matter since this will be hosted on the VPN
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(pr.router)
app.include_router(summaries.router)


@app.get("/")
async def root():
    return {"message": "Hello World"}
