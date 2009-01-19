# Copyright (c) 2008 Joost Cassee
# Licensed under the terms of the MIT License (see LICENSE.txt)

from django.conf import settings
from django.core import urlresolvers
from django.utils import translation
import localeurl
import localeurl.settings
from localeurl import utils

if localeurl.settings.URL_TYPE == 'path_prefix':
    def reverse(viewname, urlconf=None, args=[], kwargs={}, prefix=None):
        locale = utils.supported_language(kwargs.pop('locale',
                translation.get_language()))
        path = django_reverse(viewname, urlconf, args, kwargs, prefix)
        if not settings.USE_I18N:
            return path
        return utils.locale_url(path, locale)

    django_reverse = urlresolvers.reverse
    urlresolvers.reverse = reverse
