"""
.. module:: console
   :platform: Unix, Windows
   :synopsis: Stallion entry-point for console commands

.. moduleauthor:: Christian S. Perone <christian.perone@gmail.com>

:mod:`console` -- Stallion entry-point for console commands
==================================================================
"""
import stallion
from stallion.main import get_shared_data, get_pkg_res
from stallion import metadata

from docopt import docopt

from colorama import init
from colorama import Fore, Back, Style

def ellipsize(msg, max_size=80):
    """This function will ellipsize the string.

    :param msg: Text to ellipsize.
    :param max_size: The maximum size before ellipsizing,
                    default is 80.
    :return: The ellipsized string if len > max_size, otherwise
             the original string.
    """
    if len(msg) >= max_size:
        return "%s (...)" % msg[0:max_size-6]
    else:
        return msg

def parse_dict(mdata, key, ellip=False):
    """ This function will read the field from the dict and
    if not present will return the string 'Not Specified'

    :param mdata: the distribution info dict
    :param key: the key of the dict
    :ellip: if it will ellipsize
    :return: the string message or 'Not Specified' if empty
    """
    try:
        data = mdata[key]
        if ellip:
            return ellipsize(data)
        else:
            return data
    except KeyError:
        return 'Not Specified'


def get_field_formatted(mdata, key):
    """ This function will get the formatted and colored 
    key data from the dictionary.

    :param mdata: distribution dict
    :param key: the key of the dict
    :return: the formatted and colored string
    """
    field = parse_dict(mdata, key.lower())
    if isinstance(field, list):
        field = ', '.join(field)

    text = Fore.WHITE + Style.BRIGHT + '  %s: ' % key
    text += Fore.WHITE + Style.NORMAL + field
    return text

def cmd_list(args):
    """This function implements the package list command.

    :param args: the docopt parsed arguments
    """
    filt = args['<filter>']
    distributions = get_shared_data()['distributions']
    for d in distributions:
        if filt:
            if filt.lower() not in d.project_name.lower():
                continue

        pkg_dist = get_pkg_res().get_distribution(d.key)
        pkg_metadata = pkg_dist.get_metadata(metadata.METADATA_NAME)
        parsed, key_known = metadata.parse_metadata(pkg_metadata)
        distinfo = metadata.metadata_to_dict(parsed, key_known)
        
        proj_head = Fore.GREEN + Style.BRIGHT + d.project_name
        proj_head += Fore.YELLOW + Style.BRIGHT + ' ' + d.version
        print proj_head,

        proj_sum = Fore.WHITE + Style.DIM
        proj_sum += '- ' + parse_dict(distinfo, 'summary', True)
        print proj_sum

        print get_field_formatted(distinfo, 'Author'),
        author_email = distinfo.get('author-email')
        if author_email:
            print '<%s>' % author_email
        else: print

        print get_field_formatted(distinfo, 'Home-page')
        print get_field_formatted(distinfo, 'License')
        print get_field_formatted(distinfo, 'Platform')

        print Fore.RESET + Back.RESET + Style.RESET_ALL

def run_main():
    """Stallion - Python List Packages (PLP)

    Usage:
      plp list [<filter>]

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
    init()
    run_main()
