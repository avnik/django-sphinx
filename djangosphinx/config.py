#!/usr/bin/env python

import os, sys, os.path, warnings

# Add the project to the python path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', '..'))

# Set our settings module
if not os.environ.get('DJANGO_SETTINGS_MODULE'):
    raise ValueError('`DJANGO_SETTINGS_MODULE` was not set. Please use DJANGO_SETTINGS_MODULE=project.settings <command> --config sphinx.py.')

from django.conf import settings
from djangosphinx.utils.config import DEFAULT_SPHINX_PARAMS

assert getattr(settings, 'SPHINX_ROOT', None) is not None, "You must specify `SPHINX_ROOT` in your settings."

from django.template import RequestContext

if 'coffin' in settings.INSTALLED_APPS:
    import jinja2
    from coffin.shortcuts import render_to_string as dj_render_to_string
else:
    from django.template.loader import render_to_string as dj_render_to_string
    
def render_to_string(template, context, request=None):
    if request:
        context_instance = RequestContext(request)
    else:
        context_instance = None
    return dj_render_to_string(template, context, context_instance)

def relative_path(*args):
    return os.path.abspath(os.path.join(settings.SPHINX_ROOT, *args))

context = {
    'SPHINX_HOST': getattr(settings, 'SPHINX_HOST', '127.0.0.1'),
    'SPHINX_PORT': getattr(settings, 'SPHINX_PORT', '3312'),
    'relative_path': relative_path,
}
context.update(DEFAULT_SPHINX_PARAMS)

# Old code works with uppercased params
context.update({
    'DATABASE_HOST': DEFAULT_SPHINX_PARAMS['database_host'],
    'DATABASE_PASSWORD': DEFAULT_SPHINX_PARAMS['database_password'],
    'DATABASE_USER': DEFAULT_SPHINX_PARAMS['database_user'],
    'DATABASE_PORT': DEFAULT_SPHINX_PARAMS['database_port'],
    'DATABASE_NAME': DEFAULT_SPHINX_PARAMS['database_name'],
})

def main():
    print render_to_string(getattr(settings, 
        'SPHINX_CONFIG_TEMPLATE', 'conf/sphinx.conf'), context)

if __name__ == '__main__':
    main()
