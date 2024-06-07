import os
import random
import secrets
from typing import Optional

from pydantic import BaseModel

NAMES = ['Name1', 'Name2', 'Name3', 'Name4', 'Name5', 'Name6', 'Name7', 'Name8']
AVATARS_PATH = 'app/assets/avatars/'


def get_files_in_directory(folder_path):
    files = []
    for file_name in os.listdir(folder_path):
        if os.path.isfile(os.path.join(folder_path, file_name)):
            files.append(file_name)
    return files


AVATARS_NAMES = get_files_in_directory(AVATARS_PATH)


class User(BaseModel):
    name: str
    token: str
    avatar: str
    socket_sid: Optional[str]
    current_room: Optional[str]

    @staticmethod
    def create():
        name = random.choice(NAMES)

        token = secrets.token_urlsafe(6)
        # while users.get(token) is not None:
        #     token = secrets.token_urlsafe(6)

        avatar_url = 'users/avatars/' + random.choice(AVATARS_NAMES)
        print('New user: ' + name + ' ' + token + ' ' + avatar_url, flush=True)
        return User(name=name, token=token, avatar=avatar_url, socket_sid=None)

    def update(self, data):
        for key, value in data.dict().items():
            if hasattr(self, key):
                setattr(self, key, value)


class UserOptional(User):
    __annotations__ = {k: Optional[v] for k, v in User.__annotations__.items()}
