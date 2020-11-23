import factory
from server.users.models import User
from factory.django import DjangoModelFactory


class UserFactory(DjangoModelFactory):
    """Construct a user of the system."""

    name = factory.Faker('name')
    email = factory.Sequence(lambda n: 'user_{0}@tradingbot.com'.format(n))
    password = factory.PostGenerationMethodCall('set_password', None)

    class Meta:  # NOQA
        model = User
        django_get_or_create = ('email',)


class AdminFactory(UserFactory):
    """Construct an admin of the system."""

    is_staff = True
