Welcome to the localeurl documentation
======================================

The localeurl Django_ application allow you to specify the language of a page
in the URL.

Suppose you have a Django website in multiple languages. The localeurl
application allow you to specify the language of a page in the URL, like so:
```http://www.example.com/nl/company/profile``. Any URLs without language
prefix will be redirected to add the prefix for the default language.

Some reasons for using localeurl:

  * Search engines will index all languages.
  * Every page should have a unique URL. If you feel that different languages
    means different pages, then each language should get its own unique URL.
  * Setting the language for the website should be done using a POST request
    (because it influences subsequent page views, see `Django ticket #3651`_).
    You might not want to use POST requests.

The localeurl code is licensed under the `MIT License`_. See the
``LICENSE.txt`` file in the distribution.

.. _Django: http://www.djangoproject.com/
.. _`Django ticket #3651`: http://code.djangoproject.com/ticket/3651
.. _`MIT License`: http://www.opensource.org/licenses/mit-license.php


Documentation
-------------

.. toctree::
	:maxdepth: 2

	installation
	usage
	history
