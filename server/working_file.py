import os

import django
from django.conf import settings

os.environ["DJANGO_SETTINGS_MODULE"] = "config.settings"
django.setup()


def main():
    from core.tasks import moving_average
    from users.models import User

    superuser = User.objects.filter(is_superuser=True).first()
    moving_average(superuser)


if __name__ == "__main__":
    main()
