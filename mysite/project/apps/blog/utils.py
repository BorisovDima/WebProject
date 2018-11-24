from time import time
from django.utils.text import slugify

def slug_generate(string):
    if len(string) > 55:
        string = '_'.join(string[:55].split()[:-1])
    slug = '%s-%d' % (slugify(string, allow_unicode=True), int(time()))
    return slug

def replacer(text, count):
    title_sentences = text.split()
    for n, line in enumerate(title_sentences):
        if len(line) > count:
            title_sentences[n] = ''.join([line[i: i + count] + ' '
                                             for i in range(0, len(line), count)]).rstrip()
    return ' '.join(title_sentences)



