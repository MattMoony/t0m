"""Defines a user class"""

import pash.misc
from lib import db

class User(object):
    """
    Represents a Tellonym user.

    ...

    Attributes
    ----------
    avatar : str
        The URL to the user's profile-pic or None.
    followers : int
        The amount of followers the user has.
    following : int
        How many people the user follows.
    id : int
        The user's id.
    name : str
        The user's full name.
    uname : str
        The user's username.
    about : str
        The user's about text.
    likes : int
        The total amount of likes the user has received.
    answers : int
        The amount of answers the user has given.
    tells : int
        How many tells the user has received.
    verified : bool
        Whether or not the user is verified.

    Methods
    -------
    store()
        Will store/update all the user's attributes in the sqlite db.
    print_info()
        Prints the most important details to the console.
    """

    def __init__(self, avatar: str, followers: int, following: int, id: int, name: str, uname: str,
                       about: str, likes: int, answers: int, tells: int, verified: bool):
        """
        Parameters
        ----------
        avatar : str
            The user's profile-pic URL or None.
        followers : int
            The amount of followers.
        following : int
            The amount of following.
        id : int
            The user's id.
        name : str
            The user's full name.
        uname : str
            The user's username.
        about : str
            The user's about text.
        likes : int
            The user's total amount of likes.
        answers : int
            The user's total amount of answers.
        tells : int
            The user's total amount of tells.
        verified : bool
            Whether or not the user is verified.
        """
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
        self.store()

    def store(self) -> None:
        """Stores/updates all the user's information in the sqlite db."""
        con, c = db.connect()
        if not db.exists('SELECT * FROM users WHERE id = ?', self.id, con=con):
            c.execute('INSERT INTO users VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)', 
                      (self.avatar, self.followers, self.following, self.id, self.name, 
                      self.uname, self.about, self.likes, self.answers, self.tells, self.verified,))
        c.execute('UPDATE users SET avatar=?, followers=?, following=?, name=?, uname=?, '+\
                  'about=?, likes=?, answers=?, tells=?, verified=? WHERE id = ?', (self.avatar, 
                  self.followers, self.following, self.name, self.uname, self.about, self.likes, 
                  self.answers, self.tells, self.verified, self.id,))
        db.close(con)

    def print_info(self) -> None:
        """Prints the most important info to the console."""
        pash.misc.print_table([
            ['Id', str(self.id)],
            ['Name', self.name],
            ['Username', self.uname],
            ['-', '-'],
            ['Tells', str(self.tells)],
            ['Answers', str(self.answers)],
            ['-', '-'],
            ['Followers', str(self.followers)],
            ['Following', str(self.following)],
            ['Likes', str(self.likes)],
        ])

    def __str__(self) -> str:
        """Gives a short sring representation of the Tellonym user."""
        if self.name:
            return '{} ({})'.format(self.name, self.uname)
        return self.uname