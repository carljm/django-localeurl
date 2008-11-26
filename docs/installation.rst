============
Installation
============

This section describes how to install the localeurl application in your Django application.

Prerequisites
-------------

The localeurl application requires **Django 1.0** or higher.

Installation
------------

Installation basically consists of installing the middleware. If you want to use the template tags and filters also add localeurl to the installed applications.

#. Place the ``localeurl`` module in your Python path. You could put it into your Django project directory or run ``python setup.py install`` from a shell.)

#. Add ``'localeurl.middleware.LocaleURLMiddleware'`` to ``settings.MIDDLEWARE_CLASSES``. It must come *after* ``'django.middleware.locale.LocaleMiddleware'`` if you want to use HTTP language negotiation as a fall-back language discovery mechanism. Also, it must come *before* ``'django.middleware.common.CommonMiddleware'`` or ``settings.APPEND_SLASH`` will not work.

#. Add ``'localeurl'`` to ``settings.INSTALLED_APPS``.

#. Make sure ``settings.LANGUAGE_CODE`` or its root language is in ``settings.LANGUAGES``. For example, if ``LANGUAGE_CODE == 'en-us'`` then ``LANGUAGES`` must contain either ``'en-us'`` or ``'en'``. If you have not changed either option you do not have to do anything.
  
.. _`the latest release`: http://code.google.com/p/django-localeurl/downloads/list/|release|

Configuration
-------------

The application can be configured by editing the project's ``settings.py`` file.

``LOCALE_INDEPENDENT_PATHS``
  A tuple of regular expression objects matching paths that will not be redirected to add the language prefix. For example, a site with a language selection splash page would add ``'^/$'`` as a locale independent path match. Note that for performance reasons you must use ``re`` objects, not strings. Additionally, any path starting with ``settings.MEDIA_URL`` will also not be redirected. This only works if it is a path, i.e. not a full URL.

Example::

  import re
  LOCALE_INDEPENDENT_PATHS = (
      re.compile('^/$'),
      re.compile('^/games/'),
      re.compile('^/ajax/'),
  )

``REDIRECT_LOCALE_INDEPENDENT_PATHS`` (default: ``False``)
  Whether a locale independent path that is accessed with a locale prefix will be redirected to the same path without the prefix. In the previous example, a request for ``/de/games/pacman/`` would automatically be redirected to ``/games/pacman/``.

``PREFIX_DEFAULT_LANGUAGE`` (default: ``True``)
  Whether to add the prefix for the default language (``settings.LANGUAGE_CODE``). For example, if ``LANGUAGE_CODE == 'en'`` then the path ``/about/`` will be passed to the URL resolver unchanged and ``/en/about/`` will be redirected to ``/about/``.

