============
Installation
============

This section describes how to install the localeurl application in your Django project.


Prerequisites
-------------

The localeurl application requires Django_ 1.0 or higher.

.. _Django: http://www.djangoproject.com/download/


Installation
------------

Installation basically consists of installing the middleware. If you want to
use the template tags and filters also add localeurl to the installed
applications.

#. Place the ``localeurl`` module in your Python path. You can put it into your
   Django project directory or run ``python setup.py install`` from a shell.

#. Add ``'localeurl.middleware.LocaleURLMiddleware'`` to
   ``settings.MIDDLEWARE_CLASSES``. It must come *before*
   ``'django.middleware.common.CommonMiddleware'`` or ``settings.APPEND_SLASH``
   will not work.

#. Add ``'localeurl'`` to ``settings.INSTALLED_APPS``.

#. Make sure ``settings.LANGUAGE_CODE`` or its root language is in
   ``settings.LANGUAGES``. For example, if ``LANGUAGE_CODE == 'en-us'`` then
   ``LANGUAGES`` must contain either ``'en-us'`` or ``'en'``. If you have not
   changed either option you do not have to do anything.


.. _configuration:

Configuration
-------------

The application can be configured by editing the project's ``settings.py``
file. How the locale is derived from the URL depends on the resolver that is
used. The resolver is configured using the ``LOCALEURL_RESOLVER`` settings
option. Resolvers can define their own configuration options.

The following resolvers are available in the localeurl distribution.

Path prefix resolver
^^^^^^^^^^^^^^^^^^^^

``localeurl.resolvers.path_prefix.PathPrefixResolver``

This is the default resolver and expects the locale to be specified as a
prefix to the URL path, i.e. ``http://example.com/<locale>/path/``. The
resolver uses the following settings:

``LOCALE_INDEPENDENT_PATHS``
  A tuple of regular expression objects matching paths that are not prefixed
  by a locale and do not have their locale set. For example, a site with a
  language selection splash page would add ``'^/$'`` as a locale independent
  path match.

  Note that for performance reasons you must use ``re`` objects, not strings.
  Additionally, any path starting with ``settings.MEDIA_URL`` will also not be
  redirected. Obviously, this is only relevant if it is a path, i.e. not a
  full URL.

  Example::

    import re
    LOCALE_INDEPENDENT_PATHS = (
        re.compile('^/$'),
        re.compile('^/games/'),
        re.compile('^/ajax/'),
    )

``PREFIX_DEFAULT_LANGUAGE`` (default: ``True``)
  Whether to add the prefix for the default language
  (``settings.LANGUAGE_CODE``). For example, if ``LANGUAGE_CODE == 'en'`` then
  the path ``/about/`` will be passed to the URL resolver unchanged, setting
  the locale to ``'en'``, and ``/en/about/`` will be redirected to ``/about/``.

Domain prefix resolver
^^^^^^^^^^^^^^^^^^^^^^

``localeurl.resolver,domain_prefix.DomainPrefixResolver``

This resolver derived the locale from the first component of the domain, i.e.
``http://<locale>.example.com/path/``

Domains resolver
^^^^^^^^^^^^^^^^

``localeurl.resolver,domains.DomainsResolver``

This resolver maps the domain to the locale.

