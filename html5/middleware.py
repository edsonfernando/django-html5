import re
from django.conf import settings

try:
    from threading import local
except ImportError:
    from django.utils._threading_local import local

EXP_CHROME = re.compile('.* Chrome/(\d)\..*')
EXP_FIREFOX = re.compile('.* Firefox/(\d\.\d)\..*')
EXP_SAFARI = re.compile('.*/(\d+\.\d+)[\.\d]* Safari/.*')
EXP_OPERA = re.compile('^Opera/(\d)\..*')
EXP_YAHOO = re.compile('.* Yahoo.*')
EXP_GOOGLEBOT = re.compile('.* GoogleBot.*')
EXP_IE = re.compile('.* MSIE (\d\.\d).*')

_thread_locals = local()
def current_request_supports_html5():
    return getattr(_thread_locals, 'supports_html5', None)

class HTML5Middleware(object):
    """Detects browser supports HTML5 features and sets a boolean attribute 'Request.supports_html5'.
    
    This is based on http://caniuse.com/
    
    Only browsers with 70% or more set True to that attribute."""

    force_html5 = None

    def process_request(self, request):
        # Default is False
        request.supports_html5 = False

        # Checks cookie
        if not request.supports_html5 and request.COOKIES.get('force_html5', None):
            request.supports_html5 = True

        # Checks GET param
        if request.GET.get('force_html5', False) == '1':
            self.force_html5 = True
            request.supports_html5 = True
        elif request.GET.get('force_html5', False) == '0':
            self.force_html5 = False
            request.supports_html5 = False

        if not request.supports_html5:
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
            if m and float(m.group(1)) >= 9:
                request.supports_html5 = True

            # Yahoo! Slurp
            m = EXP_YAHOO.match(request.META['HTTP_USER_AGENT'])
            if m:
                request.supports_html5 = True

            # GoogleBot
            m = EXP_GOOGLEBOT.match(request.META['HTTP_USER_AGENT'])
            if m:
                request.supports_html5 = True

        # Stores in thread locals
        _thread_locals.supports_html5 = request.supports_html5

        # Check if current browser is MS Internet Explorer
        m = EXP_IE.match(request.META['HTTP_USER_AGENT'])
        request.is_ie = bool(m)
        request.is_bad_ie = bool(m and float(m.group(1)) < 8)

    def process_response(self, request, response):
        # Stores force HTML5 or force old version
        if self.force_html5 == True:
            response.set_cookie('force_html5', '1')
        elif self.force_html5 == False:
            response.delete_cookie('force_html5')

        return response

