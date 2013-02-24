# Stallion

Stallion is a Python Package Manager interface created to provide an "easy-to-use" visual interface
for Python newcomers. Today we have many nice distribution utilities like pip, distribute, etc, but
we don't have a nice visual approach with these same goals. 

## Screenshots

### Screenshot: The home

![The home](screenshots/main_screen.png)

![The home](http://pyevolve.sourceforge.net/wordpress/wp-content/uploads/2011/12/main_page.png)

### Screenshot: Installed package information

![Installed package information](http://pyevolve.sourceforge.net/wordpress/wp-content/uploads/2011/12/distr.png)

### Screenshot: Package metadata

![Package metadata](http://pyevolve.sourceforge.net/wordpress/wp-content/uploads/2011/12/metadata.png)

### Screenshot: Check PyPI for updates available

![Updates](http://pyevolve.sourceforge.net/wordpress/wp-content/uploads/2011/12/updates_avail.png)

![Updates](http://pyevolve.sourceforge.net/wordpress/wp-content/uploads/2011/12/updates.png)

![Updates](http://pyevolve.sourceforge.net/wordpress/wp-content/uploads/2011/12/updates2.png)

## Screenshot: PyPI version mismatch diagnosis

![Version mismatch](http://pyevolve.sourceforge.net/wordpress/wp-content/uploads/2011/12/diagnosis.png)

## Using Stallion

    $ stallion

or
   
    $ python -m stallion.main [--help]

## Easy to Install

Installing using pip:

    $ pip install stallion

Upgrading using pip:

    $ pip install --upgrade stallion

or using easy install:

Installing using easy_install:

    $ easy_install stallion

Upgrading using easy_install:

    $ easy_install -U stallion

## Setting a development environment
-------------------------------------------------------------------------------

    $ python setup.py develop
    $ stallion

## Requirements

Stallion uses the following external projects:

[Flask](https://github.com/mitsuhiko/flask)

> A microframework based on Werkzeug, Jinja2 and good intentions

[Twitter Bootstrap](https://github.com/twitter/bootstrap)

> HTML, CSS, and JS toolkit from Twitter

[docutils](http://docutils.sourceforge.net/)

> Docutils is an open-source text processing system for processing plaintext documentation
> into useful formats, such as HTML or LaTeX.

[Jinja2](https://github.com/mitsuhiko/jinja2) (Flask requirement)

>The Jinja2 template engine

[Werkzeug](https://github.com/mitsuhiko/werkzeug) (Flask requirement)

> A flexible WSGI implementation and toolkit

[Simplejson](http://pypi.python.org/pypi/simplejson/) (If you use Python 2.5)

> Simple, fast, extensible JSON encoder/decoder for Python

## Compatibility

Stallion is compatible with:

  - Python 2.5
  - Jython 2.5.2
  - Python 2.6
  - Python 2.7
  - PyPy 1.7 *(and possibly older versions too)*

## Supported browsers

Stallion is compatible with:

  - Firefox
  - Google Chrome
  - Internet Explorer 9 (IE9)
  - Safari

## What's new in release v0.4 (development version)

  - Added a new script called 'plp' (Python List Packages)
  - Added the command 'list' for plp
  - Added the command 'show' for plp
  - Added the command 'check' for plp
  - Added the command 'scripts' for plp
  - Added 'Console Scripts' section into the distribution info
    at the web frontend
  - Added the 'Console Scripts' global section on the
    web frontend
  - Added new font type for the web frontend

## What's new in release v0.3

  - Bug fixes, tests, CI with Travis CI
  - Update to latest Twitter Bootstrap version 2.3.0
  - Added a sample launchd plist for managing Stallion on Mac OS X
  - Added a console_scripts entry point for "stallion"
  - Added -w (--web-browser) option to open a web browser to Stallion
  - Python 3 compatibility fixes
  - PEP8 fixes

## What's new in release v0.2

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

## Reporting bug

Open an issue in Github with the traceback. To get the traceback, you'll 
have to run Stallion in debugging mode:

    $ stallion -drvi

## License

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

## Contributors

  See the [Contributors](https://github.com/perone/stallion/contributors).
  
## Links

[Project Site - Github](https://github.com/perone/stallion)
