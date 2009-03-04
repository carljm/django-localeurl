# Copyright (c) 2008 Joost Cassee
# Licensed under the terms of the MIT License (see LICENSE.txt)

from django.conf import settings
from django.core import urlresolvers
from django.utils import translation
import localeurl
import localeurl.settings
from localeurl.resolver import resolver

if settings.USE_I18N:
    def reverse(viewname, urlconf=None, args=[], kwargs={}, prefix=None):
        return resolver.reverse(django_reverse, viewname, urlconf, args,
                kwargs, prefix)

    django_reverse = urlresolvers.reverse
    urlresolvers.reverse = reverse
