from django.template import loader, TemplateDoesNotExist

old_find_template = loader.find_template

def find_template(name, dirs=None):
    """This monkey patch forces Django template finder to search for templates with
    extension '.html5' before '.html'."""

    if name.endswith('.html'):
        try:
            return old_find_template(name+'5', dirs)
        except TemplateDoesNotExist:
            pass

    return old_find_template(name, dirs)
loader.find_template = find_template

