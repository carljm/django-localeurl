============
Installation
============

This section describes how to install the localeurl application in your Django
project.


Prerequisites
-------------

The localeurl application requires Django_ 1.0 or higher.

.. _Django: http://www.djangoproject.com/download/


Setup
-----

Setup consists of installing the middleware and adding ``'localeurl'``
to the installed applications list.

#. Add ``'localeurl.middleware.LocaleURLMiddleware'`` to
   ``settings.MIDDLEWARE_CLASSES``. It must come *before*
   ``'django.middleware.common.CommonMiddleware'`` or ``settings.APPEND_SLASH``
   will not work. Make sure Django's built-in ``LocaleMiddleware`` is **not**
   in your ``MIDDLEWARE_CLASSES`` setting; ``LocaleURLMiddleware`` replaces it
   and the two will not work together.

#. Add ``'localeurl'`` to ``settings.INSTALLED_APPS``. Because the application
   needs to replace the standard ``urlresolvers.reverse`` function, it is
   important to place it at the top of the list::

     INSTALLED_APPS = (
         'localeurl',
         ...
     )

#. If you want to use the view, include the localeurl URLconf module in your
   project::

     urlpatterns = patterns('',
         ...
         (r'^localeurl/', include('localeurl.urls')),
         ...
     )

#. Make sure ``settings.LANGUAGE_CODE`` or its root language is in
   ``settings.LANGUAGES``. For example, if ``LANGUAGE_CODE == 'en-us'`` then
   ``LANGUAGES`` must contain either ``'en-us'`` or ``'en'``. If you have not
   changed either option you do not have to do anything.


.. _configuration:

Configuration
-------------

The application can be configured by editing the project's ``settings.py``
file.

``LOCALE_INDEPENDENT_PATHS``
  A tuple of regular expressions matching paths that will not be redirected to
  add the language prefix. For example, a site with a language selection splash
  page would add ``'^/$'`` as a locale independent path match.

  Example::

    LOCALE_INDEPENDENT_PATHS = (
        r'^/$',
        r'^/games/',
        r'^/ajax/',
    )

``LOCALE_INDEPENDENT_MEDIA_URL`` (default: ``True``)
  Whether paths starting with ``settings.MEDIA_URL`` (if it is a path, i.e. not
  a full URL) are considered to be locale-independent.

``LOCALE_INDEPENDENT_STATIC_URL`` (default: ``True``)
  Whether paths starting with ``settings.STATIC_URL`` (if it is a path, i.e. not
  a full URL) are considered to be locale-independent.

``PREFIX_DEFAULT_LOCALE`` (default: ``True``)
  Whether to add the prefix for the default language
  (``settings.LANGUAGE_CODE``). For example, if ``LANGUAGE_CODE == 'en'`` then
  the path ``/about/`` will be passed to the URL resolver unchanged and
  ``/en/about/`` will be redirected to ``/about/``.

``LOCALEURL_USE_ACCEPT_LANGUAGE`` (default: ``False``)
  Whether to check the ``Accept-Language`` header from the browser as
  an intermediate fallback in case no locale is specified in the
  URL. (The default behavior, preserved for backwards compatibility,
  is to fallback directly to ``settings.LANGUAGE_CODE``).

``LOCALE_REDIRECT_PERMANENT`` (default: ``True``)
  Whether to use a permanent redirect (301 status code) or temporary
  redirect (302) when redirecting users from the no-locale version of a URL
  to the default locale (or the locale specified in their Accept-Language
  header if ``LOCALEURL_USE_ACCEPT_LANGUAGE`` is True).  If Accept-Language
  is not used, these redirects will never change (as long as the default
  locale never changes), so 301 (the default) is a fine choice.  If you use
  Accept-Language you may want to consider switching this to ``False``, as
  the redirect will then be dependent on the user's Accept-Language header.
