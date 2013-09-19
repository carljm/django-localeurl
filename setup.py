#!/usr/bin/env python
#
# Copyright (c) 2008 Joost Cassee
# Licensed under the terms of the MIT License (see LICENSE.txt)

from setuptools import setup
import metadata

app_name = metadata.name
version = metadata.version

long_description = open('docs/index.rst').read().split('split here', 1)[0] + """

See the `full documentation`_.

.. _`full documentation`: http://django-localeurl.readthedocs.org
"""

setup(
    name = "django-%s" % app_name,
    version = version,

    packages = [app_name, '%s.templatetags' % app_name, '%s.tests' % app_name],

    author = "Joost Cassee",
    author_email = "joost@cassee.net",
    maintainer = "Carl Meyer",
    maintainer_email = "carl@oddbird.net",
    description = "A Django application that allow you to specify the" \
            " language of a page in the URL.",
    long_description = long_description,
    license = "MIT License",
    keywords = "django i18n",
    classifiers = [
        'Development Status :: 5 - Production/Stable',
        'Environment :: Web Environment',
        'Framework :: Django',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Topic :: Software Development :: Libraries :: Application Frameworks',
        'Topic :: Software Development :: Libraries :: Python Modules',
        'Topic :: Software Development :: Localization',
    ],
    url = "http://django-%s.readthedocs.org/" % app_name,
    test_suite = 'runtests.runtests',
)
