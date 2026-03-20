import json  # Importa json.
from decimal import Decimal  # Importa Decimal desde `decimal`.
from urllib.parse import urlencode  # Importa urlencode desde `urllib.parse`.
from urllib.request import Request, urlopen  # Importa Request, urlopen desde `urllib.request`.

from django.conf import settings  # Importa settings desde `django.conf`.
from django.db import transaction  # Importa transaction desde `django.db`.
from django.utils import timezone  # Importa timezone desde `django.utils`.
from rest_framework import generics, permissions, serializers, status  # Importa generics, permissions, serializers, status desde `rest_framework`.
from rest_framework.parsers import FormParser, JSONParser, MultiPartParser  # Importa FormParser, JSONParser, MultiPartParser desde `rest_framework.parsers`.
from django.contrib.auth.models import User  # Importa User desde `django.contrib.auth.models`.
from django.db.models import Count, Min, Q, Sum  # Importa Count, Min, Q, Sum desde `django.db.models`.
from rest_framework.response import Response  # Importa Response desde `rest_framework.response`.
from rest_framework.views import APIView  # Importa APIView desde `rest_framework.views`.
from rest_framework_simplejwt.tokens import RefreshToken  # Importa RefreshToken desde `rest_framework_simplejwt.tokens`.

from .models import (  # Importa ( desde `.models`.
    Banner,  # Referencia `Banner` en la estructura/expresion.
    Category,  # Referencia `Category` en la estructura/expresion.
    Product,  # Referencia `Product` en la estructura/expresion.
    Cart,  # Referencia `Cart` en la estructura/expresion.
    DeliveryAddress,  # Referencia `DeliveryAddress` en la estructura/expresion.
    RoleChangeRequest,  # Referencia `RoleChangeRequest` en la estructura/expresion.
    Order,  # Referencia `Order` en la estructura/expresion.
    OrderItem,  # Referencia `OrderItem` en la estructura/expresion.
    Shipment,  # Referencia `Shipment` en la estructura/expresion.
    ShipmentLocation,  # Referencia `ShipmentLocation` en la estructura/expresion.
)  # Cierra el bloque/estructura.
from .serializers import (  # Importa ( desde `.serializers`.
    BannerSerializer,  # Referencia `BannerSerializer` en la estructura/expresion.
    CategorySerializer,  # Referencia `CategorySerializer` en la estructura/expresion.
    ProductSerializer,  # Referencia `ProductSerializer` en la estructura/expresion.
    CartSerializer,  # Referencia `CartSerializer` en la estructura/expresion.
    RegisterSerializer,  # Referencia `RegisterSerializer` en la estructura/expresion.
    RegisteredUserSerializer,  # Referencia `RegisteredUserSerializer` en la estructura/expresion.
    OrderCreateSerializer,  # Referencia `OrderCreateSerializer` en la estructura/expresion.
    OrderSerializer,  # Referencia `OrderSerializer` en la estructura/expresion.
    ShipmentSerializer,  # Referencia `ShipmentSerializer` en la estructura/expresion.
    ShipmentAssignDriverSerializer,  # Referencia `ShipmentAssignDriverSerializer` en la estructura/expresion.
    ShipmentLocationUpdateSerializer,  # Referencia `ShipmentLocationUpdateSerializer` en la estructura/expresion.
    DeliveryAddressSerializer,  # Referencia `DeliveryAddressSerializer` en la estructura/expresion.
    MeSerializer,  # Referencia `MeSerializer` en la estructura/expresion.
    ChangePasswordSerializer,  # Referencia `ChangePasswordSerializer` en la estructura/expresion.
    RoleChangeRequestSerializer,  # Referencia `RoleChangeRequestSerializer` en la estructura/expresion.
)  # Cierra el bloque/estructura.


class RegisterView(generics.ListCreateAPIView):  # Define la clase `RegisterView`.
    queryset = User.objects.select_related('profile').prefetch_related('groups').order_by('-id')  # Asigna a `queryset` el resultado de `User.objects.select_related`.
    permission_classes = [permissions.AllowAny]  # Asigna un valor a `permission_classes`.

    def get_serializer_class(self):  # Define la funcion `get_serializer_class`.
        if self.request.method == 'GET':  # Evalua la condicion del `if`.
            return RegisteredUserSerializer  # Devuelve un valor (`return`).
        return RegisterSerializer  # Devuelve un valor (`return`).


class LoginView(APIView):  # Define la clase `LoginView`.
    permission_classes = [permissions.AllowAny]  # Asigna un valor a `permission_classes`.

    def post(self, request):  # Define la funcion `post`.
        identifier = (  # Asigna un valor a `identifier`.
            request.data.get('username')  # Ejecuta `request.data.get`.
            or request.data.get('email')  # Continua la expresion con `or`.
            or request.data.get('identifier')  # Continua la expresion con `or`.
            or ''  # Continua la expresion con `or`.
        ).strip()  # Continua el encadenamiento y llama `.strip`.
        password = request.data.get('password') or ''  # Asigna a `password` el resultado de `request.data.get`.

        if not identifier or not password:  # Evalua la condicion del `if`.
            return Response({'error': 'Debes enviar email/username y password.'}, status=400)  # Devuelve un valor (`return`).

        user = User.objects.filter(  # Asigna a `user` el resultado de `User.objects.filter`.
            Q(username__iexact=identifier) | Q(email__iexact=identifier)  # Ejecuta `Q`.
        ).first()  # Continua el encadenamiento y llama `.first`.

        if not user:  # Evalua la condicion del `if`.
            return Response({'error': 'Usuario no existe'}, status=400)  # Devuelve un valor (`return`).

        if not user.check_password(password):  # Evalua la condicion del `if`.
            return Response({'error': 'Credenciales invalidas'}, status=400)  # Devuelve un valor (`return`).

        refresh = RefreshToken.for_user(user)  # Asigna a `refresh` el resultado de `RefreshToken.for_user`.
        user_data = MeSerializer(user).data  # Asigna a `user_data` el resultado de `MeSerializer`.

        return Response({  # Devuelve un valor (`return`).
            'access': str(refresh.access_token),  # Asigna la clave `access` con el resultado de `str`.
            'refresh': str(refresh),  # Asigna la clave `refresh` con el resultado de `str`.
            'user': user_data  # Asigna la clave `user` en un diccionario.
        })  # Cierra la estructura.


class MeView(APIView):  # Define la clase `MeView`.
    permission_classes = [permissions.IsAuthenticated]  # Asigna un valor a `permission_classes`.
    parser_classes = [MultiPartParser, FormParser, JSONParser]  # Asigna un valor a `parser_classes`.

    def get(self, request):  # Define la funcion `get`.
        serializer = MeSerializer(request.user)  # Asigna a `serializer` el resultado de `MeSerializer`.
        return Response(serializer.data)  # Devuelve un valor (`return`).

    def patch(self, request):  # Define la funcion `patch`.
        serializer = MeSerializer(request.user, data=request.data, partial=True)  # Asigna a `serializer` el resultado de `MeSerializer`.
        serializer.is_valid(raise_exception=True)  # Ejecuta `serializer.is_valid`.
        serializer.save()  # Ejecuta `serializer.save`.
        return Response(serializer.data)  # Devuelve un valor (`return`).


class ChangePasswordView(APIView):  # Define la clase `ChangePasswordView`.
    permission_classes = [permissions.IsAuthenticated]  # Asigna un valor a `permission_classes`.

    def post(self, request):  # Define la funcion `post`.
        serializer = ChangePasswordSerializer(data=request.data)  # Asigna a `serializer` el resultado de `ChangePasswordSerializer`.
        serializer.is_valid(raise_exception=True)  # Ejecuta `serializer.is_valid`.

        current_password = serializer.validated_data['current_password']  # Asigna un valor a `current_password`.
        new_password = serializer.validated_data['new_password']  # Asigna un valor a `new_password`.

        if not request.user.check_password(current_password):  # Evalua la condicion del `if`.
            return Response({'error': 'La contrasena actual es incorrecta.'}, status=status.HTTP_400_BAD_REQUEST)  # Devuelve un valor (`return`).

        if request.user.check_password(new_password):  # Evalua la condicion del `if`.
            return Response(  # Devuelve un valor (`return`).
                {'error': 'La nueva contrasena debe ser diferente a la actual.'},  # Define un diccionario literal.
                status=status.HTTP_400_BAD_REQUEST  # Asigna un valor a `status`.
            )  # Cierra el bloque/estructura.

        request.user.set_password(new_password)  # Ejecuta `request.user.set_password`.
        request.user.save(update_fields=['password'])  # Ejecuta `request.user.save`.

        return Response({'message': 'Contrasena actualizada correctamente.'}, status=status.HTTP_200_OK)  # Devuelve un valor (`return`).


class ProductListView(generics.ListCreateAPIView):  # Define la clase `ProductListView`.
    queryset = Product.objects.select_related('category').all()  # Asigna a `queryset` el resultado de `Product.objects.select_related`.
    serializer_class = ProductSerializer  # Asigna un valor a `serializer_class`.
    permission_classes = [permissions.AllowAny]  # Asigna un valor a `permission_classes`.
    parser_classes = [MultiPartParser, FormParser, JSONParser]  # Asigna un valor a `parser_classes`.

    def get_queryset(self):  # Define la funcion `get_queryset`.
        queryset = super().get_queryset()  # Asigna a `queryset` el resultado de `super`.
        category_id = (self.request.query_params.get('category_id') or '').strip()  # Asigna un valor a `category_id`.
        category_name = (self.request.query_params.get('category') or '').strip()  # Asigna un valor a `category_name`.

        if category_id.isdigit():  # Evalua la condicion del `if`.
            if int(category_id) == 0:  # Evalua la condicion del `if`.
                return queryset  # Devuelve un valor (`return`).
            return queryset.filter(category_id=int(category_id))  # Devuelve un valor (`return`).

        if category_name and category_name.lower() not in {'todos', 'all'}:  # Evalua la condicion del `if`.
            return queryset.filter(category__name__iexact=category_name)  # Devuelve un valor (`return`).

        return queryset  # Devuelve un valor (`return`).


class ProductDetailView(generics.RetrieveAPIView):  # Define la clase `ProductDetailView`.
    queryset = Product.objects.select_related('category').all()  # Asigna a `queryset` el resultado de `Product.objects.select_related`.
    serializer_class = ProductSerializer  # Asigna un valor a `serializer_class`.
    permission_classes = [permissions.AllowAny]  # Asigna un valor a `permission_classes`.


class CategoryListView(generics.ListAPIView):  # Define la clase `CategoryListView`.
    queryset = Category.objects.all()  # Asigna a `queryset` el resultado de `Category.objects.all`.
    serializer_class = CategorySerializer  # Asigna un valor a `serializer_class`.
    permission_classes = [permissions.AllowAny]  # Asigna un valor a `permission_classes`.

    def list(self, request, *args, **kwargs):  # Define la funcion `list`.
        response = super().list(request, *args, **kwargs)  # Asigna a `response` el resultado de `super`.
        response.data = [{  # Asigna un valor a `response.data`.
            'id': 0,  # Asigna la clave `id` en un diccionario.
            'name': 'Todos',  # Agrega un literal a la estructura.
            'order': 0,  # Asigna la clave `order` en un diccionario.
            'image': '',  # Agrega un literal a la estructura.
            'image_url': '',  # Agrega un literal a la estructura.
        }] + list(response.data)  # Concatena el elemento inicial con la lista de resultados de la respuesta.
        return response  # Devuelve un valor (`return`).


class BannerListView(generics.ListAPIView):  # Define la clase `BannerListView`.
    serializer_class = BannerSerializer  # Asigna un valor a `serializer_class`.
    permission_classes = [permissions.AllowAny]  # Asigna un valor a `permission_classes`.

    def get_queryset(self):  # Define la funcion `get_queryset`.
        return Banner.objects.filter(is_active=True).order_by('order', 'id')  # Devuelve un valor (`return`).


class CartView(generics.ListCreateAPIView):  # Define la clase `CartView`.
    serializer_class = CartSerializer  # Asigna un valor a `serializer_class`.
    permission_classes = [permissions.IsAuthenticated]  # Asigna un valor a `permission_classes`.

    def get_queryset(self):  # Define la funcion `get_queryset`.
        return Cart.objects.filter(user=self.request.user)  # Devuelve un valor (`return`).

    def perform_create(self, serializer):  # Define la funcion `perform_create`.
        serializer.save(user=self.request.user)  # Ejecuta `serializer.save`.

    def create(self, request, *args, **kwargs):  # Define la funcion `create`.
        serializer = self.get_serializer(data=request.data)  # Asigna a `serializer` el resultado de `self.get_serializer`.
        serializer.is_valid(raise_exception=True)  # Ejecuta `serializer.is_valid`.

        product = serializer.validated_data['product']  # Asigna un valor a `product`.
        quantity = serializer.validated_data.get('quantity', 1)  # Asigna a `quantity` el resultado de `serializer.validated_data.get`.

        cart_item, created = Cart.objects.get_or_create(  # Asigna a `cart_item` y `created` el resultado de `Cart.objects.get_or_create`.
            user=request.user,  # Asigna un valor a `user`.
            product=product,  # Asigna un valor a `product`.
            defaults={'quantity': quantity},  # Asigna un valor a `defaults`.
        )  # Cierra el bloque/estructura.

        if not created:  # Evalua la condicion del `if`.
            cart_item.quantity += quantity  # Actualiza `cart_item.quantity` con `+=`.
            cart_item.save(update_fields=['quantity'])  # Ejecuta `cart_item.save`.

        output_serializer = self.get_serializer(cart_item)  # Asigna a `output_serializer` el resultado de `self.get_serializer`.
        response_status = status.HTTP_201_CREATED if created else status.HTTP_200_OK  # Asigna un valor a `response_status`.

        payload = dict(output_serializer.data)  # Asigna a `payload` el resultado de `dict`.
        payload['message'] = (  # Asigna un valor a `payload['message']`.
            'Producto agregado al carrito'  # Agrega un literal a la estructura.
            if created  # Evalua la condicion del `if`.
            else 'Cantidad del producto actualizada en el carrito'  # Rama `else` del operador ternario.
        )  # Cierra el bloque/estructura.

        return Response(payload, status=response_status)  # Devuelve un valor (`return`).

    def patch(self, request, *args, **kwargs):  # Define la funcion `patch`.
        cart_item_id = (  # Asigna un valor a `cart_item_id`.
            request.data.get('cart_item_id')  # Ejecuta `request.data.get`.
            or request.data.get('id')  # Continua la expresion con `or`.
            or request.query_params.get('cart_item_id')  # Continua la expresion con `or`.
            or request.query_params.get('id')  # Continua la expresion con `or`.
        )  # Cierra el bloque/estructura.
        product_id = (  # Asigna un valor a `product_id`.
            request.data.get('product')  # Ejecuta `request.data.get`.
            or request.data.get('product_id')  # Continua la expresion con `or`.
            or request.query_params.get('product')  # Continua la expresion con `or`.
            or request.query_params.get('product_id')  # Continua la expresion con `or`.
        )  # Cierra el bloque/estructura.
        quantity = request.data.get('quantity', request.data.get('cantidad'))  # Asigna a `quantity` el resultado de `request.data.get`.

        if quantity is None:  # Evalua la condicion del `if`.
            return Response({'error': 'Debes enviar quantity.'}, status=status.HTTP_400_BAD_REQUEST)  # Devuelve un valor (`return`).

        try:  # Inicia un bloque `try`.
            quantity = int(quantity)  # Asigna a `quantity` el resultado de `int`.
        except (TypeError, ValueError):  # Maneja una excepcion en `except`.
            return Response({'error': 'quantity debe ser un numero entero.'}, status=status.HTTP_400_BAD_REQUEST)  # Devuelve un valor (`return`).

        if quantity < 0:  # Evalua la condicion del `if`.
            return Response({'error': 'quantity no puede ser negativo.'}, status=status.HTTP_400_BAD_REQUEST)  # Devuelve un valor (`return`).

        queryset = Cart.objects.filter(user=request.user)  # Asigna a `queryset` el resultado de `Cart.objects.filter`.
        if cart_item_id:  # Evalua la condicion del `if`.
            queryset = queryset.filter(id=cart_item_id)  # Asigna a `queryset` el resultado de `queryset.filter`.
        elif product_id:  # Evalua la condicion del `elif`.
            queryset = queryset.filter(product_id=product_id)  # Asigna a `queryset` el resultado de `queryset.filter`.
        else:  # Ejecuta la rama `else`.
            return Response(  # Devuelve un valor (`return`).
                {'error': 'Debes enviar cart_item_id/id o product/product_id.'},  # Define un diccionario literal.
                status=status.HTTP_400_BAD_REQUEST  # Asigna un valor a `status`.
            )  # Cierra el bloque/estructura.

        cart_item = queryset.first()  # Asigna a `cart_item` el resultado de `queryset.first`.
        if not cart_item:  # Evalua la condicion del `if`.
            return Response({'error': 'Producto no encontrado en el carrito.'}, status=status.HTTP_404_NOT_FOUND)  # Devuelve un valor (`return`).

        if quantity == 0:  # Evalua la condicion del `if`.
            cart_item.delete()  # Ejecuta `cart_item.delete`.
            return Response({'message': 'Producto eliminado del carrito.'}, status=status.HTTP_200_OK)  # Devuelve un valor (`return`).

        cart_item.quantity = quantity  # Asigna un valor a `cart_item.quantity`.
        cart_item.save(update_fields=['quantity'])  # Ejecuta `cart_item.save`.
        output_serializer = self.get_serializer(cart_item)  # Asigna a `output_serializer` el resultado de `self.get_serializer`.
        payload = dict(output_serializer.data)  # Asigna a `payload` el resultado de `dict`.
        payload['message'] = 'Cantidad actualizada en el carrito'  # Asigna un valor a `payload['message']`.
        return Response(payload, status=status.HTTP_200_OK)  # Devuelve un valor (`return`).

    def delete(self, request, *args, **kwargs):  # Define la funcion `delete`.
        cart_item_id = (  # Asigna un valor a `cart_item_id`.
            request.data.get('cart_item_id')  # Ejecuta `request.data.get`.
            or request.data.get('id')  # Continua la expresion con `or`.
            or request.query_params.get('cart_item_id')  # Continua la expresion con `or`.
            or request.query_params.get('id')  # Continua la expresion con `or`.
        )  # Cierra el bloque/estructura.
        product_id = (  # Asigna un valor a `product_id`.
            request.data.get('product')  # Ejecuta `request.data.get`.
            or request.data.get('product_id')  # Continua la expresion con `or`.
            or request.query_params.get('product')  # Continua la expresion con `or`.
            or request.query_params.get('product_id')  # Continua la expresion con `or`.
        )  # Cierra el bloque/estructura.

        queryset = Cart.objects.filter(user=request.user)  # Asigna a `queryset` el resultado de `Cart.objects.filter`.

        if cart_item_id:  # Evalua la condicion del `if`.
            deleted_count, _ = queryset.filter(id=cart_item_id).delete()  # Asigna a `deleted_count` y `_` el resultado de `queryset.filter`.
            if deleted_count == 0:  # Evalua la condicion del `if`.
                return Response({'error': 'Producto no encontrado en el carrito.'}, status=status.HTTP_404_NOT_FOUND)  # Devuelve un valor (`return`).
            return Response(  # Devuelve un valor (`return`).
                {'message': 'Producto eliminado del carrito.', 'deleted': deleted_count},  # Define un diccionario literal.
                status=status.HTTP_200_OK  # Asigna un valor a `status`.
            )  # Cierra el bloque/estructura.

        if product_id:  # Evalua la condicion del `if`.
            deleted_count, _ = queryset.filter(product_id=product_id).delete()  # Asigna a `deleted_count` y `_` el resultado de `queryset.filter`.
            if deleted_count == 0:  # Evalua la condicion del `if`.
                return Response({'error': 'Producto no encontrado en el carrito.'}, status=status.HTTP_404_NOT_FOUND)  # Devuelve un valor (`return`).
            return Response(  # Devuelve un valor (`return`).
                {'message': 'Producto eliminado del carrito.', 'deleted': deleted_count},  # Define un diccionario literal.
                status=status.HTTP_200_OK  # Asigna un valor a `status`.
            )  # Cierra el bloque/estructura.

        deleted_count, _ = queryset.delete()  # Asigna a `deleted_count` y `_` el resultado de `queryset.delete`.
        return Response(  # Devuelve un valor (`return`).
            {'message': 'Carrito vaciado.', 'deleted': deleted_count},  # Define un diccionario literal.
            status=status.HTTP_200_OK  # Asigna un valor a `status`.
        )  # Cierra el bloque/estructura.


class CartCountView(APIView):  # Define la clase `CartCountView`.
    permission_classes = [permissions.IsAuthenticated]  # Asigna un valor a `permission_classes`.

    def get(self, request):  # Define la funcion `get`.
        queryset = Cart.objects.filter(user=request.user)  # Asigna a `queryset` el resultado de `Cart.objects.filter`.
        distinct_items = queryset.count()  # Asigna a `distinct_items` el resultado de `queryset.count`.
        total_quantity = queryset.aggregate(total=Sum('quantity')).get('total') or 0  # Asigna a `total_quantity` el resultado de `queryset.aggregate`.

        return Response({  # Devuelve un valor (`return`).
            'count': int(total_quantity),  # Asigna la clave `count` con el resultado de `int`.
            'distinct_items': distinct_items,  # Asigna la clave `distinct_items` en un diccionario.
        })  # Cierra la estructura.


def pick_auto_driver():  # Define la funcion `pick_auto_driver`.
    group_driver_ids = set(  # Asigna a `group_driver_ids` el resultado de `set`.
        User.objects.filter(  # Ejecuta `User.objects.filter`.
            is_active=True,  # Asigna un valor a `is_active`.
            groups__name__in=['DRIVER', 'REPARTIDOR'],  # Asigna un valor a `groups__name__in`.
        ).values_list('id', flat=True)  # Continua el encadenamiento y llama `.values_list`.
    )  # Cierra el bloque/estructura.
    requested_driver_ids = set(  # Asigna a `requested_driver_ids` el resultado de `set`.
        RoleChangeRequest.objects.filter(  # Ejecuta `RoleChangeRequest.objects.filter`.
            requested_role='driver',  # Asigna un valor a `requested_role`.
            status='approved',  # Asigna un valor a `status`.
            user__is_active=True,  # Asigna un valor a `user__is_active`.
        ).values_list('user_id', flat=True)  # Continua el encadenamiento y llama `.values_list`.
    )  # Cierra el bloque/estructura.
    candidate_ids = group_driver_ids.union(requested_driver_ids)  # Asigna a `candidate_ids` el resultado de `group_driver_ids.union`.
    if not candidate_ids:  # Evalua la condicion del `if`.
        return None  # Devuelve un valor (`return`).

    active_statuses = ['assigned', 'picked_up', 'on_the_way', 'nearby']  # Asigna un valor a `active_statuses`.
    return (  # Devuelve un valor (`return`).
        User.objects.filter(id__in=candidate_ids, is_active=True)  # Ejecuta `User.objects.filter`.
        .annotate(  # Continua el encadenamiento y llama `.annotate`.
            active_shipments=Count(  # Asigna a `active_shipments` el resultado de `Count`.
                'shipments_assigned',  # Agrega un literal a la estructura.
                filter=Q(shipments_assigned__status__in=active_statuses),  # Asigna a `filter` el resultado de `Q`.
                distinct=True,  # Asigna un valor a `distinct`.
            ),  # Cierra el bloque/estructura.
            first_active_shipment_at=Min(  # Asigna a `first_active_shipment_at` el resultado de `Min`.
                'shipments_assigned__created_at',  # Agrega un literal a la estructura.
                filter=Q(shipments_assigned__status__in=active_statuses),  # Asigna a `filter` el resultado de `Q`.
            ),  # Cierra el bloque/estructura.
        )  # Cierra el bloque/estructura.
        .order_by('active_shipments', 'first_active_shipment_at', 'id')  # Continua el encadenamiento y llama `.order_by`.
        .first()  # Continua el encadenamiento y llama `.first`.
    )  # Cierra el bloque/estructura.


class OrderListCreateView(generics.ListCreateAPIView):  # Define la clase `OrderListCreateView`.
    permission_classes = [permissions.IsAuthenticated]  # Asigna un valor a `permission_classes`.

    def get_queryset(self):  # Define la funcion `get_queryset`.
        return (  # Devuelve un valor (`return`).
            Order.objects.filter(user=self.request.user)  # Ejecuta `Order.objects.filter`.
            .select_related('delivery_address')  # Continua el encadenamiento y llama `.select_related`.
            .prefetch_related('items__product')  # Continua el encadenamiento y llama `.prefetch_related`.
        )  # Cierra el bloque/estructura.

    def get_serializer_class(self):  # Define la funcion `get_serializer_class`.
        if self.request.method == 'POST':  # Evalua la condicion del `if`.
            return OrderCreateSerializer  # Devuelve un valor (`return`).
        return OrderSerializer  # Devuelve un valor (`return`).

    def create(self, request, *args, **kwargs):  # Define la funcion `create`.
        input_serializer = self.get_serializer(data=request.data)  # Asigna a `input_serializer` el resultado de `self.get_serializer`.
        input_serializer.is_valid(raise_exception=True)  # Ejecuta `input_serializer.is_valid`.

        user = request.user  # Asigna un valor a `user`.
        with transaction.atomic():  # Abre un contexto con `with`.
            cart_items = list(Cart.objects.select_related('product').filter(user=user))  # Asigna a `cart_items` el resultado de `list`.
            if not cart_items:  # Evalua la condicion del `if`.
                return Response({'error': 'El carrito esta vacio.'}, status=status.HTTP_400_BAD_REQUEST)  # Devuelve un valor (`return`).

            address = input_serializer.validated_data.get('delivery_address')  # Asigna a `address` el resultado de `input_serializer.validated_data.get`.
            if address and address.user_id != user.id:  # Evalua la condicion del `if`.
                return Response(  # Devuelve un valor (`return`).
                    {'error': 'La direccion seleccionada no pertenece al usuario autenticado.'},  # Define un diccionario literal.
                    status=status.HTTP_400_BAD_REQUEST  # Asigna un valor a `status`.
                )  # Cierra el bloque/estructura.

            if address is None:  # Evalua la condicion del `if`.
                address = DeliveryAddress.objects.filter(user=user, is_default=True).first()  # Asigna a `address` el resultado de `DeliveryAddress.objects.filter`.
            if address is None:  # Evalua la condicion del `if`.
                address = DeliveryAddress.objects.filter(user=user).order_by('-id').first()  # Asigna a `address` el resultado de `DeliveryAddress.objects.filter`.
            if address is None:  # Evalua la condicion del `if`.
                return Response(  # Devuelve un valor (`return`).
                    {'error': 'Debes registrar una direccion de entrega antes de crear un pedido.'},  # Define un diccionario literal.
                    status=status.HTTP_400_BAD_REQUEST  # Asigna un valor a `status`.
                )  # Cierra el bloque/estructura.

            product_ids = [item.product_id for item in cart_items]  # Asigna un valor a `product_ids`.
            locked_products = Product.objects.select_for_update().filter(id__in=product_ids)  # Asigna a `locked_products` el resultado de `Product.objects.select_for_update`.
            products_by_id = {product.id: product for product in locked_products}  # Asigna un valor a `products_by_id`.

            stock_errors = []  # Asigna un valor a `stock_errors`.
            for cart_item in cart_items:  # Itera en un bucle `for`.
                product = products_by_id.get(cart_item.product_id)  # Asigna a `product` el resultado de `products_by_id.get`.
                if not product:  # Evalua la condicion del `if`.
                    stock_errors.append({  # Ejecuta `stock_errors.append`.
                        'product_id': cart_item.product_id,  # Asigna la clave `product_id` en un diccionario.
                        'error': 'Producto no encontrado.',  # Agrega un literal a la estructura.
                    })  # Cierra la estructura.
                    continue  # Continua el bucle (`continue`).
                if product.stock < cart_item.quantity:  # Evalua la condicion del `if`.
                    stock_errors.append({  # Ejecuta `stock_errors.append`.
                        'product_id': product.id,  # Asigna la clave `product_id` en un diccionario.
                        'product_name': product.name,  # Asigna la clave `product_name` en un diccionario.
                        'requested': cart_item.quantity,  # Asigna la clave `requested` en un diccionario.
                        'available': product.stock,  # Asigna la clave `available` en un diccionario.
                    })  # Cierra la estructura.

            if stock_errors:  # Evalua la condicion del `if`.
                return Response(  # Devuelve un valor (`return`).
                    {  # Inicia una estructura literal.
                        'error': 'No hay stock suficiente para completar el pedido.',  # Agrega un literal a la estructura.
                        'details': stock_errors,  # Asigna la clave `details` en un diccionario.
                    },  # Cierra el bloque/estructura.
                    status=status.HTTP_400_BAD_REQUEST  # Asigna un valor a `status`.
                )  # Cierra el bloque/estructura.

            order = Order.objects.create(  # Asigna a `order` el resultado de `Order.objects.create`.
                user=user,  # Asigna un valor a `user`.
                delivery_address=address,  # Asigna un valor a `delivery_address`.
                delivery_main_address=address.main_address,  # Asigna un valor a `delivery_main_address`.
                delivery_secondary_street=address.secondary_street,  # Asigna un valor a `delivery_secondary_street`.
                delivery_apartment=address.apartment,  # Asigna un valor a `delivery_apartment`.
                delivery_city=address.city,  # Asigna un valor a `delivery_city`.
                delivery_latitude=getattr(address, 'latitude', None),  # Asigna a `delivery_latitude` el resultado de `getattr`.
                delivery_longitude=getattr(address, 'longitude', None),  # Asigna a `delivery_longitude` el resultado de `getattr`.
                delivery_instructions=address.delivery_instructions,  # Asigna un valor a `delivery_instructions`.
                status='pending',  # Asigna un valor a `status`.
                total_amount=Decimal('0.00'),  # Asigna a `total_amount` el resultado de `Decimal`.
                total_items=0,  # Asigna un valor a `total_items`.
            )  # Cierra el bloque/estructura.
            auto_driver = pick_auto_driver()  # Asigna a `auto_driver` el resultado de `pick_auto_driver`.
            shipment_status = 'assigned' if auto_driver else 'pending_assignment'  # Asigna un valor a `shipment_status`.
            Shipment.objects.create(  # Ejecuta `Shipment.objects.create`.
                order=order,  # Asigna un valor a `order`.
                driver=auto_driver,  # Asigna un valor a `driver`.
                status=shipment_status,  # Asigna un valor a `status`.
            )  # Cierra el bloque/estructura.
            if auto_driver:  # Evalua la condicion del `if`.
                order.status = 'confirmed'  # Asigna un valor a `order.status`.
                order.save(update_fields=['status'])  # Ejecuta `order.save`.

            total_amount = Decimal('0.00')  # Asigna a `total_amount` el resultado de `Decimal`.
            total_items = 0  # Asigna un valor a `total_items`.

            for cart_item in cart_items:  # Itera en un bucle `for`.
                product = products_by_id[cart_item.product_id]  # Asigna un valor a `product`.
                quantity = int(cart_item.quantity)  # Asigna a `quantity` el resultado de `int`.
                subtotal = product.price * quantity  # Asigna un valor a `subtotal`.

                OrderItem.objects.create(  # Ejecuta `OrderItem.objects.create`.
                    order=order,  # Asigna un valor a `order`.
                    product=product,  # Asigna un valor a `product`.
                    product_name=product.name,  # Asigna un valor a `product_name`.
                    product_price=product.price,  # Asigna un valor a `product_price`.
                    quantity=quantity,  # Asigna un valor a `quantity`.
                    subtotal=subtotal,  # Asigna un valor a `subtotal`.
                )  # Cierra el bloque/estructura.

                product.stock -= quantity  # Actualiza `product.stock` con `-=`.
                product.save(update_fields=['stock'])  # Ejecuta `product.save`.

                total_amount += subtotal  # Actualiza `total_amount` con `+=`.
                total_items += quantity  # Actualiza `total_items` con `+=`.

            order.total_amount = total_amount  # Asigna un valor a `order.total_amount`.
            order.total_items = total_items  # Asigna un valor a `order.total_items`.
            order.save(update_fields=['total_amount', 'total_items'])  # Ejecuta `order.save`.

            Cart.objects.filter(user=user).delete()  # Ejecuta `Cart.objects.filter`.

        output_serializer = OrderSerializer(order, context=self.get_serializer_context())  # Asigna a `output_serializer` el resultado de `OrderSerializer`.
        payload = dict(output_serializer.data)  # Asigna a `payload` el resultado de `dict`.
        payload['message'] = 'Pedido creado correctamente.'  # Asigna un valor a `payload['message']`.
        return Response(payload, status=status.HTTP_201_CREATED)  # Devuelve un valor (`return`).


class OrderDetailView(generics.RetrieveAPIView):  # Define la clase `OrderDetailView`.
    serializer_class = OrderSerializer  # Asigna un valor a `serializer_class`.
    permission_classes = [permissions.IsAuthenticated]  # Asigna un valor a `permission_classes`.

    def get_queryset(self):  # Define la funcion `get_queryset`.
        return (  # Devuelve un valor (`return`).
            Order.objects.filter(user=self.request.user)  # Ejecuta `Order.objects.filter`.
            .select_related('delivery_address')  # Continua el encadenamiento y llama `.select_related`.
            .prefetch_related('items__product')  # Continua el encadenamiento y llama `.prefetch_related`.
        )  # Cierra el bloque/estructura.


class OrderTrackingView(APIView):  # Define la clase `OrderTrackingView`.
    permission_classes = [permissions.IsAuthenticated]  # Asigna un valor a `permission_classes`.

    def get(self, request, pk):  # Define la funcion `get`.
        include_map = parse_bool(request.query_params.get('include_map'), default=False)  # Asigna a `include_map` el resultado de `parse_bool`.
        include_route = parse_bool(request.query_params.get('include_route'), default=False)  # Asigna a `include_route` el resultado de `parse_bool`.
        travel_mode = (request.query_params.get('travel_mode') or 'DRIVE').strip().upper()  # Asigna un valor a `travel_mode`.
        alternatives = parse_bool(request.query_params.get('alternatives'), default=False)  # Asigna a `alternatives` el resultado de `parse_bool`.

        order_queryset = Order.objects.select_related(  # Asigna a `order_queryset` el resultado de `Order.objects.select_related`.
            'delivery_address',  # Agrega un literal a la estructura.
            'shipment',  # Agrega un literal a la estructura.
            'shipment__driver',  # Agrega un literal a la estructura.
        )  # Cierra el bloque/estructura.
        if not request.user.is_staff:  # Evalua la condicion del `if`.
            order_queryset = order_queryset.filter(user=request.user)  # Asigna a `order_queryset` el resultado de `order_queryset.filter`.

        order = order_queryset.filter(id=pk).first()  # Asigna a `order` el resultado de `order_queryset.filter`.
        if not order:  # Evalua la condicion del `if`.
            return Response({'error': 'Pedido no encontrado.'}, status=status.HTTP_404_NOT_FOUND)  # Devuelve un valor (`return`).

        shipment, _ = Shipment.objects.get_or_create(  # Asigna a `shipment` y `_` el resultado de `Shipment.objects.get_or_create`.
            order=order,  # Asigna un valor a `order`.
            defaults={'status': 'pending_assignment'},  # Asigna un valor a `defaults`.
        )  # Cierra el bloque/estructura.
        if shipment.driver_id is None:  # Evalua la condicion del `if`.
            auto_driver = pick_auto_driver()  # Asigna a `auto_driver` el resultado de `pick_auto_driver`.
            if auto_driver:  # Evalua la condicion del `if`.
                shipment.driver = auto_driver  # Asigna un valor a `shipment.driver`.
                if shipment.status == 'pending_assignment':  # Evalua la condicion del `if`.
                    shipment.status = 'assigned'  # Asigna un valor a `shipment.status`.
                shipment.save(update_fields=['driver', 'status', 'updated_at'])  # Ejecuta `shipment.save`.
                if order.status == 'pending':  # Evalua la condicion del `if`.
                    order.status = 'confirmed'  # Asigna un valor a `order.status`.
                    order.save(update_fields=['status'])  # Ejecuta `order.save`.
        shipment_data = ShipmentSerializer(shipment, context={'request': request}).data  # Asigna a `shipment_data` el resultado de `ShipmentSerializer`.

        payload = {  # Asigna un valor a `payload`.
            'order': {  # Asigna la clave `order` con un diccionario.
                'id': order.id,  # Asigna la clave `id` en un diccionario.
                'status': order.status,  # Asigna la clave `status` en un diccionario.
                'status_label': order.get_status_display(),  # Asigna la clave `status_label` con el resultado de `order.get_status_display`.
                'total_amount': order.total_amount,  # Asigna la clave `total_amount` en un diccionario.
                'total_items': order.total_items,  # Asigna la clave `total_items` en un diccionario.
                'created_at': order.created_at,  # Asigna la clave `created_at` en un diccionario.
                'delivery_city': order.delivery_city,  # Asigna la clave `delivery_city` en un diccionario.
                'delivery_main_address': order.delivery_main_address,  # Asigna la clave `delivery_main_address` en un diccionario.
            },  # Cierra el bloque/estructura.
            'shipment': shipment_data,  # Asigna la clave `shipment` en un diccionario.
        }  # Cierra el bloque/estructura.

        if include_map:  # Evalua la condicion del `if`.
            stored_lat = safe_float(getattr(order, 'delivery_latitude', None))  # Asigna a `stored_lat` el resultado de `safe_float`.
            stored_lng = safe_float(getattr(order, 'delivery_longitude', None))  # Asigna a `stored_lng` el resultado de `safe_float`.

            dest_lat = stored_lat if stored_lat is not None else safe_float(  # Asigna un valor a `dest_lat`.
                request.query_params.get('dest_lat')  # Ejecuta `request.query_params.get`.
                or request.query_params.get('destination_lat')  # Continua la expresion con `or`.
                or request.query_params.get('delivery_lat')  # Continua la expresion con `or`.
            )  # Cierra el bloque/estructura.
            dest_lng = stored_lng if stored_lng is not None else safe_float(  # Asigna un valor a `dest_lng`.
                request.query_params.get('dest_lng')  # Ejecuta `request.query_params.get`.
                or request.query_params.get('destination_lng')  # Continua la expresion con `or`.
                or request.query_params.get('delivery_lng')  # Continua la expresion con `or`.
            )  # Cierra el bloque/estructura.

            origin = {  # Asigna un valor a `origin`.
                'lat': safe_float(shipment.current_latitude),  # Asigna la clave `lat` con el resultado de `safe_float`.
                'lng': safe_float(shipment.current_longitude),  # Asigna la clave `lng` con el resultado de `safe_float`.
            }  # Cierra el bloque/estructura.
            if origin['lat'] is None or origin['lng'] is None:  # Evalua la condicion del `if`.
                last_point = (  # Asigna un valor a `last_point`.
                    ShipmentLocation.objects  # Referencia `ShipmentLocation.objects` en la estructura/expresion.
                    .filter(shipment=shipment)  # Continua el encadenamiento y llama `.filter`.
                    .order_by('-recorded_at', '-id')  # Continua el encadenamiento y llama `.order_by`.
                    .values('latitude', 'longitude')  # Continua el encadenamiento y llama `.values`.
                    .first()  # Continua el encadenamiento y llama `.first`.
                )  # Cierra el bloque/estructura.
                if last_point:  # Evalua la condicion del `if`.
                    origin = {  # Asigna un valor a `origin`.
                        'lat': safe_float(last_point.get('latitude')),  # Asigna la clave `lat` con el resultado de `safe_float`.
                        'lng': safe_float(last_point.get('longitude')),  # Asigna la clave `lng` con el resultado de `safe_float`.
                    }  # Cierra el bloque/estructura.

            destination = {'lat': dest_lat, 'lng': dest_lng} if dest_lat is not None and dest_lng is not None else None  # Asigna un valor a `destination`.
            geocode_payload = None  # Asigna un valor a `geocode_payload`.

            if destination is None:  # Evalua la condicion del `if`.
                query = ', '.join([  # Asigna un valor a `query`.
                    part for part in [  # Construye una comprension (filtra/une partes no vacias).
                        (order.delivery_main_address or '').strip(),  # Agrega una tupla a la estructura.
                        (order.delivery_secondary_street or '').strip(),  # Agrega una tupla a la estructura.
                        (order.delivery_city or '').strip(),  # Agrega una tupla a la estructura.
                    ]  # Cierra el bloque/estructura.
                    if part  # Evalua la condicion del `if`.
                ]).strip()  # Continua el encadenamiento y llama `.strip`.
                geocode_payload = try_geocode_address(query)  # Asigna a `geocode_payload` el resultado de `try_geocode_address`.
                first = (geocode_payload.get('results') or [None])[0]  # Asigna un valor a `first`.
                if first and safe_float(first.get('lat')) is not None and safe_float(first.get('lng')) is not None:  # Evalua la condicion del `if`.
                    destination = {  # Asigna un valor a `destination`.
                        'lat': safe_float(first.get('lat')),  # Asigna la clave `lat` con el resultado de `safe_float`.
                        'lng': safe_float(first.get('lng')),  # Asigna la clave `lng` con el resultado de `safe_float`.
                    }  # Cierra el bloque/estructura.

            route_payload = None  # Asigna un valor a `route_payload`.
            if include_route and origin.get('lat') is not None and origin.get('lng') is not None and destination:  # Evalua la condicion del `if`.
                route_payload = try_estimate_route(  # Asigna a `route_payload` el resultado de `try_estimate_route`.
                    origin=origin,  # Asigna un valor a `origin`.
                    destination=destination,  # Asigna un valor a `destination`.
                    travel_mode=travel_mode,  # Asigna un valor a `travel_mode`.
                    alternatives=alternatives,  # Asigna un valor a `alternatives`.
                )  # Cierra el bloque/estructura.

            payload['map'] = {  # Asigna un valor a `payload['map']`.
                'origin': origin if origin.get('lat') is not None and origin.get('lng') is not None else None,  # Asigna la clave `origin` en un diccionario.
                'destination': destination,  # Asigna la clave `destination` en un diccionario.
                'geocode': geocode_payload,  # Asigna la clave `geocode` en un diccionario.
                'route': route_payload,  # Asigna la clave `route` en un diccionario.
            }  # Cierra el bloque/estructura.

        return Response(payload)  # Devuelve un valor (`return`).


class OrderTrackingLocationUpdateView(APIView):  # Define la clase `OrderTrackingLocationUpdateView`.
    permission_classes = [permissions.IsAuthenticated]  # Asigna un valor a `permission_classes`.

    def _can_update_tracking(self, user, shipment):  # Define la funcion `_can_update_tracking`.
        if not user.is_authenticated:  # Evalua la condicion del `if`.
            return False  # Devuelve un valor (`return`).

        if user.is_staff or user.is_superuser:  # Evalua la condicion del `if`.
            return True  # Devuelve un valor (`return`).

        allowed_groups = ['ADMIN', 'DRIVER', 'REPARTIDOR']  # Asigna un valor a `allowed_groups`.
        is_ops_user = user.groups.filter(name__in=allowed_groups).exists()  # Asigna a `is_ops_user` el resultado de `user.groups.filter`.

        if shipment.driver_id and shipment.driver_id == user.id:  # Evalua la condicion del `if`.
            return True  # Devuelve un valor (`return`).

        if is_ops_user and shipment.driver_id is None:  # Evalua la condicion del `if`.
            return True  # Devuelve un valor (`return`).

        return False  # Devuelve un valor (`return`).

    def post(self, request, pk):  # Define la funcion `post`.
        order_queryset = Order.objects.select_related('shipment', 'shipment__driver')  # Asigna a `order_queryset` el resultado de `Order.objects.select_related`.
        if not request.user.is_staff:  # Evalua la condicion del `if`.
            order_queryset = order_queryset.filter(  # Asigna a `order_queryset` el resultado de `order_queryset.filter`.
                Q(user=request.user) | Q(shipment__driver=request.user)  # Ejecuta `Q`.
            )  # Cierra el bloque/estructura.

        order = order_queryset.filter(id=pk).first()  # Asigna a `order` el resultado de `order_queryset.filter`.
        if not order:  # Evalua la condicion del `if`.
            return Response({'error': 'Pedido no encontrado.'}, status=status.HTTP_404_NOT_FOUND)  # Devuelve un valor (`return`).

        shipment, _ = Shipment.objects.get_or_create(  # Asigna a `shipment` y `_` el resultado de `Shipment.objects.get_or_create`.
            order=order,  # Asigna un valor a `order`.
            defaults={'status': 'pending_assignment'},  # Asigna un valor a `defaults`.
        )  # Cierra el bloque/estructura.

        if not self._can_update_tracking(request.user, shipment):  # Evalua la condicion del `if`.
            return Response(  # Devuelve un valor (`return`).
                {'error': 'No tienes permisos para actualizar la ubicacion de este envio.'},  # Define un diccionario literal.
                status=status.HTTP_403_FORBIDDEN  # Asigna un valor a `status`.
            )  # Cierra el bloque/estructura.

        serializer = ShipmentLocationUpdateSerializer(data=request.data)  # Asigna a `serializer` el resultado de `ShipmentLocationUpdateSerializer`.
        serializer.is_valid(raise_exception=True)  # Ejecuta `serializer.is_valid`.

        data = serializer.validated_data  # Asigna un valor a `data`.
        shipment.current_latitude = data['latitude']  # Asigna un valor a `shipment.current_latitude`.
        shipment.current_longitude = data['longitude']  # Asigna un valor a `shipment.current_longitude`.
        shipment.last_location_at = timezone.now()  # Asigna a `shipment.last_location_at` el resultado de `timezone.now`.

        if 'heading' in data:  # Evalua la condicion del `if`.
            shipment.current_heading = data.get('heading')  # Asigna a `shipment.current_heading` el resultado de `data.get`.
        if 'speed' in data:  # Evalua la condicion del `if`.
            shipment.current_speed = data.get('speed')  # Asigna a `shipment.current_speed` el resultado de `data.get`.
        if 'status' in data:  # Evalua la condicion del `if`.
            shipment.status = data['status']  # Asigna un valor a `shipment.status`.
        if 'eta_minutes' in data:  # Evalua la condicion del `if`.
            shipment.eta_minutes = data.get('eta_minutes')  # Asigna a `shipment.eta_minutes` el resultado de `data.get`.
        if 'notes' in data:  # Evalua la condicion del `if`.
            shipment.notes = data.get('notes', '')  # Asigna a `shipment.notes` el resultado de `data.get`.

        shipment.save()  # Ejecuta `shipment.save`.

        ShipmentLocation.objects.create(  # Ejecuta `ShipmentLocation.objects.create`.
            shipment=shipment,  # Asigna un valor a `shipment`.
            latitude=data['latitude'],  # Asigna un valor a `latitude`.
            longitude=data['longitude'],  # Asigna un valor a `longitude`.
            heading=data.get('heading'),  # Asigna a `heading` el resultado de `data.get`.
            speed=data.get('speed'),  # Asigna a `speed` el resultado de `data.get`.
        )  # Cierra el bloque/estructura.

        order_status_map = {  # Asigna un valor a `order_status_map`.
            'pending_assignment': 'pending',  # Agrega un literal a la estructura.
            'assigned': 'confirmed',  # Agrega un literal a la estructura.
            'picked_up': 'preparing',  # Agrega un literal a la estructura.
            'on_the_way': 'on_the_way',  # Agrega un literal a la estructura.
            'nearby': 'on_the_way',  # Agrega un literal a la estructura.
            'delivered': 'delivered',  # Agrega un literal a la estructura.
            'cancelled': 'cancelled',  # Agrega un literal a la estructura.
        }  # Cierra el bloque/estructura.
        mapped_status = order_status_map.get(shipment.status)  # Asigna a `mapped_status` el resultado de `order_status_map.get`.
        if mapped_status and mapped_status != order.status:  # Evalua la condicion del `if`.
            order.status = mapped_status  # Asigna un valor a `order.status`.
            order.save(update_fields=['status'])  # Ejecuta `order.save`.

        payload = ShipmentSerializer(shipment, context={'request': request}).data  # Asigna a `payload` el resultado de `ShipmentSerializer`.
        payload['message'] = 'Ubicacion de envio actualizada.'  # Asigna un valor a `payload['message']`.
        return Response(payload, status=status.HTTP_200_OK)  # Devuelve un valor (`return`).


class OrderTrackingAssignDriverView(APIView):  # Define la clase `OrderTrackingAssignDriverView`.
    permission_classes = [permissions.IsAuthenticated]  # Asigna un valor a `permission_classes`.

    def _can_assign(self, user):  # Define la funcion `_can_assign`.
        if not user.is_authenticated:  # Evalua la condicion del `if`.
            return False  # Devuelve un valor (`return`).
        if user.is_staff or user.is_superuser:  # Evalua la condicion del `if`.
            return True  # Devuelve un valor (`return`).
        return user.groups.filter(name='ADMIN').exists()  # Devuelve un valor (`return`).

    def post(self, request, pk):  # Define la funcion `post`.
        serializer = ShipmentAssignDriverSerializer(data=request.data)  # Asigna a `serializer` el resultado de `ShipmentAssignDriverSerializer`.
        serializer.is_valid(raise_exception=True)  # Ejecuta `serializer.is_valid`.

        order = (  # Asigna un valor a `order`.
            Order.objects.select_related('shipment', 'shipment__driver')  # Ejecuta `Order.objects.select_related`.
            .filter(id=pk)  # Continua el encadenamiento y llama `.filter`.
            .first()  # Continua el encadenamiento y llama `.first`.
        )  # Cierra el bloque/estructura.
        if not order:  # Evalua la condicion del `if`.
            return Response({'error': 'Pedido no encontrado.'}, status=status.HTTP_404_NOT_FOUND)  # Devuelve un valor (`return`).

        shipment, _ = Shipment.objects.get_or_create(  # Asigna a `shipment` y `_` el resultado de `Shipment.objects.get_or_create`.
            order=order,  # Asigna un valor a `order`.
            defaults={'status': 'pending_assignment'},  # Asigna un valor a `defaults`.
        )  # Cierra el bloque/estructura.

        validated = serializer.validated_data  # Asigna un valor a `validated`.
        has_driver_id = 'driver_id' in validated  # Asigna un valor a `has_driver_id`.
        driver_id = validated.get('driver_id')  # Asigna a `driver_id` el resultado de `validated.get`.
        auto_assign = validated.get('auto_assign')  # Asigna a `auto_assign` el resultado de `validated.get`.

        # Regla pedida:
        # - body vacio => auto asignar
        # - auto_assign=true => auto asignar
        # - driver_id=null => desasignar explicito
        if auto_assign is None and not has_driver_id:  # Evalua la condicion del `if`.
            auto_assign = True  # Asigna un valor a `auto_assign`.

        can_assign_all = self._can_assign(request.user)  # Asigna a `can_assign_all` el resultado de `self._can_assign`.
        is_owner = request.user.is_authenticated and order.user_id == request.user.id  # Asigna un valor a `is_owner`.

        # Clientes: solo permitimos auto-asignacion (Reintentar) para su propio pedido.
        # Admin/staff: pueden auto-asignar, asignar manual, o desasignar.
        if not can_assign_all:  # Evalua la condicion del `if`.
            if not (is_owner and bool(auto_assign) and not has_driver_id):  # Evalua la condicion del `if`.
                return Response(  # Devuelve un valor (`return`).
                    {'error': 'No tienes permisos para asignar repartidor.'},  # Define un diccionario literal.
                    status=status.HTTP_403_FORBIDDEN  # Asigna un valor a `status`.
                )  # Cierra el bloque/estructura.
            # Forzamos la operacion a auto-asignar.
            auto_assign = True  # Asigna un valor a `auto_assign`.
            has_driver_id = False  # Asigna un valor a `has_driver_id`.
            driver_id = None  # Asigna un valor a `driver_id`.

        if auto_assign:  # Evalua la condicion del `if`.
            auto_driver = pick_auto_driver()  # Asigna a `auto_driver` el resultado de `pick_auto_driver`.
            if auto_driver is None:  # Evalua la condicion del `if`.
                shipment.driver = None  # Asigna un valor a `shipment.driver`.
                if shipment.status not in {'delivered', 'cancelled'}:  # Evalua la condicion del `if`.
                    shipment.status = 'pending_assignment'  # Asigna un valor a `shipment.status`.
                shipment.save(update_fields=['driver', 'status', 'updated_at'])  # Ejecuta `shipment.save`.
                payload = ShipmentSerializer(shipment, context={'request': request}).data  # Asigna a `payload` el resultado de `ShipmentSerializer`.
                payload['message'] = 'No hay repartidores disponibles para auto-asignacion.'  # Asigna un valor a `payload['message']`.
                return Response(payload, status=status.HTTP_200_OK)  # Devuelve un valor (`return`).

            shipment.driver = auto_driver  # Asigna un valor a `shipment.driver`.
            if shipment.status in {'pending_assignment', 'cancelled'}:  # Evalua la condicion del `if`.
                shipment.status = 'assigned'  # Asigna un valor a `shipment.status`.
            shipment.save(update_fields=['driver', 'status', 'updated_at'])  # Ejecuta `shipment.save`.

            if order.status == 'pending':  # Evalua la condicion del `if`.
                order.status = 'confirmed'  # Asigna un valor a `order.status`.
                order.save(update_fields=['status'])  # Ejecuta `order.save`.

            payload = ShipmentSerializer(shipment, context={'request': request}).data  # Asigna a `payload` el resultado de `ShipmentSerializer`.
            payload['message'] = 'Repartidor auto-asignado correctamente.'  # Asigna un valor a `payload['message']`.
            return Response(payload, status=status.HTTP_200_OK)  # Devuelve un valor (`return`).

        if has_driver_id and driver_id is None:  # Evalua la condicion del `if`.
            shipment.driver = None  # Asigna un valor a `shipment.driver`.
            if shipment.status not in {'delivered', 'cancelled'}:  # Evalua la condicion del `if`.
                shipment.status = 'pending_assignment'  # Asigna un valor a `shipment.status`.
            shipment.save(update_fields=['driver', 'status', 'updated_at'])  # Ejecuta `shipment.save`.
            payload = ShipmentSerializer(shipment, context={'request': request}).data  # Asigna a `payload` el resultado de `ShipmentSerializer`.
            payload['message'] = 'Repartidor desasignado correctamente.'  # Asigna un valor a `payload['message']`.
            return Response(payload, status=status.HTTP_200_OK)  # Devuelve un valor (`return`).

        if not has_driver_id:  # Evalua la condicion del `if`.
            return Response(  # Devuelve un valor (`return`).
                {'error': 'Debes enviar driver_id, driver_id=null o auto_assign=true.'},  # Define un diccionario literal.
                status=status.HTTP_400_BAD_REQUEST  # Asigna un valor a `status`.
            )  # Cierra el bloque/estructura.

        driver = User.objects.get(id=driver_id)  # Asigna a `driver` el resultado de `User.objects.get`.
        shipment.driver = driver  # Asigna un valor a `shipment.driver`.
        if shipment.status == 'pending_assignment':  # Evalua la condicion del `if`.
            shipment.status = 'assigned'  # Asigna un valor a `shipment.status`.
        shipment.save(update_fields=['driver', 'status', 'updated_at'])  # Ejecuta `shipment.save`.

        if order.status == 'pending':  # Evalua la condicion del `if`.
            order.status = 'confirmed'  # Asigna un valor a `order.status`.
            order.save(update_fields=['status'])  # Ejecuta `order.save`.

        payload = ShipmentSerializer(shipment, context={'request': request}).data  # Asigna a `payload` el resultado de `ShipmentSerializer`.
        payload['message'] = 'Repartidor asignado correctamente.'  # Asigna un valor a `payload['message']`.
        return Response(payload, status=status.HTTP_200_OK)  # Devuelve un valor (`return`).


class DeliveryAddressListCreateView(generics.ListCreateAPIView):  # Define la clase `DeliveryAddressListCreateView`.
    serializer_class = DeliveryAddressSerializer  # Asigna un valor a `serializer_class`.
    permission_classes = [permissions.IsAuthenticated]  # Asigna un valor a `permission_classes`.

    def get_queryset(self):  # Define la funcion `get_queryset`.
        return DeliveryAddress.objects.filter(user=self.request.user)  # Devuelve un valor (`return`).

    def perform_create(self, serializer):  # Define la funcion `perform_create`.
        queryset = DeliveryAddress.objects.filter(user=self.request.user)  # Asigna a `queryset` el resultado de `DeliveryAddress.objects.filter`.
        requested_default = serializer.validated_data.get('is_default', False)  # Asigna a `requested_default` el resultado de `serializer.validated_data.get`.
        should_be_default = requested_default or not queryset.exists()  # Asigna un valor a `should_be_default`.

        address = serializer.save(user=self.request.user, is_default=should_be_default)  # Asigna a `address` el resultado de `serializer.save`.
        if should_be_default:  # Evalua la condicion del `if`.
            queryset.exclude(id=address.id).update(is_default=False)  # Ejecuta `queryset.exclude`.


class DeliveryAddressDetailView(generics.RetrieveUpdateDestroyAPIView):  # Define la clase `DeliveryAddressDetailView`.
    serializer_class = DeliveryAddressSerializer  # Asigna un valor a `serializer_class`.
    permission_classes = [permissions.IsAuthenticated]  # Asigna un valor a `permission_classes`.

    def get_queryset(self):  # Define la funcion `get_queryset`.
        return DeliveryAddress.objects.filter(user=self.request.user)  # Devuelve un valor (`return`).

    def perform_update(self, serializer):  # Define la funcion `perform_update`.
        address = serializer.save()  # Asigna a `address` el resultado de `serializer.save`.
        if address.is_default:  # Evalua la condicion del `if`.
            DeliveryAddress.objects.filter(user=self.request.user).exclude(id=address.id).update(is_default=False)  # Ejecuta `DeliveryAddress.objects.filter`.
            return  # Devuelve un valor (`return`).

        has_default = DeliveryAddress.objects.filter(user=self.request.user, is_default=True).exists()  # Asigna a `has_default` el resultado de `DeliveryAddress.objects.filter`.
        if not has_default:  # Evalua la condicion del `if`.
            address.is_default = True  # Asigna un valor a `address.is_default`.
            address.save(update_fields=['is_default'])  # Ejecuta `address.save`.

    def perform_destroy(self, instance):  # Define la funcion `perform_destroy`.
        user = instance.user  # Asigna un valor a `user`.
        was_default = instance.is_default  # Asigna un valor a `was_default`.
        instance.delete()  # Ejecuta `instance.delete`.

        if was_default:  # Evalua la condicion del `if`.
            replacement = DeliveryAddress.objects.filter(user=user).order_by('-id').first()  # Asigna a `replacement` el resultado de `DeliveryAddress.objects.filter`.
            if replacement:  # Evalua la condicion del `if`.
                replacement.is_default = True  # Asigna un valor a `replacement.is_default`.
                replacement.save(update_fields=['is_default'])  # Ejecuta `replacement.save`.


class RoleChangeRequestListCreateView(generics.ListCreateAPIView):  # Define la clase `RoleChangeRequestListCreateView`.
    serializer_class = RoleChangeRequestSerializer  # Asigna un valor a `serializer_class`.
    permission_classes = [permissions.IsAuthenticated]  # Asigna un valor a `permission_classes`.

    def get_queryset(self):  # Define la funcion `get_queryset`.
        return RoleChangeRequest.objects.filter(user=self.request.user)  # Devuelve un valor (`return`).

    def perform_create(self, serializer):  # Define la funcion `perform_create`.
        requested_role = serializer.validated_data['requested_role']  # Asigna un valor a `requested_role`.
        has_pending = RoleChangeRequest.objects.filter(  # Asigna a `has_pending` el resultado de `RoleChangeRequest.objects.filter`.
            user=self.request.user,  # Asigna un valor a `user`.
            requested_role=requested_role,  # Asigna un valor a `requested_role`.
            status='pending',  # Asigna un valor a `status`.
        ).exists()  # Continua el encadenamiento y llama `.exists`.
        if has_pending:  # Evalua la condicion del `if`.
            raise serializers.ValidationError({  # Lanza una excepcion (`raise`).
                'requested_role': 'Ya tienes una solicitud pendiente para este rol.'  # Agrega un literal a la estructura.
            })  # Cierra la estructura.
        serializer.save(user=self.request.user)  # Ejecuta `serializer.save`.


def geo_provider():  # Define la funcion `geo_provider`.
    return (getattr(settings, 'GEO_PROVIDER', 'osm') or 'osm').strip().lower()  # Devuelve un valor (`return`).


def osm_nominatim_base_url():  # Define la funcion `osm_nominatim_base_url`.
    return (getattr(settings, 'OSM_NOMINATIM_BASE_URL', 'https://nominatim.openstreetmap.org') or '').rstrip('/')  # Devuelve un valor (`return`).


def osm_router_base_url():  # Define la funcion `osm_router_base_url`.
    return (getattr(settings, 'OSM_ROUTER_BASE_URL', 'https://router.project-osrm.org') or '').rstrip('/')  # Devuelve un valor (`return`).


def geocoder_user_agent():  # Define la funcion `geocoder_user_agent`.
    return (getattr(settings, 'GEOCODER_USER_AGENT', 'api-guayabal/1.0 (mobile-app)') or 'api-guayabal/1.0')  # Devuelve un valor (`return`).


def http_json_get(endpoint, params=None, timeout=8, headers=None):  # Define la funcion `http_json_get`.
    url = endpoint if not params else f"{endpoint}?{urlencode(params)}"  # Asigna un valor a `url`.
    req = Request(  # Asigna a `req` el resultado de `Request`.
        url,  # Referencia `url` en la estructura/expresion.
        headers=headers or {  # Asigna un valor a `headers`.
            'Accept': 'application/json',  # Agrega un literal a la estructura.
        },  # Cierra el bloque/estructura.
    )  # Cierra el bloque/estructura.
    with urlopen(req, timeout=timeout) as resp:  # Abre un contexto con `with`.
        return json.loads(resp.read().decode('utf-8'))  # Devuelve un valor (`return`).


def extract_nominatim_result(item):  # Define la funcion `extract_nominatim_result`.
    address = item.get('address') or {}  # Asigna a `address` el resultado de `item.get`.
    display_name = item.get('display_name') or ''  # Asigna a `display_name` el resultado de `item.get`.
    road = (  # Asigna un valor a `road`.
        address.get('road')  # Ejecuta `address.get`.
        or address.get('pedestrian')  # Continua la expresion con `or`.
        or address.get('footway')  # Continua la expresion con `or`.
        or address.get('path')  # Continua la expresion con `or`.
        or address.get('cycleway')  # Continua la expresion con `or`.
        or ''  # Continua la expresion con `or`.
    )  # Cierra el bloque/estructura.
    house_number = address.get('house_number') or ''  # Asigna a `house_number` el resultado de `address.get`.
    main_address = (  # Asigna un valor a `main_address`.
        f"{road} {house_number}".strip()  # Aplica `.strip` a una cadena.
        or road  # Continua la expresion con `or`.
        or (display_name.split(',')[0].strip() if display_name else '')  # Ejecuta `or`.
    )  # Cierra el bloque/estructura.
    secondary_street = (  # Asigna un valor a `secondary_street`.
        address.get('suburb')  # Ejecuta `address.get`.
        or address.get('neighbourhood')  # Continua la expresion con `or`.
        or address.get('quarter')  # Continua la expresion con `or`.
        or address.get('city_district')  # Continua la expresion con `or`.
        or ''  # Continua la expresion con `or`.
    )  # Cierra el bloque/estructura.
    city = (  # Asigna un valor a `city`.
        address.get('city')  # Ejecuta `address.get`.
        or address.get('town')  # Continua la expresion con `or`.
        or address.get('village')  # Continua la expresion con `or`.
        or address.get('hamlet')  # Continua la expresion con `or`.
        or ''  # Continua la expresion con `or`.
    )  # Cierra el bloque/estructura.
    region = address.get('state') or address.get('county') or ''  # Asigna a `region` el resultado de `address.get`.
    country_name = address.get('country') or ''  # Asigna a `country_name` el resultado de `address.get`.

    try:  # Inicia un bloque `try`.
        lat = float(item.get('lat')) if item.get('lat') is not None else None  # Asigna a `lat` el resultado de `float`.
    except (TypeError, ValueError):  # Maneja una excepcion en `except`.
        lat = None  # Asigna un valor a `lat`.
    try:  # Inicia un bloque `try`.
        lng = float(item.get('lon')) if item.get('lon') is not None else None  # Asigna a `lng` el resultado de `float`.
    except (TypeError, ValueError):  # Maneja una excepcion en `except`.
        lng = None  # Asigna un valor a `lng`.

    return {  # Devuelve un valor (`return`).
        'place_id': str(item.get('place_id') or ''),  # Asigna la clave `place_id` con el resultado de `str`.
        'osm_id': str(item.get('osm_id') or ''),  # Asigna la clave `osm_id` con el resultado de `str`.
        'osm_type': item.get('osm_type') or '',  # Agrega un literal a la estructura.
        'label': display_name,  # Asigna la clave `label` en un diccionario.
        'main_address': main_address,  # Asigna la clave `main_address` en un diccionario.
        'secondary_street': secondary_street,  # Asigna la clave `secondary_street` en un diccionario.
        'city': city,  # Asigna la clave `city` en un diccionario.
        'region': region,  # Asigna la clave `region` en un diccionario.
        'country': country_name,  # Asigna la clave `country` en un diccionario.
        'lat': lat,  # Asigna la clave `lat` en un diccionario.
        'lng': lng,  # Asigna la clave `lng` en un diccionario.
    }  # Cierra el bloque/estructura.


def parse_google_duration(value):  # Define la funcion `parse_google_duration`.
    if not value or not isinstance(value, str):  # Evalua la condicion del `if`.
        return None  # Devuelve un valor (`return`).
    if not value.endswith('s'):  # Evalua la condicion del `if`.
        return None  # Devuelve un valor (`return`).
    try:  # Inicia un bloque `try`.
        return int(float(value[:-1]))  # Devuelve un valor (`return`).
    except (TypeError, ValueError):  # Maneja una excepcion en `except`.
        return None  # Devuelve un valor (`return`).


def parse_bool(value, default=False):  # Define la funcion `parse_bool`.
    if value is None:  # Evalua la condicion del `if`.
        return default  # Devuelve un valor (`return`).
    if isinstance(value, bool):  # Evalua la condicion del `if`.
        return value  # Devuelve un valor (`return`).
    value = str(value).strip().lower()  # Asigna a `value` el resultado de `str`.
    if value in {'1', 'true', 't', 'yes', 'y', 'si', 'sí', 'on'}:  # Evalua la condicion del `if`.
        return True  # Devuelve un valor (`return`).
    if value in {'0', 'false', 'f', 'no', 'n', 'off'}:  # Evalua la condicion del `if`.
        return False  # Devuelve un valor (`return`).
    return default  # Devuelve un valor (`return`).


def safe_float(value):  # Define la funcion `safe_float`.
    if value is None:  # Evalua la condicion del `if`.
        return None  # Devuelve un valor (`return`).
    try:  # Inicia un bloque `try`.
        return float(value)  # Devuelve un valor (`return`).
    except (TypeError, ValueError):  # Maneja una excepcion en `except`.
        return None  # Devuelve un valor (`return`).


def _google_maps_server_key():  # Define la funcion `_google_maps_server_key`.
    return (getattr(settings, 'GOOGLE_MAPS_SERVER_API_KEY', '') or '').strip()  # Devuelve un valor (`return`).


def _google_maps_language():  # Define la funcion `_google_maps_language`.
    return (getattr(settings, 'GOOGLE_MAPS_LANGUAGE', 'es') or 'es').strip()  # Devuelve un valor (`return`).


def try_geocode_address(address):  # Define la funcion `try_geocode_address`.
    # Best-effort geocode used by tracking map payloads.
    # Returns: dict with {provider, results} compatible (subset) with GeoGeocodeView.
    # Never raises.
    address = (address or '').strip()  # Asigna un valor a `address`.
    if not address:  # Evalua la condicion del `if`.
        return {'provider': geo_provider(), 'results': []}  # Devuelve un valor (`return`).

    if geo_provider() != 'google':  # Evalua la condicion del `if`.
        try:  # Inicia un bloque `try`.
            raw_results = http_json_get(  # Asigna a `raw_results` el resultado de `http_json_get`.
                f'{osm_nominatim_base_url()}/search',  # Agrega un literal a la estructura.
                {  # Inicia una estructura literal.
                    'format': 'jsonv2',  # Agrega un literal a la estructura.
                    'addressdetails': 1,  # Asigna la clave `addressdetails` en un diccionario.
                    'limit': 1,  # Asigna la clave `limit` en un diccionario.
                    'q': address,  # Asigna la clave `q` en un diccionario.
                },  # Cierra el bloque/estructura.
                headers={  # Asigna un valor a `headers`.
                    'User-Agent': geocoder_user_agent(),  # Asigna la clave `User-Agent` con el resultado de `geocoder_user_agent`.
                    'Accept': 'application/json',  # Agrega un literal a la estructura.
                }  # Cierra el bloque/estructura.
            ) or []  # Usa `[]` como valor por defecto si la expresion es falsy.
        except Exception:  # Maneja una excepcion en `except`.
            return {'provider': 'osm', 'results': []}  # Devuelve un valor (`return`).

        results = [extract_nominatim_result(item) for item in raw_results[:1]]  # Asigna un valor a `results`.
        return {'provider': 'osm', 'results': results}  # Devuelve un valor (`return`).

    key = _google_maps_server_key()  # Asigna a `key` el resultado de `_google_maps_server_key`.
    if not key:  # Evalua la condicion del `if`.
        return {'provider': 'google', 'results': [], 'error': 'Falta configurar GOOGLE_MAPS_SERVER_API_KEY.'}  # Devuelve un valor (`return`).

    try:  # Inicia un bloque `try`.
        payload = http_json_get(  # Asigna a `payload` el resultado de `http_json_get`.
            'https://maps.googleapis.com/maps/api/geocode/json',  # Agrega un literal a la estructura.
            {  # Inicia una estructura literal.
                'language': _google_maps_language(),  # Asigna la clave `language` con el resultado de `_google_maps_language`.
                'key': key,  # Asigna la clave `key` en un diccionario.
                'address': address,  # Asigna la clave `address` en un diccionario.
            },  # Cierra el bloque/estructura.
            headers={'Accept': 'application/json'},  # Asigna un valor a `headers`.
            timeout=6,  # Asigna un valor a `timeout`.
        )  # Cierra el bloque/estructura.
    except Exception:  # Maneja una excepcion en `except`.
        return {'provider': 'google', 'results': []}  # Devuelve un valor (`return`).

    status_name = (payload or {}).get('status')  # Asigna un valor a `status_name`.
    if status_name not in {'OK', 'ZERO_RESULTS'}:  # Evalua la condicion del `if`.
        return {  # Devuelve un valor (`return`).
            'provider': 'google',  # Agrega un literal a la estructura.
            'results': [],  # Asigna la clave `results` con una lista.
            'error': (payload or {}).get('error_message') or status_name or 'Geocoding fallo.',  # Agrega un literal a la estructura.
        }  # Cierra el bloque/estructura.

    results = []  # Asigna un valor a `results`.
    for item in (payload.get('results') or [])[:1]:  # Itera en un bucle `for`.
        geometry = item.get('geometry') or {}  # Asigna a `geometry` el resultado de `item.get`.
        location = geometry.get('location') or {}  # Asigna a `location` el resultado de `geometry.get`.
        results.append({  # Ejecuta `results.append`.
            'place_id': item.get('place_id') or '',  # Agrega un literal a la estructura.
            'label': item.get('formatted_address') or '',  # Agrega un literal a la estructura.
            'lat': safe_float(location.get('lat')),  # Asigna la clave `lat` con el resultado de `safe_float`.
            'lng': safe_float(location.get('lng')),  # Asigna la clave `lng` con el resultado de `safe_float`.
        })  # Cierra la estructura.
    return {'provider': 'google', 'results': results}  # Devuelve un valor (`return`).


def try_estimate_route(origin, destination, travel_mode='DRIVE', alternatives=False):  # Define la funcion `try_estimate_route`.
    # Best-effort route estimation used by tracking map payloads.
    # Returns: dict compatible (subset) with GeoRouteEstimateView, never raises.
    origin_lat = safe_float((origin or {}).get('lat'))  # Asigna a `origin_lat` el resultado de `safe_float`.
    origin_lng = safe_float((origin or {}).get('lng'))  # Asigna a `origin_lng` el resultado de `safe_float`.
    dest_lat = safe_float((destination or {}).get('lat'))  # Asigna a `dest_lat` el resultado de `safe_float`.
    dest_lng = safe_float((destination or {}).get('lng'))  # Asigna a `dest_lng` el resultado de `safe_float`.
    if origin_lat is None or origin_lng is None or dest_lat is None or dest_lng is None:  # Evalua la condicion del `if`.
        return {'provider': geo_provider(), 'routes': []}  # Devuelve un valor (`return`).

    mode = (travel_mode or 'DRIVE').strip().upper()  # Asigna un valor a `mode`.

    if geo_provider() != 'google':  # Evalua la condicion del `if`.
        profile_map = {  # Asigna un valor a `profile_map`.
            'DRIVE': 'driving',  # Agrega un literal a la estructura.
            'WALK': 'walking',  # Agrega un literal a la estructura.
            'BICYCLE': 'cycling',  # Agrega un literal a la estructura.
            'TWO_WHEELER': 'driving',  # Agrega un literal a la estructura.
        }  # Cierra el bloque/estructura.
        profile = profile_map.get(mode, 'driving')  # Asigna a `profile` el resultado de `profile_map.get`.
        endpoint = f"{osm_router_base_url()}/route/v1/{profile}/{origin_lng},{origin_lat};{dest_lng},{dest_lat}"  # Asigna un valor a `endpoint`.
        try:  # Inicia un bloque `try`.
            data = http_json_get(  # Asigna a `data` el resultado de `http_json_get`.
                endpoint,  # Referencia `endpoint` en la estructura/expresion.
                {  # Inicia una estructura literal.
                    'overview': 'full',  # Agrega un literal a la estructura.
                    'geometries': 'polyline',  # Agrega un literal a la estructura.
                    'alternatives': str(bool(alternatives)).lower(),  # Asigna la clave `alternatives` con el resultado de `str`.
                    'steps': 'false',  # Agrega un literal a la estructura.
                },  # Cierra el bloque/estructura.
                headers={'Accept': 'application/json'},  # Asigna un valor a `headers`.
            )  # Cierra el bloque/estructura.
        except Exception:  # Maneja una excepcion en `except`.
            return {'provider': 'osm', 'routes': [], 'error': 'Routes API fallo.'}  # Devuelve un valor (`return`).

        if (data or {}).get('code') != 'Ok':  # Evalua la condicion del `if`.
            return {  # Devuelve un valor (`return`).
                'provider': 'osm',  # Agrega un literal a la estructura.
                'routes': [],  # Asigna la clave `routes` con una lista.
                'error': (data or {}).get('message') or 'No se pudo calcular la ruta.',  # Agrega un literal a la estructura.
                'raw': data,  # Asigna la clave `raw` en un diccionario.
            }  # Cierra el bloque/estructura.

        normalized = []  # Asigna un valor a `normalized`.
        for route in (data.get('routes') or []):  # Itera en un bucle `for`.
            distance_m = route.get('distance')  # Asigna a `distance_m` el resultado de `route.get`.
            duration_sec = route.get('duration')  # Asigna a `duration_sec` el resultado de `route.get`.
            normalized.append({  # Ejecuta `normalized.append`.
                'distance_meters': distance_m,  # Asigna la clave `distance_meters` en un diccionario.
                'distance_km': round(float(distance_m) / 1000, 2) if distance_m is not None else None,  # Asigna la clave `distance_km` con el resultado de `round`.
                'duration': f'{duration_sec}s' if duration_sec is not None else None,  # Asigna la clave `duration` en un diccionario.
                'static_duration': f'{duration_sec}s' if duration_sec is not None else None,  # Asigna la clave `static_duration` en un diccionario.
                'duration_seconds': int(duration_sec) if duration_sec is not None else None,  # Asigna la clave `duration_seconds` con el resultado de `int`.
                'static_duration_seconds': int(duration_sec) if duration_sec is not None else None,  # Asigna la clave `static_duration_seconds` con el resultado de `int`.
                'polyline': route.get('geometry') or '',  # Agrega un literal a la estructura.
            })  # Cierra la estructura.

        return {'provider': 'osm', 'routes': normalized}  # Devuelve un valor (`return`).

    key = _google_maps_server_key()  # Asigna a `key` el resultado de `_google_maps_server_key`.
    if not key:  # Evalua la condicion del `if`.
        return {'provider': 'google', 'routes': [], 'error': 'Falta configurar GOOGLE_MAPS_SERVER_API_KEY.'}  # Devuelve un valor (`return`).

    routing_preference = 'TRAFFIC_AWARE'  # Asigna un valor a `routing_preference`.
    units = 'METRIC'  # Asigna un valor a `units`.

    payload = {  # Asigna un valor a `payload`.
        'origin': {  # Asigna la clave `origin` con un diccionario.
            'location': {  # Asigna la clave `location` con un diccionario.
                'latLng': {  # Asigna la clave `latLng` con un diccionario.
                    'latitude': origin_lat,  # Asigna la clave `latitude` en un diccionario.
                    'longitude': origin_lng,  # Asigna la clave `longitude` en un diccionario.
                }  # Cierra el bloque/estructura.
            }  # Cierra el bloque/estructura.
        },  # Cierra el bloque/estructura.
        'destination': {  # Asigna la clave `destination` con un diccionario.
            'location': {  # Asigna la clave `location` con un diccionario.
                'latLng': {  # Asigna la clave `latLng` con un diccionario.
                    'latitude': dest_lat,  # Asigna la clave `latitude` en un diccionario.
                    'longitude': dest_lng,  # Asigna la clave `longitude` en un diccionario.
                }  # Cierra el bloque/estructura.
            }  # Cierra el bloque/estructura.
        },  # Cierra el bloque/estructura.
        'travelMode': mode,  # Asigna la clave `travelMode` en un diccionario.
        'routingPreference': routing_preference,  # Asigna la clave `routingPreference` en un diccionario.
        'computeAlternativeRoutes': bool(alternatives),  # Asigna la clave `computeAlternativeRoutes` con el resultado de `bool`.
        'units': units,  # Asigna la clave `units` en un diccionario.
    }  # Cierra el bloque/estructura.

    field_mask = ','.join([  # Asigna un valor a `field_mask`.
        'routes.distanceMeters',  # Agrega un literal a la estructura.
        'routes.duration',  # Agrega un literal a la estructura.
        'routes.staticDuration',  # Agrega un literal a la estructura.
        'routes.polyline.encodedPolyline',  # Agrega un literal a la estructura.
    ])  # Cierra la estructura.

    try:  # Inicia un bloque `try`.
        req = Request(  # Asigna a `req` el resultado de `Request`.
            f'https://routes.googleapis.com/directions/v2:computeRoutes?key={key}',  # Agrega un literal a la estructura.
            data=json.dumps(payload).encode('utf-8'),  # Asigna a `data` el resultado de `json.dumps`.
            headers={  # Asigna un valor a `headers`.
                'Accept': 'application/json',  # Agrega un literal a la estructura.
                'Content-Type': 'application/json',  # Agrega un literal a la estructura.
                'X-Goog-FieldMask': field_mask,  # Asigna la clave `X-Goog-FieldMask` en un diccionario.
            },  # Cierra el bloque/estructura.
            method='POST',  # Asigna un valor a `method`.
        )  # Cierra el bloque/estructura.
        with urlopen(req, timeout=8) as resp:  # Abre un contexto con `with`.
            data = json.loads(resp.read().decode('utf-8'))  # Asigna a `data` el resultado de `json.loads`.
    except Exception:  # Maneja una excepcion en `except`.
        return {'provider': 'google', 'routes': [], 'error': 'Routes API fallo.'}  # Devuelve un valor (`return`).

    normalized = []  # Asigna un valor a `normalized`.
    for route in (data.get('routes') or []):  # Itera en un bucle `for`.
        distance_m = route.get('distanceMeters')  # Asigna a `distance_m` el resultado de `route.get`.
        duration_raw = route.get('duration')  # Asigna a `duration_raw` el resultado de `route.get`.
        static_duration_raw = route.get('staticDuration')  # Asigna a `static_duration_raw` el resultado de `route.get`.
        encoded_polyline = (route.get('polyline') or {}).get('encodedPolyline') or ''  # Asigna un valor a `encoded_polyline`.
        normalized.append({  # Ejecuta `normalized.append`.
            'distance_meters': distance_m,  # Asigna la clave `distance_meters` en un diccionario.
            'distance_km': round(float(distance_m) / 1000, 2) if distance_m is not None else None,  # Asigna la clave `distance_km` con el resultado de `round`.
            'duration': duration_raw,  # Asigna la clave `duration` en un diccionario.
            'static_duration': static_duration_raw,  # Asigna la clave `static_duration` en un diccionario.
            'duration_seconds': parse_google_duration(duration_raw),  # Asigna la clave `duration_seconds` con el resultado de `parse_google_duration`.
            'static_duration_seconds': parse_google_duration(static_duration_raw),  # Asigna la clave `static_duration_seconds` con el resultado de `parse_google_duration`.
            'polyline': encoded_polyline,  # Asigna la clave `polyline` en un diccionario.
        })  # Cierra la estructura.

    return {'provider': 'google', 'routes': normalized}  # Devuelve un valor (`return`).


class GeoAutocompleteView(APIView):  # Define la clase `GeoAutocompleteView`.
    permission_classes = [permissions.IsAuthenticated]  # Asigna un valor a `permission_classes`.

    def _google_api_key(self):  # Define la funcion `_google_api_key`.
        return (getattr(settings, 'GOOGLE_MAPS_SERVER_API_KEY', '') or '').strip()  # Devuelve un valor (`return`).

    def _google_language(self):  # Define la funcion `_google_language`.
        return (getattr(settings, 'GOOGLE_MAPS_LANGUAGE', 'es') or 'es').strip()  # Devuelve un valor (`return`).

    def _google_region(self):  # Define la funcion `_google_region`.
        return (getattr(settings, 'GOOGLE_MAPS_REGION', 'ec') or 'ec').strip().lower()  # Devuelve un valor (`return`).

    def _http_json_get(self, endpoint, params, timeout=6):  # Define la funcion `_http_json_get`.
        req = Request(  # Asigna a `req` el resultado de `Request`.
            f"{endpoint}?{urlencode(params)}",  # Agrega un literal a la estructura.
            headers={  # Asigna un valor a `headers`.
                'Accept': 'application/json',  # Agrega un literal a la estructura.
            },  # Cierra el bloque/estructura.
        )  # Cierra el bloque/estructura.
        with urlopen(req, timeout=timeout) as resp:  # Abre un contexto con `with`.
            return json.loads(resp.read().decode('utf-8'))  # Devuelve un valor (`return`).

    def _extract_from_geocode_result(self, geocode_result):  # Define la funcion `_extract_from_geocode_result`.
        components = geocode_result.get('address_components') or []  # Asigna a `components` el resultado de `geocode_result.get`.
        values = {}  # Asigna un valor a `values`.
        for component in components:  # Itera en un bucle `for`.
            name = component.get('long_name') or ''  # Asigna a `name` el resultado de `component.get`.
            for ctype in component.get('types') or []:  # Itera en un bucle `for`.
                if ctype not in values:  # Evalua la condicion del `if`.
                    values[ctype] = name  # Asigna un valor a `values[ctype]`.

        road = values.get('route') or ''  # Asigna a `road` el resultado de `values.get`.
        house_number = values.get('street_number') or ''  # Asigna a `house_number` el resultado de `values.get`.
        main_address = (  # Asigna un valor a `main_address`.
            f"{road} {house_number}".strip()  # Aplica `.strip` a una cadena.
            or geocode_result.get('formatted_address', '').split(',')[0].strip()  # Continua la expresion con `or`.
        )  # Cierra el bloque/estructura.
        secondary_street = (  # Asigna un valor a `secondary_street`.
            values.get('sublocality')  # Ejecuta `values.get`.
            or values.get('sublocality_level_1')  # Continua la expresion con `or`.
            or values.get('neighborhood')  # Continua la expresion con `or`.
            or values.get('premise')  # Continua la expresion con `or`.
            or ''  # Continua la expresion con `or`.
        )  # Cierra el bloque/estructura.
        city = (  # Asigna un valor a `city`.
            values.get('locality')  # Ejecuta `values.get`.
            or values.get('administrative_area_level_2')  # Continua la expresion con `or`.
            or values.get('postal_town')  # Continua la expresion con `or`.
            or ''  # Continua la expresion con `or`.
        )  # Cierra el bloque/estructura.
        region = values.get('administrative_area_level_1') or ''  # Asigna a `region` el resultado de `values.get`.
        country_name = values.get('country') or ''  # Asigna a `country_name` el resultado de `values.get`.

        geometry = geocode_result.get('geometry') or {}  # Asigna a `geometry` el resultado de `geocode_result.get`.
        location = geometry.get('location') or {}  # Asigna a `location` el resultado de `geometry.get`.
        try:  # Inicia un bloque `try`.
            lat = float(location.get('lat')) if location.get('lat') is not None else None  # Asigna a `lat` el resultado de `float`.
        except (TypeError, ValueError):  # Maneja una excepcion en `except`.
            lat = None  # Asigna un valor a `lat`.
        try:  # Inicia un bloque `try`.
            lng = float(location.get('lng')) if location.get('lng') is not None else None  # Asigna a `lng` el resultado de `float`.
        except (TypeError, ValueError):  # Maneja una excepcion en `except`.
            lng = None  # Asigna un valor a `lng`.

        return {  # Devuelve un valor (`return`).
            'label': geocode_result.get('formatted_address', ''),  # Asigna la clave `label` con el resultado de `geocode_result.get`.
            'main_address': main_address,  # Asigna la clave `main_address` en un diccionario.
            'secondary_street': secondary_street,  # Asigna la clave `secondary_street` en un diccionario.
            'city': city,  # Asigna la clave `city` en un diccionario.
            'region': region,  # Asigna la clave `region` en un diccionario.
            'country': country_name,  # Asigna la clave `country` en un diccionario.
            'lat': lat,  # Asigna la clave `lat` en un diccionario.
            'lng': lng,  # Asigna la clave `lng` en un diccionario.
        }  # Cierra el bloque/estructura.

    def _geocode_place_id(self, place_id):  # Define la funcion `_geocode_place_id`.
        key = self._google_api_key()  # Asigna a `key` el resultado de `self._google_api_key`.
        if not key or not place_id:  # Evalua la condicion del `if`.
            return None  # Devuelve un valor (`return`).
        params = {  # Asigna un valor a `params`.
            'place_id': place_id,  # Asigna la clave `place_id` en un diccionario.
            'language': self._google_language(),  # Asigna la clave `language` con el resultado de `self._google_language`.
            'key': key,  # Asigna la clave `key` en un diccionario.
        }  # Cierra el bloque/estructura.
        payload = self._http_json_get(  # Asigna a `payload` el resultado de `self._http_json_get`.
            'https://maps.googleapis.com/maps/api/geocode/json',  # Agrega un literal a la estructura.
            params,  # Referencia `params` en la estructura/expresion.
        )  # Cierra el bloque/estructura.
        if payload.get('status') != 'OK':  # Evalua la condicion del `if`.
            return None  # Devuelve un valor (`return`).
        results = payload.get('results') or []  # Asigna a `results` el resultado de `payload.get`.
        if not results:  # Evalua la condicion del `if`.
            return None  # Devuelve un valor (`return`).
        return self._extract_from_geocode_result(results[0])  # Devuelve un valor (`return`).

    def get(self, request):  # Define la funcion `get`.
        query = (request.query_params.get('q') or request.query_params.get('query') or '').strip()  # Asigna un valor a `query`.
        if len(query) < 3:  # Evalua la condicion del `if`.
            return Response({'results': [], 'provider': geo_provider()})  # Devuelve un valor (`return`).

        country = (request.query_params.get('country') or self._google_region()).strip().lower()  # Asigna un valor a `country`.
        try:  # Inicia un bloque `try`.
            limit = int(request.query_params.get('limit', 5))  # Asigna a `limit` el resultado de `int`.
        except (TypeError, ValueError):  # Maneja una excepcion en `except`.
            limit = 5  # Asigna un valor a `limit`.
        limit = max(1, min(limit, 10))  # Asigna a `limit` el resultado de `max`.

        if geo_provider() != 'google':  # Evalua la condicion del `if`.
            params = {  # Asigna un valor a `params`.
                'format': 'jsonv2',  # Agrega un literal a la estructura.
                'addressdetails': 1,  # Asigna la clave `addressdetails` en un diccionario.
                'countrycodes': country,  # Asigna la clave `countrycodes` en un diccionario.
                'limit': limit,  # Asigna la clave `limit` en un diccionario.
                'q': query,  # Asigna la clave `q` en un diccionario.
            }  # Cierra el bloque/estructura.
            try:  # Inicia un bloque `try`.
                payload = http_json_get(  # Asigna a `payload` el resultado de `http_json_get`.
                    f'{osm_nominatim_base_url()}/search',  # Agrega un literal a la estructura.
                    params,  # Referencia `params` en la estructura/expresion.
                    headers={  # Asigna un valor a `headers`.
                        'User-Agent': geocoder_user_agent(),  # Asigna la clave `User-Agent` con el resultado de `geocoder_user_agent`.
                        'Accept': 'application/json',  # Agrega un literal a la estructura.
                    }  # Cierra el bloque/estructura.
                ) or []  # Usa `[]` como valor por defecto si la expresion es falsy.
            except Exception:  # Maneja una excepcion en `except`.
                return Response({'results': [], 'provider': 'osm'})  # Devuelve un valor (`return`).

            results = [extract_nominatim_result(item) for item in payload]  # Asigna un valor a `results`.
            return Response({'results': results, 'provider': 'osm'})  # Devuelve un valor (`return`).

        key = self._google_api_key()  # Asigna a `key` el resultado de `self._google_api_key`.
        if not key:  # Evalua la condicion del `if`.
            return Response(  # Devuelve un valor (`return`).
                {  # Inicia una estructura literal.
                    'results': [],  # Asigna la clave `results` con una lista.
                    'provider': 'google',  # Agrega un literal a la estructura.
                    'error': 'Falta configurar GOOGLE_MAPS_SERVER_API_KEY en el backend.',  # Agrega un literal a la estructura.
                },  # Cierra el bloque/estructura.
                status=status.HTTP_503_SERVICE_UNAVAILABLE  # Asigna un valor a `status`.
            )  # Cierra el bloque/estructura.

        params = {  # Asigna un valor a `params`.
            'input': query,  # Asigna la clave `input` en un diccionario.
            'language': self._google_language(),  # Asigna la clave `language` con el resultado de `self._google_language`.
            'components': f'country:{country}',  # Agrega un literal a la estructura.
            'types': 'address',  # Agrega un literal a la estructura.
            'key': key,  # Asigna la clave `key` en un diccionario.
        }  # Cierra el bloque/estructura.
        try:  # Inicia un bloque `try`.
            payload = self._http_json_get(  # Asigna a `payload` el resultado de `self._http_json_get`.
                'https://maps.googleapis.com/maps/api/place/autocomplete/json',  # Agrega un literal a la estructura.
                params,  # Referencia `params` en la estructura/expresion.
            )  # Cierra el bloque/estructura.
        except Exception:  # Maneja una excepcion en `except`.
            return Response({'results': [], 'provider': 'google'})  # Devuelve un valor (`return`).

        status_name = payload.get('status')  # Asigna a `status_name` el resultado de `payload.get`.
        if status_name not in {'OK', 'ZERO_RESULTS'}:  # Evalua la condicion del `if`.
            return Response({  # Devuelve un valor (`return`).
                'results': [],  # Asigna la clave `results` con una lista.
                'provider': 'google',  # Agrega un literal a la estructura.
                'error': payload.get('error_message') or status_name or 'Autocomplete fallo.',  # Agrega un literal a la estructura.
            })  # Cierra la estructura.

        predictions = (payload.get('predictions') or [])[:limit]  # Asigna un valor a `predictions`.
        results = []  # Asigna un valor a `results`.
        for item in predictions:  # Itera en un bucle `for`.
            place_id = item.get('place_id') or ''  # Asigna a `place_id` el resultado de `item.get`.
            geocoded = self._geocode_place_id(place_id) or {}  # Asigna a `geocoded` el resultado de `self._geocode_place_id`.
            label = item.get('description') or geocoded.get('label') or ''  # Asigna a `label` el resultado de `item.get`.
            structured = item.get('structured_formatting') or {}  # Asigna a `structured` el resultado de `item.get`.
            main_text = structured.get('main_text') or ''  # Asigna a `main_text` el resultado de `structured.get`.
            secondary_text = structured.get('secondary_text') or ''  # Asigna a `secondary_text` el resultado de `structured.get`.

            results.append({  # Ejecuta `results.append`.
                'place_id': place_id,  # Asigna la clave `place_id` en un diccionario.
                'label': label,  # Asigna la clave `label` en un diccionario.
                'main_text': main_text,  # Asigna la clave `main_text` en un diccionario.
                'secondary_text': secondary_text,  # Asigna la clave `secondary_text` en un diccionario.
                'main_address': geocoded.get('main_address') or main_text or label,  # Asigna la clave `main_address` con el resultado de `geocoded.get`.
                'secondary_street': geocoded.get('secondary_street') or secondary_text or '',  # Agrega un literal a la estructura.
                'city': geocoded.get('city') or '',  # Agrega un literal a la estructura.
                'region': geocoded.get('region') or '',  # Agrega un literal a la estructura.
                'country': geocoded.get('country') or '',  # Agrega un literal a la estructura.
                'lat': geocoded.get('lat'),  # Asigna la clave `lat` con el resultado de `geocoded.get`.
                'lng': geocoded.get('lng'),  # Asigna la clave `lng` con el resultado de `geocoded.get`.
            })  # Cierra la estructura.

        return Response({'results': results, 'provider': 'google'})  # Devuelve un valor (`return`).


class GeoGeocodeView(APIView):  # Define la clase `GeoGeocodeView`.
    permission_classes = [permissions.IsAuthenticated]  # Asigna un valor a `permission_classes`.

    def _google_api_key(self):  # Define la funcion `_google_api_key`.
        return (getattr(settings, 'GOOGLE_MAPS_SERVER_API_KEY', '') or '').strip()  # Devuelve un valor (`return`).

    def _google_language(self):  # Define la funcion `_google_language`.
        return (getattr(settings, 'GOOGLE_MAPS_LANGUAGE', 'es') or 'es').strip()  # Devuelve un valor (`return`).

    def _http_json_get(self, endpoint, params, timeout=6):  # Define la funcion `_http_json_get`.
        req = Request(  # Asigna a `req` el resultado de `Request`.
            f"{endpoint}?{urlencode(params)}",  # Agrega un literal a la estructura.
            headers={  # Asigna un valor a `headers`.
                'Accept': 'application/json',  # Agrega un literal a la estructura.
            },  # Cierra el bloque/estructura.
        )  # Cierra el bloque/estructura.
        with urlopen(req, timeout=timeout) as resp:  # Abre un contexto con `with`.
            return json.loads(resp.read().decode('utf-8'))  # Devuelve un valor (`return`).

    def _extract_from_geocode_result(self, geocode_result):  # Define la funcion `_extract_from_geocode_result`.
        components = geocode_result.get('address_components') or []  # Asigna a `components` el resultado de `geocode_result.get`.
        values = {}  # Asigna un valor a `values`.
        for component in components:  # Itera en un bucle `for`.
            name = component.get('long_name') or ''  # Asigna a `name` el resultado de `component.get`.
            for ctype in component.get('types') or []:  # Itera en un bucle `for`.
                if ctype not in values:  # Evalua la condicion del `if`.
                    values[ctype] = name  # Asigna un valor a `values[ctype]`.

        road = values.get('route') or ''  # Asigna a `road` el resultado de `values.get`.
        house_number = values.get('street_number') or ''  # Asigna a `house_number` el resultado de `values.get`.
        main_address = (  # Asigna un valor a `main_address`.
            f"{road} {house_number}".strip()  # Aplica `.strip` a una cadena.
            or geocode_result.get('formatted_address', '').split(',')[0].strip()  # Continua la expresion con `or`.
        )  # Cierra el bloque/estructura.
        secondary_street = (  # Asigna un valor a `secondary_street`.
            values.get('sublocality')  # Ejecuta `values.get`.
            or values.get('sublocality_level_1')  # Continua la expresion con `or`.
            or values.get('neighborhood')  # Continua la expresion con `or`.
            or values.get('premise')  # Continua la expresion con `or`.
            or ''  # Continua la expresion con `or`.
        )  # Cierra el bloque/estructura.
        city = (  # Asigna un valor a `city`.
            values.get('locality')  # Ejecuta `values.get`.
            or values.get('administrative_area_level_2')  # Continua la expresion con `or`.
            or values.get('postal_town')  # Continua la expresion con `or`.
            or ''  # Continua la expresion con `or`.
        )  # Cierra el bloque/estructura.
        region = values.get('administrative_area_level_1') or ''  # Asigna a `region` el resultado de `values.get`.
        country_name = values.get('country') or ''  # Asigna a `country_name` el resultado de `values.get`.

        geometry = geocode_result.get('geometry') or {}  # Asigna a `geometry` el resultado de `geocode_result.get`.
        location = geometry.get('location') or {}  # Asigna a `location` el resultado de `geometry.get`.
        try:  # Inicia un bloque `try`.
            lat = float(location.get('lat')) if location.get('lat') is not None else None  # Asigna a `lat` el resultado de `float`.
        except (TypeError, ValueError):  # Maneja una excepcion en `except`.
            lat = None  # Asigna un valor a `lat`.
        try:  # Inicia un bloque `try`.
            lng = float(location.get('lng')) if location.get('lng') is not None else None  # Asigna a `lng` el resultado de `float`.
        except (TypeError, ValueError):  # Maneja una excepcion en `except`.
            lng = None  # Asigna un valor a `lng`.

        return {  # Devuelve un valor (`return`).
            'place_id': geocode_result.get('place_id') or '',  # Agrega un literal a la estructura.
            'label': geocode_result.get('formatted_address', ''),  # Asigna la clave `label` con el resultado de `geocode_result.get`.
            'main_address': main_address,  # Asigna la clave `main_address` en un diccionario.
            'secondary_street': secondary_street,  # Asigna la clave `secondary_street` en un diccionario.
            'city': city,  # Asigna la clave `city` en un diccionario.
            'region': region,  # Asigna la clave `region` en un diccionario.
            'country': country_name,  # Asigna la clave `country` en un diccionario.
            'lat': lat,  # Asigna la clave `lat` en un diccionario.
            'lng': lng,  # Asigna la clave `lng` en un diccionario.
        }  # Cierra el bloque/estructura.

    def get(self, request):  # Define la funcion `get`.
        place_id = (request.query_params.get('place_id') or '').strip()  # Asigna un valor a `place_id`.
        address = (request.query_params.get('q') or request.query_params.get('address') or '').strip()  # Asigna un valor a `address`.
        lat = (request.query_params.get('lat') or '').strip()  # Asigna un valor a `lat`.
        lng = (request.query_params.get('lng') or '').strip()  # Asigna un valor a `lng`.

        if geo_provider() != 'google':  # Evalua la condicion del `if`.
            try:  # Inicia un bloque `try`.
                if lat and lng:  # Evalua la condicion del `if`.
                    payload = http_json_get(  # Asigna a `payload` el resultado de `http_json_get`.
                        f'{osm_nominatim_base_url()}/reverse',  # Agrega un literal a la estructura.
                        {  # Inicia una estructura literal.
                            'format': 'jsonv2',  # Agrega un literal a la estructura.
                            'addressdetails': 1,  # Asigna la clave `addressdetails` en un diccionario.
                            'lat': lat,  # Asigna la clave `lat` en un diccionario.
                            'lon': lng,  # Asigna la clave `lon` en un diccionario.
                        },  # Cierra el bloque/estructura.
                        headers={  # Asigna un valor a `headers`.
                            'User-Agent': geocoder_user_agent(),  # Asigna la clave `User-Agent` con el resultado de `geocoder_user_agent`.
                            'Accept': 'application/json',  # Agrega un literal a la estructura.
                        }  # Cierra el bloque/estructura.
                    )  # Cierra el bloque/estructura.
                    raw_results = [payload] if isinstance(payload, dict) else []  # Asigna un valor a `raw_results`.
                elif address:  # Evalua la condicion del `elif`.
                    raw_results = http_json_get(  # Asigna a `raw_results` el resultado de `http_json_get`.
                        f'{osm_nominatim_base_url()}/search',  # Agrega un literal a la estructura.
                        {  # Inicia una estructura literal.
                            'format': 'jsonv2',  # Agrega un literal a la estructura.
                            'addressdetails': 1,  # Asigna la clave `addressdetails` en un diccionario.
                            'limit': 5,  # Asigna la clave `limit` en un diccionario.
                            'q': address,  # Asigna la clave `q` en un diccionario.
                        },  # Cierra el bloque/estructura.
                        headers={  # Asigna un valor a `headers`.
                            'User-Agent': geocoder_user_agent(),  # Asigna la clave `User-Agent` con el resultado de `geocoder_user_agent`.
                            'Accept': 'application/json',  # Agrega un literal a la estructura.
                        }  # Cierra el bloque/estructura.
                    ) or []  # Usa `[]` como valor por defecto si la expresion es falsy.
                elif place_id:  # Evalua la condicion del `elif`.
                    raw_results = http_json_get(  # Asigna a `raw_results` el resultado de `http_json_get`.
                        f'{osm_nominatim_base_url()}/lookup',  # Agrega un literal a la estructura.
                        {  # Inicia una estructura literal.
                            'format': 'jsonv2',  # Agrega un literal a la estructura.
                            'addressdetails': 1,  # Asigna la clave `addressdetails` en un diccionario.
                            'place_ids': place_id,  # Asigna la clave `place_ids` en un diccionario.
                        },  # Cierra el bloque/estructura.
                        headers={  # Asigna un valor a `headers`.
                            'User-Agent': geocoder_user_agent(),  # Asigna la clave `User-Agent` con el resultado de `geocoder_user_agent`.
                            'Accept': 'application/json',  # Agrega un literal a la estructura.
                        }  # Cierra el bloque/estructura.
                    ) or []  # Usa `[]` como valor por defecto si la expresion es falsy.
                else:  # Ejecuta la rama `else`.
                    return Response(  # Devuelve un valor (`return`).
                        {'error': 'Debes enviar place_id, q/address o lat+lng.'},  # Define un diccionario literal.
                        status=status.HTTP_400_BAD_REQUEST  # Asigna un valor a `status`.
                    )  # Cierra el bloque/estructura.
            except Exception:  # Maneja una excepcion en `except`.
                return Response({'results': [], 'provider': 'osm'})  # Devuelve un valor (`return`).

            results = [extract_nominatim_result(item) for item in raw_results]  # Asigna un valor a `results`.
            return Response({'results': results, 'provider': 'osm'})  # Devuelve un valor (`return`).

        key = self._google_api_key()  # Asigna a `key` el resultado de `self._google_api_key`.
        if not key:  # Evalua la condicion del `if`.
            return Response(  # Devuelve un valor (`return`).
                {  # Inicia una estructura literal.
                    'results': [],  # Asigna la clave `results` con una lista.
                    'provider': 'google',  # Agrega un literal a la estructura.
                    'error': 'Falta configurar GOOGLE_MAPS_SERVER_API_KEY en el backend.',  # Agrega un literal a la estructura.
                },  # Cierra el bloque/estructura.
                status=status.HTTP_503_SERVICE_UNAVAILABLE  # Asigna un valor a `status`.
            )  # Cierra el bloque/estructura.

        params = {  # Asigna un valor a `params`.
            'language': self._google_language(),  # Asigna la clave `language` con el resultado de `self._google_language`.
            'key': key,  # Asigna la clave `key` en un diccionario.
        }  # Cierra el bloque/estructura.

        if place_id:  # Evalua la condicion del `if`.
            params['place_id'] = place_id  # Asigna un valor a `params['place_id']`.
        elif address:  # Evalua la condicion del `elif`.
            params['address'] = address  # Asigna un valor a `params['address']`.
        elif lat and lng:  # Evalua la condicion del `elif`.
            params['latlng'] = f'{lat},{lng}'  # Asigna un valor a `params['latlng']`.
        else:  # Ejecuta la rama `else`.
            return Response(  # Devuelve un valor (`return`).
                {'error': 'Debes enviar place_id, q/address o lat+lng.'},  # Define un diccionario literal.
                status=status.HTTP_400_BAD_REQUEST  # Asigna un valor a `status`.
            )  # Cierra el bloque/estructura.

        try:  # Inicia un bloque `try`.
            payload = self._http_json_get(  # Asigna a `payload` el resultado de `self._http_json_get`.
                'https://maps.googleapis.com/maps/api/geocode/json',  # Agrega un literal a la estructura.
                params,  # Referencia `params` en la estructura/expresion.
            )  # Cierra el bloque/estructura.
        except Exception:  # Maneja una excepcion en `except`.
            return Response({'results': [], 'provider': 'google'})  # Devuelve un valor (`return`).

        status_name = payload.get('status')  # Asigna a `status_name` el resultado de `payload.get`.
        if status_name not in {'OK', 'ZERO_RESULTS'}:  # Evalua la condicion del `if`.
            return Response({  # Devuelve un valor (`return`).
                'results': [],  # Asigna la clave `results` con una lista.
                'provider': 'google',  # Agrega un literal a la estructura.
                'error': payload.get('error_message') or status_name or 'Geocoding fallo.',  # Agrega un literal a la estructura.
            })  # Cierra la estructura.

        results = [  # Asigna un valor a `results`.
            self._extract_from_geocode_result(item)  # Ejecuta `self._extract_from_geocode_result`.
            for item in (payload.get('results') or [])  # Itera en un bucle `for`.
        ]  # Cierra el bloque/estructura.
        return Response({'results': results, 'provider': 'google'})  # Devuelve un valor (`return`).


class GeoAddressValidationView(APIView):  # Define la clase `GeoAddressValidationView`.
    permission_classes = [permissions.IsAuthenticated]  # Asigna un valor a `permission_classes`.

    def _google_api_key(self):  # Define la funcion `_google_api_key`.
        return (getattr(settings, 'GOOGLE_MAPS_SERVER_API_KEY', '') or '').strip()  # Devuelve un valor (`return`).

    def _google_region(self):  # Define la funcion `_google_region`.
        return (getattr(settings, 'GOOGLE_MAPS_REGION', 'EC') or 'EC').strip().upper()  # Devuelve un valor (`return`).

    def _http_json_post(self, endpoint, payload, timeout=8):  # Define la funcion `_http_json_post`.
        req = Request(  # Asigna a `req` el resultado de `Request`.
            endpoint,  # Referencia `endpoint` en la estructura/expresion.
            data=json.dumps(payload).encode('utf-8'),  # Asigna a `data` el resultado de `json.dumps`.
            headers={  # Asigna un valor a `headers`.
                'Accept': 'application/json',  # Agrega un literal a la estructura.
                'Content-Type': 'application/json',  # Agrega un literal a la estructura.
            },  # Cierra el bloque/estructura.
            method='POST',  # Asigna un valor a `method`.
        )  # Cierra el bloque/estructura.
        with urlopen(req, timeout=timeout) as resp:  # Abre un contexto con `with`.
            return json.loads(resp.read().decode('utf-8'))  # Devuelve un valor (`return`).

    def post(self, request):  # Define la funcion `post`.
        address = (request.data.get('address') or '').strip()  # Asigna un valor a `address`.
        if not address:  # Evalua la condicion del `if`.
            address = (  # Asigna un valor a `address`.
                request.data.get('main_address')  # Ejecuta `request.data.get`.
                or request.data.get('full_address')  # Continua la expresion con `or`.
                or request.data.get('q')  # Continua la expresion con `or`.
                or ''  # Continua la expresion con `or`.
            ).strip()  # Continua el encadenamiento y llama `.strip`.

        if not address:  # Evalua la condicion del `if`.
            return Response(  # Devuelve un valor (`return`).
                {'error': 'Debes enviar address/main_address/full_address.'},  # Define un diccionario literal.
                status=status.HTTP_400_BAD_REQUEST  # Asigna un valor a `status`.
            )  # Cierra el bloque/estructura.

        secondary = (request.data.get('secondary_street') or '').strip()  # Asigna un valor a `secondary`.
        city = (request.data.get('city') or '').strip()  # Asigna un valor a `city`.
        region = (request.data.get('region') or '').strip()  # Asigna un valor a `region`.
        country = (request.data.get('country') or self._google_region()).strip()  # Asigna un valor a `country`.

        if geo_provider() != 'google':  # Evalua la condicion del `if`.
            query = ', '.join([part for part in [address, secondary, city, region, country] if part]).strip()  # Asigna un valor a `query`.
            try:  # Inicia un bloque `try`.
                payload = http_json_get(  # Asigna a `payload` el resultado de `http_json_get`.
                    f'{osm_nominatim_base_url()}/search',  # Agrega un literal a la estructura.
                    {  # Inicia una estructura literal.
                        'format': 'jsonv2',  # Agrega un literal a la estructura.
                        'addressdetails': 1,  # Asigna la clave `addressdetails` en un diccionario.
                        'limit': 1,  # Asigna la clave `limit` en un diccionario.
                        'q': query,  # Asigna la clave `q` en un diccionario.
                    },  # Cierra el bloque/estructura.
                    headers={  # Asigna un valor a `headers`.
                        'User-Agent': geocoder_user_agent(),  # Asigna la clave `User-Agent` con el resultado de `geocoder_user_agent`.
                        'Accept': 'application/json',  # Agrega un literal a la estructura.
                    }  # Cierra el bloque/estructura.
                ) or []  # Usa `[]` como valor por defecto si la expresion es falsy.
            except Exception:  # Maneja una excepcion en `except`.
                return Response({'provider': 'osm', 'valid': False, 'error': 'Address Validation fallo.'})  # Devuelve un valor (`return`).

            first = payload[0] if payload else None  # Asigna un valor a `first`.
            if not first:  # Evalua la condicion del `if`.
                return Response({  # Devuelve un valor (`return`).
                    'provider': 'osm',  # Agrega un literal a la estructura.
                    'valid': False,  # Asigna la clave `valid` en un diccionario.
                    'address_complete': False,  # Asigna la clave `address_complete` en un diccionario.
                    'formatted_address': '',  # Agrega un literal a la estructura.
                    'place_id': '',  # Agrega un literal a la estructura.
                    'lat': None,  # Asigna la clave `lat` en un diccionario.
                    'lng': None,  # Asigna la clave `lng` en un diccionario.
                    'raw': payload,  # Asigna la clave `raw` en un diccionario.
                })  # Cierra la estructura.

            parsed = extract_nominatim_result(first)  # Asigna a `parsed` el resultado de `extract_nominatim_result`.
            importance = first.get('importance')  # Asigna a `importance` el resultado de `first.get`.
            try:  # Inicia un bloque `try`.
                importance = float(importance) if importance is not None else None  # Asigna a `importance` el resultado de `float`.
            except (TypeError, ValueError):  # Maneja una excepcion en `except`.
                importance = None  # Asigna un valor a `importance`.

            return Response({  # Devuelve un valor (`return`).
                'provider': 'osm',  # Agrega un literal a la estructura.
                'valid': True,  # Asigna la clave `valid` en un diccionario.
                'address_complete': True,  # Asigna la clave `address_complete` en un diccionario.
                'has_inferred_components': False,  # Asigna la clave `has_inferred_components` en un diccionario.
                'has_unconfirmed_components': False,  # Asigna la clave `has_unconfirmed_components` en un diccionario.
                'formatted_address': parsed.get('label') or '',  # Agrega un literal a la estructura.
                'place_id': parsed.get('place_id') or '',  # Agrega un literal a la estructura.
                'lat': parsed.get('lat'),  # Asigna la clave `lat` con el resultado de `parsed.get`.
                'lng': parsed.get('lng'),  # Asigna la clave `lng` con el resultado de `parsed.get`.
                'confidence': importance,  # Asigna la clave `confidence` en un diccionario.
                'raw': payload,  # Asigna la clave `raw` en un diccionario.
            })  # Cierra la estructura.

        key = self._google_api_key()  # Asigna a `key` el resultado de `self._google_api_key`.
        if not key:  # Evalua la condicion del `if`.
            return Response(  # Devuelve un valor (`return`).
                {  # Inicia una estructura literal.
                    'provider': 'google',  # Agrega un literal a la estructura.
                    'error': 'Falta configurar GOOGLE_MAPS_SERVER_API_KEY en el backend.',  # Agrega un literal a la estructura.
                },  # Cierra el bloque/estructura.
                status=status.HTTP_503_SERVICE_UNAVAILABLE  # Asigna un valor a `status`.
            )  # Cierra el bloque/estructura.

        lines = [address]  # Asigna un valor a `lines`.
        if secondary:  # Evalua la condicion del `if`.
            lines.append(secondary)  # Ejecuta `lines.append`.
        if city:  # Evalua la condicion del `if`.
            lines.append(city)  # Ejecuta `lines.append`.
        if region:  # Evalua la condicion del `if`.
            lines.append(region)  # Ejecuta `lines.append`.
        if country:  # Evalua la condicion del `if`.
            lines.append(country)  # Ejecuta `lines.append`.

        payload = {  # Asigna un valor a `payload`.
            'address': {  # Asigna la clave `address` con un diccionario.
                'addressLines': lines,  # Asigna la clave `addressLines` en un diccionario.
                'regionCode': self._google_region(),  # Asigna la clave `regionCode` con el resultado de `self._google_region`.
            }  # Cierra el bloque/estructura.
        }  # Cierra el bloque/estructura.
        if country:  # Evalua la condicion del `if`.
            payload['address']['regionCode'] = country[:2].upper()  # Asigna `regionCode` usando las 2 primeras letras del pais.

        try:  # Inicia un bloque `try`.
            data = self._http_json_post(  # Asigna a `data` el resultado de `self._http_json_post`.
                f'https://addressvalidation.googleapis.com/v1:validateAddress?key={key}',  # Agrega un literal a la estructura.
                payload,  # Referencia `payload` en la estructura/expresion.
            )  # Cierra el bloque/estructura.
        except Exception:  # Maneja una excepcion en `except`.
            return Response({'provider': 'google', 'valid': False, 'error': 'Address Validation fallo.'})  # Devuelve un valor (`return`).

        verdict = data.get('result', {}).get('verdict', {})  # Asigna a `verdict` el resultado de `data.get`.
        geocode = data.get('result', {}).get('geocode', {})  # Asigna a `geocode` el resultado de `data.get`.
        location = geocode.get('location') or {}  # Asigna a `location` el resultado de `geocode.get`.
        address_info = data.get('result', {}).get('address', {})  # Asigna a `address_info` el resultado de `data.get`.

        try:  # Inicia un bloque `try`.
            lat = float(location.get('latitude')) if location.get('latitude') is not None else None  # Asigna a `lat` el resultado de `float`.
        except (TypeError, ValueError):  # Maneja una excepcion en `except`.
            lat = None  # Asigna un valor a `lat`.
        try:  # Inicia un bloque `try`.
            lng = float(location.get('longitude')) if location.get('longitude') is not None else None  # Asigna a `lng` el resultado de `float`.
        except (TypeError, ValueError):  # Maneja una excepcion en `except`.
            lng = None  # Asigna un valor a `lng`.

        is_valid = bool(verdict.get('addressComplete')) or bool(verdict.get('validationGranularity'))  # Asigna a `is_valid` el resultado de `bool`.

        return Response({  # Devuelve un valor (`return`).
            'provider': 'google',  # Agrega un literal a la estructura.
            'valid': is_valid,  # Asigna la clave `valid` en un diccionario.
            'address_complete': bool(verdict.get('addressComplete')),  # Asigna la clave `address_complete` con el resultado de `bool`.
            'has_inferred_components': bool(verdict.get('hasInferredComponents')),  # Asigna la clave `has_inferred_components` con el resultado de `bool`.
            'has_unconfirmed_components': bool(verdict.get('hasUnconfirmedComponents')),  # Asigna la clave `has_unconfirmed_components` con el resultado de `bool`.
            'formatted_address': address_info.get('formattedAddress') or '',  # Agrega un literal a la estructura.
            'place_id': geocode.get('placeId') or '',  # Agrega un literal a la estructura.
            'lat': lat,  # Asigna la clave `lat` en un diccionario.
            'lng': lng,  # Asigna la clave `lng` en un diccionario.
            'raw': data,  # Asigna la clave `raw` en un diccionario.
        })  # Cierra la estructura.


class GeoRouteEstimateView(APIView):  # Define la clase `GeoRouteEstimateView`.
    permission_classes = [permissions.IsAuthenticated]  # Asigna un valor a `permission_classes`.

    def _google_api_key(self):  # Define la funcion `_google_api_key`.
        return (getattr(settings, 'GOOGLE_MAPS_SERVER_API_KEY', '') or '').strip()  # Devuelve un valor (`return`).

    def _http_json_post(self, endpoint, payload, field_mask, timeout=8):  # Define la funcion `_http_json_post`.
        req = Request(  # Asigna a `req` el resultado de `Request`.
            endpoint,  # Referencia `endpoint` en la estructura/expresion.
            data=json.dumps(payload).encode('utf-8'),  # Asigna a `data` el resultado de `json.dumps`.
            headers={  # Asigna un valor a `headers`.
                'Accept': 'application/json',  # Agrega un literal a la estructura.
                'Content-Type': 'application/json',  # Agrega un literal a la estructura.
                'X-Goog-FieldMask': field_mask,  # Asigna la clave `X-Goog-FieldMask` en un diccionario.
            },  # Cierra el bloque/estructura.
            method='POST',  # Asigna un valor a `method`.
        )  # Cierra el bloque/estructura.
        with urlopen(req, timeout=timeout) as resp:  # Abre un contexto con `with`.
            return json.loads(resp.read().decode('utf-8'))  # Devuelve un valor (`return`).

    def post(self, request):  # Define la funcion `post`.
        origin = request.data.get('origin') or {}  # Asigna a `origin` el resultado de `request.data.get`.
        destination = request.data.get('destination') or {}  # Asigna a `destination` el resultado de `request.data.get`.
        mode = (request.data.get('travel_mode') or 'DRIVE').strip().upper()  # Asigna un valor a `mode`.

        if not isinstance(origin, dict) or not isinstance(destination, dict):  # Evalua la condicion del `if`.
            return Response(  # Devuelve un valor (`return`).
                {'error': 'origin y destination deben ser objetos con lat/lng.'},  # Define un diccionario literal.
                status=status.HTTP_400_BAD_REQUEST  # Asigna un valor a `status`.
            )  # Cierra el bloque/estructura.

        if origin.get('lat') is None or origin.get('lng') is None:  # Evalua la condicion del `if`.
            return Response({'error': 'origin.lat y origin.lng son obligatorios.'}, status=status.HTTP_400_BAD_REQUEST)  # Devuelve un valor (`return`).
        if destination.get('lat') is None or destination.get('lng') is None:  # Evalua la condicion del `if`.
            return Response(  # Devuelve un valor (`return`).
                {'error': 'destination.lat y destination.lng son obligatorios.'},  # Define un diccionario literal.
                status=status.HTTP_400_BAD_REQUEST  # Asigna un valor a `status`.
            )  # Cierra el bloque/estructura.

        if geo_provider() != 'google':  # Evalua la condicion del `if`.
            profile_map = {  # Asigna un valor a `profile_map`.
                'DRIVE': 'driving',  # Agrega un literal a la estructura.
                'WALK': 'walking',  # Agrega un literal a la estructura.
                'BICYCLE': 'cycling',  # Agrega un literal a la estructura.
                'TWO_WHEELER': 'driving',  # Agrega un literal a la estructura.
            }  # Cierra el bloque/estructura.
            profile = profile_map.get(mode, 'driving')  # Asigna a `profile` el resultado de `profile_map.get`.
            try:  # Inicia un bloque `try`.
                orig_lat = float(origin['lat'])  # Asigna a `orig_lat` el resultado de `float`.
                orig_lng = float(origin['lng'])  # Asigna a `orig_lng` el resultado de `float`.
                dst_lat = float(destination['lat'])  # Asigna a `dst_lat` el resultado de `float`.
                dst_lng = float(destination['lng'])  # Asigna a `dst_lng` el resultado de `float`.
            except (TypeError, ValueError):  # Maneja una excepcion en `except`.
                return Response({'error': 'lat/lng deben ser numericos.'}, status=status.HTTP_400_BAD_REQUEST)  # Devuelve un valor (`return`).

            endpoint = (  # Asigna un valor a `endpoint`.
                f"{osm_router_base_url()}/route/v1/{profile}/"  # Agrega un literal a la estructura.
                f"{orig_lng},{orig_lat};{dst_lng},{dst_lat}"  # Agrega un literal a la estructura.
            )  # Cierra el bloque/estructura.
            try:  # Inicia un bloque `try`.
                data = http_json_get(  # Asigna a `data` el resultado de `http_json_get`.
                    endpoint,  # Referencia `endpoint` en la estructura/expresion.
                    {  # Inicia una estructura literal.
                        'overview': 'full',  # Agrega un literal a la estructura.
                        'geometries': 'polyline',  # Agrega un literal a la estructura.
                        'alternatives': str(bool(request.data.get('alternatives', False))).lower(),  # Asigna la clave `alternatives` con el resultado de `str`.
                        'steps': 'false',  # Agrega un literal a la estructura.
                    },  # Cierra el bloque/estructura.
                    headers={'Accept': 'application/json'}  # Asigna un valor a `headers`.
                )  # Cierra el bloque/estructura.
            except Exception:  # Maneja una excepcion en `except`.
                return Response({'provider': 'osm', 'routes': [], 'error': 'Routes API fallo.'})  # Devuelve un valor (`return`).

            if (data or {}).get('code') != 'Ok':  # Evalua la condicion del `if`.
                return Response({  # Devuelve un valor (`return`).
                    'provider': 'osm',  # Agrega un literal a la estructura.
                    'routes': [],  # Asigna la clave `routes` con una lista.
                    'error': (data or {}).get('message') or 'No se pudo calcular la ruta.',  # Agrega un literal a la estructura.
                    'raw': data,  # Asigna la clave `raw` en un diccionario.
                })  # Cierra la estructura.

            routes = data.get('routes') or []  # Asigna a `routes` el resultado de `data.get`.
            normalized = []  # Asigna un valor a `normalized`.
            for route in routes:  # Itera en un bucle `for`.
                distance_m = route.get('distance')  # Asigna a `distance_m` el resultado de `route.get`.
                duration_sec = route.get('duration')  # Asigna a `duration_sec` el resultado de `route.get`.
                normalized.append({  # Ejecuta `normalized.append`.
                    'distance_meters': distance_m,  # Asigna la clave `distance_meters` en un diccionario.
                    'distance_km': round(float(distance_m) / 1000, 2) if distance_m is not None else None,  # Asigna la clave `distance_km` con el resultado de `round`.
                    'duration': f'{duration_sec}s' if duration_sec is not None else None,  # Asigna la clave `duration` en un diccionario.
                    'static_duration': f'{duration_sec}s' if duration_sec is not None else None,  # Asigna la clave `static_duration` en un diccionario.
                    'duration_seconds': int(duration_sec) if duration_sec is not None else None,  # Asigna la clave `duration_seconds` con el resultado de `int`.
                    'static_duration_seconds': int(duration_sec) if duration_sec is not None else None,  # Asigna la clave `static_duration_seconds` con el resultado de `int`.
                    'polyline': route.get('geometry') or '',  # Agrega un literal a la estructura.
                    'leg': {  # Asigna la clave `leg` con un diccionario.
                        'distance_meters': distance_m,  # Asigna la clave `distance_meters` en un diccionario.
                        'duration': f'{duration_sec}s' if duration_sec is not None else None,  # Asigna la clave `duration` en un diccionario.
                        'static_duration': f'{duration_sec}s' if duration_sec is not None else None,  # Asigna la clave `static_duration` en un diccionario.
                        'polyline': route.get('geometry') or '',  # Agrega un literal a la estructura.
                    },  # Cierra el bloque/estructura.
                })  # Cierra la estructura.

            return Response({'provider': 'osm', 'routes': normalized, 'raw': data})  # Devuelve un valor (`return`).

        key = self._google_api_key()  # Asigna a `key` el resultado de `self._google_api_key`.
        if not key:  # Evalua la condicion del `if`.
            return Response(  # Devuelve un valor (`return`).
                {  # Inicia una estructura literal.
                    'provider': 'google',  # Agrega un literal a la estructura.
                    'error': 'Falta configurar GOOGLE_MAPS_SERVER_API_KEY en el backend.',  # Agrega un literal a la estructura.
                },  # Cierra el bloque/estructura.
                status=status.HTTP_503_SERVICE_UNAVAILABLE  # Asigna un valor a `status`.
            )  # Cierra el bloque/estructura.

        routing_preference = (request.data.get('routing_preference') or 'TRAFFIC_AWARE').strip().upper()  # Asigna un valor a `routing_preference`.
        units = (request.data.get('units') or 'METRIC').strip().upper()  # Asigna un valor a `units`.

        payload = {  # Asigna un valor a `payload`.
            'origin': {  # Asigna la clave `origin` con un diccionario.
                'location': {  # Asigna la clave `location` con un diccionario.
                    'latLng': {  # Asigna la clave `latLng` con un diccionario.
                        'latitude': float(origin['lat']),  # Asigna la clave `latitude` con el resultado de `float`.
                        'longitude': float(origin['lng']),  # Asigna la clave `longitude` con el resultado de `float`.
                    }  # Cierra el bloque/estructura.
                }  # Cierra el bloque/estructura.
            },  # Cierra el bloque/estructura.
            'destination': {  # Asigna la clave `destination` con un diccionario.
                'location': {  # Asigna la clave `location` con un diccionario.
                    'latLng': {  # Asigna la clave `latLng` con un diccionario.
                        'latitude': float(destination['lat']),  # Asigna la clave `latitude` con el resultado de `float`.
                        'longitude': float(destination['lng']),  # Asigna la clave `longitude` con el resultado de `float`.
                    }  # Cierra el bloque/estructura.
                }  # Cierra el bloque/estructura.
            },  # Cierra el bloque/estructura.
            'travelMode': mode,  # Asigna la clave `travelMode` en un diccionario.
            'routingPreference': routing_preference,  # Asigna la clave `routingPreference` en un diccionario.
            'computeAlternativeRoutes': bool(request.data.get('alternatives', False)),  # Asigna la clave `computeAlternativeRoutes` con el resultado de `bool`.
            'units': units,  # Asigna la clave `units` en un diccionario.
        }  # Cierra el bloque/estructura.

        field_mask = ','.join([  # Asigna un valor a `field_mask`.
            'routes.distanceMeters',  # Agrega un literal a la estructura.
            'routes.duration',  # Agrega un literal a la estructura.
            'routes.staticDuration',  # Agrega un literal a la estructura.
            'routes.polyline.encodedPolyline',  # Agrega un literal a la estructura.
            'routes.legs.distanceMeters',  # Agrega un literal a la estructura.
            'routes.legs.duration',  # Agrega un literal a la estructura.
            'routes.legs.staticDuration',  # Agrega un literal a la estructura.
            'routes.legs.polyline.encodedPolyline',  # Agrega un literal a la estructura.
        ])  # Cierra la estructura.

        try:  # Inicia un bloque `try`.
            data = self._http_json_post(  # Asigna a `data` el resultado de `self._http_json_post`.
                f'https://routes.googleapis.com/directions/v2:computeRoutes?key={key}',  # Agrega un literal a la estructura.
                payload,  # Referencia `payload` en la estructura/expresion.
                field_mask=field_mask,  # Asigna un valor a `field_mask`.
            )  # Cierra el bloque/estructura.
        except Exception:  # Maneja una excepcion en `except`.
            return Response({'provider': 'google', 'routes': [], 'error': 'Routes API fallo.'})  # Devuelve un valor (`return`).

        routes = data.get('routes') or []  # Asigna a `routes` el resultado de `data.get`.
        normalized = []  # Asigna un valor a `normalized`.
        for route in routes:  # Itera en un bucle `for`.
            distance_m = route.get('distanceMeters')  # Asigna a `distance_m` el resultado de `route.get`.
            duration_raw = route.get('duration')  # Asigna a `duration_raw` el resultado de `route.get`.
            static_duration_raw = route.get('staticDuration')  # Asigna a `static_duration_raw` el resultado de `route.get`.
            encoded_polyline = (route.get('polyline') or {}).get('encodedPolyline') or ''  # Asigna un valor a `encoded_polyline`.
            leg = (route.get('legs') or [{}])[0]  # Asigna un valor a `leg`.
            normalized.append({  # Ejecuta `normalized.append`.
                'distance_meters': distance_m,  # Asigna la clave `distance_meters` en un diccionario.
                'distance_km': round(float(distance_m) / 1000, 2) if distance_m is not None else None,  # Asigna la clave `distance_km` con el resultado de `round`.
                'duration': duration_raw,  # Asigna la clave `duration` en un diccionario.
                'static_duration': static_duration_raw,  # Asigna la clave `static_duration` en un diccionario.
                'duration_seconds': self._parse_google_duration(duration_raw),  # Asigna la clave `duration_seconds` con el resultado de `self._parse_google_duration`.
                'static_duration_seconds': self._parse_google_duration(static_duration_raw),  # Asigna la clave `static_duration_seconds` con el resultado de `self._parse_google_duration`.
                'polyline': encoded_polyline,  # Asigna la clave `polyline` en un diccionario.
                'leg': {  # Asigna la clave `leg` con un diccionario.
                    'distance_meters': leg.get('distanceMeters'),  # Asigna la clave `distance_meters` con el resultado de `leg.get`.
                    'duration': leg.get('duration'),  # Asigna la clave `duration` con el resultado de `leg.get`.
                    'static_duration': leg.get('staticDuration'),  # Asigna la clave `static_duration` con el resultado de `leg.get`.
                    'polyline': (leg.get('polyline') or {}).get('encodedPolyline') or '',  # Agrega un literal a la estructura.
                },  # Cierra el bloque/estructura.
            })  # Cierra la estructura.

        return Response({'provider': 'google', 'routes': normalized, 'raw': data})  # Devuelve un valor (`return`).

    def _parse_google_duration(self, value):  # Define la funcion `_parse_google_duration`.
        # Google duration viene como string tipo "123s".
        if not value or not isinstance(value, str):  # Evalua la condicion del `if`.
            return None  # Devuelve un valor (`return`).
        if not value.endswith('s'):  # Evalua la condicion del `if`.
            return None  # Devuelve un valor (`return`).
        try:  # Inicia un bloque `try`.
            return int(float(value[:-1]))  # Devuelve un valor (`return`).
        except (TypeError, ValueError):  # Maneja una excepcion en `except`.
            return None  # Devuelve un valor (`return`).
