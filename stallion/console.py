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

from pkg_resources import DistributionNotFound

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

def get_kv_colored(key, value):
    text = Fore.WHITE + Style.BRIGHT + '  %s: ' % key.capitalize()
    text += Fore.WHITE + Style.NORMAL + value
    return text

def get_field_formatted(mdata, key):
    """ This function will get the formatted and colored 
    key data from the dictionary.

    :param mdata: distribution dict
    :param key: the key of the dict
    :return: the formatted and colored string
    """
    
    def recursive_dict(d, depth=2, final=''):
        final_str = final
        for k,v in sorted(d.items(), key=lambda x: x[0]):
            if isinstance(v, dict):
                if depth==2:
                    final_str += Fore.BLUE + Style.BRIGHT
                else:
                    final_str += Fore.WHITE + Style.NORMAL

                final_str += '  ' * depth + str(k) + '\n'
                final_str += recursive_dict(v, depth+1, final)
            else:
                final_str =+ ("  ")*depth + str(k) + ' ' + str(v) + '\n'
        return final_str

    field = parse_dict(mdata, key.lower())
    
    if isinstance(field, list):
        field = ', '.join(field)

    if isinstance(field, dict):
        field = '\n\n' + recursive_dict(field)

    text = get_kv_colored(key, field)
    return text

def cmd_show(args):
    """This function implements the package show command.

    :param args: the docopt parsed arguments
    """
    proj_name = args['<project_name>']

    try:
        pkg_dist = get_pkg_res().get_distribution(proj_name)
    except:
        print Fore.RED + Style.BRIGHT + 'Error: unable to locate the project \'%s\' !' % proj_name
        print Fore.RESET + Back.RESET + Style.RESET_ALL
        return

    pkg_metadata = pkg_dist.get_metadata(metadata.METADATA_NAME)
    parsed, key_known = metadata.parse_metadata(pkg_metadata)
    distinfo = metadata.metadata_to_dict(parsed, key_known)

    proj_head = Fore.GREEN + Style.BRIGHT + pkg_dist.project_name
    proj_head += Fore.YELLOW + Style.BRIGHT + ' ' + pkg_dist.version
    print proj_head,

    proj_sum = Fore.WHITE + Style.DIM
    proj_sum += '- ' + parse_dict(distinfo, 'summary', True)
    print proj_sum

    # Remove long fields and used fields
    if 'description' in distinfo:
        del distinfo['description']

    if 'summary' in distinfo:
        del distinfo['summary']

    if 'name' in distinfo:
        del distinfo['name']

    if 'version' in distinfo:
        del distinfo['version']

    classifier = None
    if 'classifier' in distinfo:
        classifier = distinfo['classifier']
        del distinfo['classifier']

    for key in distinfo:
        print get_field_formatted(distinfo, key)

    print
    print get_kv_colored('location', pkg_dist.location)
    requires = pkg_dist.requires()

    if len(requires) == 0:
        print get_kv_colored('requires', 'none')
    else:
        req_text = '\n'
        for req in requires:
            req_text += ' '*4 + str(req) + '\n'
        print get_kv_colored('requires', req_text)

    distinfo['classifier'] = classifier
    print get_field_formatted(distinfo, 'classifier')


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
      plp show <project_name>

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

    if arguments['show']:
        cmd_show(arguments)
        
if __name__ == '__main__':
    init()
    run_main()
