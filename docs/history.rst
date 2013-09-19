=======
History
=======

Changelog
---------

Release 2.0.1: (2013-09-19)
  * Change canonical documentation links from
    http://pythonhosted.org/django-localeurl/ to
    http://django-localeurl.readthedocs.org

Release 2.0: (2013-09-19)
  * BACKWARDS-INCOMPATIBLE: Drop support for Django 1.0 - 1.2; Python 2.4 and 2.5.
  * Deprecate ``localeurl_future`` tag library, always use new url tag syntax.
  * Try importing ``patterns, url`` first from ``django.conf.urls``; use
    ``django.conf.urls.defaults`` only as Django 1.3 fallback. Fixes #36.
  * Don't try to parse referrer if not present. Fixes #33. Thanks Simon Luijk.
  * Add support for a session-stored locale fallback. Thanks Sylvain Fourmanoit
    for report and draft patch, and Alex Marandon for adding tests. Fixes #23.
  * Make language-code matching case-insensitive, per RFC. Thanks torgeilo for
    the report. Fixes #32.
  * Fix issue with non-ASCII characters in URLs. Thanks Chris Adams.

Release 1.5: (2011-08-24)
  * Added ``LOCALE_REDIRECT_PERMANENT`` setting; defaults to True, if set to
    ``False`` 302 redirects are used rather than 301. Thanks oyvindeh.
  * ``LOCALE_INDEPENDENT_PATHS`` can now be plain string regular expressions,
    they don't have to be compiled regex objects. Fixes #9.
  * Added import of ``localeurl.models`` to ``localeurl.middleware``, to ensure
    that ``reverse`` is monkeypatched before any requests are
    served. Fixes #5. Thanks Antti Kaihola for the report, Andrey Shipilov and
    jefurii for fix confirmation.
  * Added iri_to_uri encoding of non-ASCII redirect URLs. Fixes #13.
  * Sorted language codes longest-first to avoid matching e.g. 'pt' before
    'pt-br'. Fixes #15. Thanks Roman Barczyński for report and draft patch.
  * Added ``LOCALE_INDEPENDENT_STATIC_URL`` setting to mirror
    ``LOCALE_INDEPENDENT_MEDIA_URL``. This setting defaults to True, so if you
    want URLs under STATIC_URL to be locale-dependent, you will need to set it
    to False.
  * Fixed middleware redirection when there is a script
    prefix. Fixes #10. Thanks iro for report and draft patch.
  * Added ``localeurl_future`` template tag library to provide ``locale_url``
    tag that wraps the new Django ``url`` tag to allow using the new syntax and
    avoid deprecation warnings under Django 1.3. Fixes #17. Thanks Fabian
    Büchler for the report.
  * Accounted for reverse() receiving kwargs=None. Fixes #18. Thanks Alexander
    Clausen for report and tests, Joel Ryan for draft patch.
  * Prevented change_locale view from stripping query params from ``next``.
    Fixes #7. Thanks Sverre Johansen.

Release 1.4: (2010-03-19)
  * Moved localeurl settings from localeurl/__init__.py to
    localeurl/settings.py.
  * Added ``LocaleurlSitemap`` for easier creation of multilingual
    sitemaps.
  * Added ``LOCALEURL_USE_ACCEPT_LANGUAGE`` setting to check HTTP
    Accept-Language header before resorting to
    ``settings.LANGUAGE_CODE`` when locale is not specified in URL.
  * Switched to 301 permanent redirects for no-locale URL redirect.
  * Moved to `BitBucket`_ for source code hosting.
  * Added the ``change_locale`` view, contributed by Panos Laganakos.

Release 1.3: (2009-04-06)
  * Changed chlocale tag to strip prefix of locale-independent paths.
  * Moved the monkey-patching of urlresolvers.reverse to models.py.
  * Removed ``REDIRECT_LOCALE_INDEPENDENT_PATHS`` settings option; this is now
    the default.

Release 1.2: (2009-01-19):
  * Moved the documentation into the source tree. (Based on `a blog post`_ by
    Andi Albrecht.)
  * Released version 1.2.

Release 1.1: (2008-11-20):
  * Added the ``PREFIX_DEFAULT_LOCALE`` settings option contributed by Jonas
    Christian.
  * Added ``REDIRECT_LOCALE_INDEPENDENT_PATHS`` settings option.

Release 1.0: (2008-09-10):
  * Added Django 1.0 or higher as a prerequisite.
  * Moved to Google Code.

.. _`BitBucket`: http://www.bitbucket.org/carljm/django-localeurl/
.. _`a blog post`: http://andialbrecht.blogspot.com/2008/10/google-code-sphinx-theme.html

Credits
-------

localeurl was developed by `Joost Cassee`_ based on the work by Atli
Þorbjörnsson. Contributions by Jonas Christian. Includes code from the
`django-localize`_ project by `Artiom Diomin`_. Currently maintained
by `Carl Meyer`_.

It was partly taken from and partly inspired by discussions on the
django-users_ and django-multilingual_ mailinglists:

 * Atli Þorbjörnsson: `Locale from URL Middleware`_
 * Panos Laganakos: `creating a multilingual middleware`_
 * Piotr Majewski: `multilingual middleware NEW FEATURE!`_

See also `this blog post on internationalisation`_ by Yann Malet that
references Atli's code.

The announcement of localeurl on these lists can be found here:
 * `Announcement on django-users`_
 * `Announcement on django-multilingual`_

.. _`Carl Meyer`: http://www.oddbird.net/
.. _`Joost Cassee`: http://joost.cassee.net/
.. _`django-localize`: http://github.com/kron4eg/django-localize/tree/master
.. _`Artiom Diomin`: http://jabber.linux.md/
.. _django-users: http://groups.google.com/group/django-users
.. _django-multilingual: http://code.google.com/p/django-multilingual/
.. _`Locale from URL Middleware`: http://groups.google.com/group/django-users/browse_thread/thread/7c5508174340191a/8cb2eb93168ef282
.. _`creating a multilingual middleware`: http://groups.google.com/group/django-multilingual/browse_thread/thread/b05fc30232069e1d/3e2e3ef2830cc36a
.. _`multilingual middleware NEW FEATURE!`: http://groups.google.com/group/django-multilingual/browse_thread/thread/6801ea196d2aa2a9/1c8c854c474cb420
.. _`this blog post on internationalisation`: http://yml-blog.blogspot.com/2007/12/django-internationalisation.html
.. _`Announcement on django-users`: http://groups.google.com/group/django-users/browse_thread/thread/413e46ab3517831
.. _`Announcement on django-multilingual`: http://groups.google.com/group/django-multilingual/browse_thread/thread/bb56598b289bd488

