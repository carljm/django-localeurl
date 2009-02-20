=========
Changelog
=========

Repository:
  * Changed to plugin architecture.
  * Changed chlocale tag to strip prefix of locale-independent paths.
  * Moved the monkey-patching of urlresolvers.reverse to models.py.
  * Removed ``REDIRECT_LOCALE_INDEPENDENT_PATHS`` settings option; this is now the default.
  * Added Artiom Diomin as a maintainer.

Release 1.2 (2008-11-26):
  * Moved the documentation into the source tree. (Based on `a blog post`_ by Andi Albrecht.)

Release 1.1 (2008-11-20):
  * Added the ``PREFIX_DEFAULT_LANGUAGE`` settings option contributed by Jonas Christian.
  * Added ``REDIRECT_LOCALE_INDEPENDENT_PATHS`` settings option.
  * Added Django 1.0 or higher as a prerequisite.

Release 1.0 (2008-08-10):
  * Added Django 1.0-alpha or higher as a prerequisite.
  * Added setup.py.
  * Fixed problems with empty MEDIA_URL.

Release 0.9 (2008-06-10):
  * Moved to Google Code.

.. _`a blog post`: http://andialbrecht.blogspot.com/2008/10/google-code-sphinx-theme.html


Credits
-------

localeurl is developed by `Joost Cassee`_ and `Artiom Diomin`_ based on the work by Atli Þorbjörnsson. Contributions by Jonas Christian.

It was partly taken from and partly inspired by discussions on the django-users_ and django-multilingual_ mailinglists:
 * Atli Þorbjörnsson: `Locale from URL Middleware`_
 * Panos Laganakos: `creating a multilingual middleware`_
 * Piotr Majewski: `multilingual middleware NEW FEATURE!`_

See also `this blog post on internationalisation`_ by Yann Malet that references Atli's code.

The announcement of localeurl on these lists can be found here:
 * `Announcement on django-users`_
 * `Announcement on django-multilingual`_

.. _`Joost Cassee`: http://joost.cassee.net/
.. _`Artiom Diomin`: http://jabber.linux.md/
.. _django-users: http://groups.google.com/group/django-users
.. _django-multilingual: http://code.google.com/p/django-multilingual/
.. _`Locale from URL Middleware`: http://groups.google.com/group/django-users/browse_thread/thread/7c5508174340191a/8cb2eb93168ef282
.. _`creating a multilingual middleware`: http://groups.google.com/group/django-multilingual/browse_thread/thread/b05fc30232069e1d/3e2e3ef2830cc36a
.. _`multilingual middleware NEW FEATURE!`: http://groups.google.com/group/django-multilingual/browse_thread/thread/6801ea196d2aa2a9/1c8c854c474cb420
.. _`this blog post on internationalisation`: http://yml-blog.blogspot.com/2007/12/django-internationalisation.html
.. _`Announcement on django-users`: http://groups.google.com/group/django-users/browse_thread/thread/413e46ab3517831
.. _`Announcement on django-multilingual`: http://groups.google.com/group/django-multilingual/browse_thread/thread/bb56598b289bd488

