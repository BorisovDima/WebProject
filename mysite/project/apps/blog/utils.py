from django.core.cache import cache
from PIL import Image
import os
from io import BytesIO
from django.core.files.base import ContentFile
import logging

logger = logging.getLogger(__name__)

def make_thumbnail(image, size, icon=False, field=None):
    """Make thumbnail."""

    if icon:
        make_thumbnail(image, icon[0], field=icon[1])

    file, ex = os.path.splitext(image.name.lower())
    if ex in ['.jpg', '.jpeg']: thumb_ex = 'JPEG'
    elif ex == 'GIF': thumb_ex = 'GIF'
    else: thumb_ex = 'PNG'

    img = Image.open(image)
    name = file + 'new-' + str(img.width) + '-' + str(img.height) + ex

    img.thumbnail(size, Image.ANTIALIAS)

    fileobj = BytesIO()
    img.save(fileobj, format=thumb_ex)
    fileobj.seek(0)
    getattr(image if not field else field, 'save')(name, ContentFile(fileobj.read()), save=False)
    fileobj.close()



import re
hashtag_pattern = re.compile(r'#([\w-]{0,44})')

def do_hashtags(text):
    """Return hashtags-generator."""
    yield from hashtag_pattern.findall(text)


def delete_cache(key):
    """Delete cache """
    cache.delete(key)
    logger.info('Cache delete key: %s' % key)





