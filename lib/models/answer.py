"""Defines an answer class"""

import datetime
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

    Methods
    -------
    store()
        Stores/updates the answer in the sqlite database.
    """

    def __init__(self, id: int, answer: str, likes: int, created: datetime.datetime, 
                       tell: str, user: User):
        self.id: int = id
        self.answer: str = answer
        self.likes: int = likes
        self.created: datetime.datetime = created
        self.tell: str = tell
        self.user: User = user
        self.store()

    def store(self) -> None:
        """Stores/updates the answer in the sqlite database."""
        con, c = db.connect()
        if not db.exists('SELECT * FROM answers WHERE id = ?', self.id, con=con):
            c.execute('INSERT INTO answers VALUES (?, ?, ?, ?, ?, ?)', (self.id, self.answer, 
                      self.likes, self.created, self.tell, self.user.id,))
        c.execute('UPDATE answers SET answer=?, likes=?, created=?, tell=?, user=? '+\
                  'WHERE id = ?', (self.answer, self.likes, self.created, self.tell, 
                  self.user.id, self.id,))
        db.close(con)

    def __str__(self) -> str:
        """Returns a short string representation of the answer."""
        return '[Q]: {}?\n[A]: {}'.format(self.tell, self.answer)