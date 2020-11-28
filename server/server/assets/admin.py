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
                'id', 'status', 'name', 'symbol', 'asset_class', 'exchange',
                'tradable', 'shortable', 'marginable', 'easy_to_borrow'
            )
        }),
    )
    list_display = ('symbol', 'name', 'asset_class', 'exchange')
    readonly_fields = ['id', ]


admin.site.register(Exchange, ExchangeAdmin)
admin.site.register(Asset, AssetAdmin)
admin.site.register(AssetClass, AssetClassAdmin)
