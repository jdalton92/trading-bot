from django.db.models import QuerySet


class StrategyQuerySet(QuerySet):
    """Custom queryset methods for strategies."""

    def visible(self, user):
        """
        Return visible strategies for the given user.

        If a user is an admin then return all strategies, if a user is not an
        admin then return only their own strategy.
        """
        if user.is_staff:
            return self.all()
        return self.filter(user=user)
