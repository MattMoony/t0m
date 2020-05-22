"""Handles the interactive shell for the user"""

import colorama as cr
cr.init()
import pash.shell, pash.cmds, pash.command as pcmd
from typing import List

"""The basic prompt for the t0m shell"""
BPROMPT: str = cr.Fore.LIGHTBLUE_EX + 't0m' + cr.Fore.LIGHTBLACK_EX + '$ ' + cr.Fore.RESET
"""The shell itself"""
sh: pash.shell.Shell = pash.shell.Shell(prompt=BPROMPT)

def on_exit(cmd: pcmd.Command, args: List[str]) -> None:
    """Callback for `exit` - quits the shell"""
    sh.exit()

def start() -> None:
    """Start prompting the user for input."""
    sh.add_cmd(pcmd.Command('clear', 'cls', callback=pash.cmds.clear, hint='Clear the console ... '))
    sh.add_cmd(pcmd.Command('exit', 'quit', callback=on_exit, hint='Quit the shell ... '))
    sh.prompt_until_exit()