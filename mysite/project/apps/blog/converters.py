from .models import Thread

class CategoryConverter:
    regex = '\w+'

    def to_python(self, value):
        if not bool(Thread.objects.filter(name=value)): raise ValueError
        return str(value)

    def to_url(self, value):
        return str(value)

