"""Handles all interactions with the sqlite db"""

import os, sqlite3
from typing import Tuple, Dict, Any, Optional, Union, List

from lib import params
from lib.models.user import User
from lib.models.answer import Answer

"""Path to the sqlilte db file"""
DB_PATH: str = os.path.join(params.TMP_PATH, 'info.db')

# =========================================================================================================================== #

def connect() -> Tuple[sqlite3.Connection, sqlite3.Cursor]:
    """
    Creates a connection to the sqlite db.
    
    Returns
    -------
    Tuple[sqlite3.Connection, sqlite3.Cursor]
        A tuple consisting of both the connection to the db and a cursor for the
        sqlite db.
    """
    con = sqlite3.connect(DB_PATH)
    return (con, con.cursor())

def close(con: sqlite3.Connection) -> None:
    """
    Closes the connection to the sqlite db.

    Parameters
    ----------
    con : sqlite3.Connection
        The connection to the db.
    """
    con.commit()
    con.close()

def exec(query: str, *args: Any, con: Optional[sqlite3.Connection] = None) -> None:
    """
    Opens a connection, executes the given query and closes the connection again.

    Parameters
    ----------
    query : str
        The query.
    *args : Any
        Arguments for the query (escaped parameters, i.e. '?' ...)
    con : Optional[sqlite3.Connection]
        Connection to the db.
    """
    arti = not con
    if arti:
        con, c = connect()
    else:
        c = con.cursor()
    c.execute(query, (*args, ))
    if arti:
        close(con)

def fetchone(query: str, *args: Any, con: Optional[sqlite3.Connection] = None) -> Union[Tuple[Any], None]:
    """
    Opens a connection, executes the query and returns the first result.

    Parameters
    ----------
    query : str
        The query.
    *args : Any
        Arguments for the query.
    con : Optional[sqlite3.Connection]
        Connection to the db. 
    
    Returns
    -------
    Union[Tuple[Any], None]
        Returns the first result (if any).
    """
    arti = not con
    if arti:
        con, c = connect()
    else:
        c = con.cursor()
    c.execute(query, (*args, ))
    res = c.fetchone()
    if arti:
        close(con)
    return res

def fetchall(query: str, *args: Any, con: Optional[sqlite3.Connection] = None) -> List[Tuple[Any]]:
    """
    Opens a connection, executes the query and returns all results.

    Parameters
    ----------
    query : str
        The query.
    *args : Any
        The arguments for the query.
    con : Optional[sqlite3.Connection]
        Connection to the db.
    
    Returns
    -------
    List[Tuple[Any]]
        Returns resulting rows (or empty list)
    """
    arti = not con
    if arti:
        con, c = connect()
    else:
        c = con.cursor()
    c.execute(query, (*args, ))
    res = c.fetchall()
    if arti:
        close(con)
    return res

# =========================================================================================================================== #

def exists(query: str, *args: Any, con: Optional[sqlite3.Connection] = None) -> bool:
    """
    Checks whether or not the given query yields a result.

    Parameters
    ----------
    query : str
        The query.
    *args : Any
        Arguments for the query (escaped parameters; '?' ...)
    con : Optional[sqlite3.Connection]
        Connection to the db.

    Returns
    -------
    bool
        Whether or not the query has yielded a result.
    """
    arti = not con
    if arti:
        con, c = connect()
    else:
        c = con.cursor()
    c.execute(query, (*args, ))
    res = bool(c.fetchone())
    if arti:
        close(con)
    return res

def get_user(uname: str, con: Optional[sqlite3.Connection] = None) -> Union[User, None]:
    """
    Load a user from the sqlite database by its username.
    
    Parameters
    ----------
    uname : str
        The user's username.
    con : Optional[sqlite3.Connection]
        Connection to the db.

    Returns
    -------
    Union[User, None]
        The user or None if it wasn't found.
    """
    u = fetchone('SELECT * FROM users WHERE uname = ?', uname)
    if not u:
        return None
    return User(*u)

def get_all_users(con: Optional[sqlite3.Connection] = None) -> List[User]:
    """
    Gets all users stored in the sqlite db.

    Parameters
    ----------
    con : Optional[sqlite3.Connection]
        Connection to the db.

    Returns
    -------
    List[User]
        List containing all users or empty.
    """
    users = fetchall('SELECT * FROM users', con=con)
    return [User(*u) for u in users]

def get_all_answers(uid: int, con: Optional[sqlite3.Connection] = None) -> List[Answer]:
    """
    Gets all the answers a user has ever given.

    Parameters
    ----------
    uid : int
        The user's id.
    con : Optional[sqlite3.Connection]
        Connection to the db.

    Returns
    -------
    List[Answers]
        List containing all answers or empty.
    """
    anss = fetchall('SELECT * FROM answers WHERE user = ?', uid, con=con)
    return [Answer(*a) for a in anss]

def get_total_of_answers(uname: Optional[str] = None, con: Optional[sqlite3.Connection] = None) -> int:
    """
    Gets the total amount of answers that are stored in the sqlite db.

    Parameters
    ----------
    uname : Optional[str]
        To only count answers by this user.
    con : Optional[sqlite3.Connection]
        Connection to the db.

    Returns
    -------
    int
        The total amount of answers.
    """
    if uname:
        noans = fetchone('SELECT COUNT(*) FROM answers a INNER JOIN users u ON a.user = u.id WHERE u.uname = ?', uname, con=con)
    else:
        noans = fetchone('SELECT COUNT(*) FROM answers', con=con)
    if not noans:
        return 0
    return noans[0]