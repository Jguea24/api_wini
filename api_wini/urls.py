from django.contrib import admin  # Importa admin desde `django.contrib`.
from django.conf import settings  # Importa settings desde `django.conf`.
from django.conf.urls.static import static  # Importa static desde `django.conf.urls.static`.
from django.urls import path  # Importa path desde `django.urls`.
from django.http import JsonResponse  # Importa JsonResponse desde `django.http`.
from rest_framework_simplejwt.views import TokenRefreshView  # Importa TokenRefreshView desde `rest_framework_simplejwt.views`.


from app.views import (  # Importa ( desde `app.views`.
    BannerListView,  # Referencia `BannerListView` en la estructura/expresion.
    CartCountView,  # Referencia `CartCountView` en la estructura/expresion.
    ChangePasswordView,  # Referencia `ChangePasswordView` en la estructura/expresion.
    DeliveryAddressDetailView,  # Referencia `DeliveryAddressDetailView` en la estructura/expresion.
    DeliveryAddressListCreateView,  # Referencia `DeliveryAddressListCreateView` en la estructura/expresion.
    GeoAddressValidationView,  # Referencia `GeoAddressValidationView` en la estructura/expresion.
    GeoAutocompleteView,  # Referencia `GeoAutocompleteView` en la estructura/expresion.
    GeoGeocodeView,  # Referencia `GeoGeocodeView` en la estructura/expresion.
    GeoRouteEstimateView,  # Referencia `GeoRouteEstimateView` en la estructura/expresion.
    CategoryListView,  # Referencia `CategoryListView` en la estructura/expresion.
    LoginView,  # Referencia `LoginView` en la estructura/expresion.
    MeView,  # Referencia `MeView` en la estructura/expresion.
    OrderDetailView,  # Referencia `OrderDetailView` en la estructura/expresion.
    OrderListCreateView,  # Referencia `OrderListCreateView` en la estructura/expresion.
    OrderTrackingAssignDriverView,  # Referencia `OrderTrackingAssignDriverView` en la estructura/expresion.
    OrderTrackingLocationUpdateView,  # Referencia `OrderTrackingLocationUpdateView` en la estructura/expresion.
    OrderTrackingView,  # Referencia `OrderTrackingView` en la estructura/expresion.
    RegisterView,  # Referencia `RegisterView` en la estructura/expresion.
    RoleChangeRequestListCreateView,  # Referencia `RoleChangeRequestListCreateView` en la estructura/expresion.
    ProductDetailView,  # Referencia `ProductDetailView` en la estructura/expresion.
    ProductListView,  # Referencia `ProductListView` en la estructura/expresion.
    CartView  # Referencia `CartView` en la estructura/expresion.
)  # Cierra el bloque/estructura.

# 🔹 Vista raíz (opcional pero recomendada)
def home(request):  # Define la funcion `home`.
    return JsonResponse({  # Devuelve un valor (`return`).
        "status": "OK",  # Agrega un literal a la estructura.
        "message": " Api de Wini S.A.S funcionando correctamente admin/ register/ login/ token/refresh/ products/ cart/"  # Agrega un literal a la estructura.
    })  # Cierra la estructura.

urlpatterns = [  # Asigna un valor a `urlpatterns`.
    # Ruta raíz
    path('', home),  # Ejecuta `path`.

    # Admin
    path('admin/', admin.site.urls),  # Ejecuta `path`.

    # Autenticación
    path('register/', RegisterView.as_view()),  # Ejecuta `path`.
    path('login/', LoginView.as_view()),  # Ejecuta `path`.
    path('token/refresh/', TokenRefreshView.as_view()),  # Ejecuta `path`.
    path('me/', MeView.as_view()),  # Ejecuta `path`.
    path('me/change-password/', ChangePasswordView.as_view()),  # Ejecuta `path`.

    # Recursos
    path('banners/', BannerListView.as_view()),  # Ejecuta `path`.
    path('categories/', CategoryListView.as_view()),  # Ejecuta `path`.
    path('products/', ProductListView.as_view()),  # Ejecuta `path`.
    path('products/<int:pk>/', ProductDetailView.as_view()),  # Ejecuta `path`.
    path('cart/count/', CartCountView.as_view()),  # Ejecuta `path`.
    path('cart/', CartView.as_view()),  # Ejecuta `path`.
    path('orders/', OrderListCreateView.as_view()),  # Ejecuta `path`.
    path('orders/<int:pk>/', OrderDetailView.as_view()),  # Ejecuta `path`.
    path('orders/<int:pk>/tracking/', OrderTrackingView.as_view()),  # Ejecuta `path`.
    path('orders/<int:pk>/tracking/assign-driver/', OrderTrackingAssignDriverView.as_view()),  # Ejecuta `path`.
    path('orders/<int:pk>/tracking/location/', OrderTrackingLocationUpdateView.as_view()),  # Ejecuta `path`.
    path('addresses/', DeliveryAddressListCreateView.as_view()),  # Ejecuta `path`.
    path('addresses/<int:pk>/', DeliveryAddressDetailView.as_view()),  # Ejecuta `path`.
    path('role-requests/', RoleChangeRequestListCreateView.as_view()),  # Ejecuta `path`.
    path('geo/autocomplete/', GeoAutocompleteView.as_view()),  # Ejecuta `path`.
    path('geo/geocode/', GeoGeocodeView.as_view()),  # Ejecuta `path`.
    path('geo/validate-address/', GeoAddressValidationView.as_view()),  # Ejecuta `path`.
    path('geo/routes/estimate/', GeoRouteEstimateView.as_view()),  # Ejecuta `path`.
]  # Cierra el bloque/estructura.

if settings.DEBUG:  # Evalua la condicion del `if`.
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)  # Actualiza `urlpatterns` con `+=`.
