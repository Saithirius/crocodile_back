from fastapi import APIRouter, status
from fastapi.responses import FileResponse, JSONResponse

from ..classes.GameManager import GameManager
from ..classes.User import User, UserOptional, AVATARS_NAMES, AVATARS_PATH

router = APIRouter(
    prefix='/users',
    responses={404: {'description': 'Not found'}},
)


@router.post('')
async def create_user():
    user = User.create()
    GameManager.add_user(user)
    return user


@router.get('/{token}')
async def get_user(token: str):
    user = GameManager.find_user_by_token(token)
    if user is not None:
        return user.dict()
    else:
        return JSONResponse(status_code=status.HTTP_404_NOT_FOUND, content={'error': 'Not Found'})


# TODO: затирает все поля в None
@router.patch('/{token}')
async def patch_user(token: str, body: UserOptional):
    user = GameManager.find_user_by_token(token)
    if user is not None:
        user.update(body)
        print(user)
        return user
    else:
        return JSONResponse(status_code=status.HTTP_404_NOT_FOUND, content={'error': 'Not Found'})


@router.get('/avatars/{name}')
async def get_avatar(name: str):
    avatars = AVATARS_NAMES
    if (name in avatars):
        avatar_path = AVATARS_PATH + name
        return FileResponse(avatar_path)
    else:
        return JSONResponse(status_code=status.HTTP_404_NOT_FOUND, content={'error': 'Not Found'})
