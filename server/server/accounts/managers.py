from django.db.models import QuerySet


class AccountQuerySet(QuerySet):
    """Custom queryset methods for accounts."""

    def visible(self, user):
        """
        Return visible accounts for the given user.

        If a user is an admin then return all accounts, if a user is not an
        admin then return only their own account.
        """
        if user.is_staff:
            return self.all()
        return self.filter(user=user)
