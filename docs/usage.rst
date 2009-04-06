=====
Usage
=====

The localeurl application provides a middleware class that sets
``request.LANGUAGE_CODE`` based on a prefix on the URL path. It stripping off
this language prefix from ``request.path_info`` so that the URLconf modules do
not need to change. Existing applications should work transparently with
localeurl if they follow the usual Django convention of using ``url`` tags in
templates and (and the ``urlresolvers.reverse`` function in Python code) to
generate internal links.

Paths without locale prefix are redirected to the default locale, either from
``request.LANGUAGE_CODE`` (set by a previous language discovery middleware such
as ``django.middleware.locale.LocaleMiddleware``) or from
``settings.LANGUAGE_CODE``. So a request for ``/about/`` would be redirected to
``/fr/about/`` if French is the default language. (This behavior can be changed
using ``settings.PREFIX_DEFAULT_LOCALE``.)

The application adds one template tag and two filters. Add the following at the
top of a template to enable them::

  {% load localeurl_tags %}


The ``locale_url`` tag
----------------------

The localeurl application replaces the ``urlresolvers.reverse`` function to
return locale-specific URLs, so existing templates should not need to be
changed. To manipulate the language on rendered URLs you can use the
``locale_url`` tag. This tag behaves exactly like the standard ``url`` tag,
except you specify a language.

Examples
^^^^^^^^

You can refer to a specific URL in a specified language like this::

  <a href="{% locale_url "de" articles.views.display id=article.id %}">Show article in German</a>


The ``chlocale`` filter
-----------------------

To add or change the locale prefix of a path use ``chlocale``. It takes one
argument: the new locale. If the path is locale-independent any prefix on the
path will be stripped. This is also the case if
``settings.PREFIX_DEFAULT_LOCALE == False`` and the locale argument is the
default locale.

Examples
^^^^^^^^

To change the language of a URL to Dutch::

	Please click <a href="{{ help_url|chlocale:"nl" }}">here</a> for Dutch help.

This filter can be used to allow users to go to a different language version of
the same page. If you have this in your settings file::

	_ = lambda s: s
	LANGUAGES = (
	    ('en', _(u'English')),
	    ('nl', _(u'Nederlands')),
	    ('de', _(u'Deutsch')),
	    ('fr', _(u'Français')),
	)
	TEMPLATE_CONTEXT_PROCESSORS = (
	    'django.core.context_processors.request',
	    ...
	)

... then you can add a language selection menu in templates like this::

	{% for lang in LANGUAGES %}
		{% ifequal lang.0 LANGUAGE_CODE %}
		    <li class="selected">{{ lang.1 }}</li>
		{% else %}
		    <li><a href="{{ request.path|chlocale:lang.0 }}">{{ lang.1 }}</a></li>
		{% endifequal %}
	{% endfor %}

The ``rmlocale`` filter
-----------------------

You can use the ``rmlocale`` filter to remove the locale prefix from a path. It
takes no arguments.

Examples
^^^^^^^^

To remove the language prefix for a URL:

	The language-independent URL for this page is <tt>{{ request.path|rmlocale }}</tt>.
