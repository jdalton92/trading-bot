from django.contrib import admin

from .models import Asset, AssetClass, Exchange


class AssetClassAdmin(admin.ModelAdmin):
    search_fields = ['name', 'alt_name']
    list_display = ['name', 'alt_name', 'is_current']


class ExchangeAdmin(admin.ModelAdmin):
    search_fields = ['name', 'alt_name']
    list_display = ['name', 'alt_name', 'is_current']


class AssetAdmin(admin.ModelAdmin):
    fieldsets = (
        ('Asset', {
            'fields': (
                'status', 'name', 'symbol', 'asset_class', 'exchange',
                'tradeable', 'shortable', 'marginable', 'easy_to_borrow'
            )
        }),
    )


admin.site.register(Exchange, ExchangeAdmin)
admin.site.register(Asset, AssetAdmin)
admin.site.register(AssetClass, AssetClassAdmin)
