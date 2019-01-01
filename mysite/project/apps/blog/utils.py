from time import time
from django.utils.text import slugify
from PIL import Image
import os
from io import BytesIO
from django.core.files.base import ContentFile

def slug_generate(string):
    if len(string) > 55:
        string = '_'.join(string[:55].split()[:-1])
    slug = '%s-%d' % (slugify(string, allow_unicode=True), int(time()))
    return slug

def replacer(text, count, bool_=False):
    flag = False
    title_sentences = text.split()
    for n, line in enumerate(title_sentences):
        if len(line) > count:
            flag = True
            title_sentences[n] = ''.join([line[i: i + count] + ' '
                                                for i in range(0, len(line), count)]).rstrip()

    return ' '.join(title_sentences) if not bool_ else flag




def make_thumbnail(image, size, icon=False):

    file, ex = os.path.splitext(image.name.lower())
    if ex in ['.jpg', '.jpeg']: thumb_ex = 'JPEG'
    elif ex == 'GIF': thumb_ex = 'GIF'
    else: thumb_ex = 'PNG'

    img = Image.open(image)
    name = file + 'new-' + str(img.width) + '-' + str(img.height) + ex

    if icon:
        img_icon = Image.open(image)
        img_icon.thumbnail(icon[0], Image.ANTIALIAS)
        fileobj = BytesIO()
        img_icon.save(fileobj, format=thumb_ex)
        fileobj.seek(0)
        name = 'icon-' + name
        icon[1].save(name, ContentFile(fileobj.read()), save=False)
        fileobj.close()

    name = file + 'new-' + str(img.width) + '-' + str(img.height) + ex
    img.thumbnail(size, Image.ANTIALIAS)

    fileobj = BytesIO()
    img.save(fileobj, format=thumb_ex)
    fileobj.seek(0)

    image.save(name, ContentFile(fileobj.read()), save=False)
    fileobj.close()





import re
hashtag_pattern = re.compile(r'#([\w-]+)')


def do_hashtags(text):
    for hashtag in hashtag_pattern.findall(text):
        if len(hashtag) < 44:
            yield hashtag






