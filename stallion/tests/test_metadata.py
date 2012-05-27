import sys
sys.path.insert(0, '.')

import unittest

from stallion import __version__
from stallion.metadata import parse_metadata, metadata_to_dict


class Test_metadata(unittest.TestCase):

    def test_metadata(self):
        jinja_metadata = 'Metadata-Version: 1.0\r\nName: Jinja2\r\nVersion: 2.6\r\nSummary: A small but fast and easy to use stand-alone template engine written in pure python.\r\nHome-page: http://jinja.pocoo.org/\r\nAuthor: Armin Ronacher\r\nAuthor-email: armin.ronacher@active-4.com\r\nLicense: BSD\r\nDescription: \r\n        Jinja2\r\n        ~~~~~~\r\n        \r\n        Jinja2 is a template engine written in pure Python.  It provides a\r\n        `Django`_ inspired non-XML syntax but supports inline expressions and\r\n        an optional `sandboxed`_ environment.\r\n        \r\n        Nutshell\r\n        --------\r\n        \r\n        Here a small example of a Jinja template::\r\n        \r\n            {% extends \'base.html\' %}\r\n            {% block title %}Memberlist{% endblock %}\r\n            {% block content %}\r\n              <ul>\r\n              {% for user in users %}\r\n                <li><a href="{{ user.url }}">{{ user.username }}</a></li>\r\n              {% endfor %}\r\n              </ul>\r\n            {% endblock %}\r\n        \r\n        Philosophy\r\n        ----------\r\n        \r\n        Application logic is for the controller but don\'t try to make the life\r\n        for the template designer too hard by giving him too few functionality.\r\n        \r\n        For more informations visit the new `Jinja2 webpage`_ and `documentation`_.\r\n        \r\n        .. _sandboxed: http://en.wikipedia.org/wiki/Sandbox_(computer_security)\r\n        .. _Django: http://www.djangoproject.com/\r\n        .. _Jinja2 webpage: http://jinja.pocoo.org/\r\n        .. _documentation: http://jinja.pocoo.org/2/documentation/\r\n        \r\nPlatform: UNKNOWN\r\nClassifier: Development Status :: 5 - Production/Stable\r\nClassifier: Environment :: Web Environment\r\nClassifier: Intended Audience :: Developers\r\nClassifier: License :: OSI Approved :: BSD License\r\nClassifier: Operating System :: OS Independent\r\nClassifier: Programming Language :: Python\r\nClassifier: Programming Language :: Python :: 3\r\nClassifier: Topic :: Internet :: WWW/HTTP :: Dynamic Content\r\nClassifier: Topic :: Software Development :: Libraries :: Python Modules\r\nClassifier: Topic :: Text Processing :: Markup :: HTML\r\n'
        parsed, key_known = parse_metadata(jinja_metadata)
        ret = metadata_to_dict(parsed, key_known)
        self.assertEquals({
            'name': 'Jinja2',
            'license': 'BSD',
            'author': 'Armin Ronacher',
            'metadata-version': '1.0',
            'home-page': 'http://jinja.pocoo.org/',
            'summary': 'A small but fast and easy to use stand-alone template engine written in pure python.',
            'version': '2.6',
            'classifier': {
                'Intended Audience': {'Developers': {}},
                'Operating System': {'OS Independent': {}},
                'Development Status': {'5 - Production/Stable': {}},
                'License': {'OSI Approved': {'BSD License': {}}},
                'Environment': {'Web Environment': {}},
                'Topic': {
                    'Software Development': {'Libraries': {'Python Modules': {}}},
                    'Text Processing': {'Markup': {'HTML': {}}},
                    'Internet': {'WWW/HTTP': {'Dynamic Content': {}}}},
                'Programming Language': {'Python': {'3': {}}}},
            'author-email': 'armin.ronacher@active-4.com',
            'description': 'Jinja2\n~~~~~~\n\nJinja2 is a template engine written in pure Python.  It provides a\n`Django`_ inspired non-XML syntax but supports inline expressions and\nan optional `sandboxed`_ environment.\n\nNutshell\n--------\n\nHere a small example of a Jinja template::\n\n    {% extends \'base.html\' %}\n    {% block title %}Memberlist{% endblock %}\n    {% block content %}\n      <ul>\n      {% for user in users %}\n        <li><a href="{{ user.url }}">{{ user.username }}</a></li>\n      {% endfor %}\n      </ul>\n    {% endblock %}\n\nPhilosophy\n----------\n\nApplication logic is for the controller but don\'t try to make the life\nfor the template designer too hard by giving him too few functionality.\n\nFor more informations visit the new `Jinja2 webpage`_ and `documentation`_.\n\n.. _sandboxed: http://en.wikipedia.org/wiki/Sandbox_(computer_security)\n.. _Django: http://www.djangoproject.com/\n.. _Jinja2 webpage: http://jinja.pocoo.org/\n.. _documentation: http://jinja.pocoo.org/2/documentation/'
        }, ret)

if __name__ == '__main__':
    print("Stallion v.%s" % __version__)
    unittest.main()
