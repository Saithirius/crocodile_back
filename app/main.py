import uvicorn
from fastapi import FastAPI

from .routers import users
from .routers.rooms import socket_app

app = FastAPI()

app.include_router(users.router)

app.mount("/", socket_app)


@app.get("/")
def read_root():
    return {"message": "this is crocodile backend"}


if __name__ == "__main__":
    print('SERVER RUNNING')
    uvicorn.run('app.main:app', host='0.0.0.0', port=8000, reload=True)
