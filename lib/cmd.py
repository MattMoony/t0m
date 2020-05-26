"""Handles the interactive shell for the user"""

import colorama as cr
cr.init()
import pash.shell, pash.cmds, pash.command as pcmd
from typing import List, Optional
import time, re

from lib import db
from lib.api import public
from lib.models.answer import Answer

"""The basic prompt for the t0m shell"""
BPROMPT: str = cr.Fore.LIGHTBLUE_EX + 't0m' + cr.Fore.LIGHTBLACK_EX + '$ ' + cr.Fore.RESET
"""The shell itself"""
sh: pash.shell.Shell = pash.shell.Shell(prompt=BPROMPT)

def on_exit(cmd: pcmd.Command, args: List[str]) -> None:
    """Callback for `exit` - quits the shell"""
    sh.exit()

def on_get_user(cmd: pcmd.Command, args: List[str], uname: str, force: bool) -> None:
    """Callback for `get user` - gets user info"""
    u = db.get_user(uname)
    if force or not u:
        u = public.get_user(uname)
    u.print_info()

def on_get_answers(cmd: pcmd.Command, args: List[str], uname: str) -> None:
    """Callback for `get answers` - gets all answers a user's ever given"""
    stime = time.time()
    anss = public.get_answers(uname)
    if not anss:
        print(' No answers found, are you sure the user exists?')
        return
    print(' Found & stored a total of %s%d%s answers in %.2fs ... ' % (cr.Fore.LIGHTGREEN_EX, len(anss), cr.Fore.RESET, (time.time()-stime)))

def on_ls_user(cmd: pcmd.Command, args: List[str]) -> None:
    """Callback for `ls user` - gets and displays all users from the db"""
    us = db.get_all_users()
    print(' Users:')
    for u in us:
        print('  -> %s' % u)
    print(' A total of %s%d%s users are currently stored in the sqlite database.' % (cr.Fore.LIGHTGREEN_EX, len(us), cr.Fore.RESET))

def on_ls_answers(cmd: pcmd.Command, args: List[str], uname: Optional[str] = None) -> None:
    """Callback for `ls answers` - gets and displays the total amount of answers stored in the db"""
    print(' A total of %s%d%s answers %sare currently stored in the sqlite database.' % (cr.Fore.LIGHTGREEN_EX, db.get_total_of_answers(uname), 
          cr.Fore.RESET, 'by {}{}{} '.format(cr.Fore.LIGHTCYAN_EX, uname, cr.Fore.RESET) if uname else ''))

def on_find(cmd: pcmd.Command, args: List[str], uname: str, substr: str) -> None:
    """Callback for `find` - gets all of a user's answers containing a substring"""
    substr = substr.lower()
    u = db.get_user(uname)
    print(uname)
    res = db.fetchall('SELECT a.* FROM answers a INNER JOIN users u ON a.user = u.id WHERE u.uname = ? AND (LOWER(a.answer) LIKE ? OR LOWER(a.tell) LIKE ?)', 
                      uname, '%'+substr+'%', '%'+substr+'%')
    match = re.compile(substr, re.IGNORECASE)
    repma = lambda s: match.sub(cr.Fore.LIGHTMAGENTA_EX+substr+cr.Fore.RESET, s)
    print(' Matches:')
    for a in [Answer(*r[:-2], u, r[-1]) for r in res]:
        print('  -> [Q]: %s || [A]: %s || [%s]' % (repma(a.tell or ''), repma(a.answer or ''), a.created.isoformat()))
    print(' A total of %s%d%s answers by %s%s%s match the current substring.' % (cr.Fore.LIGHTGREEN_EX, len(res), cr.Fore.RESET, cr.Fore.LIGHTCYAN_EX,
          uname, cr.Fore.RESET))

def start() -> None:
    """Start prompting the user for input."""
    # ---------------------------------------------------------------------------------------------------------------------- #
    sh.add_cmd(pcmd.Command('clear', 'cls', callback=pash.cmds.clear, hint='Clear the console ... '))
    # ---------------------------------------------------------------------------------------------------------------------- #
    sh.add_cmd(pcmd.Command('exit', 'quit', callback=on_exit, hint='Quit the shell ... '))
    # ---------------------------------------------------------------------------------------------------------------------- #
    get_user_cmd = pcmd.Command('user', 'u', callback=on_get_user, hint='Get, store and display a user\'s info ... ')
    get_user_cmd.add_arg('uname', type=str, help='Specify the username ... ')
    get_user_cmd.add_arg('-f', '--force-refresh', action='store_true', dest='force', help='Force reload info?')
    get_anss_cmd = pcmd.Command('answers', 'a', callback=on_get_answers, hint='Get and store all answers a user has ever given ... ')
    get_anss_cmd.add_arg('uname', type=str, help='Specify the username ... ')
    sh.add_cmd(pcmd.CascCommand('get', cmds=[
        get_user_cmd,
        get_anss_cmd,
    ], hint='Get data from the API ... '))
    # ---------------------------------------------------------------------------------------------------------------------- #
    ls_anss_cmd = pcmd.Command('answers', 'a', callback=on_ls_answers, hint='Get amount of answers stored in the db ... ')
    ls_anss_cmd.add_arg('-u', dest='uname', type=str, help='Specify a username ... ', required=False)
    sh.add_cmd(pcmd.CascCommand('ls', cmds=[
        pcmd.Command('user', 'u', callback=on_ls_user, hint='Get and display all users stored in the db ... '),
        ls_anss_cmd,
    ], hint='List data from the db ... '))
    # ---------------------------------------------------------------------------------------------------------------------- #
    find_cmd = pcmd.Command('find', 'query', callback=on_find, hint='Find all of a user\'s answers containing a substring ... ')
    find_cmd.add_arg('uname', type=str, help='Specify the username ... ')
    find_cmd.add_arg('substr', type=str, help='Specify the substring ... ')
    sh.add_cmd(find_cmd)
    # ---------------------------------------------------------------------------------------------------------------------- #
    sh.prompt_until_exit()