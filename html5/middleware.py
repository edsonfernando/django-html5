import re
from django.conf import settings

EXP_CHROME = re.compile('.* Chrome/(\d)\..*')
EXP_FIREFOX = re.compile('.* Firefox/(\d\.\d)\..*')
EXP_SAFARI = re.compile('.*/(\d+\.\d+)[\.\d]* Safari/.*')
EXP_OPERA = re.compile('^Opera/(\d)\..*')

class HTML5Middleware(object):
    """Detects browser supports HTML5 features and sets a boolean attribute 'Request.supports_html5'.
    
    This is based on http://caniuse.com/
    
    Only browsers with 70% or more set True to that attribute."""

    def process_request(self, request):
        # Default is False
        request.supports_html5 = False

        # Google Chrome 3.0 or higher
        m = EXP_CHROME.match(request.META['HTTP_USER_AGENT'])
        if m and int(m.group(1)) >= 3:
            request.supports_html5 = True

        # Mozilla Firefox 3.5 or higher
        m = EXP_FIREFOX.match(request.META['HTTP_USER_AGENT'])
        if m and float(m.group(1)) >= 3.5:
            request.supports_html5 = True

        # Apple Safari 4 or higher
        m = EXP_SAFARI.match(request.META['HTTP_USER_AGENT'])
        if m and float(m.group(1)) >= 4:
            request.supports_html5 = True

        # Opera or higher
        m = EXP_OPERA.match(request.META['HTTP_USER_AGENT'])
        if m and float(m.group(1)) >= 10:
            request.supports_html5 = True

        # Just to debug
        #if not request.supports_html5:
        #    raise Exception(request.META)
