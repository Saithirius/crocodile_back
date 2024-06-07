from .User import User


class Room:
    def __init__(self, id: str, creator: User):
        self.id = id
        self.creator = creator
        self.users = [creator]

    def add_user(self, user):
        self.users.append(user)

    def remove_user(self, user):
        self.users.remove(user)
