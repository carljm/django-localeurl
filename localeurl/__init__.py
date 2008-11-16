# Copyright (c) 2008 Joost Cassee
# Licensed under the terms of the MIT License (see LICENSE.txt)

from django.conf import settings

PREFIX_DEFAULT_LOCALE = getattr(settings, "PREFIX_DEFAULT_LOCALE", True)

REDIRECT_LOCALE_INDEPENDENT_PATHS = getattr(settings,
        'REDIRECT_LOCALE_INDEPENDENT_PATHS', False)

LOCALE_INDEPENDENT_PATHS = getattr(settings, 'LOCALE_INDEPENDENT_PATHS', ())
