import requests
from django.contrib.gis.geoip2 import GeoIP2
from django.conf import settings

def check_google_captcha(req):
    recaptcha_response = req.POST.get('g-recaptcha-response')
    data = {
        'secret': settings.GOOGLE_RECAPTCHA_SECRET_KEY,
        'response': recaptcha_response
    }
    result = requests.post('https://www.google.com/recaptcha/api/siteverify', data=data)
    return result.json()['success']



def handler_ip(request):
    x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
    if x_forwarded_for:
        ip = x_forwarded_for.split(',')[-1].strip()
    else:
        ip = request.META.get('HTTP_X_REAL_IP') or request.META.get('REMOTE_ADDR')
    return ip


def get_geo(request):
    ip = handler_ip(request)
    success = True
    try:
        geo = GeoIP2().country(ip)['country_code']
    except Exception:
        geo = settings.DEFAULT_GEO
        success = False
    return geo, success

def set_geo(user, request):
    geo, stat = get_geo(request)
    user.geo = geo
    user.save(update_fields=['geo'])


def social_user(backend, user, response, *args, **kwargs):
    if not user.is_verified:
        set_geo(user, kwargs['request'])
        user.is_verified = True
        user.save(update_fields=['is_verified'])



