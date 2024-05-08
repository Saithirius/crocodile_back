import os
import random
import secrets
from typing import Optional

from fastapi import APIRouter, status
from fastapi.responses import FileResponse, JSONResponse
from pydantic import BaseModel


class User(BaseModel):
    name: str
    token: str
    avatar: str

    def update(self, data):
        for key, value in data.dict().items():
            if hasattr(self, key):
                setattr(self, key, value)


class UserOptional(User):
    __annotations__ = {k: Optional[v] for k, v in User.__annotations__.items()}


NAMES = ['Name1', 'Name2', 'Name3', 'Name4', 'Name5', 'Name6', 'Name7', 'Name8']
AVATARS_PATH = 'app/assets/avatars/'
users = {}  # { [token]: User }


def get_files_in_directory(folder_path):
    files = []
    for file_name in os.listdir(folder_path):
        if os.path.isfile(os.path.join(folder_path, file_name)):
            files.append(file_name)
    return files


def get_avatars_names():
    return get_files_in_directory(AVATARS_PATH)


def get_new_user():
    name = random.choice(NAMES)

    token = secrets.token_urlsafe(6)
    while users.get(token) is not None:
        token = secrets.token_urlsafe(6)

    avatars = get_avatars_names()
    avatar_url = 'users/avatars/' + random.choice(avatars)

    return User(name=name, token=token, avatar=avatar_url)


router = APIRouter(
    prefix='/users',
    responses={404: {'description': 'Not found'}},
)


@router.post('')
async def create_user():
    user = get_new_user()
    users[user.token] = user
    return user


@router.get('/{token}')
async def get_user(token: str):
    if users.get(token) is not None:
        return users.get(token)
    else:
        return JSONResponse(status_code=status.HTTP_404_NOT_FOUND, content={'error': 'Not Found'})


@router.patch('/{token}')
async def patch_user(token: str, body: UserOptional):
    if users.get(token) is not None:
        user = users.get(token)
        user.update(body)
        print(user)
        return user
    else:
        return JSONResponse(status_code=status.HTTP_404_NOT_FOUND, content={'error': 'Not Found'})


@router.get('/avatars/{name}')
async def get_avatar(name: str):
    avatars = get_avatars_names()
    if (name in avatars):
        avatar_path = 'app/assets/avatars/' + name
        return FileResponse(avatar_path)
    else:
        return JSONResponse(status_code=status.HTTP_404_NOT_FOUND, content={'error': 'Not Found'})
