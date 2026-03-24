from rest_framework import status
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework.views import APIView

from .models import ChocolateLot


def _image_url_for(request, product):
    if not getattr(product, "image", None):
        return ""
    if not product.image:
        return ""
    url = product.image.url
    return request.build_absolute_uri(url)


class TraceabilityByQrView(APIView):
    permission_classes = [AllowAny]
    authentication_classes = []

    def get(self, request, qr_code):
        code = (qr_code or "").strip()
        if not code:
            return Response({"error": "qr_code es requerido."}, status=status.HTTP_400_BAD_REQUEST)

        lot = (
            ChocolateLot.objects.select_related("product", "product__category")
            .prefetch_related("events")
            .filter(qr_code=code, is_active=True)
            .first()
        )
        if not lot:
            lot = (
                ChocolateLot.objects.select_related("product", "product__category")
                .prefetch_related("events")
                .filter(lot_code=code, is_active=True)
                .first()
            )
        if not lot:
            return Response({"error": "No existe trazabilidad para este codigo QR."}, status=status.HTTP_404_NOT_FOUND)

        product = lot.product
        cocoa_info = getattr(product, "cocoa_info", None)

        traceability = [
            {
                "id": event.id,
                "step": event.step,
                "status": event.status,
                "event_date": event.event_date,
                "location": event.location,
                "details": event.details,
            }
            for event in lot.events.all().order_by("event_date", "id")
        ]

        payload = {
            "qr_code": lot.qr_code,
            "lot": {
                "id": lot.id,
                "lot_code": lot.lot_code,
                "production_date": lot.production_date,
                "expiration_date": lot.expiration_date,
                "cacao_percentage": lot.cacao_percentage,
                "bean_origin": lot.bean_origin,
                "notes": lot.notes,
            },
            "product": {
                "id": product.id,
                "name": product.name,
                "description": product.description,
                "price": product.price,
                "stock": product.stock,
                "image_url": _image_url_for(request, product),
                "category_id": product.category_id,
                "category_name": product.category.name if product.category else "",
            },
            "cocoa_info": {
                "cacao_variety": cocoa_info.cacao_variety,
                "origin_country": cocoa_info.origin_country,
                "origin_region": cocoa_info.origin_region,
                "farm_name": cocoa_info.farm_name,
                "fermentation_hours": cocoa_info.fermentation_hours,
                "drying_days": cocoa_info.drying_days,
                "roasting_profile": cocoa_info.roasting_profile,
                "story": cocoa_info.story,
            }
            if cocoa_info
            else None,
            "traceability": traceability,
        }
        return Response(payload)

