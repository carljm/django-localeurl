Welcome to django-localeurl
===========================

The localeurl Django_ application allows you to specify the language
of a page in the URL.

Suppose you have a Django website in multiple languages. Using
localeurl, without modifying your URLconfs, you can have URLs like
this: ``http://www.example.com/nl/company/profile``. Any URLs without
a language prefix will be redirected to add the prefix for the default
language (or, optionally, the language preferred in the user's browser
settings).

Some reasons for using localeurl:

  * Search engines will index all languages.
  * Every page should have a unique URL. If you feel that different languages
    means different pages, then each language should get its own unique URL.
  * If you don't set the language via the URL, setting the language
    for the website should be done using a POST request (because it
    influences subsequent page views, see `Django ticket #3651`_).
    You might prefer a simple link for changing the language, and
    localeurl allows this.

.. _Django: http://www.djangoproject.com/
.. _`Django ticket #3651`: http://code.djangoproject.com/ticket/3651

You can install localeurl with pip_::

    pip install django-localeurl

or install the `in-development version`_::

    pip install django-localeurl==dev

.. _pip: http://pip.openplans.org
.. _`in-development version`: http://bitbucket.org/carljm/django-localeurl/get/tip.gz#egg=django-localeurl-dev

.. comment: split here

The localeurl code is licensed under the `MIT License`_. See the
``LICENSE.txt`` file in the distribution.

.. _`MIT License`: http://www.opensource.org/licenses/mit-license.php


Documentation
-------------

.. toctree::
	:maxdepth: 2

	setup
	usage
	history
