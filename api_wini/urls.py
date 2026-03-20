from django.contrib import admin  # comentario
from django.conf import settings  # comentario
from django.conf.urls.static import static  # comentario
from django.urls import path  # comentario
from django.http import JsonResponse  # comentario
from rest_framework_simplejwt.views import TokenRefreshView  # comentario


from app.views import (  # comentario
    BannerListView,  # comentario
    CartCountView,  # comentario
    ChangePasswordView,  # comentario
    DeliveryAddressDetailView,  # comentario
    DeliveryAddressListCreateView,  # comentario
    GeoAddressValidationView,  # comentario
    GeoAutocompleteView,  # comentario
    GeoGeocodeView,  # comentario
    GeoRouteEstimateView,  # comentario
    CategoryListView,  # comentario
    LoginView,  # comentario
    MeView,  # comentario
    OrderDetailView,  # comentario
    OrderListCreateView,  # comentario
    OrderTrackingAssignDriverView,  # comentario
    OrderTrackingLocationUpdateView,  # comentario
    OrderTrackingView,  # comentario
    RegisterView,  # comentario
    RoleChangeRequestListCreateView,  # comentario
    ProductDetailView,  # comentario
    ProductListView,  # comentario
    CartView  # comentario
)  # comentario

# 🔹 Vista raíz (opcional pero recomendada)
def home(request):  # comentario
    return JsonResponse({  # comentario
        "status": "OK",  # comentario
        "message": " Api de Wini S.A.S funcionando correctamente admin/ register/ login/ token/refresh/ products/ cart/"  # comentario
    })  # comentario

urlpatterns = [  # comentario
    # Ruta raíz
    path('', home),  # comentario

    # Admin
    path('admin/', admin.site.urls),  # comentario

    # Autenticación
    path('register/', RegisterView.as_view()),  # comentario
    path('login/', LoginView.as_view()),  # comentario
    path('token/refresh/', TokenRefreshView.as_view()),  # comentario
    path('me/', MeView.as_view()),  # comentario
    path('me/change-password/', ChangePasswordView.as_view()),  # comentario

    # Recursos
    path('banners/', BannerListView.as_view()),  # comentario
    path('categories/', CategoryListView.as_view()),  # comentario
    path('products/', ProductListView.as_view()),  # comentario
    path('products/<int:pk>/', ProductDetailView.as_view()),  # comentario
    path('cart/count/', CartCountView.as_view()),  # comentario
    path('cart/', CartView.as_view()),  # comentario
    path('orders/', OrderListCreateView.as_view()),  # comentario
    path('orders/<int:pk>/', OrderDetailView.as_view()),  # comentario
    path('orders/<int:pk>/tracking/', OrderTrackingView.as_view()),  # comentario
    path('orders/<int:pk>/tracking/assign-driver/', OrderTrackingAssignDriverView.as_view()),  # comentario
    path('orders/<int:pk>/tracking/location/', OrderTrackingLocationUpdateView.as_view()),  # comentario
    path('addresses/', DeliveryAddressListCreateView.as_view()),  # comentario
    path('addresses/<int:pk>/', DeliveryAddressDetailView.as_view()),  # comentario
    path('role-requests/', RoleChangeRequestListCreateView.as_view()),  # comentario
    path('geo/autocomplete/', GeoAutocompleteView.as_view()),  # comentario
    path('geo/geocode/', GeoGeocodeView.as_view()),  # comentario
    path('geo/validate-address/', GeoAddressValidationView.as_view()),  # comentario
    path('geo/routes/estimate/', GeoRouteEstimateView.as_view()),  # comentario
]  # comentario

if settings.DEBUG:  # comentario
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)  # comentario
