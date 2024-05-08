from fastapi import FastAPI

from .routers import users

app = FastAPI()

app.include_router(users.router)


@app.get("/")
def read_root():
    return {"message": "this is crocodile backend"}


if __name__ == "__main__":
    print('SERVER RUNNING')
