from django.contrib.auth import get_user_model
from django.db.models import Count

from project.apps.myauth.utils import get_geo

from itertools import chain, islice


def get_user_recommends(user, request, count=7):
    """Return interesting people"""
    model = get_user_model()
    geo, stat = get_geo(request)

    my_subs = model.objects.filter(my_followers__user=user).annotate(sort=Count('my_followers')).order_by('-sort')
    follow = model.objects.filter(subscribe__type='U', subscribe__object_id__in=my_subs.values('id')).exclude(id=user.id)

    users = model.objects.filter(geo=geo) if stat else model.objects.all()
    users = users.annotate(sort=Count('my_followers')).order_by('-sort').exclude(id=user.id)
    objs = chain(follow, users)
    return {'objs': islice(objs, 0, count)}


