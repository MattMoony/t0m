"""Defines an answer class"""

import datetime, dateutil.parser
from typing import Union
from lib import db
from lib.models.user import User

class Answer(object):
    """
    Represents a Tellonym answer.

    ...

    Attributes
    ----------
    id : int
        The answer's id.
    answer : str
        The actual answer - the content.
    likes : int
        The total amount of likes the answer has received.
    created : datetime.datetime
        A timestamp of the answer's creation.
    tell : str
        The original tell (question).
    user : User
        The user that answered the question.
    parent_id : int
        The id of the previous tell to which this is a follow-up.

    Methods
    -------
    store()
        Stores/updates the answer in the sqlite database.
    """

    def __init__(self, id: int, answer: str, likes: int, created: Union[datetime.datetime, str], 
                       tell: str, user: User, parent_id: int):
        self.id: int = id
        self.answer: str = answer
        self.likes: int = likes
        self.created: datetime.datetime = created if isinstance(created, datetime.datetime) else dateutil.parser.parse(created)
        self.tell: str = tell
        self.user: User = user
        self.parent_id: int = parent_id
        self.store()

    def store(self) -> None:
        """Stores/updates the answer in the sqlite database."""
        con, c = db.connect()
        if not db.exists('SELECT * FROM answers WHERE id = ?', self.id, con=con):
            c.execute('INSERT INTO answers VALUES (?, ?, ?, ?, ?, ?, ?)', (self.id, self.answer, 
                      self.likes, self.created, self.tell, self.user.id, self.parent_id,))
        c.execute('UPDATE answers SET answer=?, likes=?, created=?, tell=?, user=? '+\
                  'WHERE id = ?', (self.answer, self.likes, self.created, self.tell, 
                  self.user.id, self.id,))
        db.close(con)

    def __str__(self) -> str:
        """Returns a short string representation of the answer."""
        return '[Q]: {} || [A]: {} || [{}]'.format(self.tell, self.answer, self.created.isoformat())