# Copyright (c) 2008 Joost Cassee
# Licensed under the terms of the MIT License (see LICENSE.txt)

from django.conf import settings

RESOLVER = getattr(settings, 'LOCALEURL_RESOLVER',
        'localeurl.resolver.path_prefix.PathPrefixResolver')
