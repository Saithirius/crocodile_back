import secrets

from .Room import Room
from .User import User


class GameManager:
    users_by_token: dict[str, User] = {}
    users_by_socket_sid: dict[str, User] = {}
    rooms: dict[str, Room] = {}

    @staticmethod
    def add_user(user: User):
        GameManager.users_by_token[user.token] = user
        GameManager.users_by_socket_sid[user.socket_sid] = user

    @staticmethod
    def find_user_by_socket_sid(socket_sid: str) -> User | None:
        return GameManager.users_by_socket_sid.get(socket_sid)

    @staticmethod
    def find_user_by_token(token: str) -> User | None:
        return GameManager.users_by_token.get(token)

    @staticmethod
    def create_room(socket_sid) -> Room | None:
        creator = GameManager.find_user_by_socket_sid(socket_sid)
        if creator is not None and creator.current_room is None:
            room_id = secrets.token_urlsafe(6)
            room = Room(room_id, creator)
            GameManager.rooms[room_id] = room
            return room
        else:
            return None

    @staticmethod
    def join_room(room_id, socket_id) -> Room | None:
        room = GameManager.rooms.get(room_id)
        user = GameManager.find_user_by_socket_sid(socket_id)
        if room and user and user.current_room is None:
            room.add_user(user)
            return room
        else:
            return None

    @staticmethod
    def leave_room(socket_id) -> bool:
        user = GameManager.find_user_by_socket_sid(socket_id)
        if user and user.current_room is not None:
            room = GameManager.rooms.get(user.current_room)
            room.remove_user(user)
            return True
        else:
            return False
