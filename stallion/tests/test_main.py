import pkg_resources as _pkg_resources
from xmlrpc.client import ServerProxy
import unittest
import sys
sys.path.insert(0, '.')
from stallion import main



class TestMain(unittest.TestCase):

    def test_crumb_params_true(self):
        crumb = main.Crumb(title='TestCrumb',
                           href='#testcrumb')
        self.assertEqual(crumb.title, 'TestCrumb')
        self.assertEqual(crumb.href, '#testcrumb')

    def test_pypi_proxy_instance_true(self):
        proxy = main.get_pypi_proxy()
        self.assertTrue(isinstance(proxy, ServerProxy))

    def test_get_shared_data_instance_true(self):
        data = main.get_shared_data()
        self.assertTrue(isinstance(data, dict))
        self.assertEqual(sorted(data.keys()), ['distributions', 'pypi_update_cache'])

    def test_get_pkg_res_instance_true(self):
        pkg = main.get_pkg_res()
        self.assertEqual(pkg, _pkg_resources)
