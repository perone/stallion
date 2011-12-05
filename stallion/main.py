"""
.. module:: main
   :platform: Unix, Windows
   :synopsis: Main Stallion entry-point.

.. moduleauthor:: Christian S. Perone <christian.perone@gmail.com>

:mod:`main` -- main Stallion entry-point
==================================================================
"""
from optparse import OptionParser
from optparse import OptionGroup

import sys
import platform
import logging
import xmlrpclib

import pkg_resources

from flask import Flask
from flask import render_template
from flask import url_for
from flask import jsonify

from docutils.core import publish_parts

import metadata
import __init__ as stallion

app = Flask(__name__)

class Crumb(object):
    """ Represents each level on the bootstrap breadcrumb. """
    def __init__(self, title, href='#'):
        """ Instatiates a new breadcrum level.

        :param title: the title
        :param href: the link
        """
        self.title = title
        self.href = href

def get_shared_data():
    """ Returns a new dictionary with the shared-data between different
    Stallion views (ie. a lista of distribution packages).

    :rtype: dict
    :return: the dictionary with the shared data.
    """
    shared_data = {}
    shared_data['distributions'] = [d for d in pkg_resources.working_set]
    return shared_data

PYPI_XMLRPC = 'http://pypi.python.org/pypi'

def get_pypi_proxy():
    """ Returns a RPC ServerProxy object pointing to the PyPI RPC
    URL.

    :rtype: xmlrpclib.ServerProxy
    :return: the RPC ServerProxy to PyPI repository.
    """
    return xmlrpclib.ServerProxy(PYPI_XMLRPC)
    
@app.route('/pypi/releases/<dist_name>')
def releases(dist_name):
    """ This is the /pypi/releases/<dist_name> entry point, it is the interface
    between Stallion and the PyPI RPC service when checking for updates. 
    
    :param dist_name: the package name (distribution name).
    """
    data = {}

    pkg_dist_version = pkg_resources.get_distribution(dist_name).version

    pypi = get_pypi_proxy()
    show_hidden = True
    ret = pypi.package_releases(dist_name, show_hidden)

    if not ret:
        ret = pypi.package_releases(dist_name.capitalize(), show_hidden)

    ret.sort(key=lambda v: pkg_resources.parse_version(v), reverse=True)

    data["dist_name"] = dist_name
    data["pypi_info"] = ret
    data["current_version"] = pkg_dist_version

    if ret:
        data["last_is_great"] = pkg_resources.parse_version(ret[0]) > pkg_resources.parse_version(pkg_dist_version)
        data["last_version_differ"] = pkg_dist_version.lower() != ret[0].lower()
    
    return render_template('pypi_update.html', **data)

@app.route('/')
def index():
    """ The main Flask entry-point (/) for the Stallion server. """
    data = {}
    data['breadpath'] = [Crumb('Main')]
    
    data.update(get_shared_data())
    data['menu_home'] = 'active'

    sys_info = {}
    sys_info['Python Platform'] = sys.platform
    sys_info['Python Version'] = sys.version
    sys_info['Python Prefix'] = sys.prefix
    sys_info['Machine Type'] = platform.machine()
    sys_info['Platform'] = platform.platform()
    sys_info['Processor'] = platform.processor()
    sys_info['Python Implementation'] = platform.python_implementation()
    sys_info['System'] = platform.system()
    sys_info['System Arch'] = platform.architecture()

    data['system_information'] = sys_info

    return render_template('system_information.html', **data)

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
    """ The Distribution entry-point (/distribution/<dist_name>) for the Stallion server.
    
    :param dist_name: the package name
    """
    pkg_dist = pkg_resources.get_distribution(dist_name)

    data = {}
    data.update(get_shared_data())

    data['dist'] = pkg_dist
    data['breadpath'] = [Crumb('Main', url_for('index')), Crumb('Package'), Crumb(pkg_dist.project_name)]

    settings_overrides = {
        'raw_enabled': 0, # no raw HTML code
        'file_insertion_enabled': 0, # no file/URL access
        'halt_level': 2, # at warnings or errors, raise an exception
        'report_level': 5, # never report problems with the reST code
    }

    pkg_metadata = pkg_dist.get_metadata(metadata.METADATA_NAME)
    parsed, key_known = metadata.parse_metadata(pkg_metadata)
    distinfo = metadata.metadata_to_dict(parsed, key_known)
    
    parts = None
    try:
        parts = publish_parts(source = distinfo['description'],
                              writer_name = 'html', settings_overrides = settings_overrides)
    except:
        pass

    data['distinfo'] = distinfo

    if parts is not None:
        data['description_render'] = parts['body']
    
    return render_template('distribution.html', **data)

def run_main():
    """ The main entry-point of Stallion. """

    print 'Stallion %s - Python Package Manager' % (stallion.__version__,)
    print 'By %s 2011\n' % (stallion.__author__,)
    parser = OptionParser()

    parser.add_option('-s', '--host', dest='host',
                    help='The hostname to listen on, set to \'0.0.0.0\' to have the'
                         'server available externally as well. '
                         'Default is \'127.0.0.1\' (localhost only).',
                    metavar="HOST", default='127.0.0.1')

    parser.add_option('-d', '--debug', action='store_true',
                  help='Start Stallion in Debug mode (useful to report bugs).',
                  dest='debug', default=False)

    parser.add_option('-r', '--reloader', action='store_true',
                  help='Uses the reloader.', dest='reloader', default=False)

    parser.add_option('-i', '--interactive', action='store_true',
                  help='Enable the interactive interpreter for debugging (useful to debug errors).',
                  dest='evalx', default=False)

    parser.add_option('-p', '--port', dest='port',
                    help='The port to listen on. Default is the port \'5000\'.',
                    metavar="PORT", default='5000')

    parser.add_option('-v', '--verbose', dest='verbose', action='store_true',
                    help='Turn on verbose messages (show HTTP requests). Default is False.',
                    default=False)

    (options, args) = parser.parse_args()

    if not options.verbose:
        print " * Running on http://%s:%s/" % (options.host, options.port)
        werk_log = logging.getLogger('werkzeug')
        werk_log.setLevel(logging.WARNING)

    app.run(debug=options.debug, host=options.host, port=options.port,
            use_evalex=options.evalx, use_reloader=options.reloader)

if __name__ == '__main__':
    run_main()
