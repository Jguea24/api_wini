import json  # comentario
from decimal import Decimal  # comentario
from urllib.parse import urlencode  # comentario
from urllib.request import Request, urlopen  # comentario

from django.conf import settings  # comentario
from django.db import transaction  # comentario
from django.utils import timezone  # comentario
from rest_framework import generics, permissions, serializers, status  # comentario
from rest_framework.parsers import FormParser, JSONParser, MultiPartParser  # comentario
from django.contrib.auth.models import User  # comentario
from django.db.models import Count, Min, Q, Sum  # comentario
from rest_framework.response import Response  # comentario
from rest_framework.views import APIView  # comentario
from rest_framework_simplejwt.tokens import RefreshToken  # comentario

from .models import (  # comentario
    Banner,  # comentario
    Category,  # comentario
    Product,  # comentario
    Cart,  # comentario
    DeliveryAddress,  # comentario
    RoleChangeRequest,  # comentario
    Order,  # comentario
    OrderItem,  # comentario
    Shipment,  # comentario
    ShipmentLocation,  # comentario
)  # comentario
from .serializers import (  # comentario
    BannerSerializer,  # comentario
    CategorySerializer,  # comentario
    ProductSerializer,  # comentario
    CartSerializer,  # comentario
    RegisterSerializer,  # comentario
    RegisteredUserSerializer,  # comentario
    OrderCreateSerializer,  # comentario
    OrderSerializer,  # comentario
    ShipmentSerializer,  # comentario
    ShipmentAssignDriverSerializer,  # comentario
    ShipmentLocationUpdateSerializer,  # comentario
    DeliveryAddressSerializer,  # comentario
    MeSerializer,  # comentario
    ChangePasswordSerializer,  # comentario
    RoleChangeRequestSerializer,  # comentario
)  # comentario


class RegisterView(generics.ListCreateAPIView):  # comentario
    queryset = User.objects.select_related('profile').prefetch_related('groups').order_by('-id')  # comentario
    permission_classes = [permissions.AllowAny]  # comentario

    def get_serializer_class(self):  # comentario
        if self.request.method == 'GET':  # comentario
            return RegisteredUserSerializer  # comentario
        return RegisterSerializer  # comentario


class LoginView(APIView):  # comentario
    permission_classes = [permissions.AllowAny]  # comentario

    def post(self, request):  # comentario
        identifier = (  # comentario
            request.data.get('username')  # comentario
            or request.data.get('email')  # comentario
            or request.data.get('identifier')  # comentario
            or ''  # comentario
        ).strip()  # comentario
        password = request.data.get('password') or ''  # comentario

        if not identifier or not password:  # comentario
            return Response({'error': 'Debes enviar email/username y password.'}, status=400)  # comentario

        user = User.objects.filter(  # comentario
            Q(username__iexact=identifier) | Q(email__iexact=identifier)  # comentario
        ).first()  # comentario

        if not user:  # comentario
            return Response({'error': 'Usuario no existe'}, status=400)  # comentario

        if not user.check_password(password):  # comentario
            return Response({'error': 'Credenciales invalidas'}, status=400)  # comentario

        refresh = RefreshToken.for_user(user)  # comentario
        user_data = MeSerializer(user).data  # comentario

        return Response({  # comentario
            'access': str(refresh.access_token),  # comentario
            'refresh': str(refresh),  # comentario
            'user': user_data  # comentario
        })  # comentario


class MeView(APIView):  # comentario
    permission_classes = [permissions.IsAuthenticated]  # comentario
    parser_classes = [MultiPartParser, FormParser, JSONParser]  # comentario

    def get(self, request):  # comentario
        serializer = MeSerializer(request.user)  # comentario
        return Response(serializer.data)  # comentario

    def patch(self, request):  # comentario
        serializer = MeSerializer(request.user, data=request.data, partial=True)  # comentario
        serializer.is_valid(raise_exception=True)  # comentario
        serializer.save()  # comentario
        return Response(serializer.data)  # comentario


class ChangePasswordView(APIView):  # comentario
    permission_classes = [permissions.IsAuthenticated]  # comentario

    def post(self, request):  # comentario
        serializer = ChangePasswordSerializer(data=request.data)  # comentario
        serializer.is_valid(raise_exception=True)  # comentario

        current_password = serializer.validated_data['current_password']  # comentario
        new_password = serializer.validated_data['new_password']  # comentario

        if not request.user.check_password(current_password):  # comentario
            return Response({'error': 'La contrasena actual es incorrecta.'}, status=status.HTTP_400_BAD_REQUEST)  # comentario

        if request.user.check_password(new_password):  # comentario
            return Response(  # comentario
                {'error': 'La nueva contrasena debe ser diferente a la actual.'},  # comentario
                status=status.HTTP_400_BAD_REQUEST  # comentario
            )  # comentario

        request.user.set_password(new_password)  # comentario
        request.user.save(update_fields=['password'])  # comentario

        return Response({'message': 'Contrasena actualizada correctamente.'}, status=status.HTTP_200_OK)  # comentario


class ProductListView(generics.ListCreateAPIView):  # comentario
    queryset = Product.objects.select_related('category').all()  # comentario
    serializer_class = ProductSerializer  # comentario
    permission_classes = [permissions.AllowAny]  # comentario
    parser_classes = [MultiPartParser, FormParser, JSONParser]  # comentario

    def get_queryset(self):  # comentario
        queryset = super().get_queryset()  # comentario
        category_id = (self.request.query_params.get('category_id') or '').strip()  # comentario
        category_name = (self.request.query_params.get('category') or '').strip()  # comentario

        if category_id.isdigit():  # comentario
            if int(category_id) == 0:  # comentario
                return queryset  # comentario
            return queryset.filter(category_id=int(category_id))  # comentario

        if category_name and category_name.lower() not in {'todos', 'all'}:  # comentario
            return queryset.filter(category__name__iexact=category_name)  # comentario

        return queryset  # comentario


class ProductDetailView(generics.RetrieveAPIView):  # comentario
    queryset = Product.objects.select_related('category').all()  # comentario
    serializer_class = ProductSerializer  # comentario
    permission_classes = [permissions.AllowAny]  # comentario


class CategoryListView(generics.ListAPIView):  # comentario
    queryset = Category.objects.all()  # comentario
    serializer_class = CategorySerializer  # comentario
    permission_classes = [permissions.AllowAny]  # comentario

    def list(self, request, *args, **kwargs):  # comentario
        response = super().list(request, *args, **kwargs)  # comentario
        response.data = [{  # comentario
            'id': 0,  # comentario
            'name': 'Todos',  # comentario
            'order': 0,  # comentario
            'image': '',  # comentario
            'image_url': '',  # comentario
        }] + list(response.data)  # comentario
        return response  # comentario


class BannerListView(generics.ListAPIView):  # comentario
    serializer_class = BannerSerializer  # comentario
    permission_classes = [permissions.AllowAny]  # comentario

    def get_queryset(self):  # comentario
        return Banner.objects.filter(is_active=True).order_by('order', 'id')  # comentario


class CartView(generics.ListCreateAPIView):  # comentario
    serializer_class = CartSerializer  # comentario
    permission_classes = [permissions.IsAuthenticated]  # comentario

    def get_queryset(self):  # comentario
        return Cart.objects.filter(user=self.request.user)  # comentario

    def perform_create(self, serializer):  # comentario
        serializer.save(user=self.request.user)  # comentario

    def create(self, request, *args, **kwargs):  # comentario
        serializer = self.get_serializer(data=request.data)  # comentario
        serializer.is_valid(raise_exception=True)  # comentario

        product = serializer.validated_data['product']  # comentario
        quantity = serializer.validated_data.get('quantity', 1)  # comentario

        cart_item, created = Cart.objects.get_or_create(  # comentario
            user=request.user,  # comentario
            product=product,  # comentario
            defaults={'quantity': quantity},  # comentario
        )  # comentario

        if not created:  # comentario
            cart_item.quantity += quantity  # comentario
            cart_item.save(update_fields=['quantity'])  # comentario

        output_serializer = self.get_serializer(cart_item)  # comentario
        response_status = status.HTTP_201_CREATED if created else status.HTTP_200_OK  # comentario

        payload = dict(output_serializer.data)  # comentario
        payload['message'] = (  # comentario
            'Producto agregado al carrito'  # comentario
            if created  # comentario
            else 'Cantidad del producto actualizada en el carrito'  # comentario
        )  # comentario

        return Response(payload, status=response_status)  # comentario

    def patch(self, request, *args, **kwargs):  # comentario
        cart_item_id = (  # comentario
            request.data.get('cart_item_id')  # comentario
            or request.data.get('id')  # comentario
            or request.query_params.get('cart_item_id')  # comentario
            or request.query_params.get('id')  # comentario
        )  # comentario
        product_id = (  # comentario
            request.data.get('product')  # comentario
            or request.data.get('product_id')  # comentario
            or request.query_params.get('product')  # comentario
            or request.query_params.get('product_id')  # comentario
        )  # comentario
        quantity = request.data.get('quantity', request.data.get('cantidad'))  # comentario

        if quantity is None:  # comentario
            return Response({'error': 'Debes enviar quantity.'}, status=status.HTTP_400_BAD_REQUEST)  # comentario

        try:  # comentario
            quantity = int(quantity)  # comentario
        except (TypeError, ValueError):  # comentario
            return Response({'error': 'quantity debe ser un numero entero.'}, status=status.HTTP_400_BAD_REQUEST)  # comentario

        if quantity < 0:  # comentario
            return Response({'error': 'quantity no puede ser negativo.'}, status=status.HTTP_400_BAD_REQUEST)  # comentario

        queryset = Cart.objects.filter(user=request.user)  # comentario
        if cart_item_id:  # comentario
            queryset = queryset.filter(id=cart_item_id)  # comentario
        elif product_id:  # comentario
            queryset = queryset.filter(product_id=product_id)  # comentario
        else:  # comentario
            return Response(  # comentario
                {'error': 'Debes enviar cart_item_id/id o product/product_id.'},  # comentario
                status=status.HTTP_400_BAD_REQUEST  # comentario
            )  # comentario

        cart_item = queryset.first()  # comentario
        if not cart_item:  # comentario
            return Response({'error': 'Producto no encontrado en el carrito.'}, status=status.HTTP_404_NOT_FOUND)  # comentario

        if quantity == 0:  # comentario
            cart_item.delete()  # comentario
            return Response({'message': 'Producto eliminado del carrito.'}, status=status.HTTP_200_OK)  # comentario

        cart_item.quantity = quantity  # comentario
        cart_item.save(update_fields=['quantity'])  # comentario
        output_serializer = self.get_serializer(cart_item)  # comentario
        payload = dict(output_serializer.data)  # comentario
        payload['message'] = 'Cantidad actualizada en el carrito'  # comentario
        return Response(payload, status=status.HTTP_200_OK)  # comentario

    def delete(self, request, *args, **kwargs):  # comentario
        cart_item_id = (  # comentario
            request.data.get('cart_item_id')  # comentario
            or request.data.get('id')  # comentario
            or request.query_params.get('cart_item_id')  # comentario
            or request.query_params.get('id')  # comentario
        )  # comentario
        product_id = (  # comentario
            request.data.get('product')  # comentario
            or request.data.get('product_id')  # comentario
            or request.query_params.get('product')  # comentario
            or request.query_params.get('product_id')  # comentario
        )  # comentario

        queryset = Cart.objects.filter(user=request.user)  # comentario

        if cart_item_id:  # comentario
            deleted_count, _ = queryset.filter(id=cart_item_id).delete()  # comentario
            if deleted_count == 0:  # comentario
                return Response({'error': 'Producto no encontrado en el carrito.'}, status=status.HTTP_404_NOT_FOUND)  # comentario
            return Response(  # comentario
                {'message': 'Producto eliminado del carrito.', 'deleted': deleted_count},  # comentario
                status=status.HTTP_200_OK  # comentario
            )  # comentario

        if product_id:  # comentario
            deleted_count, _ = queryset.filter(product_id=product_id).delete()  # comentario
            if deleted_count == 0:  # comentario
                return Response({'error': 'Producto no encontrado en el carrito.'}, status=status.HTTP_404_NOT_FOUND)  # comentario
            return Response(  # comentario
                {'message': 'Producto eliminado del carrito.', 'deleted': deleted_count},  # comentario
                status=status.HTTP_200_OK  # comentario
            )  # comentario

        deleted_count, _ = queryset.delete()  # comentario
        return Response(  # comentario
            {'message': 'Carrito vaciado.', 'deleted': deleted_count},  # comentario
            status=status.HTTP_200_OK  # comentario
        )  # comentario


class CartCountView(APIView):  # comentario
    permission_classes = [permissions.IsAuthenticated]  # comentario

    def get(self, request):  # comentario
        queryset = Cart.objects.filter(user=request.user)  # comentario
        distinct_items = queryset.count()  # comentario
        total_quantity = queryset.aggregate(total=Sum('quantity')).get('total') or 0  # comentario

        return Response({  # comentario
            'count': int(total_quantity),  # comentario
            'distinct_items': distinct_items,  # comentario
        })  # comentario


def pick_auto_driver():  # comentario
    group_driver_ids = set(  # comentario
        User.objects.filter(  # comentario
            is_active=True,  # comentario
            groups__name__in=['DRIVER', 'REPARTIDOR'],  # comentario
        ).values_list('id', flat=True)  # comentario
    )  # comentario
    requested_driver_ids = set(  # comentario
        RoleChangeRequest.objects.filter(  # comentario
            requested_role='driver',  # comentario
            status='approved',  # comentario
            user__is_active=True,  # comentario
        ).values_list('user_id', flat=True)  # comentario
    )  # comentario
    candidate_ids = group_driver_ids.union(requested_driver_ids)  # comentario
    if not candidate_ids:  # comentario
        return None  # comentario

    active_statuses = ['assigned', 'picked_up', 'on_the_way', 'nearby']  # comentario
    return (  # comentario
        User.objects.filter(id__in=candidate_ids, is_active=True)  # comentario
        .annotate(  # comentario
            active_shipments=Count(  # comentario
                'shipments_assigned',  # comentario
                filter=Q(shipments_assigned__status__in=active_statuses),  # comentario
                distinct=True,  # comentario
            ),  # comentario
            first_active_shipment_at=Min(  # comentario
                'shipments_assigned__created_at',  # comentario
                filter=Q(shipments_assigned__status__in=active_statuses),  # comentario
            ),  # comentario
        )  # comentario
        .order_by('active_shipments', 'first_active_shipment_at', 'id')  # comentario
        .first()  # comentario
    )  # comentario


class OrderListCreateView(generics.ListCreateAPIView):  # comentario
    permission_classes = [permissions.IsAuthenticated]  # comentario

    def get_queryset(self):  # comentario
        return (  # comentario
            Order.objects.filter(user=self.request.user)  # comentario
            .select_related('delivery_address')  # comentario
            .prefetch_related('items__product')  # comentario
        )  # comentario

    def get_serializer_class(self):  # comentario
        if self.request.method == 'POST':  # comentario
            return OrderCreateSerializer  # comentario
        return OrderSerializer  # comentario

    def create(self, request, *args, **kwargs):  # comentario
        input_serializer = self.get_serializer(data=request.data)  # comentario
        input_serializer.is_valid(raise_exception=True)  # comentario

        user = request.user  # comentario
        with transaction.atomic():  # comentario
            cart_items = list(Cart.objects.select_related('product').filter(user=user))  # comentario
            if not cart_items:  # comentario
                return Response({'error': 'El carrito esta vacio.'}, status=status.HTTP_400_BAD_REQUEST)  # comentario

            address = input_serializer.validated_data.get('delivery_address')  # comentario
            if address and address.user_id != user.id:  # comentario
                return Response(  # comentario
                    {'error': 'La direccion seleccionada no pertenece al usuario autenticado.'},  # comentario
                    status=status.HTTP_400_BAD_REQUEST  # comentario
                )  # comentario

            if address is None:  # comentario
                address = DeliveryAddress.objects.filter(user=user, is_default=True).first()  # comentario
            if address is None:  # comentario
                address = DeliveryAddress.objects.filter(user=user).order_by('-id').first()  # comentario
            if address is None:  # comentario
                return Response(  # comentario
                    {'error': 'Debes registrar una direccion de entrega antes de crear un pedido.'},  # comentario
                    status=status.HTTP_400_BAD_REQUEST  # comentario
                )  # comentario

            product_ids = [item.product_id for item in cart_items]  # comentario
            locked_products = Product.objects.select_for_update().filter(id__in=product_ids)  # comentario
            products_by_id = {product.id: product for product in locked_products}  # comentario

            stock_errors = []  # comentario
            for cart_item in cart_items:  # comentario
                product = products_by_id.get(cart_item.product_id)  # comentario
                if not product:  # comentario
                    stock_errors.append({  # comentario
                        'product_id': cart_item.product_id,  # comentario
                        'error': 'Producto no encontrado.',  # comentario
                    })  # comentario
                    continue  # comentario
                if product.stock < cart_item.quantity:  # comentario
                    stock_errors.append({  # comentario
                        'product_id': product.id,  # comentario
                        'product_name': product.name,  # comentario
                        'requested': cart_item.quantity,  # comentario
                        'available': product.stock,  # comentario
                    })  # comentario

            if stock_errors:  # comentario
                return Response(  # comentario
                    {  # comentario
                        'error': 'No hay stock suficiente para completar el pedido.',  # comentario
                        'details': stock_errors,  # comentario
                    },  # comentario
                    status=status.HTTP_400_BAD_REQUEST  # comentario
                )  # comentario

            order = Order.objects.create(  # comentario
                user=user,  # comentario
                delivery_address=address,  # comentario
                delivery_main_address=address.main_address,  # comentario
                delivery_secondary_street=address.secondary_street,  # comentario
                delivery_apartment=address.apartment,  # comentario
                delivery_city=address.city,  # comentario
                delivery_latitude=getattr(address, 'latitude', None),  # comentario
                delivery_longitude=getattr(address, 'longitude', None),  # comentario
                delivery_instructions=address.delivery_instructions,  # comentario
                status='pending',  # comentario
                total_amount=Decimal('0.00'),  # comentario
                total_items=0,  # comentario
            )  # comentario
            auto_driver = pick_auto_driver()  # comentario
            shipment_status = 'assigned' if auto_driver else 'pending_assignment'  # comentario
            Shipment.objects.create(  # comentario
                order=order,  # comentario
                driver=auto_driver,  # comentario
                status=shipment_status,  # comentario
            )  # comentario
            if auto_driver:  # comentario
                order.status = 'confirmed'  # comentario
                order.save(update_fields=['status'])  # comentario

            total_amount = Decimal('0.00')  # comentario
            total_items = 0  # comentario

            for cart_item in cart_items:  # comentario
                product = products_by_id[cart_item.product_id]  # comentario
                quantity = int(cart_item.quantity)  # comentario
                subtotal = product.price * quantity  # comentario

                OrderItem.objects.create(  # comentario
                    order=order,  # comentario
                    product=product,  # comentario
                    product_name=product.name,  # comentario
                    product_price=product.price,  # comentario
                    quantity=quantity,  # comentario
                    subtotal=subtotal,  # comentario
                )  # comentario

                product.stock -= quantity  # comentario
                product.save(update_fields=['stock'])  # comentario

                total_amount += subtotal  # comentario
                total_items += quantity  # comentario

            order.total_amount = total_amount  # comentario
            order.total_items = total_items  # comentario
            order.save(update_fields=['total_amount', 'total_items'])  # comentario

            Cart.objects.filter(user=user).delete()  # comentario

        output_serializer = OrderSerializer(order, context=self.get_serializer_context())  # comentario
        payload = dict(output_serializer.data)  # comentario
        payload['message'] = 'Pedido creado correctamente.'  # comentario
        return Response(payload, status=status.HTTP_201_CREATED)  # comentario


class OrderDetailView(generics.RetrieveAPIView):  # comentario
    serializer_class = OrderSerializer  # comentario
    permission_classes = [permissions.IsAuthenticated]  # comentario

    def get_queryset(self):  # comentario
        return (  # comentario
            Order.objects.filter(user=self.request.user)  # comentario
            .select_related('delivery_address')  # comentario
            .prefetch_related('items__product')  # comentario
        )  # comentario


class OrderTrackingView(APIView):  # comentario
    permission_classes = [permissions.IsAuthenticated]  # comentario

    def get(self, request, pk):  # comentario
        include_map = parse_bool(request.query_params.get('include_map'), default=False)  # comentario
        include_route = parse_bool(request.query_params.get('include_route'), default=False)  # comentario
        travel_mode = (request.query_params.get('travel_mode') or 'DRIVE').strip().upper()  # comentario
        alternatives = parse_bool(request.query_params.get('alternatives'), default=False)  # comentario

        order_queryset = Order.objects.select_related(  # comentario
            'delivery_address',  # comentario
            'shipment',  # comentario
            'shipment__driver',  # comentario
        )  # comentario
        if not request.user.is_staff:  # comentario
            order_queryset = order_queryset.filter(user=request.user)  # comentario

        order = order_queryset.filter(id=pk).first()  # comentario
        if not order:  # comentario
            return Response({'error': 'Pedido no encontrado.'}, status=status.HTTP_404_NOT_FOUND)  # comentario

        shipment, _ = Shipment.objects.get_or_create(  # comentario
            order=order,  # comentario
            defaults={'status': 'pending_assignment'},  # comentario
        )  # comentario
        if shipment.driver_id is None:  # comentario
            auto_driver = pick_auto_driver()  # comentario
            if auto_driver:  # comentario
                shipment.driver = auto_driver  # comentario
                if shipment.status == 'pending_assignment':  # comentario
                    shipment.status = 'assigned'  # comentario
                shipment.save(update_fields=['driver', 'status', 'updated_at'])  # comentario
                if order.status == 'pending':  # comentario
                    order.status = 'confirmed'  # comentario
                    order.save(update_fields=['status'])  # comentario
        shipment_data = ShipmentSerializer(shipment, context={'request': request}).data  # comentario

        payload = {  # comentario
            'order': {  # comentario
                'id': order.id,  # comentario
                'status': order.status,  # comentario
                'status_label': order.get_status_display(),  # comentario
                'total_amount': order.total_amount,  # comentario
                'total_items': order.total_items,  # comentario
                'created_at': order.created_at,  # comentario
                'delivery_city': order.delivery_city,  # comentario
                'delivery_main_address': order.delivery_main_address,  # comentario
            },  # comentario
            'shipment': shipment_data,  # comentario
        }  # comentario

        if include_map:  # comentario
            stored_lat = safe_float(getattr(order, 'delivery_latitude', None))  # comentario
            stored_lng = safe_float(getattr(order, 'delivery_longitude', None))  # comentario

            dest_lat = stored_lat if stored_lat is not None else safe_float(  # comentario
                request.query_params.get('dest_lat')  # comentario
                or request.query_params.get('destination_lat')  # comentario
                or request.query_params.get('delivery_lat')  # comentario
            )  # comentario
            dest_lng = stored_lng if stored_lng is not None else safe_float(  # comentario
                request.query_params.get('dest_lng')  # comentario
                or request.query_params.get('destination_lng')  # comentario
                or request.query_params.get('delivery_lng')  # comentario
            )  # comentario

            origin = {  # comentario
                'lat': safe_float(shipment.current_latitude),  # comentario
                'lng': safe_float(shipment.current_longitude),  # comentario
            }  # comentario
            if origin['lat'] is None or origin['lng'] is None:  # comentario
                last_point = (  # comentario
                    ShipmentLocation.objects  # comentario
                    .filter(shipment=shipment)  # comentario
                    .order_by('-recorded_at', '-id')  # comentario
                    .values('latitude', 'longitude')  # comentario
                    .first()  # comentario
                )  # comentario
                if last_point:  # comentario
                    origin = {  # comentario
                        'lat': safe_float(last_point.get('latitude')),  # comentario
                        'lng': safe_float(last_point.get('longitude')),  # comentario
                    }  # comentario

            destination = {'lat': dest_lat, 'lng': dest_lng} if dest_lat is not None and dest_lng is not None else None  # comentario
            geocode_payload = None  # comentario

            if destination is None:  # comentario
                query = ', '.join([  # comentario
                    part for part in [  # comentario
                        (order.delivery_main_address or '').strip(),  # comentario
                        (order.delivery_secondary_street or '').strip(),  # comentario
                        (order.delivery_city or '').strip(),  # comentario
                    ]  # comentario
                    if part  # comentario
                ]).strip()  # comentario
                geocode_payload = try_geocode_address(query)  # comentario
                first = (geocode_payload.get('results') or [None])[0]  # comentario
                if first and safe_float(first.get('lat')) is not None and safe_float(first.get('lng')) is not None:  # comentario
                    destination = {  # comentario
                        'lat': safe_float(first.get('lat')),  # comentario
                        'lng': safe_float(first.get('lng')),  # comentario
                    }  # comentario

            route_payload = None  # comentario
            if include_route and origin.get('lat') is not None and origin.get('lng') is not None and destination:  # comentario
                route_payload = try_estimate_route(  # comentario
                    origin=origin,  # comentario
                    destination=destination,  # comentario
                    travel_mode=travel_mode,  # comentario
                    alternatives=alternatives,  # comentario
                )  # comentario

            payload['map'] = {  # comentario
                'origin': origin if origin.get('lat') is not None and origin.get('lng') is not None else None,  # comentario
                'destination': destination,  # comentario
                'geocode': geocode_payload,  # comentario
                'route': route_payload,  # comentario
            }  # comentario

        return Response(payload)  # comentario


class OrderTrackingLocationUpdateView(APIView):  # comentario
    permission_classes = [permissions.IsAuthenticated]  # comentario

    def _can_update_tracking(self, user, shipment):  # comentario
        if not user.is_authenticated:  # comentario
            return False  # comentario

        if user.is_staff or user.is_superuser:  # comentario
            return True  # comentario

        allowed_groups = ['ADMIN', 'DRIVER', 'REPARTIDOR']  # comentario
        is_ops_user = user.groups.filter(name__in=allowed_groups).exists()  # comentario

        if shipment.driver_id and shipment.driver_id == user.id:  # comentario
            return True  # comentario

        if is_ops_user and shipment.driver_id is None:  # comentario
            return True  # comentario

        return False  # comentario

    def post(self, request, pk):  # comentario
        order_queryset = Order.objects.select_related('shipment', 'shipment__driver')  # comentario
        if not request.user.is_staff:  # comentario
            order_queryset = order_queryset.filter(  # comentario
                Q(user=request.user) | Q(shipment__driver=request.user)  # comentario
            )  # comentario

        order = order_queryset.filter(id=pk).first()  # comentario
        if not order:  # comentario
            return Response({'error': 'Pedido no encontrado.'}, status=status.HTTP_404_NOT_FOUND)  # comentario

        shipment, _ = Shipment.objects.get_or_create(  # comentario
            order=order,  # comentario
            defaults={'status': 'pending_assignment'},  # comentario
        )  # comentario

        if not self._can_update_tracking(request.user, shipment):  # comentario
            return Response(  # comentario
                {'error': 'No tienes permisos para actualizar la ubicacion de este envio.'},  # comentario
                status=status.HTTP_403_FORBIDDEN  # comentario
            )  # comentario

        serializer = ShipmentLocationUpdateSerializer(data=request.data)  # comentario
        serializer.is_valid(raise_exception=True)  # comentario

        data = serializer.validated_data  # comentario
        shipment.current_latitude = data['latitude']  # comentario
        shipment.current_longitude = data['longitude']  # comentario
        shipment.last_location_at = timezone.now()  # comentario

        if 'heading' in data:  # comentario
            shipment.current_heading = data.get('heading')  # comentario
        if 'speed' in data:  # comentario
            shipment.current_speed = data.get('speed')  # comentario
        if 'status' in data:  # comentario
            shipment.status = data['status']  # comentario
        if 'eta_minutes' in data:  # comentario
            shipment.eta_minutes = data.get('eta_minutes')  # comentario
        if 'notes' in data:  # comentario
            shipment.notes = data.get('notes', '')  # comentario

        shipment.save()  # comentario

        ShipmentLocation.objects.create(  # comentario
            shipment=shipment,  # comentario
            latitude=data['latitude'],  # comentario
            longitude=data['longitude'],  # comentario
            heading=data.get('heading'),  # comentario
            speed=data.get('speed'),  # comentario
        )  # comentario

        order_status_map = {  # comentario
            'pending_assignment': 'pending',  # comentario
            'assigned': 'confirmed',  # comentario
            'picked_up': 'preparing',  # comentario
            'on_the_way': 'on_the_way',  # comentario
            'nearby': 'on_the_way',  # comentario
            'delivered': 'delivered',  # comentario
            'cancelled': 'cancelled',  # comentario
        }  # comentario
        mapped_status = order_status_map.get(shipment.status)  # comentario
        if mapped_status and mapped_status != order.status:  # comentario
            order.status = mapped_status  # comentario
            order.save(update_fields=['status'])  # comentario

        payload = ShipmentSerializer(shipment, context={'request': request}).data  # comentario
        payload['message'] = 'Ubicacion de envio actualizada.'  # comentario
        return Response(payload, status=status.HTTP_200_OK)  # comentario


class OrderTrackingAssignDriverView(APIView):  # comentario
    permission_classes = [permissions.IsAuthenticated]  # comentario

    def _can_assign(self, user):  # comentario
        if not user.is_authenticated:  # comentario
            return False  # comentario
        if user.is_staff or user.is_superuser:  # comentario
            return True  # comentario
        return user.groups.filter(name='ADMIN').exists()  # comentario

    def post(self, request, pk):  # comentario
        serializer = ShipmentAssignDriverSerializer(data=request.data)  # comentario
        serializer.is_valid(raise_exception=True)  # comentario

        order = (  # comentario
            Order.objects.select_related('shipment', 'shipment__driver')  # comentario
            .filter(id=pk)  # comentario
            .first()  # comentario
        )  # comentario
        if not order:  # comentario
            return Response({'error': 'Pedido no encontrado.'}, status=status.HTTP_404_NOT_FOUND)  # comentario

        shipment, _ = Shipment.objects.get_or_create(  # comentario
            order=order,  # comentario
            defaults={'status': 'pending_assignment'},  # comentario
        )  # comentario

        validated = serializer.validated_data  # comentario
        has_driver_id = 'driver_id' in validated  # comentario
        driver_id = validated.get('driver_id')  # comentario
        auto_assign = validated.get('auto_assign')  # comentario

        # Regla pedida:
        # - body vacio => auto asignar
        # - auto_assign=true => auto asignar
        # - driver_id=null => desasignar explicito
        if auto_assign is None and not has_driver_id:  # comentario
            auto_assign = True  # comentario

        can_assign_all = self._can_assign(request.user)  # comentario
        is_owner = request.user.is_authenticated and order.user_id == request.user.id  # comentario

        # Clientes: solo permitimos auto-asignacion (Reintentar) para su propio pedido.
        # Admin/staff: pueden auto-asignar, asignar manual, o desasignar.
        if not can_assign_all:  # comentario
            if not (is_owner and bool(auto_assign) and not has_driver_id):  # comentario
                return Response(  # comentario
                    {'error': 'No tienes permisos para asignar repartidor.'},  # comentario
                    status=status.HTTP_403_FORBIDDEN  # comentario
                )  # comentario
            # Forzamos la operacion a auto-asignar.
            auto_assign = True  # comentario
            has_driver_id = False  # comentario
            driver_id = None  # comentario

        if auto_assign:  # comentario
            auto_driver = pick_auto_driver()  # comentario
            if auto_driver is None:  # comentario
                shipment.driver = None  # comentario
                if shipment.status not in {'delivered', 'cancelled'}:  # comentario
                    shipment.status = 'pending_assignment'  # comentario
                shipment.save(update_fields=['driver', 'status', 'updated_at'])  # comentario
                payload = ShipmentSerializer(shipment, context={'request': request}).data  # comentario
                payload['message'] = 'No hay repartidores disponibles para auto-asignacion.'  # comentario
                return Response(payload, status=status.HTTP_200_OK)  # comentario

            shipment.driver = auto_driver  # comentario
            if shipment.status in {'pending_assignment', 'cancelled'}:  # comentario
                shipment.status = 'assigned'  # comentario
            shipment.save(update_fields=['driver', 'status', 'updated_at'])  # comentario

            if order.status == 'pending':  # comentario
                order.status = 'confirmed'  # comentario
                order.save(update_fields=['status'])  # comentario

            payload = ShipmentSerializer(shipment, context={'request': request}).data  # comentario
            payload['message'] = 'Repartidor auto-asignado correctamente.'  # comentario
            return Response(payload, status=status.HTTP_200_OK)  # comentario

        if has_driver_id and driver_id is None:  # comentario
            shipment.driver = None  # comentario
            if shipment.status not in {'delivered', 'cancelled'}:  # comentario
                shipment.status = 'pending_assignment'  # comentario
            shipment.save(update_fields=['driver', 'status', 'updated_at'])  # comentario
            payload = ShipmentSerializer(shipment, context={'request': request}).data  # comentario
            payload['message'] = 'Repartidor desasignado correctamente.'  # comentario
            return Response(payload, status=status.HTTP_200_OK)  # comentario

        if not has_driver_id:  # comentario
            return Response(  # comentario
                {'error': 'Debes enviar driver_id, driver_id=null o auto_assign=true.'},  # comentario
                status=status.HTTP_400_BAD_REQUEST  # comentario
            )  # comentario

        driver = User.objects.get(id=driver_id)  # comentario
        shipment.driver = driver  # comentario
        if shipment.status == 'pending_assignment':  # comentario
            shipment.status = 'assigned'  # comentario
        shipment.save(update_fields=['driver', 'status', 'updated_at'])  # comentario

        if order.status == 'pending':  # comentario
            order.status = 'confirmed'  # comentario
            order.save(update_fields=['status'])  # comentario

        payload = ShipmentSerializer(shipment, context={'request': request}).data  # comentario
        payload['message'] = 'Repartidor asignado correctamente.'  # comentario
        return Response(payload, status=status.HTTP_200_OK)  # comentario


class DeliveryAddressListCreateView(generics.ListCreateAPIView):  # comentario
    serializer_class = DeliveryAddressSerializer  # comentario
    permission_classes = [permissions.IsAuthenticated]  # comentario

    def get_queryset(self):  # comentario
        return DeliveryAddress.objects.filter(user=self.request.user)  # comentario

    def perform_create(self, serializer):  # comentario
        queryset = DeliveryAddress.objects.filter(user=self.request.user)  # comentario
        requested_default = serializer.validated_data.get('is_default', False)  # comentario
        should_be_default = requested_default or not queryset.exists()  # comentario

        address = serializer.save(user=self.request.user, is_default=should_be_default)  # comentario
        if should_be_default:  # comentario
            queryset.exclude(id=address.id).update(is_default=False)  # comentario


class DeliveryAddressDetailView(generics.RetrieveUpdateDestroyAPIView):  # comentario
    serializer_class = DeliveryAddressSerializer  # comentario
    permission_classes = [permissions.IsAuthenticated]  # comentario

    def get_queryset(self):  # comentario
        return DeliveryAddress.objects.filter(user=self.request.user)  # comentario

    def perform_update(self, serializer):  # comentario
        address = serializer.save()  # comentario
        if address.is_default:  # comentario
            DeliveryAddress.objects.filter(user=self.request.user).exclude(id=address.id).update(is_default=False)  # comentario
            return  # comentario

        has_default = DeliveryAddress.objects.filter(user=self.request.user, is_default=True).exists()  # comentario
        if not has_default:  # comentario
            address.is_default = True  # comentario
            address.save(update_fields=['is_default'])  # comentario

    def perform_destroy(self, instance):  # comentario
        user = instance.user  # comentario
        was_default = instance.is_default  # comentario
        instance.delete()  # comentario

        if was_default:  # comentario
            replacement = DeliveryAddress.objects.filter(user=user).order_by('-id').first()  # comentario
            if replacement:  # comentario
                replacement.is_default = True  # comentario
                replacement.save(update_fields=['is_default'])  # comentario


class RoleChangeRequestListCreateView(generics.ListCreateAPIView):  # comentario
    serializer_class = RoleChangeRequestSerializer  # comentario
    permission_classes = [permissions.IsAuthenticated]  # comentario

    def get_queryset(self):  # comentario
        return RoleChangeRequest.objects.filter(user=self.request.user)  # comentario

    def perform_create(self, serializer):  # comentario
        requested_role = serializer.validated_data['requested_role']  # comentario
        has_pending = RoleChangeRequest.objects.filter(  # comentario
            user=self.request.user,  # comentario
            requested_role=requested_role,  # comentario
            status='pending',  # comentario
        ).exists()  # comentario
        if has_pending:  # comentario
            raise serializers.ValidationError({  # comentario
                'requested_role': 'Ya tienes una solicitud pendiente para este rol.'  # comentario
            })  # comentario
        serializer.save(user=self.request.user)  # comentario


def geo_provider():  # comentario
    return (getattr(settings, 'GEO_PROVIDER', 'osm') or 'osm').strip().lower()  # comentario


def osm_nominatim_base_url():  # comentario
    return (getattr(settings, 'OSM_NOMINATIM_BASE_URL', 'https://nominatim.openstreetmap.org') or '').rstrip('/')  # comentario


def osm_router_base_url():  # comentario
    return (getattr(settings, 'OSM_ROUTER_BASE_URL', 'https://router.project-osrm.org') or '').rstrip('/')  # comentario


def geocoder_user_agent():  # comentario
    return (getattr(settings, 'GEOCODER_USER_AGENT', 'api-guayabal/1.0 (mobile-app)') or 'api-guayabal/1.0')  # comentario


def http_json_get(endpoint, params=None, timeout=8, headers=None):  # comentario
    url = endpoint if not params else f"{endpoint}?{urlencode(params)}"  # comentario
    req = Request(  # comentario
        url,  # comentario
        headers=headers or {  # comentario
            'Accept': 'application/json',  # comentario
        },  # comentario
    )  # comentario
    with urlopen(req, timeout=timeout) as resp:  # comentario
        return json.loads(resp.read().decode('utf-8'))  # comentario


def extract_nominatim_result(item):  # comentario
    address = item.get('address') or {}  # comentario
    display_name = item.get('display_name') or ''  # comentario
    road = (  # comentario
        address.get('road')  # comentario
        or address.get('pedestrian')  # comentario
        or address.get('footway')  # comentario
        or address.get('path')  # comentario
        or address.get('cycleway')  # comentario
        or ''  # comentario
    )  # comentario
    house_number = address.get('house_number') or ''  # comentario
    main_address = (  # comentario
        f"{road} {house_number}".strip()  # comentario
        or road  # comentario
        or (display_name.split(',')[0].strip() if display_name else '')  # comentario
    )  # comentario
    secondary_street = (  # comentario
        address.get('suburb')  # comentario
        or address.get('neighbourhood')  # comentario
        or address.get('quarter')  # comentario
        or address.get('city_district')  # comentario
        or ''  # comentario
    )  # comentario
    city = (  # comentario
        address.get('city')  # comentario
        or address.get('town')  # comentario
        or address.get('village')  # comentario
        or address.get('hamlet')  # comentario
        or ''  # comentario
    )  # comentario
    region = address.get('state') or address.get('county') or ''  # comentario
    country_name = address.get('country') or ''  # comentario

    try:  # comentario
        lat = float(item.get('lat')) if item.get('lat') is not None else None  # comentario
    except (TypeError, ValueError):  # comentario
        lat = None  # comentario
    try:  # comentario
        lng = float(item.get('lon')) if item.get('lon') is not None else None  # comentario
    except (TypeError, ValueError):  # comentario
        lng = None  # comentario

    return {  # comentario
        'place_id': str(item.get('place_id') or ''),  # comentario
        'osm_id': str(item.get('osm_id') or ''),  # comentario
        'osm_type': item.get('osm_type') or '',  # comentario
        'label': display_name,  # comentario
        'main_address': main_address,  # comentario
        'secondary_street': secondary_street,  # comentario
        'city': city,  # comentario
        'region': region,  # comentario
        'country': country_name,  # comentario
        'lat': lat,  # comentario
        'lng': lng,  # comentario
    }  # comentario


def parse_google_duration(value):  # comentario
    if not value or not isinstance(value, str):  # comentario
        return None  # comentario
    if not value.endswith('s'):  # comentario
        return None  # comentario
    try:  # comentario
        return int(float(value[:-1]))  # comentario
    except (TypeError, ValueError):  # comentario
        return None  # comentario


def parse_bool(value, default=False):  # comentario
    if value is None:  # comentario
        return default  # comentario
    if isinstance(value, bool):  # comentario
        return value  # comentario
    value = str(value).strip().lower()  # comentario
    if value in {'1', 'true', 't', 'yes', 'y', 'si', 'sí', 'on'}:  # comentario
        return True  # comentario
    if value in {'0', 'false', 'f', 'no', 'n', 'off'}:  # comentario
        return False  # comentario
    return default  # comentario


def safe_float(value):  # comentario
    if value is None:  # comentario
        return None  # comentario
    try:  # comentario
        return float(value)  # comentario
    except (TypeError, ValueError):  # comentario
        return None  # comentario


def _google_maps_server_key():  # comentario
    return (getattr(settings, 'GOOGLE_MAPS_SERVER_API_KEY', '') or '').strip()  # comentario


def _google_maps_language():  # comentario
    return (getattr(settings, 'GOOGLE_MAPS_LANGUAGE', 'es') or 'es').strip()  # comentario


def try_geocode_address(address):  # comentario
    """
    Best-effort geocode used by tracking map payloads.
    Returns: dict with {provider, results} compatible (subset) with GeoGeocodeView.
    Never raises.
    """
    address = (address or '').strip()  # comentario
    if not address:  # comentario
        return {'provider': geo_provider(), 'results': []}  # comentario

    if geo_provider() != 'google':  # comentario
        try:  # comentario
            raw_results = http_json_get(  # comentario
                f'{osm_nominatim_base_url()}/search',  # comentario
                {  # comentario
                    'format': 'jsonv2',  # comentario
                    'addressdetails': 1,  # comentario
                    'limit': 1,  # comentario
                    'q': address,  # comentario
                },  # comentario
                headers={  # comentario
                    'User-Agent': geocoder_user_agent(),  # comentario
                    'Accept': 'application/json',  # comentario
                }  # comentario
            ) or []  # comentario
        except Exception:  # comentario
            return {'provider': 'osm', 'results': []}  # comentario

        results = [extract_nominatim_result(item) for item in raw_results[:1]]  # comentario
        return {'provider': 'osm', 'results': results}  # comentario

    key = _google_maps_server_key()  # comentario
    if not key:  # comentario
        return {'provider': 'google', 'results': [], 'error': 'Falta configurar GOOGLE_MAPS_SERVER_API_KEY.'}  # comentario

    try:  # comentario
        payload = http_json_get(  # comentario
            'https://maps.googleapis.com/maps/api/geocode/json',  # comentario
            {  # comentario
                'language': _google_maps_language(),  # comentario
                'key': key,  # comentario
                'address': address,  # comentario
            },  # comentario
            headers={'Accept': 'application/json'},  # comentario
            timeout=6,  # comentario
        )  # comentario
    except Exception:  # comentario
        return {'provider': 'google', 'results': []}  # comentario

    status_name = (payload or {}).get('status')  # comentario
    if status_name not in {'OK', 'ZERO_RESULTS'}:  # comentario
        return {  # comentario
            'provider': 'google',  # comentario
            'results': [],  # comentario
            'error': (payload or {}).get('error_message') or status_name or 'Geocoding fallo.',  # comentario
        }  # comentario

    results = []  # comentario
    for item in (payload.get('results') or [])[:1]:  # comentario
        geometry = item.get('geometry') or {}  # comentario
        location = geometry.get('location') or {}  # comentario
        results.append({  # comentario
            'place_id': item.get('place_id') or '',  # comentario
            'label': item.get('formatted_address') or '',  # comentario
            'lat': safe_float(location.get('lat')),  # comentario
            'lng': safe_float(location.get('lng')),  # comentario
        })  # comentario
    return {'provider': 'google', 'results': results}  # comentario


def try_estimate_route(origin, destination, travel_mode='DRIVE', alternatives=False):  # comentario
    """
    Best-effort route estimation used by tracking map payloads.
    Returns: dict compatible (subset) with GeoRouteEstimateView, never raises.
    """
    origin_lat = safe_float((origin or {}).get('lat'))  # comentario
    origin_lng = safe_float((origin or {}).get('lng'))  # comentario
    dest_lat = safe_float((destination or {}).get('lat'))  # comentario
    dest_lng = safe_float((destination or {}).get('lng'))  # comentario
    if origin_lat is None or origin_lng is None or dest_lat is None or dest_lng is None:  # comentario
        return {'provider': geo_provider(), 'routes': []}  # comentario

    mode = (travel_mode or 'DRIVE').strip().upper()  # comentario

    if geo_provider() != 'google':  # comentario
        profile_map = {  # comentario
            'DRIVE': 'driving',  # comentario
            'WALK': 'walking',  # comentario
            'BICYCLE': 'cycling',  # comentario
            'TWO_WHEELER': 'driving',  # comentario
        }  # comentario
        profile = profile_map.get(mode, 'driving')  # comentario
        endpoint = f"{osm_router_base_url()}/route/v1/{profile}/{origin_lng},{origin_lat};{dest_lng},{dest_lat}"  # comentario
        try:  # comentario
            data = http_json_get(  # comentario
                endpoint,  # comentario
                {  # comentario
                    'overview': 'full',  # comentario
                    'geometries': 'polyline',  # comentario
                    'alternatives': str(bool(alternatives)).lower(),  # comentario
                    'steps': 'false',  # comentario
                },  # comentario
                headers={'Accept': 'application/json'},  # comentario
            )  # comentario
        except Exception:  # comentario
            return {'provider': 'osm', 'routes': [], 'error': 'Routes API fallo.'}  # comentario

        if (data or {}).get('code') != 'Ok':  # comentario
            return {  # comentario
                'provider': 'osm',  # comentario
                'routes': [],  # comentario
                'error': (data or {}).get('message') or 'No se pudo calcular la ruta.',  # comentario
                'raw': data,  # comentario
            }  # comentario

        normalized = []  # comentario
        for route in (data.get('routes') or []):  # comentario
            distance_m = route.get('distance')  # comentario
            duration_sec = route.get('duration')  # comentario
            normalized.append({  # comentario
                'distance_meters': distance_m,  # comentario
                'distance_km': round(float(distance_m) / 1000, 2) if distance_m is not None else None,  # comentario
                'duration': f'{duration_sec}s' if duration_sec is not None else None,  # comentario
                'static_duration': f'{duration_sec}s' if duration_sec is not None else None,  # comentario
                'duration_seconds': int(duration_sec) if duration_sec is not None else None,  # comentario
                'static_duration_seconds': int(duration_sec) if duration_sec is not None else None,  # comentario
                'polyline': route.get('geometry') or '',  # comentario
            })  # comentario

        return {'provider': 'osm', 'routes': normalized}  # comentario

    key = _google_maps_server_key()  # comentario
    if not key:  # comentario
        return {'provider': 'google', 'routes': [], 'error': 'Falta configurar GOOGLE_MAPS_SERVER_API_KEY.'}  # comentario

    routing_preference = 'TRAFFIC_AWARE'  # comentario
    units = 'METRIC'  # comentario

    payload = {  # comentario
        'origin': {  # comentario
            'location': {  # comentario
                'latLng': {  # comentario
                    'latitude': origin_lat,  # comentario
                    'longitude': origin_lng,  # comentario
                }  # comentario
            }  # comentario
        },  # comentario
        'destination': {  # comentario
            'location': {  # comentario
                'latLng': {  # comentario
                    'latitude': dest_lat,  # comentario
                    'longitude': dest_lng,  # comentario
                }  # comentario
            }  # comentario
        },  # comentario
        'travelMode': mode,  # comentario
        'routingPreference': routing_preference,  # comentario
        'computeAlternativeRoutes': bool(alternatives),  # comentario
        'units': units,  # comentario
    }  # comentario

    field_mask = ','.join([  # comentario
        'routes.distanceMeters',  # comentario
        'routes.duration',  # comentario
        'routes.staticDuration',  # comentario
        'routes.polyline.encodedPolyline',  # comentario
    ])  # comentario

    try:  # comentario
        req = Request(  # comentario
            f'https://routes.googleapis.com/directions/v2:computeRoutes?key={key}',  # comentario
            data=json.dumps(payload).encode('utf-8'),  # comentario
            headers={  # comentario
                'Accept': 'application/json',  # comentario
                'Content-Type': 'application/json',  # comentario
                'X-Goog-FieldMask': field_mask,  # comentario
            },  # comentario
            method='POST',  # comentario
        )  # comentario
        with urlopen(req, timeout=8) as resp:  # comentario
            data = json.loads(resp.read().decode('utf-8'))  # comentario
    except Exception:  # comentario
        return {'provider': 'google', 'routes': [], 'error': 'Routes API fallo.'}  # comentario

    normalized = []  # comentario
    for route in (data.get('routes') or []):  # comentario
        distance_m = route.get('distanceMeters')  # comentario
        duration_raw = route.get('duration')  # comentario
        static_duration_raw = route.get('staticDuration')  # comentario
        encoded_polyline = (route.get('polyline') or {}).get('encodedPolyline') or ''  # comentario
        normalized.append({  # comentario
            'distance_meters': distance_m,  # comentario
            'distance_km': round(float(distance_m) / 1000, 2) if distance_m is not None else None,  # comentario
            'duration': duration_raw,  # comentario
            'static_duration': static_duration_raw,  # comentario
            'duration_seconds': parse_google_duration(duration_raw),  # comentario
            'static_duration_seconds': parse_google_duration(static_duration_raw),  # comentario
            'polyline': encoded_polyline,  # comentario
        })  # comentario

    return {'provider': 'google', 'routes': normalized}  # comentario


class GeoAutocompleteView(APIView):  # comentario
    permission_classes = [permissions.IsAuthenticated]  # comentario

    def _google_api_key(self):  # comentario
        return (getattr(settings, 'GOOGLE_MAPS_SERVER_API_KEY', '') or '').strip()  # comentario

    def _google_language(self):  # comentario
        return (getattr(settings, 'GOOGLE_MAPS_LANGUAGE', 'es') or 'es').strip()  # comentario

    def _google_region(self):  # comentario
        return (getattr(settings, 'GOOGLE_MAPS_REGION', 'ec') or 'ec').strip().lower()  # comentario

    def _http_json_get(self, endpoint, params, timeout=6):  # comentario
        req = Request(  # comentario
            f"{endpoint}?{urlencode(params)}",  # comentario
            headers={  # comentario
                'Accept': 'application/json',  # comentario
            },  # comentario
        )  # comentario
        with urlopen(req, timeout=timeout) as resp:  # comentario
            return json.loads(resp.read().decode('utf-8'))  # comentario

    def _extract_from_geocode_result(self, geocode_result):  # comentario
        components = geocode_result.get('address_components') or []  # comentario
        values = {}  # comentario
        for component in components:  # comentario
            name = component.get('long_name') or ''  # comentario
            for ctype in component.get('types') or []:  # comentario
                if ctype not in values:  # comentario
                    values[ctype] = name  # comentario

        road = values.get('route') or ''  # comentario
        house_number = values.get('street_number') or ''  # comentario
        main_address = (  # comentario
            f"{road} {house_number}".strip()  # comentario
            or geocode_result.get('formatted_address', '').split(',')[0].strip()  # comentario
        )  # comentario
        secondary_street = (  # comentario
            values.get('sublocality')  # comentario
            or values.get('sublocality_level_1')  # comentario
            or values.get('neighborhood')  # comentario
            or values.get('premise')  # comentario
            or ''  # comentario
        )  # comentario
        city = (  # comentario
            values.get('locality')  # comentario
            or values.get('administrative_area_level_2')  # comentario
            or values.get('postal_town')  # comentario
            or ''  # comentario
        )  # comentario
        region = values.get('administrative_area_level_1') or ''  # comentario
        country_name = values.get('country') or ''  # comentario

        geometry = geocode_result.get('geometry') or {}  # comentario
        location = geometry.get('location') or {}  # comentario
        try:  # comentario
            lat = float(location.get('lat')) if location.get('lat') is not None else None  # comentario
        except (TypeError, ValueError):  # comentario
            lat = None  # comentario
        try:  # comentario
            lng = float(location.get('lng')) if location.get('lng') is not None else None  # comentario
        except (TypeError, ValueError):  # comentario
            lng = None  # comentario

        return {  # comentario
            'label': geocode_result.get('formatted_address', ''),  # comentario
            'main_address': main_address,  # comentario
            'secondary_street': secondary_street,  # comentario
            'city': city,  # comentario
            'region': region,  # comentario
            'country': country_name,  # comentario
            'lat': lat,  # comentario
            'lng': lng,  # comentario
        }  # comentario

    def _geocode_place_id(self, place_id):  # comentario
        key = self._google_api_key()  # comentario
        if not key or not place_id:  # comentario
            return None  # comentario
        params = {  # comentario
            'place_id': place_id,  # comentario
            'language': self._google_language(),  # comentario
            'key': key,  # comentario
        }  # comentario
        payload = self._http_json_get(  # comentario
            'https://maps.googleapis.com/maps/api/geocode/json',  # comentario
            params,  # comentario
        )  # comentario
        if payload.get('status') != 'OK':  # comentario
            return None  # comentario
        results = payload.get('results') or []  # comentario
        if not results:  # comentario
            return None  # comentario
        return self._extract_from_geocode_result(results[0])  # comentario

    def get(self, request):  # comentario
        query = (request.query_params.get('q') or request.query_params.get('query') or '').strip()  # comentario
        if len(query) < 3:  # comentario
            return Response({'results': [], 'provider': geo_provider()})  # comentario

        country = (request.query_params.get('country') or self._google_region()).strip().lower()  # comentario
        try:  # comentario
            limit = int(request.query_params.get('limit', 5))  # comentario
        except (TypeError, ValueError):  # comentario
            limit = 5  # comentario
        limit = max(1, min(limit, 10))  # comentario

        if geo_provider() != 'google':  # comentario
            params = {  # comentario
                'format': 'jsonv2',  # comentario
                'addressdetails': 1,  # comentario
                'countrycodes': country,  # comentario
                'limit': limit,  # comentario
                'q': query,  # comentario
            }  # comentario
            try:  # comentario
                payload = http_json_get(  # comentario
                    f'{osm_nominatim_base_url()}/search',  # comentario
                    params,  # comentario
                    headers={  # comentario
                        'User-Agent': geocoder_user_agent(),  # comentario
                        'Accept': 'application/json',  # comentario
                    }  # comentario
                ) or []  # comentario
            except Exception:  # comentario
                return Response({'results': [], 'provider': 'osm'})  # comentario

            results = [extract_nominatim_result(item) for item in payload]  # comentario
            return Response({'results': results, 'provider': 'osm'})  # comentario

        key = self._google_api_key()  # comentario
        if not key:  # comentario
            return Response(  # comentario
                {  # comentario
                    'results': [],  # comentario
                    'provider': 'google',  # comentario
                    'error': 'Falta configurar GOOGLE_MAPS_SERVER_API_KEY en el backend.',  # comentario
                },  # comentario
                status=status.HTTP_503_SERVICE_UNAVAILABLE  # comentario
            )  # comentario

        params = {  # comentario
            'input': query,  # comentario
            'language': self._google_language(),  # comentario
            'components': f'country:{country}',  # comentario
            'types': 'address',  # comentario
            'key': key,  # comentario
        }  # comentario
        try:  # comentario
            payload = self._http_json_get(  # comentario
                'https://maps.googleapis.com/maps/api/place/autocomplete/json',  # comentario
                params,  # comentario
            )  # comentario
        except Exception:  # comentario
            return Response({'results': [], 'provider': 'google'})  # comentario

        status_name = payload.get('status')  # comentario
        if status_name not in {'OK', 'ZERO_RESULTS'}:  # comentario
            return Response({  # comentario
                'results': [],  # comentario
                'provider': 'google',  # comentario
                'error': payload.get('error_message') or status_name or 'Autocomplete fallo.',  # comentario
            })  # comentario

        predictions = (payload.get('predictions') or [])[:limit]  # comentario
        results = []  # comentario
        for item in predictions:  # comentario
            place_id = item.get('place_id') or ''  # comentario
            geocoded = self._geocode_place_id(place_id) or {}  # comentario
            label = item.get('description') or geocoded.get('label') or ''  # comentario
            structured = item.get('structured_formatting') or {}  # comentario
            main_text = structured.get('main_text') or ''  # comentario
            secondary_text = structured.get('secondary_text') or ''  # comentario

            results.append({  # comentario
                'place_id': place_id,  # comentario
                'label': label,  # comentario
                'main_text': main_text,  # comentario
                'secondary_text': secondary_text,  # comentario
                'main_address': geocoded.get('main_address') or main_text or label,  # comentario
                'secondary_street': geocoded.get('secondary_street') or secondary_text or '',  # comentario
                'city': geocoded.get('city') or '',  # comentario
                'region': geocoded.get('region') or '',  # comentario
                'country': geocoded.get('country') or '',  # comentario
                'lat': geocoded.get('lat'),  # comentario
                'lng': geocoded.get('lng'),  # comentario
            })  # comentario

        return Response({'results': results, 'provider': 'google'})  # comentario


class GeoGeocodeView(APIView):  # comentario
    permission_classes = [permissions.IsAuthenticated]  # comentario

    def _google_api_key(self):  # comentario
        return (getattr(settings, 'GOOGLE_MAPS_SERVER_API_KEY', '') or '').strip()  # comentario

    def _google_language(self):  # comentario
        return (getattr(settings, 'GOOGLE_MAPS_LANGUAGE', 'es') or 'es').strip()  # comentario

    def _http_json_get(self, endpoint, params, timeout=6):  # comentario
        req = Request(  # comentario
            f"{endpoint}?{urlencode(params)}",  # comentario
            headers={  # comentario
                'Accept': 'application/json',  # comentario
            },  # comentario
        )  # comentario
        with urlopen(req, timeout=timeout) as resp:  # comentario
            return json.loads(resp.read().decode('utf-8'))  # comentario

    def _extract_from_geocode_result(self, geocode_result):  # comentario
        components = geocode_result.get('address_components') or []  # comentario
        values = {}  # comentario
        for component in components:  # comentario
            name = component.get('long_name') or ''  # comentario
            for ctype in component.get('types') or []:  # comentario
                if ctype not in values:  # comentario
                    values[ctype] = name  # comentario

        road = values.get('route') or ''  # comentario
        house_number = values.get('street_number') or ''  # comentario
        main_address = (  # comentario
            f"{road} {house_number}".strip()  # comentario
            or geocode_result.get('formatted_address', '').split(',')[0].strip()  # comentario
        )  # comentario
        secondary_street = (  # comentario
            values.get('sublocality')  # comentario
            or values.get('sublocality_level_1')  # comentario
            or values.get('neighborhood')  # comentario
            or values.get('premise')  # comentario
            or ''  # comentario
        )  # comentario
        city = (  # comentario
            values.get('locality')  # comentario
            or values.get('administrative_area_level_2')  # comentario
            or values.get('postal_town')  # comentario
            or ''  # comentario
        )  # comentario
        region = values.get('administrative_area_level_1') or ''  # comentario
        country_name = values.get('country') or ''  # comentario

        geometry = geocode_result.get('geometry') or {}  # comentario
        location = geometry.get('location') or {}  # comentario
        try:  # comentario
            lat = float(location.get('lat')) if location.get('lat') is not None else None  # comentario
        except (TypeError, ValueError):  # comentario
            lat = None  # comentario
        try:  # comentario
            lng = float(location.get('lng')) if location.get('lng') is not None else None  # comentario
        except (TypeError, ValueError):  # comentario
            lng = None  # comentario

        return {  # comentario
            'place_id': geocode_result.get('place_id') or '',  # comentario
            'label': geocode_result.get('formatted_address', ''),  # comentario
            'main_address': main_address,  # comentario
            'secondary_street': secondary_street,  # comentario
            'city': city,  # comentario
            'region': region,  # comentario
            'country': country_name,  # comentario
            'lat': lat,  # comentario
            'lng': lng,  # comentario
        }  # comentario

    def get(self, request):  # comentario
        place_id = (request.query_params.get('place_id') or '').strip()  # comentario
        address = (request.query_params.get('q') or request.query_params.get('address') or '').strip()  # comentario
        lat = (request.query_params.get('lat') or '').strip()  # comentario
        lng = (request.query_params.get('lng') or '').strip()  # comentario

        if geo_provider() != 'google':  # comentario
            try:  # comentario
                if lat and lng:  # comentario
                    payload = http_json_get(  # comentario
                        f'{osm_nominatim_base_url()}/reverse',  # comentario
                        {  # comentario
                            'format': 'jsonv2',  # comentario
                            'addressdetails': 1,  # comentario
                            'lat': lat,  # comentario
                            'lon': lng,  # comentario
                        },  # comentario
                        headers={  # comentario
                            'User-Agent': geocoder_user_agent(),  # comentario
                            'Accept': 'application/json',  # comentario
                        }  # comentario
                    )  # comentario
                    raw_results = [payload] if isinstance(payload, dict) else []  # comentario
                elif address:  # comentario
                    raw_results = http_json_get(  # comentario
                        f'{osm_nominatim_base_url()}/search',  # comentario
                        {  # comentario
                            'format': 'jsonv2',  # comentario
                            'addressdetails': 1,  # comentario
                            'limit': 5,  # comentario
                            'q': address,  # comentario
                        },  # comentario
                        headers={  # comentario
                            'User-Agent': geocoder_user_agent(),  # comentario
                            'Accept': 'application/json',  # comentario
                        }  # comentario
                    ) or []  # comentario
                elif place_id:  # comentario
                    raw_results = http_json_get(  # comentario
                        f'{osm_nominatim_base_url()}/lookup',  # comentario
                        {  # comentario
                            'format': 'jsonv2',  # comentario
                            'addressdetails': 1,  # comentario
                            'place_ids': place_id,  # comentario
                        },  # comentario
                        headers={  # comentario
                            'User-Agent': geocoder_user_agent(),  # comentario
                            'Accept': 'application/json',  # comentario
                        }  # comentario
                    ) or []  # comentario
                else:  # comentario
                    return Response(  # comentario
                        {'error': 'Debes enviar place_id, q/address o lat+lng.'},  # comentario
                        status=status.HTTP_400_BAD_REQUEST  # comentario
                    )  # comentario
            except Exception:  # comentario
                return Response({'results': [], 'provider': 'osm'})  # comentario

            results = [extract_nominatim_result(item) for item in raw_results]  # comentario
            return Response({'results': results, 'provider': 'osm'})  # comentario

        key = self._google_api_key()  # comentario
        if not key:  # comentario
            return Response(  # comentario
                {  # comentario
                    'results': [],  # comentario
                    'provider': 'google',  # comentario
                    'error': 'Falta configurar GOOGLE_MAPS_SERVER_API_KEY en el backend.',  # comentario
                },  # comentario
                status=status.HTTP_503_SERVICE_UNAVAILABLE  # comentario
            )  # comentario

        params = {  # comentario
            'language': self._google_language(),  # comentario
            'key': key,  # comentario
        }  # comentario

        if place_id:  # comentario
            params['place_id'] = place_id  # comentario
        elif address:  # comentario
            params['address'] = address  # comentario
        elif lat and lng:  # comentario
            params['latlng'] = f'{lat},{lng}'  # comentario
        else:  # comentario
            return Response(  # comentario
                {'error': 'Debes enviar place_id, q/address o lat+lng.'},  # comentario
                status=status.HTTP_400_BAD_REQUEST  # comentario
            )  # comentario

        try:  # comentario
            payload = self._http_json_get(  # comentario
                'https://maps.googleapis.com/maps/api/geocode/json',  # comentario
                params,  # comentario
            )  # comentario
        except Exception:  # comentario
            return Response({'results': [], 'provider': 'google'})  # comentario

        status_name = payload.get('status')  # comentario
        if status_name not in {'OK', 'ZERO_RESULTS'}:  # comentario
            return Response({  # comentario
                'results': [],  # comentario
                'provider': 'google',  # comentario
                'error': payload.get('error_message') or status_name or 'Geocoding fallo.',  # comentario
            })  # comentario

        results = [  # comentario
            self._extract_from_geocode_result(item)  # comentario
            for item in (payload.get('results') or [])  # comentario
        ]  # comentario
        return Response({'results': results, 'provider': 'google'})  # comentario


class GeoAddressValidationView(APIView):  # comentario
    permission_classes = [permissions.IsAuthenticated]  # comentario

    def _google_api_key(self):  # comentario
        return (getattr(settings, 'GOOGLE_MAPS_SERVER_API_KEY', '') or '').strip()  # comentario

    def _google_region(self):  # comentario
        return (getattr(settings, 'GOOGLE_MAPS_REGION', 'EC') or 'EC').strip().upper()  # comentario

    def _http_json_post(self, endpoint, payload, timeout=8):  # comentario
        req = Request(  # comentario
            endpoint,  # comentario
            data=json.dumps(payload).encode('utf-8'),  # comentario
            headers={  # comentario
                'Accept': 'application/json',  # comentario
                'Content-Type': 'application/json',  # comentario
            },  # comentario
            method='POST',  # comentario
        )  # comentario
        with urlopen(req, timeout=timeout) as resp:  # comentario
            return json.loads(resp.read().decode('utf-8'))  # comentario

    def post(self, request):  # comentario
        address = (request.data.get('address') or '').strip()  # comentario
        if not address:  # comentario
            address = (  # comentario
                request.data.get('main_address')  # comentario
                or request.data.get('full_address')  # comentario
                or request.data.get('q')  # comentario
                or ''  # comentario
            ).strip()  # comentario

        if not address:  # comentario
            return Response(  # comentario
                {'error': 'Debes enviar address/main_address/full_address.'},  # comentario
                status=status.HTTP_400_BAD_REQUEST  # comentario
            )  # comentario

        secondary = (request.data.get('secondary_street') or '').strip()  # comentario
        city = (request.data.get('city') or '').strip()  # comentario
        region = (request.data.get('region') or '').strip()  # comentario
        country = (request.data.get('country') or self._google_region()).strip()  # comentario

        if geo_provider() != 'google':  # comentario
            query = ', '.join([part for part in [address, secondary, city, region, country] if part]).strip()  # comentario
            try:  # comentario
                payload = http_json_get(  # comentario
                    f'{osm_nominatim_base_url()}/search',  # comentario
                    {  # comentario
                        'format': 'jsonv2',  # comentario
                        'addressdetails': 1,  # comentario
                        'limit': 1,  # comentario
                        'q': query,  # comentario
                    },  # comentario
                    headers={  # comentario
                        'User-Agent': geocoder_user_agent(),  # comentario
                        'Accept': 'application/json',  # comentario
                    }  # comentario
                ) or []  # comentario
            except Exception:  # comentario
                return Response({'provider': 'osm', 'valid': False, 'error': 'Address Validation fallo.'})  # comentario

            first = payload[0] if payload else None  # comentario
            if not first:  # comentario
                return Response({  # comentario
                    'provider': 'osm',  # comentario
                    'valid': False,  # comentario
                    'address_complete': False,  # comentario
                    'formatted_address': '',  # comentario
                    'place_id': '',  # comentario
                    'lat': None,  # comentario
                    'lng': None,  # comentario
                    'raw': payload,  # comentario
                })  # comentario

            parsed = extract_nominatim_result(first)  # comentario
            importance = first.get('importance')  # comentario
            try:  # comentario
                importance = float(importance) if importance is not None else None  # comentario
            except (TypeError, ValueError):  # comentario
                importance = None  # comentario

            return Response({  # comentario
                'provider': 'osm',  # comentario
                'valid': True,  # comentario
                'address_complete': True,  # comentario
                'has_inferred_components': False,  # comentario
                'has_unconfirmed_components': False,  # comentario
                'formatted_address': parsed.get('label') or '',  # comentario
                'place_id': parsed.get('place_id') or '',  # comentario
                'lat': parsed.get('lat'),  # comentario
                'lng': parsed.get('lng'),  # comentario
                'confidence': importance,  # comentario
                'raw': payload,  # comentario
            })  # comentario

        key = self._google_api_key()  # comentario
        if not key:  # comentario
            return Response(  # comentario
                {  # comentario
                    'provider': 'google',  # comentario
                    'error': 'Falta configurar GOOGLE_MAPS_SERVER_API_KEY en el backend.',  # comentario
                },  # comentario
                status=status.HTTP_503_SERVICE_UNAVAILABLE  # comentario
            )  # comentario

        lines = [address]  # comentario
        if secondary:  # comentario
            lines.append(secondary)  # comentario
        if city:  # comentario
            lines.append(city)  # comentario
        if region:  # comentario
            lines.append(region)  # comentario
        if country:  # comentario
            lines.append(country)  # comentario

        payload = {  # comentario
            'address': {  # comentario
                'addressLines': lines,  # comentario
                'regionCode': self._google_region(),  # comentario
            }  # comentario
        }  # comentario
        if country:  # comentario
            payload['address']['regionCode'] = country[:2].upper()  # comentario

        try:  # comentario
            data = self._http_json_post(  # comentario
                f'https://addressvalidation.googleapis.com/v1:validateAddress?key={key}',  # comentario
                payload,  # comentario
            )  # comentario
        except Exception:  # comentario
            return Response({'provider': 'google', 'valid': False, 'error': 'Address Validation fallo.'})  # comentario

        verdict = data.get('result', {}).get('verdict', {})  # comentario
        geocode = data.get('result', {}).get('geocode', {})  # comentario
        location = geocode.get('location') or {}  # comentario
        address_info = data.get('result', {}).get('address', {})  # comentario

        try:  # comentario
            lat = float(location.get('latitude')) if location.get('latitude') is not None else None  # comentario
        except (TypeError, ValueError):  # comentario
            lat = None  # comentario
        try:  # comentario
            lng = float(location.get('longitude')) if location.get('longitude') is not None else None  # comentario
        except (TypeError, ValueError):  # comentario
            lng = None  # comentario

        is_valid = bool(verdict.get('addressComplete')) or bool(verdict.get('validationGranularity'))  # comentario

        return Response({  # comentario
            'provider': 'google',  # comentario
            'valid': is_valid,  # comentario
            'address_complete': bool(verdict.get('addressComplete')),  # comentario
            'has_inferred_components': bool(verdict.get('hasInferredComponents')),  # comentario
            'has_unconfirmed_components': bool(verdict.get('hasUnconfirmedComponents')),  # comentario
            'formatted_address': address_info.get('formattedAddress') or '',  # comentario
            'place_id': geocode.get('placeId') or '',  # comentario
            'lat': lat,  # comentario
            'lng': lng,  # comentario
            'raw': data,  # comentario
        })  # comentario


class GeoRouteEstimateView(APIView):  # comentario
    permission_classes = [permissions.IsAuthenticated]  # comentario

    def _google_api_key(self):  # comentario
        return (getattr(settings, 'GOOGLE_MAPS_SERVER_API_KEY', '') or '').strip()  # comentario

    def _http_json_post(self, endpoint, payload, field_mask, timeout=8):  # comentario
        req = Request(  # comentario
            endpoint,  # comentario
            data=json.dumps(payload).encode('utf-8'),  # comentario
            headers={  # comentario
                'Accept': 'application/json',  # comentario
                'Content-Type': 'application/json',  # comentario
                'X-Goog-FieldMask': field_mask,  # comentario
            },  # comentario
            method='POST',  # comentario
        )  # comentario
        with urlopen(req, timeout=timeout) as resp:  # comentario
            return json.loads(resp.read().decode('utf-8'))  # comentario

    def post(self, request):  # comentario
        origin = request.data.get('origin') or {}  # comentario
        destination = request.data.get('destination') or {}  # comentario
        mode = (request.data.get('travel_mode') or 'DRIVE').strip().upper()  # comentario

        if not isinstance(origin, dict) or not isinstance(destination, dict):  # comentario
            return Response(  # comentario
                {'error': 'origin y destination deben ser objetos con lat/lng.'},  # comentario
                status=status.HTTP_400_BAD_REQUEST  # comentario
            )  # comentario

        if origin.get('lat') is None or origin.get('lng') is None:  # comentario
            return Response({'error': 'origin.lat y origin.lng son obligatorios.'}, status=status.HTTP_400_BAD_REQUEST)  # comentario
        if destination.get('lat') is None or destination.get('lng') is None:  # comentario
            return Response(  # comentario
                {'error': 'destination.lat y destination.lng son obligatorios.'},  # comentario
                status=status.HTTP_400_BAD_REQUEST  # comentario
            )  # comentario

        if geo_provider() != 'google':  # comentario
            profile_map = {  # comentario
                'DRIVE': 'driving',  # comentario
                'WALK': 'walking',  # comentario
                'BICYCLE': 'cycling',  # comentario
                'TWO_WHEELER': 'driving',  # comentario
            }  # comentario
            profile = profile_map.get(mode, 'driving')  # comentario
            try:  # comentario
                orig_lat = float(origin['lat'])  # comentario
                orig_lng = float(origin['lng'])  # comentario
                dst_lat = float(destination['lat'])  # comentario
                dst_lng = float(destination['lng'])  # comentario
            except (TypeError, ValueError):  # comentario
                return Response({'error': 'lat/lng deben ser numericos.'}, status=status.HTTP_400_BAD_REQUEST)  # comentario

            endpoint = (  # comentario
                f"{osm_router_base_url()}/route/v1/{profile}/"  # comentario
                f"{orig_lng},{orig_lat};{dst_lng},{dst_lat}"  # comentario
            )  # comentario
            try:  # comentario
                data = http_json_get(  # comentario
                    endpoint,  # comentario
                    {  # comentario
                        'overview': 'full',  # comentario
                        'geometries': 'polyline',  # comentario
                        'alternatives': str(bool(request.data.get('alternatives', False))).lower(),  # comentario
                        'steps': 'false',  # comentario
                    },  # comentario
                    headers={'Accept': 'application/json'}  # comentario
                )  # comentario
            except Exception:  # comentario
                return Response({'provider': 'osm', 'routes': [], 'error': 'Routes API fallo.'})  # comentario

            if (data or {}).get('code') != 'Ok':  # comentario
                return Response({  # comentario
                    'provider': 'osm',  # comentario
                    'routes': [],  # comentario
                    'error': (data or {}).get('message') or 'No se pudo calcular la ruta.',  # comentario
                    'raw': data,  # comentario
                })  # comentario

            routes = data.get('routes') or []  # comentario
            normalized = []  # comentario
            for route in routes:  # comentario
                distance_m = route.get('distance')  # comentario
                duration_sec = route.get('duration')  # comentario
                normalized.append({  # comentario
                    'distance_meters': distance_m,  # comentario
                    'distance_km': round(float(distance_m) / 1000, 2) if distance_m is not None else None,  # comentario
                    'duration': f'{duration_sec}s' if duration_sec is not None else None,  # comentario
                    'static_duration': f'{duration_sec}s' if duration_sec is not None else None,  # comentario
                    'duration_seconds': int(duration_sec) if duration_sec is not None else None,  # comentario
                    'static_duration_seconds': int(duration_sec) if duration_sec is not None else None,  # comentario
                    'polyline': route.get('geometry') or '',  # comentario
                    'leg': {  # comentario
                        'distance_meters': distance_m,  # comentario
                        'duration': f'{duration_sec}s' if duration_sec is not None else None,  # comentario
                        'static_duration': f'{duration_sec}s' if duration_sec is not None else None,  # comentario
                        'polyline': route.get('geometry') or '',  # comentario
                    },  # comentario
                })  # comentario

            return Response({'provider': 'osm', 'routes': normalized, 'raw': data})  # comentario

        key = self._google_api_key()  # comentario
        if not key:  # comentario
            return Response(  # comentario
                {  # comentario
                    'provider': 'google',  # comentario
                    'error': 'Falta configurar GOOGLE_MAPS_SERVER_API_KEY en el backend.',  # comentario
                },  # comentario
                status=status.HTTP_503_SERVICE_UNAVAILABLE  # comentario
            )  # comentario

        routing_preference = (request.data.get('routing_preference') or 'TRAFFIC_AWARE').strip().upper()  # comentario
        units = (request.data.get('units') or 'METRIC').strip().upper()  # comentario

        payload = {  # comentario
            'origin': {  # comentario
                'location': {  # comentario
                    'latLng': {  # comentario
                        'latitude': float(origin['lat']),  # comentario
                        'longitude': float(origin['lng']),  # comentario
                    }  # comentario
                }  # comentario
            },  # comentario
            'destination': {  # comentario
                'location': {  # comentario
                    'latLng': {  # comentario
                        'latitude': float(destination['lat']),  # comentario
                        'longitude': float(destination['lng']),  # comentario
                    }  # comentario
                }  # comentario
            },  # comentario
            'travelMode': mode,  # comentario
            'routingPreference': routing_preference,  # comentario
            'computeAlternativeRoutes': bool(request.data.get('alternatives', False)),  # comentario
            'units': units,  # comentario
        }  # comentario

        field_mask = ','.join([  # comentario
            'routes.distanceMeters',  # comentario
            'routes.duration',  # comentario
            'routes.staticDuration',  # comentario
            'routes.polyline.encodedPolyline',  # comentario
            'routes.legs.distanceMeters',  # comentario
            'routes.legs.duration',  # comentario
            'routes.legs.staticDuration',  # comentario
            'routes.legs.polyline.encodedPolyline',  # comentario
        ])  # comentario

        try:  # comentario
            data = self._http_json_post(  # comentario
                f'https://routes.googleapis.com/directions/v2:computeRoutes?key={key}',  # comentario
                payload,  # comentario
                field_mask=field_mask,  # comentario
            )  # comentario
        except Exception:  # comentario
            return Response({'provider': 'google', 'routes': [], 'error': 'Routes API fallo.'})  # comentario

        routes = data.get('routes') or []  # comentario
        normalized = []  # comentario
        for route in routes:  # comentario
            distance_m = route.get('distanceMeters')  # comentario
            duration_raw = route.get('duration')  # comentario
            static_duration_raw = route.get('staticDuration')  # comentario
            encoded_polyline = (route.get('polyline') or {}).get('encodedPolyline') or ''  # comentario
            leg = (route.get('legs') or [{}])[0]  # comentario
            normalized.append({  # comentario
                'distance_meters': distance_m,  # comentario
                'distance_km': round(float(distance_m) / 1000, 2) if distance_m is not None else None,  # comentario
                'duration': duration_raw,  # comentario
                'static_duration': static_duration_raw,  # comentario
                'duration_seconds': self._parse_google_duration(duration_raw),  # comentario
                'static_duration_seconds': self._parse_google_duration(static_duration_raw),  # comentario
                'polyline': encoded_polyline,  # comentario
                'leg': {  # comentario
                    'distance_meters': leg.get('distanceMeters'),  # comentario
                    'duration': leg.get('duration'),  # comentario
                    'static_duration': leg.get('staticDuration'),  # comentario
                    'polyline': (leg.get('polyline') or {}).get('encodedPolyline') or '',  # comentario
                },  # comentario
            })  # comentario

        return Response({'provider': 'google', 'routes': normalized, 'raw': data})  # comentario

    def _parse_google_duration(self, value):  # comentario
        # Google duration viene como string tipo "123s".
        if not value or not isinstance(value, str):  # comentario
            return None  # comentario
        if not value.endswith('s'):  # comentario
            return None  # comentario
        try:  # comentario
            return int(float(value[:-1]))  # comentario
        except (TypeError, ValueError):  # comentario
            return None  # comentario
