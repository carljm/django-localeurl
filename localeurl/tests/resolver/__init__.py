import unittest

from localeurl.tests.resolver import test_domain_component
from localeurl.tests.resolver import test_domains
from localeurl.tests.resolver import test_path_prefix

def suite():
    suite = unittest.TestSuite()
    loader = unittest.defaultTestLoader
    suite.addTest(loader.loadTestsFromModule(test_domain_component))
    suite.addTest(loader.loadTestsFromModule(test_domains))
    suite.addTest(loader.loadTestsFromModule(test_path_prefix))
    return suite
