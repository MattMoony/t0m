"""Provides methods for accessing all public endpoints"""

from typing import List
from lib.api import urls
from lib.models.answer import Answer
from lib.models.user import User
import requests as req
import json, dateutil.parser

def get_user(uname: str) -> User:
    """Get one Tellonym user"""
    res = req.get(urls.USER_INFO.format(uname))
    if res.status_code != 200:
        return None
    obj = json.loads(res.text)
    return User(obj['avatarFileName'], obj['followerCount']+obj['anonymousFollowerCount'], obj['followingCount'], obj['id'], obj['displayName'],
                obj['username'], obj['aboutMe'], obj['likesCount'], obj['answerCount'], obj['tellCount'], obj['isVerified'])

def get_answers(uname: str) -> List[Answer]:
    """Get all answers a user has ever given."""
    u = get_user(uname)
    c = 0
    ans = []
    while c < u.answers:
        res = req.get(urls.GET_ANSWERS.format(u.id, 25, c))
        if res.status_code != 200:
            continue
        obj = json.loads(res.text)
        a = [Answer(a['id'], a['answer'], a['likesCount'], dateutil.parser.parse(a['createdAt']), a['tell'], a['userId']) for a in obj['answers'] if a['type'] == 'answer']
        ans.extend(a)
        c += len(a)
    return ans