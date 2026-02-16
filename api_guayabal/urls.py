from django.contrib import admin
from django.conf import settings
from django.conf.urls.static import static
from django.urls import path
from django.http import JsonResponse
from rest_framework_simplejwt.views import TokenRefreshView


from app.views import (
    BannerListView,
    CategoryListView,
    LoginView,
    RegisterView,
    ProductListView,
    CartView
)

# 🔹 Vista raíz (opcional pero recomendada)
def home(request):
    return JsonResponse({
        "status": "OK",
        "message": "API Licorería Guayabal funcionando correctamente admin/ register/ login/ token/refresh/ products/ cart/"
    })

urlpatterns = [
    # Ruta raíz
    path('', home),

    # Admin
    path('admin/', admin.site.urls),

    # Autenticación
    path('register/', RegisterView.as_view()),
    path('login/', LoginView.as_view()),
    path('token/refresh/', TokenRefreshView.as_view()),

    # Recursos
    path('banners/', BannerListView.as_view()),
    path('categories/', CategoryListView.as_view()),
    path('products/', ProductListView.as_view()),
    path('cart/', CartView.as_view()),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
