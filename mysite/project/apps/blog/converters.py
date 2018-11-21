from .models import Category

class CategoryConverter:
    regex = '\w+'

    def to_python(self, value):
        if not bool(Category.objects.filter(name=value)): raise ValueError
        return str(value)

    def to_url(self, value):
        return str(value)

