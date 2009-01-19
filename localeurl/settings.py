# Copyright (c) 2008 Joost Cassee
# Licensed under the terms of the MIT License (see LICENSE.txt)

from django.conf import settings

URL_TYPES = ('path_prefix', 'domain_prefix')
URL_TYPE = getattr(settings, 'LOCALE_URL_TYPE', 'path_prefix')
assert URL_TYPE in URL_TYPES, \
        "LOCALE_URL_TYPE must be one of %s" % ', '.join(URL_TYPES)

LOCALE_INDEPENDENT_PATHS = getattr(settings, 'LOCALE_INDEPENDENT_PATHS', ())
assert not (URL_TYPE != 'path_prefix' and LOCALE_INDEPENDENT_PATHS), \
        "LOCALE_INDEPENDENT_PATHS only used with URL_TYPE == 'path_prefix'"

PREFIX_DEFAULT_LOCALE = getattr(settings, "PREFIX_DEFAULT_LOCALE", True)
assert not (URL_TYPE != 'path_prefix' and PREFIX_DEFAULT_LOCALE), \
        "PREFIX_DEFAULT_LOCALE only used with URL_TYPE == 'path_prefix'"
