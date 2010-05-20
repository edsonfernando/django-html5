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
EXP_GOOGLEBOT = re.compile('.* Googlebot.*')
EXP_IE = re.compile('.* MSIE (\d\.\d).*')
PARAM_FORCE_HTML5 = COOKIE_FORCE_HTML5 = 'force_html5'

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

        # Gets user agent (browser notation)
        user_agent = request.META.get('HTTP_USER_AGENT', None)

        # Checks GET param
        if request.GET.get(COOKIE_FORCE_HTML5, None) == '1':
            self.force_html5 = True
            request.supports_html5 = True
        elif request.GET.get(COOKIE_FORCE_HTML5, None) == '0':
            self.force_html5 = False
            request.supports_html5 = False

        # Checks cookie
        elif request.COOKIES.get(PARAM_FORCE_HTML5, None) == '1':
            request.supports_html5 = True
        elif request.COOKIES.get(PARAM_FORCE_HTML5, None) == '0':
            request.supports_html5 = False

        elif not request.supports_html5 and user_agent:
            # Google Chrome 3.0 or higher
            m = EXP_CHROME.match(user_agent)
            if m and int(m.group(1)) >= 3:
                request.supports_html5 = True

            # Mozilla Firefox 3.5 or higher
            m = EXP_FIREFOX.match(user_agent)
            if m and float(m.group(1)) >= 3.5:
                request.supports_html5 = True

            # Apple Safari 4 or higher
            m = EXP_SAFARI.match(user_agent)
            if m and float(m.group(1)) >= 4:
                request.supports_html5 = True

            # Opera or higher
            m = EXP_OPERA.match(user_agent)
            if m and float(m.group(1)) >= 9:
                request.supports_html5 = True

            # Yahoo! Slurp
            m = EXP_YAHOO.match(user_agent)
            if m:
                request.supports_html5 = True

            # GoogleBot
            m = EXP_GOOGLEBOT.match(user_agent)
            if m:
                request.supports_html5 = True

        # Stores in thread locals
        _thread_locals.supports_html5 = request.supports_html5

        # Check if current browser is MS Internet Explorer
        if user_agent:
            m = EXP_IE.match(user_agent)
            request.is_ie = bool(m)
            request.is_bad_ie = bool(m and float(m.group(1)) < 8)
        else:
            request.is_ie = None
            request.is_bad_ie = None

    def process_response(self, request, response):
        # Stores force HTML5 or force old version
        if self.force_html5 == True:
            response.set_cookie(COOKIE_FORCE_HTML5, '1')
        elif self.force_html5 == False:
            response.set_cookie(COOKIE_FORCE_HTML5, '0')

        return response

