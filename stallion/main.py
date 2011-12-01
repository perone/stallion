"""
.. module:: main
   :platform: Unix, Windows
   :synopsis: Main Stallion entry-point.

.. moduleauthor:: Christian S. Perone <christian.perone@gmail.com>

:mod:`main` -- main Stallion entry-point
==================================================================
"""

import sys
import platform

import pkg_resources

from flask import Flask
from flask import render_template

from docutils.core import publish_parts

import metadata

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
    pkg_dist = pkg_resources.get_distribution(key)

    data = {}
    data["dist"] = pkg_dist
    data["breadpath"] = [Crumb("Main", "/"), Crumb("Package"), Crumb(pkg_dist.project_name)]
    data["distributions"] = [d for d in pkg_resources.working_set]

    settings_overrides={
        'raw_enabled': 0, # no raw HTML code
        'file_insertion_enabled': 0,  # no file/URL access
        'halt_level': 2,  # at warnings or errors, raise an exception
        'report_level': 5,  # never report problems with the reST code
    }

    pkg_metadata = pkg_dist.get_metadata(metadata.METADATA_NAME)
    parsed_metadata, key_exist, key_known = metadata.parse_metadata(pkg_metadata)
    
    xx = """
Jinja2
~~~~~~~~~~~~
Jinja2 is a template engine written in pure Python.  It provides a
`Django`_ inspired non-XML syntax but supports inline expressions and
an optional `sandboxed`_ environment.
Nutshell
------------
Here a small example of a Jinja template::
{% extends 'base.html' %}
{% block title %}Memberlist{% endblock %}
{% block content %}
<ul>
{% for user in users %}
<li><a href="{{ user.url }}">{{ user.username }}</a></li>
{% endfor %}
</ul>
{% endblock %}
Philosophy
--------------
Application logic is for the controller but don't try to make the life
for the template designer too hard by giving him too few functionality.
For more informations visit the new `Jinja2 webpage`_ and `documentation`_.
.. _sandboxed: http://en.wikipedia.org/wiki/Sandbox_(computer_security)
.. _Django: http://www.djangoproject.com/
.. _Jinja2 webpage: http://jinja.pocoo.org/
.. _documentation: http://jinja.pocoo.org/2/documentation/
"""
    parts = None
    parts = publish_parts(source=xx, writer_name='html',
                          settings_overrides=settings_overrides)

    data["pkginfo"] = parsed_metadata

    if parts is None:
        data["description_render"] = None
    else:
        data["description_render"] = parts["body"]
    
    return render_template('distribution.html', **data)

if __name__ == '__main__':
    app.run(debug=True, host='127.0.0.1')
