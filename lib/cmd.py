"""Handles the interactive shell for the user"""

import colorama as cr
cr.init()
import pash.shell, pash.cmds, pash.command as pcmd
from typing import List

from lib import db
from lib.api import public

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
    get_cmd = pcmd.CascCommand('get', cmds=[
        get_user_cmd,
    ], hint='Get data from the API ... ')
    sh.add_cmd(get_cmd)
    # ---------------------------------------------------------------------------------------------------------------------- #
    sh.prompt_until_exit()