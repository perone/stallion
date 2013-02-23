"""
.. module:: console
   :platform: Unix, Windows
   :synopsis: Stallion entry-point for console commands

.. moduleauthor:: Christian S. Perone <christian.perone@gmail.com>

:mod:`console` -- Stallion entry-point for console commands
==================================================================
"""
import stallion

from docopt import docopt

def cmd_list(args):
    pass


def run_main():
    """Stallion - Python List Packages (PLP)

    Usage:
      plp list

      plp (-h | --help)
      plp --version

    Options:
      -h --help     Show this screen.
      --version     Show version.
    """

    arguments = docopt(run_main.__doc__,
        version='Stallion v.%s - Python List Packages (PLP)' %
        stallion.__version__)
    
    #print(arguments)

    if arguments['list']:
        cmd_list(arguments)
        
if __name__ == '__main__':
    run_main()
