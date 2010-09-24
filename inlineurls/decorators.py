# Copyright (c) 2009-2010, Tyler G. Hicks-Wright
# All rights reserved.
#
# Redistribution and use in source and binary forms, with or without
# modification, are permitted provided that the following conditions are met:
#
# * Redistributions of source code must retain the above copyright notice, this
#   list of conditions and the following disclaimer.
# * Redistributions in binary form must reproduce the above copyright notice,
#   this list of conditions and the following disclaimer in the documentation
#   and/or other materials provided with the distribution.

import sys

from django.shortcuts import render_to_response
from django.conf.urls.defaults import patterns
from django.conf.urls.defaults import url as _url
from django.template import RequestContext
from django.contrib.auth.decorators import login_required
from django.utils.functional import wraps

def _get_module():
    caller = sys._getframe(2).f_code.co_filename
    for m in sys.modules.values():
        if m and '__file__' in m.__dict__ and m.__file__.startswith(caller):
            return m

def view(routes, template=None, login=False, **url_kwargs):
    if isinstance(template, bool) and not login:
        # Some JS-inspired flexible parameters.
        login = template
        template = None
    if isinstance(routes, basestring):
        # Likewise, we allow one route or multiple routes.
        routes = [routes]
    module = _get_module()
    package = module.__package__.split('.')[-1]

    def _wrapper(func):
        if login:
            # Add the @login_required decorator.
            func = login_required(func)

        @wraps(func)
        def _handle_request(request, *args, **kwargs):
            result = func(request, *args, **kwargs) or dict()
            if template and isinstance(result, dict):
                # We received a context and we have a template. Render!
                return render_to_response('%s/%s' % (package, template), RequestContext(request, result))
            else:
                return result 
        if module:
            if 'urlpatterns' not in module.__dict__:
                module.urlpatterns = []
            url_kwargs.setdefault('name', func.func_name)
            for route in routes:
                module.urlpatterns += patterns('', _url(route, _handle_request, **url_kwargs))
        return _handle_request
    return _wrapper

