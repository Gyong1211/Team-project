import json

from django.conf import settings
from django.contrib.auth import get_user_model
from django.core.management import BaseCommand

User = get_user_model()


class Command(BaseCommand):
    def handle(self, *args, **options):
        config_secret_common = json.loads(open(settings.CONFIG_SECRET_COMMON_FILE).read())
        email = config_secret_common['django']['default_superuser']['email']
        password = config_secret_common['django']['default_superuser']['password']
        nickname = config_secret_common['django']['default_superuser']['nickname']
        if not User.objects.filter(email=email).exists():
            User.objects.create_superuser(
                email=email,
                password=password,
                nickname=nickname,
            )
            print('Superuser %s created' % email)
        else:
            print('Superuser %s already exist' % email)
