"""Defines a user class"""

class User(object):
    def __init__(self, avatar: str, followers: int, following: int, id: int, name: str, uname: str,
                       about: str, likes: int, answers: int, tells: int, verified: bool):
        self.avatar: str = avatar
        self.followers: int = followers
        self.following: int = following
        self.id: int = id
        self.name: str = name
        self.uname: str = uname
        self.about: str = about
        self.likes: str = likes
        self.answers: str = answers
        self.tells: int = tells
        self.verified: bool = verified