from assets.models import Asset, AssetClass
from django.db.models import QuerySet
from django.utils import timezone


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

    def active(self):
        """
        Return active strategies.

        Strategies are active if:
        * `start_date` is less than or equal to now
        * `end_date` is greater than now
        * The underlying asset has an "active" status
        """
        time_now = timezone.now()
        return self.filter(
            start_date__lte=time_now,
            end_date__gt=time_now,
            asset__status=Asset.ACTIVE,
        )
