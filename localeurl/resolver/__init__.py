 #Copyright (c) 2008-2009 Joost Cassee
# Licensed under the terms of the MIT License (see LICENSE.txt)

from django.core import exceptions
from django.utils.functional import lazy
import localeurl.settings

def load_resolver(resolver_classname):
    try:
        dot = resolver_classname.rindex('.')
    except ValueError:
        raise exceptions.ImproperlyConfigured("%s isn't a resolver module"
                % resolver_classname)
    module_name, class_name = \
            resolver_classname[:dot], resolver_classname[dot+1:]
    try:
        module = __import__(module_name, {}, {}, [''])
    except ImportError, e:
        raise exceptions.ImproperlyConfigured(
                "Error importing middleware %s: '%s'" % (module_name, e))
    try:
        resolver_class = getattr(module, class_name)
    except AttributeError:
        raise exceptions.ImproperlyConfigured(
                "Resolver module '%s' does not define a '%s' class"
                 % (module_name, class_name))
    return resolver_class()

resolver = load_resolver(localeurl.settings.RESOLVER)
