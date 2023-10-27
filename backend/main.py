from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from routers import github, db, ai

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

app.include_router(github.router)
app.include_router(db.router)
app.include_router(ai.router)


@app.get("/")
async def root():
    return {"message": "Hello World"}
