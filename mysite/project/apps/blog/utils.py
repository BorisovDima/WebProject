from time import time
from django.utils.text import slugify

def slug_generate(string):
    if len(string) > 55:
        string = '_'.join(string[:55].split()[:-1])
    slug = '%s-%d' % (slugify(string, allow_unicode=True), int(time()))
    return slug