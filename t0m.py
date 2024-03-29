"""The main file - the entry point"""

import pash.cmds, pash.misc, os, sys
from argparse import ArgumentParser

from lib import cmd

def main():
    parser = ArgumentParser()
    parser.add_argument('-gui', action='store_true', help='Start a GUI?')
    args = parser.parse_args()
    sys.argv = sys.argv[:1]

    if args.gui:
        from lib import gui
        gui.show()
        os._exit(0)

    pash.cmds.clear(None, [])
    pash.misc.fprint("""     s                                        
    :8        .n~~%x.                         
   .88      x88X   888.      ..    .     :    
  :888ooo  X888X   8888L   .888: x888  x888.  
-*8888888 X8888X   88888  ~`8888~'888X`?888f` 
  8888    88888X   88888X   X888  888X '888>  
  8888    88888X   88888X   X888  888X '88-by  
  8888    88888X   88888f   X888  888X '88-MattMoony
 .8888Lu= 48888X   88888    X888  888X '888>  
 ^%888*    ?888X   8888"   "*88%""*88" '888!` 
   'Y"      "88X   88*`      `~    "    `"`   
              ^"==="`                         
""")

    cmd.start()

if __name__ == '__main__':
    main()