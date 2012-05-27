Stallion
=========

Stallion is a Python Package Manager interface created to provide an "easy-to-use" visual interface
for Python newcomers. Today we have many nice distribution utilities like pip, distribute, etc, but
we don't have a nice visual approach with these same goals. 

Screenshots
-------------------------------------------------------------------------------

Screenshot: The home
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. image:: http://pyevolve.sourceforge.net/wordpress/wp-content/uploads/2011/12/main_page.png

Screenshot: Installed package information
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. image:: http://pyevolve.sourceforge.net/wordpress/wp-content/uploads/2011/12/distr.png

Screenshot: Package metadata
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. image:: http://pyevolve.sourceforge.net/wordpress/wp-content/uploads/2011/12/metadata.png

Screenshot: Check PyPI for updates available
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. image:: http://pyevolve.sourceforge.net/wordpress/wp-content/uploads/2011/12/updates_avail.png

.. image:: http://pyevolve.sourceforge.net/wordpress/wp-content/uploads/2011/12/updates.png

.. image:: http://pyevolve.sourceforge.net/wordpress/wp-content/uploads/2011/12/updates2.png

Screenshot: PyPI version mismatch diagnosis
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. image:: http://pyevolve.sourceforge.net/wordpress/wp-content/uploads/2011/12/diagnosis.png


Using Stallion
-------------------------------------------------------------------------------

::

    stallion [--help]

Easy to Install
-------------------------------------------------------------------------------

Installing using easy_install:

::

    $ easy_install stallion
    $ stallion

Upgrading using easy_install:

::

    $ easy_install -U stallion
    $ stallion
 

or using pip:

Installing using pip:

::

    $ pip install stallion
    $ stallion

Upgrading using pip:

::

    $ pip install --upgrade stallion
    $ stallion


Setting a development environment
-------------------------------------------------------------------------------

::

    $ python setup.py develop
    $ stallion

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
  - Jython 2.5.2
  - Python 2.6
  - Python 2.7
  - PyPy 1.7 *(and possibly older versions too)*

Status
-------------------------------------------------------------------------------
.. image:: https://secure.travis-ci.org/perone/stallion.png?branch=master
   :target: http://travis-ci.org/perone/stallion

Supported browsers
-------------------------------------------------------------------------------
Stallion is compatible with:

  - Firefox
  - Google Chrome
  - Internet Explorer 9 (IE9)
  - Safari

Run as service
-------------------------------------------------------------------------------
Windows:

  Requirements:
    - PyWin32: https://sourceforge.net/projects/pywin32/

  How To Install:
    - Install Stallion
    - Install PyWin32 package
    - Run from console

    ::

      $ stallion-service.exe --wait=1000 --startup=auto install
      $ stallion-service.exe start

    - Open http://127.0.0.1:5000/

  Uninstall:
    - Before remove Stallion package, need remove he service

    ::

      $ stallion-service.exe stop
      $ stallion-serivce.exe remove

What's new in release v0.2
-------------------------------------------------------------------------------

Bug fixes
   Lot's of bugs were fixed:
     - Unicode problem (https://github.com/perone/stallion/issues/15)
     - Python 2.5 compatibility (https://github.com/perone/stallion/issues/12)
     - Ignored explicit port (https://github.com/perone/stallion/issues/6)
     - Internet Explorer 9 compatibility (https://github.com/perone/stallion/issues/4)
     - Jinja2 version dependency (https://github.com/perone/stallion/issues/1)
     - Other small fixes

   Global checking feature
      Many people asked for a global version updates checking, now you have this
      feature under the menu "PyPI Repository". This option is going to check
      updates for all your packages. A new icon will appear on the sidebar
      packages menu warning in case of a new available update.
   
   Classifiers refactoring
      The classifiers of the package are now visually different.

Reporting bug
-------------------------------------------------------------------------------

Open an issue in Github with the traceback. To get the traceback, you'll 
have to run Stallion in debugging mode:

::

    $ stallion -drvi

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

Contributors
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Thanks to all contributors, in order of appearence:

- Christian S. Perone
- Thomas Léveil
- Simon J Greenhill
- Roman Gladkov
- Marc Abramowitz

Links
-------------------------------------------------------------------------------

* `Project Site (github) <https://github.com/perone/stallion>`_
