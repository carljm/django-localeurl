#!/usr/bin/env python

from os.path import dirname, abspath
import sys

import django
from django.conf import settings


if not settings.configured:
    settings.configure(
        INSTALLED_APPS=(
            'localeurl',
            'localeurl.tests',
            'django.contrib.sites', # for sitemap test
            'django.contrib.sessions', # for USE_SESSION
        ),
        DATABASES={
            "default": {
                "ENGINE": "django.db.backends.sqlite3"
            }
        },
        ROOT_URLCONF='localeurl.tests.test_urls',
        SITE_ID=1,
    )


if django.VERSION >= (1, 7):
    django.setup()


def runtests(*test_args):
    parent = dirname(abspath(__file__))
    sys.path.insert(0, parent)
    try:
        from django.test.runner import DiscoverRunner

        def run_tests(test_args, verbosity, interactive):
            runner = DiscoverRunner(
                verbosity=verbosity, interactive=interactive, failfast=False)
            return runner.run_tests(test_args)
    except ImportError:
        if not test_args:
            test_args = ['tests']
        try:
            from django.test.simple import DjangoTestSuiteRunner

            def run_tests(test_args, verbosity, interactive):
                runner = DjangoTestSuiteRunner(
                    verbosity=verbosity, interactive=interactive, failfast=False)
                return runner.run_tests(test_args)
        except ImportError:
            from django.test.simple import run_tests
    failures = run_tests(
        test_args, verbosity=1, interactive=True)
    sys.exit(failures)


if __name__ == '__main__':
    runtests(*sys.argv[1:])
