"""Defines an answer class"""

import datetime

class Answer(object):
    def __init__(self, id: int, answer: str, likes: int, created: datetime.datetime, 
                       tell: str, user: int):
        self.id: int = id
        self.answer: str = answer
        self.likes: int = likes
        self.created: datetime.datetime = created
        self.tell: str = tell
        self.user: int = user