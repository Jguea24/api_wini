from __future__ import annotations  # Habilita anotaciones adelantadas (mejor tipado).

import json  # Serializa datos del dashboard a JSON para los charts.
from datetime import timedelta  # Permite calcular rangos de fechas (ultimos N dias).
from decimal import Decimal  # Tipo Decimal usado por agregaciones monetarias.

from django.contrib.admin import AdminSite  # Base para crear un AdminSite personalizado.
from django.contrib.auth.models import User  # Modelo de usuarios de Django (para conteos).
from django.db.models import Count, DecimalField, IntegerField, Sum, Value  # Agregaciones y tipos/valores para metricas.
from django.db.models.functions import Coalesce, TruncDay  # Funciones ORM (default 0, truncar por dia).
from django.utils import timezone  # Manejo de fechas/horas con zona horaria.

from .models import Order, OrderItem, Product, RoleChangeRequest, Shipment  # Modelos del dominio para el dashboard.


def _to_float(value: Decimal | int | float | None) -> float:  # Convierte Decimal/None a float para JSON.
    if value is None:  # Si no hay valor...
        return 0.0  # ...retorna 0.0 como default.
    return float(value)  # Convierte a float (Decimal -> float).


class DashboardAdminSite(AdminSite):  # AdminSite personalizado con dashboard en el index.
    site_header = "Panel de administracion"  # Titulo mostrado en el header del admin.
    site_title = "Administracion"  # Titulo del sitio (pestana del navegador).
    index_title = "Dashboard"  # Titulo de la pagina principal del admin.
    index_template = "admin/dashboard.html"  # Template custom para el index.
    enable_nav_sidebar = False  # Oculta la barra lateral (deja el dashboard a ancho completo).

    def index(self, request, extra_context=None):  # Renderiza el index con contexto adicional.
        extra_context = extra_context or {}  # Garantiza un dict para inyectar datos.

        now = timezone.now()  # Fecha/hora actual.
        start_dt = now - timedelta(days=13)  # Inicio del rango (incluye hoy = 14 dias).

        users_total = User.objects.count()  # Total de usuarios.
        products_total = Product.objects.count()  # Total de productos.
        orders_total = Order.objects.count()  # Total de pedidos.
        shipments_total = Shipment.objects.count()  # Total de envios.

        pending_role_requests = RoleChangeRequest.objects.filter(status="pending").count()  # Solicitudes de rol pendientes.

        money_field = DecimalField(max_digits=12, decimal_places=2)  # Output field comun para agregaciones monetarias.
        revenue_total = _to_float(  # Total de ingresos (suma de pedidos entregados).
            Order.objects.filter(status="delivered").aggregate(  # Filtra pedidos entregados y agrega suma.
                total=Coalesce(Sum("total_amount"), Value(0, output_field=money_field), output_field=money_field)  # Evita mezclar Decimal con int.
            )["total"]  # Obtiene el total agregado.
        )  # Fin de calculo de ingresos.

        orders_by_status = list(  # Distribucion de pedidos por estado.
            Order.objects.values("status").annotate(count=Count("id")).order_by("status")  # Cuenta por status.
        )  # Fin de consulta.

        shipments_by_status = list(  # Distribucion de envios por estado.
            Shipment.objects.values("status").annotate(count=Count("id")).order_by("status")  # Cuenta por status.
        )  # Fin de consulta.

        revenue_qs = (  # Queryset de ingresos por dia (ultimos 14 dias).
            Order.objects.filter(created_at__gte=start_dt)  # Filtra por rango de fechas.
            .annotate(day=TruncDay("created_at"))  # Trunca a dia.
            .values("day")  # Agrupa por dia.
            .annotate(  # Agrega el total monetario por dia.
                total=Coalesce(Sum("total_amount"), Value(0, output_field=money_field), output_field=money_field)  # Evita tipos mezclados.
            )  # Fin de anotacion.
            .order_by("day")  # Ordena cronologicamente.
        )  # Fin de queryset.

        revenue_by_day_map = {  # Mapa dia->total para completar dias faltantes.
            row["day"].date().isoformat(): _to_float(row["total"]) for row in revenue_qs  # Convierte a {YYYY-MM-DD: float}.
        }  # Fin de mapa.

        day_labels = []  # Labels de dias para el chart.
        day_values = []  # Valores de ingresos para el chart.
        for offset in range(14):  # Itera 14 dias (incluye hoy).
            day = (start_dt.date() + timedelta(days=offset)).isoformat()  # Calcula YYYY-MM-DD.
            day_labels.append(day)  # Agrega label.
            day_values.append(revenue_by_day_map.get(day, 0.0))  # Agrega valor (0 si no hay).

        top_products = list(  # Top productos por unidades vendidas.
            OrderItem.objects.values("product_name")  # Agrupa por nombre guardado en el item.
            .annotate(  # Agrega agregaciones por producto.
                qty=Coalesce(Sum("quantity"), Value(0), output_field=IntegerField()),  # Suma cantidades (default 0).
                total=Coalesce(Sum("subtotal"), Value(0, output_field=money_field), output_field=money_field),  # Suma subtotales monetarios.
            )  # Fin de anotacion.
            .order_by("-qty", "product_name")[:8]  # Ordena por cantidad y limita a 8.
        )  # Fin de top productos.
        for row in top_products:  # Normaliza decimales a float para JSON.
            row["qty"] = int(row.get("qty") or 0)  # Fuerza qty a int.
            row["total"] = _to_float(row.get("total"))  # Fuerza total a float.

        recent_orders = list(  # Ultimos pedidos para tabla rapida.
            Order.objects.select_related("user").order_by("-id")[:10]  # Trae 10 mas recientes.
        )  # Fin de consulta.

        low_stock = list(  # Productos con bajo stock para alerta.
            Product.objects.order_by("stock", "name").filter(stock__lte=5)[:10]  # Top 10 con stock <= 5.
        )  # Fin de consulta.

        dashboard = {  # Payload principal del dashboard (serializable a JSON).
            "counts": {  # Contadores generales.
                "users": users_total,  # Cantidad de usuarios.
                "products": products_total,  # Cantidad de productos.
                "orders": orders_total,  # Cantidad de pedidos.
                "shipments": shipments_total,  # Cantidad de envios.
                "pending_role_requests": pending_role_requests,  # Cantidad de solicitudes de rol pendientes.
            },  # Fin de counts.
            "revenue_total": revenue_total,  # Ingresos totales (delivered).
            "revenue_by_day": {"labels": day_labels, "values": day_values},  # Serie de ingresos por dia.
            "orders_by_status": orders_by_status,  # Conteo por estado de pedido.
            "shipments_by_status": shipments_by_status,  # Conteo por estado de envio.
            "top_products": top_products,  # Top productos por qty.
        }  # Fin de dashboard.

        extra_context["dashboard"] = dashboard  # Expone datos al template.
        extra_context["dashboard_json"] = json.dumps(dashboard)  # Expone JSON (por si se necesita).
        extra_context["recent_orders"] = recent_orders  # Lista de pedidos recientes.
        extra_context["low_stock"] = low_stock  # Lista de productos con bajo stock.

        return super().index(request, extra_context=extra_context)  # Reusa render del admin con contexto extra.


dashboard_site = DashboardAdminSite(name="admin")  # Instancia del admin site con namespace `admin`.
