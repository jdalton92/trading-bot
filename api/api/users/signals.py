from rest_framework.authtoken.models import Token


def user_post_save(sender, instance, created, **kwargs):
    """
    Handle setup of a new or existing user.

    Create a user token for authentication
    """
    if created:
        Token.objects.create(user=instance)
