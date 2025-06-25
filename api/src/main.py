from fastapi import FastAPI

from src.routes import users

app = FastAPI(title='APA API', description='An API for the APA project')
app.include_router(users.router)


@app.get('/')
async def root():
    return {'msg': 'Hello, World!'}
