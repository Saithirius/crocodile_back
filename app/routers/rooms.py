import socketio

from ..classes.GameManager import GameManager

sio = socketio.AsyncServer(cors_allowed_origins='*', async_mode='asgi')

socket_app = socketio.ASGIApp(sio)


@sio.on("*")
async def any_event(event, sid, data):
    print(event, sid, data)


@sio.event
async def connect(sid: str, data):
    print("<< NEW USER: " + str(sid))
    await sio.emit("msg", "Hello from Server")


@sio.event
async def hello(sid: str, token: str):
    print("<< hello: " + str(sid))
    user = GameManager.find_user_by_token(token)
    if user is not None:
        user.socket_sid = sid
        await sio.emit("user", user.dict())
    else:
        await sio.emit("user", {'error': 'not found'})


@sio.event
async def create_room(sid: str, data):
    room = GameManager.create_room(sid)
    print('New room', room)
    if room:
        await sio.enter_room(sid, room.id)
        await sio.emit("create_room", {'room': room.id})
    else:
        await sio.emit("create_room", {'error': '500'})


@sio.event
async def enter_room(sid: str, room_id: str):
    room = GameManager.join_room(room_id, sid)
    if room:
        await sio.enter_room(sid, room_id)


@sio.event
async def leave_room(sid: str, data):
    user = GameManager.find_user_by_socket_sid(sid)
    if user.current_room is not None:
        room_id = user.current_room
        leaved = GameManager.leave_room(sid)
        if leaved:
            await sio.leave_room(sid, room_id)


@sio.event
async def disconnect(sid: str):
    print("<< DISCONNECT USER: " + str(sid))
    user = GameManager.find_user_by_token(sid)
    if user is not None:
        user.socket_sid = sid
        await sio.emit("user", user.dict())
