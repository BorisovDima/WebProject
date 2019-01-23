from django.core.management.base import BaseCommand, CommandError
from django.contrib.auth import get_user_model
from project.apps.account.models import Profile

class Command(BaseCommand):
    help = 'Closes the specified poll for voting'

    def add_arguments(self, parser):
        parser.add_argument('password')
        parser.add_argument('name')

    def handle(self,  **options):
        username = options['name']
        pass_ = options['password']
        model = get_user_model()
        try:
            user = model.objects.create_user(username=username)
            user.is_staff = True
            user.is_superuser = True
            user.is_verified = True
            user.set_password(pass_)
            user.save()
        except Exception as er:
            self.stderr.write(str(er))
        else:
            self.stdout.write('Successfully create %s' % user.username)