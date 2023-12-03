import uvicorn
from fastapi import FastAPI
from routers import github
from routers import users

app = FastAPI()

app.include_router(github.router)
app.include_router(users.router)


@app.get("/")
async def root():
    return {"message": "Hello World"}

if __name__ == "__main__":
  uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)