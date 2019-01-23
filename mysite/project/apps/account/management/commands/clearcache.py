from django.core.management.base import BaseCommand, CommandError
from django.core.cache import cache

class Command(BaseCommand):


    def handle(self,  **options):
        try:
            cache.clear()
        except Exception as er:
            self.stderr.write(str(er))
        else:
            self.stdout.write('Successfully cleaned cache!')