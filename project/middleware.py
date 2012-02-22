from django.http import HttpResponsePermanentRedirect
from django.conf import settings

class SecureRequiredMiddleware(object):
    def __init__(self):
        self.paths = list(getattr(settings, 'SECURE_REQUIRED_PATHS'))
        extra = []
        for p in self.paths:
            for code, dummy in settings.LANGUAGES:
                l_p = "/%s%s" % (code, p)
                extra.append(l_p)
        self.enabled = self.paths and getattr(settings, 'HTTPS_SUPPORT', True)
        self.paths += extra

    def process_request(self, request):
        return None
        if self.enabled and not request.is_secure():
            for path in self.paths:
                if request.get_full_path().startswith(path):
                    request_url = request.build_absolute_uri(request.get_full_path())
                    secure_url = request_url.replace('http://', 'https://')
                    return HttpResponsePermanentRedirect(secure_url)

        if self.enabled and request.is_secure() and not request.POST:
            not_secured = len([path for path in self.paths if request.get_full_path().startswith(path)]) == 0
            if not_secured:
                request_url = request.build_absolute_uri(request.get_full_path())
                non_secure_url = request_url.replace('https://', 'http://')
                return HttpResponsePermanentRedirect(non_secure_url)

        return None
