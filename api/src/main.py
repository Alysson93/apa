from fastapi import FastAPI

from src.routes import auth, users

app = FastAPI(title="APA API", description="An API for the APA project")
app.include_router(auth.router)
app.include_router(users.router)


@app.get("/")
async def root():
    return {"msg": "Hello, World!"}
