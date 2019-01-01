from django.conf import settings
import requests


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
        ip = request.META.get('HTTP_X_REAL_IP')
    return ip


from project.apps.account.models import Profile


def social_user(backend, user, response, *args, **kwargs):
    profile = Profile.objects.filter(bloguser=user)
    if not profile:
        Profile.objects.create(bloguser=user, name=user.username)
        user.is_verified = True
        user.save(update_fields=['is_verified'])