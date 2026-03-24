from django.db import models
from django.utils import timezone


class CocoaInfo(models.Model):
    product = models.OneToOneField(
        "app.Product",
        on_delete=models.CASCADE,
        related_name="cocoa_info",
    )
    cacao_variety = models.CharField(max_length=120, blank=True)
    origin_country = models.CharField(max_length=120, blank=True)
    origin_region = models.CharField(max_length=120, blank=True)
    farm_name = models.CharField(max_length=160, blank=True)
    fermentation_hours = models.PositiveIntegerField(null=True, blank=True)
    drying_days = models.PositiveIntegerField(null=True, blank=True)
    roasting_profile = models.CharField(max_length=160, blank=True)
    story = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["product_id"]

    def __str__(self):
        return f"Cocoa info - {self.product.name}"


class ChocolateLot(models.Model):
    product = models.ForeignKey(
        "app.Product",
        on_delete=models.CASCADE,
        related_name="lots",
    )
    lot_code = models.CharField(max_length=60, unique=True, db_index=True)
    qr_code = models.CharField(max_length=120, unique=True, db_index=True)
    production_date = models.DateField(null=True, blank=True)
    expiration_date = models.DateField(null=True, blank=True)
    cacao_percentage = models.DecimalField(max_digits=5, decimal_places=2, null=True, blank=True)
    bean_origin = models.CharField(max_length=160, blank=True)
    notes = models.TextField(blank=True)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["-id"]
        indexes = [
            models.Index(fields=["product", "is_active"]),
        ]

    def __str__(self):
        return f"{self.lot_code} - {self.product.name}"


class LotTraceEvent(models.Model):
    lot = models.ForeignKey(
        "app.ChocolateLot",
        on_delete=models.CASCADE,
        related_name="events",
    )
    step = models.CharField(max_length=120)
    status = models.CharField(max_length=40, default="completed")
    event_date = models.DateTimeField(default=timezone.now)
    details = models.TextField(blank=True)
    location = models.CharField(max_length=160, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["event_date", "id"]

    def __str__(self):
        return f"{self.lot.lot_code} - {self.step}"

