import factory
from factory.django import DjangoModelFactory
from users.models import User


class UserFactory(DjangoModelFactory):
    """Construct a user of the system."""

    first_name = factory.Faker("name")
    last_name = factory.Faker("name")
    email = factory.Sequence(lambda n: "user_{0}@tradingbot.com".format(n))
    password = factory.PostGenerationMethodCall("set_password", None)

    class Meta:
        model = User
        django_get_or_create = ("email",)


class AdminFactory(UserFactory):
    """Construct an admin of the system."""

    is_staff = True
