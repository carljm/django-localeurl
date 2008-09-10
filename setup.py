from distutils.core import setup

setup(
    name = "django-localeurl",
    version = "DEV",

    packages = ['localeurl', 'localeurl.templatetags'],
    package_data = {'localeurl': ['*.txt']},

    author = "Joost Cassee",
    author_email = "joost@cassee.net",
    description = "A Django application that allow you to specify the language of a page in the URL.",
    long_description = \
"""
Suppose you have a Django website in multiple languages. The localeurl
application allow you to specify the language of a page in the URL, like so:
`http://www.example.com/nl/company/profile`. Any URLs without language prefix
will be redirected to add the prefix for the default language.

Some reasons for using localeurl:

* Search engines will index all languages.
* Every page should have a unique URL. If you feel that different languages
  means different pages, then each language should get its own unique URL.
* Setting the language for the website should be done using a POST request
  (because it influences subsequent page views, see `Django ticket #3651`_).
  You might not want to use POST requests.

.. _Django ticket #3651: http://code.djangoproject.com/ticket/3651
""",
    license = "MIT License",
    keywords = "django i18n",
    classifiers=[
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
    url = "http://code.google.com/p/django-localeurl/",
    download_url = "http://django-localeurl.googlecode.com/files/localeurl-1.0.tar.gz",
)
