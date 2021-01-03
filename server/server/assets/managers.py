from django.db.models import QuerySet


class BarQuerySet(QuerySet):
    """Custom queryset methods for bars."""

    def visible(self, asset_id):
        """Return visible bars for the given asset."""
        return self.filter(asset__pk=asset_id)
