Stallion
=========

Stallion is a Python Package Manager interface created to provide an "easy-to-use" visual interface
for Python newcomers. Today we have many nice distribution utilities like pip, distribute, etc, but
we don't have a nice visual approach with these same goals. 

See screenshots at http://pyevolve.sourceforge.net/wordpress/?p=2200

Using Stallion
-------------------------------------------------------------------------------

::

    python -m stallion.main [--help]

Easy to Install
-------------------------------------------------------------------------------

::

    $ easy_install stallion
    $ python -m stallion.main

*(this will install Stallion as well the requirements listed below)*

Requirements
-------------------------------------------------------------------------------

Stallion uses the following external projects:

Flask (https://github.com/mitsuhiko/flask)
   A microframework based on Werkzeug, Jinja2 and good intentions

Twitter Bootstrap (https://github.com/twitter/bootstrap)
   HTML, CSS, and JS toolkit from Twitter

docutils (http://docutils.sourceforge.net/)
   Docutils is an open-source text processing system for processing plaintext documentation
   into useful formats, such as HTML or LaTeX.

Jinja2 (Flask requirement) (https://github.com/mitsuhiko/jinja2)
   The Jinja2 template engine

Werkzeug (Flask requirement) (https://github.com/mitsuhiko/werkzeug)
   A flexible WSGI implementation and toolkit

Simplejson (If you use Python 2.5) (http://pypi.python.org/pypi/simplejson/)
   Simple, fast, extensible JSON encoder/decoder for Python

Compatibility
-------------------------------------------------------------------------------
Stallion is compatible with:

  - Python 2.5
  - Python 2.6
  - Python 2.7
  - PyPy 1.7 *(and possibly older versions too)*

License
-------------------------------------------------------------------------------

   Copyright 2011 Christian S. Perone

   Licensed under the Apache License, Version 2.0 (the "License");
   you may not use this file except in compliance with the License.
   You may obtain a copy of the License at

       http://www.apache.org/licenses/LICENSE-2.0

   Unless required by applicable law or agreed to in writing, software
   distributed under the License is distributed on an "AS IS" BASIS,
   WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
   See the License for the specific language governing permissions and
   limitations under the License.

Links
-------------------------------------------------------------------------------

* `Project Site (github) <https://github.com/perone/stallion>`_
