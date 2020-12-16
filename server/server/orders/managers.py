from django.db.models import QuerySet


class OrderQuerySet(QuerySet):
    """Custom queryset methods for orders."""

    def visible(self, user):
        """
        Return visible orders for the given user.

        If a user is an admin then return all orders, if a user is not an admin
        then return only their own orders.
        """
        if user.is_staff:
            return self.all()
        return self.filter(user=user)
