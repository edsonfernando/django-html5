from django.template import loader, TemplateDoesNotExist

from middleware import current_request_supports_html5

old_find_template = loader.find_template

def find_template(name, dirs=None):
    """This monkey patch forces Django template finder to search for templates with
    extension '.html5' before '.html'."""

    if name.endswith('.html') and current_request_supports_html5():
        try:
            return old_find_template(name+'5', dirs)
        except TemplateDoesNotExist:
            pass

    return old_find_template(name, dirs)
loader.find_template = find_template

