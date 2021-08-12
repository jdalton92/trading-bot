import uuid

from django.contrib import admin

from .models import Asset, AssetClass, Bar, Exchange


class AssetClassAdmin(admin.ModelAdmin):
    search_fields = ["name", "alt_name"]
    list_display = ["name", "alt_name", "is_active"]


class ExchangeAdmin(admin.ModelAdmin):
    search_fields = ["name", "alt_name"]
    list_display = ["name", "alt_name", "is_active"]


class AssetAdmin(admin.ModelAdmin):
    fieldsets = (
        (
            "Asset",
            {
                "fields": (
                    "id",
                    "status",
                    "name",
                    "symbol",
                    "asset_class",
                    "exchange",
                    "tradable",
                    "shortable",
                    "marginable",
                    "easy_to_borrow",
                )
            },
        ),
    )
    list_display = ("symbol", "name", "asset_class", "exchange")
    readonly_fields = [
        "id",
    ]

    def save_model(self, request, obj, form, change):
        """Add UUID if saving through admin."""
        obj.id = uuid.uuid4()
        super().save_model(request, obj, form, change)


admin.site.register(Exchange, ExchangeAdmin)
admin.site.register(Asset, AssetAdmin)
admin.site.register(AssetClass, AssetClassAdmin)
admin.site.register(Bar)
