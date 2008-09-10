# Copyright (c) 2008 Joost Cassee
# Licensed under the terms of the MIT License (see LICENSE.txt)

from django.conf import settings

LOCALE_INDEPENDENT_PATHS = getattr(settings, 'LOCALE_INDEPENDENT_PATHS', ())

def is_locale_independent(path):
    """
    Returns whether the path is locale-independent.

    A path is independent if it starts with MEDIA_URL or it is matched by any
    pattern from LOCALE_INDEPENDENT_PATHS.
    """
    if settings.MEDIA_URL and path.startswith(settings.MEDIA_URL):
        return True
    for path_re in LOCALE_INDEPENDENT_PATHS:
        if path_re.search(path):
            return True
    return False

def strip_locale_prefix(path):
    """
    Returns the path without the locale prefix. If the path does not begin
    with a locale it is returned without change.
    """
    for lang in settings.LANGUAGES:
        locale = '/' + lang[0] + '/'
        if path.startswith(locale):
            return path[len(locale)-1:]
    return path
