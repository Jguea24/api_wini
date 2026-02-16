from rest_framework import generics, permissions
from rest_framework.parsers import FormParser, JSONParser, MultiPartParser
from django.contrib.auth.models import User
from django.db.models import Q
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_simplejwt.tokens import RefreshToken
from django.core.exceptions import ObjectDoesNotExist

from .models import Banner, Category, Product, Cart
from .serializers import BannerSerializer, CategorySerializer, ProductSerializer, CartSerializer, RegisterSerializer


class RegisterView(generics.CreateAPIView):
    queryset = User.objects.all()
    serializer_class = RegisterSerializer
    permission_classes = [permissions.AllowAny]


class LoginView(APIView):
    permission_classes = [permissions.AllowAny]

    def post(self, request):
        identifier = (
            request.data.get('username')
            or request.data.get('email')
            or request.data.get('identifier')
            or ''
        ).strip()
        password = request.data.get('password') or ''

        if not identifier or not password:
            return Response({'error': 'Debes enviar email/username y password.'}, status=400)

        user = User.objects.filter(
            Q(username__iexact=identifier) | Q(email__iexact=identifier)
        ).first()

        if not user:
            return Response({'error': 'Usuario no existe'}, status=400)

        if not user.check_password(password):
            return Response({'error': 'Credenciales invalidas'}, status=400)

        refresh = RefreshToken.for_user(user)
        phone = ''
        address = ''
        try:
            phone = user.profile.phone
            address = user.profile.address
        except ObjectDoesNotExist:
            phone = ''
            address = ''

        return Response({
            'access': str(refresh.access_token),
            'refresh': str(refresh),
            'user': {
                'id': user.id,
                'username': user.username,
                'email': user.email,
                'full_name': f'{user.first_name} {user.last_name}'.strip(),
                'phone': phone,
                'address': address
            }
        })


class ProductListView(generics.ListCreateAPIView):
    queryset = Product.objects.select_related('category').all()
    serializer_class = ProductSerializer
    permission_classes = [permissions.AllowAny]
    parser_classes = [MultiPartParser, FormParser, JSONParser]

    def get_queryset(self):
        queryset = super().get_queryset()
        category_id = (self.request.query_params.get('category_id') or '').strip()
        category_name = (self.request.query_params.get('category') or '').strip()

        if category_id.isdigit():
            if int(category_id) == 0:
                return queryset
            return queryset.filter(category_id=int(category_id))

        if category_name and category_name.lower() not in {'todos', 'all'}:
            return queryset.filter(category__name__iexact=category_name)

        return queryset


class CategoryListView(generics.ListAPIView):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    permission_classes = [permissions.AllowAny]

    def list(self, request, *args, **kwargs):
        response = super().list(request, *args, **kwargs)
        response.data = [{
            'id': 0,
            'name': 'Todos',
            'order': 0,
            'image': '',
            'image_url': '',
        }] + list(response.data)
        return response


class BannerListView(generics.ListAPIView):
    serializer_class = BannerSerializer
    permission_classes = [permissions.AllowAny]

    def get_queryset(self):
        return Banner.objects.filter(is_active=True).order_by('order', 'id')


class CartView(generics.ListCreateAPIView):
    serializer_class = CartSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return Cart.objects.filter(user=self.request.user)

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)
