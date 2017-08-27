from django.core.management.base import BaseCommand
from django.contrib.auth.models import User


class Command(BaseCommand):
    def add_arguments(self, parser):
        parser.add_argument(
            '--user',
            action='store',
            default=None,
            help='Username for new user')

        parser.add_argument(
            '--password',
            action='store',
            default=None,
            help='User Password')

        parser.add_argument(
            '--email',
            action='store',
            default=None,
            help='User Email Address')

    def handle(self, *args, **kwargs):
        # Check user exists
        if User.objects.filter(username=kwargs.get('user')):
            return
        user = User.objects.create_superuser(
            username=kwargs.get('user'),
            email=kwargs.get('email'),
            password=kwargs.get('password').strip(),
            )
        user.save()
