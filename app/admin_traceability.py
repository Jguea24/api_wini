from django.contrib import admin

from .admin_site import dashboard_site
from .models import ChocolateLot, CocoaInfo, LotTraceEvent


class LotTraceEventInline(admin.TabularInline):
    model = LotTraceEvent
    extra = 0
    fields = ("step", "status", "event_date", "location", "details")
    ordering = ("event_date", "id")


@admin.register(CocoaInfo, site=dashboard_site)
class CocoaInfoAdmin(admin.ModelAdmin):
    list_display = (
        "product",
        "cacao_variety",
        "origin_country",
        "origin_region",
        "farm_name",
    )
    search_fields = ("product__name", "cacao_variety", "origin_country", "origin_region", "farm_name")


@admin.register(ChocolateLot, site=dashboard_site)
class ChocolateLotAdmin(admin.ModelAdmin):
    list_display = (
        "lot_code",
        "qr_code",
        "product",
        "cacao_percentage",
        "bean_origin",
        "is_active",
        "production_date",
        "expiration_date",
    )
    list_filter = ("is_active", "production_date", "expiration_date", "product")
    search_fields = ("lot_code", "qr_code", "product__name", "bean_origin")
    inlines = (LotTraceEventInline,)


@admin.register(LotTraceEvent, site=dashboard_site)
class LotTraceEventAdmin(admin.ModelAdmin):
    list_display = ("lot", "step", "status", "event_date", "location")
    list_filter = ("status", "event_date")
    search_fields = ("lot__lot_code", "step", "location", "details")

