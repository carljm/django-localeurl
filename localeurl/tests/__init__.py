def suite():
    import doctest
    import unittest
    from localeurl.tests import resolver
    from localeurl.tests import test_middleware

    suite = unittest.TestSuite()
    loader = unittest.defaultTestLoader
#    suite.addTest(doctest.DocTestSuite(doctests))
    suite.addTests(resolver.suite())
    suite.addTest(loader.loadTestsFromModule(test_middleware))
    return suite
