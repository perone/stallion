"""
.. module:: main
   :platform: Unix, Windows
   :synopsis: Main Stallion entry-point.

.. moduleauthor:: Christian S. Perone <christian.perone@gmail.com>

:mod:`main` -- main Stallion entry-point
==================================================================
"""
from flask import Flask
from flask import render_template

import sys
import platform
import pkg_resources
import pkginfo
from docutils.core import publish_parts

app = Flask(__name__)

class Crumb(object):
    def __init__(self, title, href="#"):
        self.title = title
        self.href = href

@app.route('/')
def index():
    data = {}
    data["breadpath"] = [Crumb("Main", "/")]
    
    data["distributions"] = [d for d in pkg_resources.working_set]

    sys_info = {}
    sys_info["Python Platform"] = sys.platform
    sys_info["Python Version"] = sys.version
    sys_info["Python Prefix"] = sys.prefix
    sys_info["Machine Type"] = platform.machine()
    sys_info["Platform"] = platform.platform()
    sys_info["Processor"] = platform.processor()
    sys_info["Python Implementation"] = platform.python_implementation()
    sys_info["System"] = platform.system()
    sys_info["System Arch"] = platform.architecture()

    data["system_information"] = sys_info

    return render_template('system_information.html', **data)

@app.route('/distribution/<key>')
def package(key=None):
    dist = pkg_resources.get_distribution(key)

    data = {}
    data["dist"] = dist
    data["breadpath"] = [Crumb("Main", "/"), Crumb("Package"), Crumb(dist.project_name)]
    data["distributions"] = [d for d in pkg_resources.working_set]

    pkginfo_data = pkginfo.Installed(key)

    data["pkginfo"] = pkginfo_data

    settings_overrides={
        'raw_enabled': 0, # no raw HTML code
        'file_insertion_enabled': 0,  # no file/URL access
        'halt_level': 2,  # at warnings or errors, raise an exception
        'report_level': 5,  # never report problems with the reST code
    }

    parts = None
    try:
        parts = publish_parts(source=pkginfo_data.description, writer_name='html',
                              settings_overrides=settings_overrides)
    except:
        pass

    if parts is None:
        data["description_render"] = pkginfo_data.description
    else:
        data["description_render"] = parts["body"]
    
    return render_template('distribution.html', **data)

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0')
