"""
.. module:: main
   :platform: Unix, Windows
   :synopsis: Main Stallion entry-point.

.. moduleauthor:: Christian S. Perone <christian.perone@gmail.com>

:mod:`main` -- main Stallion entry-point
==================================================================
"""
from optparse import OptionParser

import sys
import platform
import logging

try:
    import xmlrpclib
except ImportError:
    import xmlrpc.client

import pkg_resources as _pkg_resources

from flask import Flask, render_template, url_for, jsonify

from docutils.core import publish_parts

import stallion
from stallion import metadata

app = Flask(__name__)

PYPI_XMLRPC = 'http://pypi.python.org/pypi'

# This is a cache with flags to show if a distribution
# has an update available
DIST_PYPI_CACHE = set()


class Crumb(object):
    """ Represents each level on the bootstrap breadcrumb. """
    def __init__(self, title, href='#'):
        """ Instatiates a new breadcrum level.

        :param title: the title
        :param href: the link
        """
        self.title = title
        self.href = href


def get_pkg_res():
    reload(_pkg_resources)
    return _pkg_resources


def get_shared_data():
    """ Returns a new dictionary with the shared-data between different
    Stallion views (ie. a lista of distribution packages).

    :rtype: dict
    :return: the dictionary with the shared data.
    """
    shared_data = {'pypi_update_cache': DIST_PYPI_CACHE,
                   'distributions': [d for d in get_pkg_res().working_set]}

    return shared_data


def get_pypi_proxy():
    """ Returns a RPC ServerProxy object pointing to the PyPI RPC
    URL.

    :rtype: xmlrpclib.ServerProxy
    :return: the RPC ServerProxy to PyPI repository.
    """
    return xmlrpclib.ServerProxy(PYPI_XMLRPC)


def get_pypi_releases(dist_name):
    """ Return the releases available at PyPI repository and sort them using
    the pkg_resources.parse_version, the lastest version is on the 0 index.

    :param dist_name: the distribution name
    :rtype: list
    :return: a list with the releases available at PyPI
    """
    pypi = get_pypi_proxy()

    show_hidden = True
    ret = pypi.package_releases(dist_name, show_hidden)

    if not ret:
        ret = pypi.package_releases(dist_name.capitalize(), show_hidden)

    ret.sort(key=lambda v: _pkg_resources.parse_version(v), reverse=True)

    return ret

def get_pypi_search(spec, operator='or'):
    """Search the package database using the indicated search spec

    The spec may include any of the keywords described in the above list
    (except 'stable_version' and 'classifiers'), for example: {'description': 'spam'}
    will search description fields. Within the spec, a field's value can be a string
    or a list of strings (the values within the list are combined with an OR), for
    example: {'name': ['foo', 'bar']}. Valid keys for the spec dict are listed here.

    name
    version
    author
    author_email
    maintainer
    maintainer_email
    home_page
    license
    summary
    description
    keywords
    platform
    download_url
    
    Arguments for different fields are combined using either "and" (the default) or "or".
    Example: search({'name': 'foo', 'description': 'bar'}, 'or'). The results are
    returned as a list of dicts {'name': package name, 'version': package release version,
    'summary': package release summary}
    browse(classifiers)
    """
    pypi = get_pypi_proxy()
    ret = pypi.search(spec, operator)
    ret.sort(key=lambda v: v['_pypi_ordering'], reverse=True)
    return ret


@app.route('/pypi/check_update/<dist_name>')
def check_pypi_update(dist_name):
    """ Just check for updates and return a json
    with the attribute "has_update".

    :param dist_name: distribution name
    :rtype: json
    :return: json with the attribute "has_update"
    """
    pkg_res = get_pkg_res()
    pkg_dist_version = pkg_res.get_distribution(dist_name).version
    pypi_rel = get_pypi_releases(dist_name)

    if pypi_rel:
        pypi_last_version = pkg_res.parse_version(pypi_rel[0])
        current_version = pkg_res.parse_version(pkg_dist_version)

        if pypi_last_version > current_version:
            DIST_PYPI_CACHE.add(dist_name.lower())
            return jsonify({"has_update": 1})

    try:
        DIST_PYPI_CACHE.remove(dist_name.lower())
    except KeyError:
        pass

    return jsonify({"has_update": 0})


@app.route('/pypi/releases/<dist_name>')
def releases(dist_name):
    """ This is the /pypi/releases/<dist_name> entry point, it is the interface
    between Stallion and the PyPI RPC service when checking for updates.

    :param dist_name: the package name (distribution name).
    """
    pkg_res = get_pkg_res()

    data = {}

    pkg_dist_version = pkg_res.get_distribution(dist_name).version
    pypi_rel = get_pypi_releases(dist_name)

    data["dist_name"] = dist_name
    data["pypi_info"] = pypi_rel
    data["current_version"] = pkg_dist_version

    if pypi_rel:
        pypi_last_version = pkg_res.parse_version(pypi_rel[0])
        current_version = pkg_res.parse_version(pkg_dist_version)
        last_version = pkg_dist_version.lower() != pypi_rel[0].lower()

        data["last_is_great"] = pypi_last_version > current_version
        data["last_version_differ"] = last_version

        if data["last_is_great"]:
            DIST_PYPI_CACHE.add(dist_name.lower())
        else:
            try:
                DIST_PYPI_CACHE.remove(dist_name.lower())
            except KeyError:
                pass

    return render_template('pypi_update.html', **data)


@app.route('/')
def index():
    """ The main Flask entry-point (/) for the Stallion server. """
    data = {'breadpath': [Crumb('Main')]}

    data.update(get_shared_data())
    data['menu_home'] = 'active'

    sys_info = {'Python Platform': sys.platform,
                'Python Version': sys.version,
                'Python Prefix': sys.prefix,
                'Machine Type': platform.machine(),
                'Platform': platform.platform(),
                'Processor': platform.processor()}

    try:
        sys_info['Python Implementation'] = platform.python_implementation()
    except:
        pass

    sys_info['System'] = platform.system()
    sys_info['System Arch'] = platform.architecture()

    data['system_information'] = sys_info

    return render_template('system_information.html', **data)

@app.route('/console_scripts')
def console_scripts():
    """ Entry point for the global console scripts """
    data = {}
    data.update(get_shared_data())
    data['menu_console_scripts'] = 'active'
    data['breadpath'] = [Crumb('Console Scripts')]

    entry_console = get_pkg_res().iter_entry_points('console_scripts')
    data['scripts'] = entry_console

    return render_template('console_scripts.html', **data)

@app.route('/about')
def about():
    """ The About entry-point (/about) for the Stallion server. """

    data = {}
    data.update(get_shared_data())
    data['menu_about'] = 'active'

    data['breadpath'] = [Crumb('About')]
    data['version'] = stallion.__version__
    data['author'] = stallion.__author__
    data['author_url'] = stallion.__author_url__

    return render_template('about.html', **data)


@app.route('/distribution/<dist_name>')
def distribution(dist_name=None):
    """ The Distribution entry-point (/distribution/<dist_name>)
    for the Stallion server.

    :param dist_name: the package name
    """

    pkg_dist = get_pkg_res().get_distribution(dist_name)

    data = {}
    data.update(get_shared_data())

    data['dist'] = pkg_dist
    data['breadpath'] = [Crumb('Main', url_for('index')),
                         Crumb('Package'), Crumb(pkg_dist.project_name)]

    settings_overrides = {
        'raw_enabled': 0,  # no raw HTML code
        'file_insertion_enabled': 0,  # no file/URL access
        'halt_level': 2,  # at warnings or errors, raise an exception
        'report_level': 5,  # never report problems with the reST code
    }

    pkg_metadata = pkg_dist.get_metadata(metadata.METADATA_NAME)
    parsed, key_known = metadata.parse_metadata(pkg_metadata)
    distinfo = metadata.metadata_to_dict(parsed, key_known)

    parts = None
    try:
        parts = publish_parts(source=distinfo['description'],
                              writer_name='html',
                              settings_overrides=settings_overrides)
    except:
        pass

    data['distinfo'] = distinfo
    data['entry_map'] = pkg_dist.get_entry_map()

    if parts is not None:
        data['description_render'] = parts['body']

    return render_template('distribution.html', **data)


def run_main():
    """ The main entry-point of Stallion. """

    print('Stallion %s - Python Package Manager' % (stallion.__version__,))
    print('By %s 2013\n' % (stallion.__author__,))
    parser = OptionParser()

    parser.add_option('-s', '--host', dest='host',
                    help='The hostname to listen on, ' \
                         'set to \'0.0.0.0\' to have the '
                         'server available externally as well. '
                         'Default is \'127.0.0.1\' (localhost only).',
                    metavar="HOST", default='127.0.0.1')

    parser.add_option('-d', '--debug', action='store_true',
                  help='Start Stallion in Debug mode (useful to report bugs).',
                  dest='debug', default=False)

    parser.add_option('-r', '--reloader', action='store_true',
                  help='Uses the reloader.', dest='reloader', default=False)

    parser.add_option('-i', '--interactive', action='store_true',
                  help='Enable the interactive interpreter' \
                       ' for debugging (useful to debug errors).',
                  dest='evalx', default=False)

    parser.add_option('-p', '--port', dest='port',
                    help='The port to listen on. ' \
                         'Default is the port \'5000\'.',
                    metavar="PORT", default='5000')

    parser.add_option('-v', '--verbose', dest='verbose', action='store_true',
                    help='Turn on verbose messages (show HTTP requests).' \
                         ' Default is False.',
                    default=False)

    parser.add_option('-w', '--web-browser', dest='web_browser', action='store_true',
                    help='Open a web browser to show Stallion.' \
                         ' Default is False.',
                    default=False)

    (options, args) = parser.parse_args()

    if not options.verbose:
        print(" * Running on http://%s:%s/" % (options.host, options.port))
        werk_log = logging.getLogger('werkzeug')
        werk_log.setLevel(logging.WARNING)

    if options.web_browser:
        import webbrowser
        webbrowser.open('http://%s:%s/' % (options.host, options.port))

    app.run(debug=options.debug, host=options.host, port=int(options.port),
            use_evalex=options.evalx, use_reloader=options.reloader)

if __name__ == '__main__':
    run_main()
