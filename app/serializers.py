from rest_framework import serializers  # comentario
from django.contrib.auth.models import Group, User  # comentario
from .models import (  # comentario
    Banner,  # comentario
    Category,  # comentario
    Product,  # comentario
    Cart,  # comentario
    UserProfile,  # comentario
    DeliveryAddress,  # comentario
    RoleChangeRequest,  # comentario
    Order,  # comentario
    OrderItem,  # comentario
    Shipment,  # comentario
    ShipmentLocation,  # comentario
)  # comentario


# =====================================================
# SERIALIZER DE REGISTRO DE USUARIO (SIN ROLES)
# =====================================================

class RegisterSerializer(serializers.ModelSerializer):  # comentario
    full_name = serializers.CharField(write_only=True, required=False, allow_blank=True)  # comentario
    phone = serializers.CharField(write_only=True, required=False, allow_blank=True)  # comentario
    address = serializers.CharField(write_only=True, required=False, allow_blank=True)  # comentario
    username = serializers.CharField(required=False, allow_blank=True)  # comentario
    role = serializers.CharField(write_only=True, required=False, allow_blank=True)  # comentario
    role_reason = serializers.CharField(write_only=True, required=False, allow_blank=True)  # comentario
    password = serializers.CharField(write_only=True)  # comentario
    password2 = serializers.CharField(write_only=True, required=False, allow_blank=True)  # comentario

    class Meta:  # comentario
        model = User  # comentario
        fields = [  # comentario
            'full_name',  # comentario
            'email',  # comentario
            'phone',  # comentario
            'address',  # comentario
            'username',  # comentario
            'role',  # comentario
            'role_reason',  # comentario
            'password',  # comentario
            'password2',  # comentario
        ]  # comentario
        extra_kwargs = {  # comentario
            'email': {'required': True},  # comentario
            'username': {'required': False},  # comentario
        }  # comentario

    def to_internal_value(self, data):  # comentario
        raw_data = data.copy()  # comentario

        if 'full_name' not in raw_data:  # comentario
            raw_data['full_name'] = (  # comentario
                data.get('full_name')  # comentario
                or data.get('name')  # comentario
                or data.get('nombre')  # comentario
                or data.get('fullName')  # comentario
                or ''  # comentario
            )  # comentario

        if 'phone' not in raw_data:  # comentario
            raw_data['phone'] = (  # comentario
                data.get('phone')  # comentario
                or data.get('Phone')  # comentario
                or data.get('telefono')  # comentario
                or data.get('celular')  # comentario
                or ''  # comentario
            )  # comentario

        if 'address' not in raw_data:  # comentario
            raw_data['address'] = (  # comentario
                data.get('address')  # comentario
                or data.get('Address')  # comentario
                or data.get('direccion')  # comentario
                or data.get('dirección')  # comentario
                or data.get('main_address')  # comentario
                or data.get('direccion_principal')  # comentario
                or data.get('address_line_1')  # comentario
                or data.get('street')  # comentario
                or ''  # comentario
            )  # comentario

        if 'username' not in raw_data:  # comentario
            raw_data['username'] = (  # comentario
                data.get('username')  # comentario
                or data.get('usuario')  # comentario
                or data.get('user')  # comentario
                or ''  # comentario
            )  # comentario

        if 'password' not in raw_data:  # comentario
            raw_data['password'] = data.get('password') or data.get('contrasena') or ''  # comentario

        if 'password2' not in raw_data:  # comentario
            raw_data['password2'] = (  # comentario
                data.get('password2')  # comentario
                or data.get('confirm_password')  # comentario
                or data.get('confirmPassword')  # comentario
                or data.get('password_confirmation')  # comentario
                or ''  # comentario
            )  # comentario

        if 'role' not in raw_data:  # comentario
            raw_data['role'] = (  # comentario
                data.get('role')  # comentario
                or data.get('requested_role')  # comentario
                or data.get('user_role')  # comentario
                or ''  # comentario
            )  # comentario

        if 'role_reason' not in raw_data:  # comentario
            raw_data['role_reason'] = (  # comentario
                data.get('role_reason')  # comentario
                or data.get('reason')  # comentario
                or data.get('motivo')  # comentario
                or ''  # comentario
            )  # comentario

        return super().to_internal_value(raw_data)  # comentario

    def validate(self, attrs):  # comentario
        password = attrs.get('password')  # comentario
        password2 = attrs.get('password2')  # comentario
        email = (attrs.get('email') or '').strip().lower()  # comentario
        username = (attrs.get('username') or '').strip()  # comentario
        phone = (attrs.get('phone') or '').strip()  # comentario
        address = (attrs.get('address') or '').strip()  # comentario
        role = (attrs.get('role') or '').strip().lower()  # comentario

        if not password:  # comentario
            raise serializers.ValidationError({'password': 'Este campo es obligatorio.'})  # comentario

        if password2 and password != password2:  # comentario
            raise serializers.ValidationError({'password2': 'Las contrasenas no coinciden.'})  # comentario

        if not phone:  # comentario
            raise serializers.ValidationError({'phone': 'El telefono es obligatorio.'})  # comentario

        if not phone.isdigit():  # comentario
            raise serializers.ValidationError({'phone': 'El telefono solo debe contener numeros.'})  # comentario

        if len(phone) != 10:  # comentario
            raise serializers.ValidationError({'phone': 'El telefono debe tener exactamente 10 digitos.'})  # comentario

        if not phone.startswith('09'):  # comentario
            raise serializers.ValidationError({'phone': 'El telefono debe iniciar con 09.'})  # comentario

        if not address:  # comentario
            raise serializers.ValidationError({'address': 'La direccion es obligatoria.'})  # comentario

        if User.objects.filter(email=email).exists():  # comentario
            raise serializers.ValidationError({'email': 'Ya existe una cuenta con este correo.'})  # comentario

        if not username:  # comentario
            base_username = (email.split('@')[0] if email else 'usuario').replace(' ', '')  # comentario
            username = base_username or 'usuario'  # comentario
            suffix = 1  # comentario
            candidate = username  # comentario
            while User.objects.filter(username=candidate).exists():  # comentario
                suffix += 1  # comentario
                candidate = f'{username}{suffix}'  # comentario
            attrs['username'] = candidate  # comentario
        elif User.objects.filter(username=username).exists():  # comentario
            raise serializers.ValidationError({'username': 'Este usuario ya existe.'})  # comentario

        role_map = {  # comentario
            'cliente': 'client',  # comentario
            'client': 'client',  # comentario
            'customer': 'client',  # comentario
            'usuario': 'client',  # comentario
            'user': 'client',  # comentario
            'repartidor': 'driver',  # comentario
            'driver': 'driver',  # comentario
            'proveedor': 'provider',  # comentario
            'provider': 'provider',  # comentario
        }  # comentario
        normalized_role = role_map.get(role, role)  # comentario
        if normalized_role and normalized_role not in {'client', 'driver', 'provider'}:  # comentario
            raise serializers.ValidationError({'role': 'Rol invalido. Usa client, driver o provider.'})  # comentario

        attrs['email'] = email  # comentario
        attrs['phone'] = phone  # comentario
        attrs['address'] = address  # comentario
        attrs['role'] = normalized_role  # comentario
        return attrs  # comentario

    def create(self, validated_data):  # comentario
        full_name = (validated_data.pop('full_name', '') or '').strip()  # comentario
        phone = (validated_data.pop('phone', '') or '').strip()  # comentario
        address = (validated_data.pop('address', '') or '').strip()  # comentario
        requested_role = validated_data.pop('role', '')  # comentario
        role_reason = (validated_data.pop('role_reason', '') or '').strip()  # comentario
        validated_data.pop('password2', None)  # comentario

        password = validated_data.pop('password')  # comentario
        user = User.objects.create_user(  # comentario
            password=password,  # comentario
            **validated_data  # comentario
        )  # comentario

        if full_name:  # comentario
            name_parts = full_name.split(maxsplit=1)  # comentario
            user.first_name = name_parts[0]  # comentario
            user.last_name = name_parts[1] if len(name_parts) > 1 else ''  # comentario
            user.save(update_fields=['first_name', 'last_name'])  # comentario

        UserProfile.objects.update_or_create(  # comentario
            user=user,  # comentario
            defaults={  # comentario
                'phone': phone,  # comentario
                'address': address,  # comentario
            }  # comentario
        )  # comentario

        # Rol base para todas las cuentas.
        cliente_group, _ = Group.objects.get_or_create(name='CLIENTE')  # comentario
        user.groups.add(cliente_group)  # comentario

        # Para roles operativos, crea solicitud pendiente en registro.
        if requested_role in {'driver', 'provider'}:  # comentario
            RoleChangeRequest.objects.create(  # comentario
                user=user,  # comentario
                requested_role=requested_role,  # comentario
                reason=role_reason or 'Solicitud creada durante el registro.',  # comentario
                status='pending',  # comentario
            )  # comentario

        return user  # comentario


class RegisteredUserSerializer(serializers.ModelSerializer):  # comentario
    full_name = serializers.SerializerMethodField()  # comentario
    phone = serializers.SerializerMethodField()  # comentario
    address = serializers.SerializerMethodField()  # comentario
    avatar_url = serializers.SerializerMethodField()  # comentario
    roles = serializers.SerializerMethodField()  # comentario

    class Meta:  # comentario
        model = User  # comentario
        fields = [  # comentario
            'id',  # comentario
            'username',  # comentario
            'email',  # comentario
            'full_name',  # comentario
            'phone',  # comentario
            'address',  # comentario
            'avatar_url',  # comentario
            'roles',  # comentario
            'date_joined',  # comentario
            'is_active',  # comentario
        ]  # comentario
        read_only_fields = fields  # comentario

    def get_full_name(self, instance):  # comentario
        return f'{instance.first_name} {instance.last_name}'.strip()  # comentario

    def get_phone(self, instance):  # comentario
        return getattr(getattr(instance, 'profile', None), 'phone', '')  # comentario

    def get_address(self, instance):  # comentario
        return getattr(getattr(instance, 'profile', None), 'address', '')  # comentario

    def get_avatar_url(self, instance):  # comentario
        avatar = getattr(getattr(instance, 'profile', None), 'avatar', None)  # comentario
        if not avatar:  # comentario
            return ''  # comentario
        request = self.context.get('request')  # comentario
        if request is None:  # comentario
            return avatar.url  # comentario
        return request.build_absolute_uri(avatar.url)  # comentario

    def get_roles(self, instance):  # comentario
        return sorted(list(instance.groups.values_list('name', flat=True)))  # comentario


# =====================================================
# SERIALIZER DE CATEGORIAS
# =====================================================

class CategorySerializer(serializers.ModelSerializer):  # comentario
    image_url = serializers.SerializerMethodField()  # comentario

    class Meta:  # comentario
        model = Category  # comentario
        fields = ['id', 'name', 'order', 'image', 'image_url']  # comentario

    def get_image_url(self, obj):  # comentario
        if not obj.image:  # comentario
            return ''  # comentario
        request = self.context.get('request')  # comentario
        if request is None:  # comentario
            return obj.image.url  # comentario
        return request.build_absolute_uri(obj.image.url)  # comentario


# =====================================================
# SERIALIZER DE BANNERS
# =====================================================

class BannerSerializer(serializers.ModelSerializer):  # comentario
    image_url = serializers.SerializerMethodField()  # comentario

    class Meta:  # comentario
        model = Banner  # comentario
        fields = ['id', 'title', 'image', 'image_url', 'order']  # comentario

    def get_image_url(self, obj):  # comentario
        if not obj.image:  # comentario
            return ''  # comentario
        request = self.context.get('request')  # comentario
        if request is None:  # comentario
            return obj.image.url  # comentario
        return request.build_absolute_uri(obj.image.url)  # comentario


# =====================================================
# SERIALIZER DE PRODUCTOS
# =====================================================

class ProductSerializer(serializers.ModelSerializer):  # comentario
    image_url = serializers.SerializerMethodField()  # comentario
    category_name = serializers.CharField(source='category.name', read_only=True)  # comentario

    class Meta:  # comentario
        model = Product  # comentario
        fields = [  # comentario
            'id',  # comentario
            'name',  # comentario
            'price',  # comentario
            'old_price',  # comentario
            'description',  # comentario
            'store_name',  # comentario
            'rating',  # comentario
            'reviews_count',  # comentario
            'stock',  # comentario
            'image',  # comentario
            'image_url',  # comentario
            'category',  # comentario
            'category_name',  # comentario
        ]  # comentario

    def get_image_url(self, obj):  # comentario
        if not obj.image:  # comentario
            return ''  # comentario
        request = self.context.get('request')  # comentario
        if request is None:  # comentario
            return obj.image.url  # comentario
        return request.build_absolute_uri(obj.image.url)  # comentario


# =====================================================
# SERIALIZER DE CARRITO
# =====================================================

class CartSerializer(serializers.ModelSerializer):  # comentario
    user = serializers.PrimaryKeyRelatedField(read_only=True)  # comentario
    product_name = serializers.CharField(source='product.name', read_only=True)  # comentario
    product_price = serializers.DecimalField(  # comentario
        source='product.price',  # comentario
        max_digits=8,  # comentario
        decimal_places=2,  # comentario
        read_only=True,  # comentario
    )  # comentario
    product_image_url = serializers.SerializerMethodField()  # comentario

    class Meta:  # comentario
        model = Cart  # comentario
        fields = [  # comentario
            'id',  # comentario
            'user',  # comentario
            'product',  # comentario
            'quantity',  # comentario
            'product_name',  # comentario
            'product_price',  # comentario
            'product_image_url',  # comentario
        ]  # comentario
        read_only_fields = ['id', 'user', 'product_name', 'product_price', 'product_image_url']  # comentario

    def to_internal_value(self, data):  # comentario
        raw_data = data.copy() if hasattr(data, 'copy') else dict(data)  # comentario

        if 'product' not in raw_data:  # comentario
            raw_data['product'] = (  # comentario
                data.get('product_id')  # comentario
                or data.get('productId')  # comentario
                or data.get('producto')  # comentario
                or data.get('id_producto')  # comentario
            )  # comentario

        if 'quantity' not in raw_data:  # comentario
            raw_data['quantity'] = (  # comentario
                data.get('quantity')  # comentario
                or data.get('cantidad')  # comentario
                or data.get('qty')  # comentario
                or 1  # comentario
            )  # comentario

        return super().to_internal_value(raw_data)  # comentario

    def validate_quantity(self, value):  # comentario
        if value < 1:  # comentario
            raise serializers.ValidationError('La cantidad debe ser mayor a 0.')  # comentario
        return value  # comentario

    def get_product_image_url(self, obj):  # comentario
        if not obj.product or not obj.product.image:  # comentario
            return ''  # comentario
        request = self.context.get('request')  # comentario
        if request is None:  # comentario
            return obj.product.image.url  # comentario
        return request.build_absolute_uri(obj.product.image.url)  # comentario


class OrderItemSerializer(serializers.ModelSerializer):  # comentario
    product = serializers.PrimaryKeyRelatedField(read_only=True)  # comentario
    product_image_url = serializers.SerializerMethodField()  # comentario

    class Meta:  # comentario
        model = OrderItem  # comentario
        fields = [  # comentario
            'id',  # comentario
            'product',  # comentario
            'product_name',  # comentario
            'product_price',  # comentario
            'quantity',  # comentario
            'subtotal',  # comentario
            'product_image_url',  # comentario
        ]  # comentario
        read_only_fields = fields  # comentario

    def get_product_image_url(self, obj):  # comentario
        if not obj.product or not obj.product.image:  # comentario
            return ''  # comentario
        request = self.context.get('request')  # comentario
        if request is None:  # comentario
            return obj.product.image.url  # comentario
        return request.build_absolute_uri(obj.product.image.url)  # comentario


class OrderSerializer(serializers.ModelSerializer):  # comentario
    user = serializers.PrimaryKeyRelatedField(read_only=True)  # comentario
    items = OrderItemSerializer(many=True, read_only=True)  # comentario
    status_label = serializers.CharField(source='get_status_display', read_only=True)  # comentario

    class Meta:  # comentario
        model = Order  # comentario
        fields = [  # comentario
            'id',  # comentario
            'user',  # comentario
            'delivery_address',  # comentario
            'delivery_main_address',  # comentario
            'delivery_secondary_street',  # comentario
            'delivery_apartment',  # comentario
            'delivery_city',  # comentario
            'delivery_latitude',  # comentario
            'delivery_longitude',  # comentario
            'delivery_instructions',  # comentario
            'status',  # comentario
            'status_label',  # comentario
            'total_amount',  # comentario
            'total_items',  # comentario
            'created_at',  # comentario
            'updated_at',  # comentario
            'items',  # comentario
        ]  # comentario
        read_only_fields = fields  # comentario


class OrderCreateSerializer(serializers.Serializer):  # comentario
    delivery_address = serializers.PrimaryKeyRelatedField(  # comentario
        queryset=DeliveryAddress.objects.all(),  # comentario
        required=False,  # comentario
        allow_null=True,  # comentario
    )  # comentario

    def to_internal_value(self, data):  # comentario
        raw_data = data.copy() if hasattr(data, 'copy') else dict(data)  # comentario
        if 'delivery_address' not in raw_data:  # comentario
            raw_data['delivery_address'] = (  # comentario
                data.get('delivery_address')  # comentario
                or data.get('address_id')  # comentario
                or data.get('address')  # comentario
                or data.get('direccion_id')  # comentario
            )  # comentario
        return super().to_internal_value(raw_data)  # comentario


class ShipmentLocationSerializer(serializers.ModelSerializer):  # comentario
    class Meta:  # comentario
        model = ShipmentLocation  # comentario
        fields = ['id', 'latitude', 'longitude', 'heading', 'speed', 'recorded_at']  # comentario
        read_only_fields = fields  # comentario


class ShipmentSerializer(serializers.ModelSerializer):  # comentario
    order = serializers.PrimaryKeyRelatedField(read_only=True)  # comentario
    driver = serializers.PrimaryKeyRelatedField(read_only=True)  # comentario
    driver_name = serializers.SerializerMethodField()  # comentario
    status_label = serializers.CharField(source='get_status_display', read_only=True)  # comentario
    locations = serializers.SerializerMethodField()  # comentario
    has_live_location = serializers.SerializerMethodField()  # comentario

    class Meta:  # comentario
        model = Shipment  # comentario
        fields = [  # comentario
            'id',  # comentario
            'order',  # comentario
            'driver',  # comentario
            'driver_name',  # comentario
            'status',  # comentario
            'status_label',  # comentario
            'current_latitude',  # comentario
            'current_longitude',  # comentario
            'current_heading',  # comentario
            'current_speed',  # comentario
            'last_location_at',  # comentario
            'eta_minutes',  # comentario
            'notes',  # comentario
            'created_at',  # comentario
            'updated_at',  # comentario
            'has_live_location',  # comentario
            'locations',  # comentario
        ]  # comentario
        read_only_fields = fields  # comentario

    def get_driver_name(self, obj):  # comentario
        if not obj.driver:  # comentario
            return ''  # comentario
        full_name = f'{obj.driver.first_name} {obj.driver.last_name}'.strip()  # comentario
        return full_name or obj.driver.username  # comentario

    def get_has_live_location(self, obj):  # comentario
        return obj.current_latitude is not None and obj.current_longitude is not None  # comentario

    def get_locations(self, obj):  # comentario
        request = self.context.get('request')  # comentario
        try:  # comentario
            raw_limit = request.query_params.get('points', 60) if request else 60  # comentario
            limit = int(raw_limit)  # comentario
        except (TypeError, ValueError):  # comentario
            limit = 60  # comentario
        limit = max(1, min(limit, 300))  # comentario
        qs = obj.locations.all().order_by('-recorded_at', '-id')[:limit]  # comentario
        return ShipmentLocationSerializer(qs, many=True).data  # comentario


class ShipmentLocationUpdateSerializer(serializers.Serializer):  # comentario
    latitude = serializers.DecimalField(max_digits=9, decimal_places=6)  # comentario
    longitude = serializers.DecimalField(max_digits=9, decimal_places=6)  # comentario
    heading = serializers.DecimalField(max_digits=6, decimal_places=2, required=False, allow_null=True)  # comentario
    speed = serializers.DecimalField(max_digits=6, decimal_places=2, required=False, allow_null=True)  # comentario
    status = serializers.ChoiceField(choices=Shipment.STATUS_CHOICES, required=False)  # comentario
    eta_minutes = serializers.IntegerField(required=False, allow_null=True, min_value=0)  # comentario
    notes = serializers.CharField(required=False, allow_blank=True, max_length=255)  # comentario

    def to_internal_value(self, data):  # comentario
        raw_data = data.copy() if hasattr(data, 'copy') else dict(data)  # comentario

        if 'latitude' not in raw_data:  # comentario
            raw_data['latitude'] = data.get('lat') or data.get('current_latitude')  # comentario

        if 'longitude' not in raw_data:  # comentario
            raw_data['longitude'] = data.get('lng') or data.get('lon') or data.get('current_longitude')  # comentario

        if 'eta_minutes' not in raw_data:  # comentario
            raw_data['eta_minutes'] = (  # comentario
                data.get('eta_minutes')  # comentario
                or data.get('eta')  # comentario
                or data.get('eta_min')  # comentario
            )  # comentario

        return super().to_internal_value(raw_data)  # comentario

    def validate_latitude(self, value):  # comentario
        if value < -90 or value > 90:  # comentario
            raise serializers.ValidationError('latitude debe estar entre -90 y 90.')  # comentario
        return value  # comentario

    def validate_longitude(self, value):  # comentario
        if value < -180 or value > 180:  # comentario
            raise serializers.ValidationError('longitude debe estar entre -180 y 180.')  # comentario
        return value  # comentario


class ShipmentAssignDriverSerializer(serializers.Serializer):  # comentario
    driver_id = serializers.IntegerField(required=False, allow_null=True)  # comentario
    auto_assign = serializers.BooleanField(required=False)  # comentario

    def to_internal_value(self, data):  # comentario
        raw_data = data.copy() if hasattr(data, 'copy') else dict(data)  # comentario

        if 'driver_id' not in raw_data:  # comentario
            raw_data['driver_id'] = (  # comentario
                data.get('driver_id')  # comentario
                or data.get('driver')  # comentario
                or data.get('repartidor_id')  # comentario
            )  # comentario

        if 'auto_assign' not in raw_data:  # comentario
            auto_value = (  # comentario
                data.get('auto_assign')  # comentario
                if data.get('auto_assign') is not None  # comentario
                else data.get('autoAssign')  # comentario
            )  # comentario
            if auto_value is not None:  # comentario
                raw_data['auto_assign'] = auto_value  # comentario

        # Si el cliente manda `auto_assign=true`, ignoramos cualquier driver_id (aunque venga en el body)
        # para evitar errores innecesarios en el frontend.
        auto_assign_raw = raw_data.get('auto_assign')  # comentario
        auto_assign_truthy = False  # comentario
        if isinstance(auto_assign_raw, bool):  # comentario
            auto_assign_truthy = auto_assign_raw  # comentario
        elif auto_assign_raw is not None:  # comentario
            auto_assign_truthy = str(auto_assign_raw).strip().lower() in {  # comentario
                '1', 'true', 't', 'yes', 'y', 'on', 'si', 'sí'  # comentario
            }  # comentario
        if auto_assign_truthy:  # comentario
            raw_data.pop('driver_id', None)  # comentario

        return super().to_internal_value(raw_data)  # comentario

    def validate_driver_id(self, value):  # comentario
        if value is None:  # comentario
            return None  # comentario

        exists = User.objects.filter(id=value, is_active=True).exists()  # comentario
        if not exists:  # comentario
            raise serializers.ValidationError('El repartidor no existe o esta inactivo.')  # comentario

        return value  # comentario

    def validate(self, attrs):  # comentario
        # El view resuelve la prioridad; no necesitamos ser estrictos aqui.
        return attrs  # comentario


class DeliveryAddressSerializer(serializers.ModelSerializer):  # comentario
    user = serializers.PrimaryKeyRelatedField(read_only=True)  # comentario

    class Meta:  # comentario
        model = DeliveryAddress  # comentario
        fields = [  # comentario
            'id',  # comentario
            'user',  # comentario
            'main_address',  # comentario
            'secondary_street',  # comentario
            'apartment',  # comentario
            'city',  # comentario
            'latitude',  # comentario
            'longitude',  # comentario
            'delivery_instructions',  # comentario
            'is_default',  # comentario
            'created_at',  # comentario
            'updated_at',  # comentario
        ]  # comentario
        read_only_fields = ['id', 'user', 'created_at', 'updated_at']  # comentario

    def to_internal_value(self, data):  # comentario
        raw_data = data.copy() if hasattr(data, 'copy') else dict(data)  # comentario

        if 'main_address' not in raw_data:  # comentario
            raw_data['main_address'] = (  # comentario
                data.get('direccion_principal')  # comentario
                or data.get('direccionPrincipal')  # comentario
                or data.get('address_line_1')  # comentario
                or data.get('street')  # comentario
                or ''  # comentario
            )  # comentario

        if 'secondary_street' not in raw_data:  # comentario
            raw_data['secondary_street'] = (  # comentario
                data.get('calle_secundaria')  # comentario
                or data.get('calleSecundaria')  # comentario
                or data.get('address_line_2')  # comentario
                or ''  # comentario
            )  # comentario

        if 'apartment' not in raw_data:  # comentario
            raw_data['apartment'] = (  # comentario
                data.get('piso_departamento')  # comentario
                or data.get('pisoDepartamento')  # comentario
                or data.get('departamento')  # comentario
                or ''  # comentario
            )  # comentario

        if 'city' not in raw_data:  # comentario
            raw_data['city'] = (  # comentario
                data.get('ciudad')  # comentario
                or data.get('province')  # comentario
                or data.get('provincia')  # comentario
                or ''  # comentario
            )  # comentario

        if 'latitude' not in raw_data:  # comentario
            raw_data['latitude'] = data.get('latitude') or data.get('lat')  # comentario

        if 'longitude' not in raw_data:  # comentario
            raw_data['longitude'] = (  # comentario
                data.get('longitude')  # comentario
                or data.get('lng')  # comentario
                or data.get('lon')  # comentario
            )  # comentario

        if 'delivery_instructions' not in raw_data:  # comentario
            raw_data['delivery_instructions'] = (  # comentario
                data.get('indicaciones')  # comentario
                or data.get('indicaciones_entrega')  # comentario
                or data.get('reference')  # comentario
                or data.get('notes')  # comentario
                or ''  # comentario
            )  # comentario

        if 'is_default' not in raw_data:  # comentario
            raw_data['is_default'] = (  # comentario
                data.get('default')  # comentario
                if data.get('default') is not None  # comentario
                else data.get('isDefault', False)  # comentario
            )  # comentario

        return super().to_internal_value(raw_data)  # comentario

    def validate_main_address(self, value):  # comentario
        value = (value or '').strip()  # comentario
        if not value:  # comentario
            raise serializers.ValidationError('La direccion principal es obligatoria.')  # comentario
        return value  # comentario

    def validate_latitude(self, value):  # comentario
        if value is None:  # comentario
            return None  # comentario
        if value < -90 or value > 90:  # comentario
            raise serializers.ValidationError('latitude debe estar entre -90 y 90.')  # comentario
        return value  # comentario

    def validate_longitude(self, value):  # comentario
        if value is None:  # comentario
            return None  # comentario
        if value < -180 or value > 180:  # comentario
            raise serializers.ValidationError('longitude debe estar entre -180 y 180.')  # comentario
        return value  # comentario

    def validate_city(self, value):  # comentario
        value = (value or '').strip()  # comentario
        if not value:  # comentario
            raise serializers.ValidationError('La ciudad es obligatoria.')  # comentario
        return value  # comentario


class MeSerializer(serializers.ModelSerializer):  # comentario
    full_name = serializers.CharField(required=False, allow_blank=True)  # comentario
    phone = serializers.CharField(required=False, allow_blank=True)  # comentario
    address = serializers.CharField(required=False, allow_blank=True)  # comentario
    avatar = serializers.ImageField(required=False, allow_null=True)  # comentario
    avatar_url = serializers.SerializerMethodField()  # comentario
    role = serializers.SerializerMethodField()  # comentario
    roles = serializers.SerializerMethodField()  # comentario
    pending_role_request = serializers.SerializerMethodField()  # comentario

    class Meta:  # comentario
        model = User  # comentario
        fields = [  # comentario
            'id',  # comentario
            'username',  # comentario
            'email',  # comentario
            'full_name',  # comentario
            'phone',  # comentario
            'address',  # comentario
            'avatar',  # comentario
            'avatar_url',  # comentario
            'role',  # comentario
            'roles',  # comentario
            'pending_role_request',  # comentario
        ]  # comentario
        read_only_fields = ['id', 'username', 'role', 'roles', 'pending_role_request']  # comentario

    def to_representation(self, instance):  # comentario
        data = super().to_representation(instance)  # comentario
        data['full_name'] = f'{instance.first_name} {instance.last_name}'.strip()  # comentario
        data['phone'] = getattr(getattr(instance, 'profile', None), 'phone', '')  # comentario
        data['address'] = getattr(getattr(instance, 'profile', None), 'address', '')  # comentario
        data['avatar_url'] = self.get_avatar_url(instance)  # comentario
        return data  # comentario

    def _resolve_primary_role(self, roles):  # comentario
        role_set = set(roles)  # comentario
        if 'ADMIN' in role_set:  # comentario
            return 'admin'  # comentario
        if 'DRIVER' in role_set or 'REPARTIDOR' in role_set:  # comentario
            return 'driver'  # comentario
        if 'PROVIDER' in role_set:  # comentario
            return 'provider'  # comentario
        if 'CLIENTE' in role_set:  # comentario
            return 'client'  # comentario
        return 'user'  # comentario

    def get_roles(self, instance):  # comentario
        return sorted(list(instance.groups.values_list('name', flat=True)))  # comentario

    def get_role(self, instance):  # comentario
        roles = self.get_roles(instance)  # comentario
        return self._resolve_primary_role(roles)  # comentario

    def get_pending_role_request(self, instance):  # comentario
        pending = instance.role_change_requests.filter(status='pending').order_by('-id').first()  # comentario
        if not pending:  # comentario
            return None  # comentario
        return {  # comentario
            'id': pending.id,  # comentario
            'requested_role': pending.requested_role,  # comentario
            'status': pending.status,  # comentario
            'reason': pending.reason,  # comentario
            'created_at': pending.created_at,  # comentario
        }  # comentario

    def get_avatar_url(self, instance):  # comentario
        avatar = getattr(getattr(instance, 'profile', None), 'avatar', None)  # comentario
        if not avatar:  # comentario
            return ''  # comentario
        request = self.context.get('request')  # comentario
        if request is None:  # comentario
            return avatar.url  # comentario
        return request.build_absolute_uri(avatar.url)  # comentario

    def to_internal_value(self, data):  # comentario
        raw_data = data.copy() if hasattr(data, 'copy') else dict(data)  # comentario

        if 'full_name' not in raw_data:  # comentario
            raw_data['full_name'] = (  # comentario
                data.get('full_name')  # comentario
                or data.get('name')  # comentario
                or data.get('nombre')  # comentario
                or data.get('fullName')  # comentario
                or ''  # comentario
            )  # comentario

        if 'phone' not in raw_data:  # comentario
            raw_data['phone'] = (  # comentario
                data.get('phone')  # comentario
                or data.get('telefono')  # comentario
                or data.get('celular')  # comentario
                or ''  # comentario
            )  # comentario

        if 'address' not in raw_data:  # comentario
            raw_data['address'] = (  # comentario
                data.get('address')  # comentario
                or data.get('direccion')  # comentario
                or ''  # comentario
            )  # comentario

        return super().to_internal_value(raw_data)  # comentario

    def validate_email(self, value):  # comentario
        email = (value or '').strip().lower()  # comentario
        user = self.instance  # comentario
        if User.objects.filter(email=email).exclude(id=user.id).exists():  # comentario
            raise serializers.ValidationError('Ya existe una cuenta con este correo.')  # comentario
        return email  # comentario

    def validate_phone(self, value):  # comentario
        value = (value or '').strip()  # comentario
        if not value:  # comentario
            return value  # comentario
        if not value.isdigit():  # comentario
            raise serializers.ValidationError('El telefono solo debe contener numeros.')  # comentario
        if len(value) != 10:  # comentario
            raise serializers.ValidationError('El telefono debe tener exactamente 10 digitos.')  # comentario
        if not value.startswith('09'):  # comentario
            raise serializers.ValidationError('El telefono debe iniciar con 09.')  # comentario
        return value  # comentario

    def update(self, instance, validated_data):  # comentario
        full_name = validated_data.pop('full_name', None)  # comentario
        phone = validated_data.pop('phone', None)  # comentario
        address = validated_data.pop('address', None)  # comentario
        avatar = validated_data.pop('avatar', serializers.empty)  # comentario

        if 'email' in validated_data:  # comentario
            instance.email = validated_data['email']  # comentario

        if full_name is not None:  # comentario
            full_name = full_name.strip()  # comentario
            name_parts = full_name.split(maxsplit=1) if full_name else []  # comentario
            instance.first_name = name_parts[0] if len(name_parts) > 0 else ''  # comentario
            instance.last_name = name_parts[1] if len(name_parts) > 1 else ''  # comentario

        instance.save()  # comentario

        if phone is not None or address is not None or avatar is not serializers.empty:  # comentario
            profile, _ = UserProfile.objects.get_or_create(user=instance)  # comentario
            if phone is not None:  # comentario
                profile.phone = phone.strip()  # comentario
            if address is not None:  # comentario
                profile.address = (address or '').strip()  # comentario
            if avatar is not serializers.empty:  # comentario
                profile.avatar = avatar  # comentario
            profile.save()  # comentario

        return instance  # comentario


class ChangePasswordSerializer(serializers.Serializer):  # comentario
    current_password = serializers.CharField(required=True, write_only=True)  # comentario
    new_password = serializers.CharField(required=True, write_only=True)  # comentario
    new_password2 = serializers.CharField(required=False, allow_blank=True, write_only=True)  # comentario

    def to_internal_value(self, data):  # comentario
        raw_data = data.copy() if hasattr(data, 'copy') else dict(data)  # comentario

        if 'current_password' not in raw_data:  # comentario
            raw_data['current_password'] = (  # comentario
                data.get('current_password')  # comentario
                or data.get('old_password')  # comentario
                or data.get('actual_password')  # comentario
                or ''  # comentario
            )  # comentario

        if 'new_password' not in raw_data:  # comentario
            raw_data['new_password'] = (  # comentario
                data.get('new_password')  # comentario
                or data.get('password')  # comentario
                or data.get('nueva_password')  # comentario
                or ''  # comentario
            )  # comentario

        if 'new_password2' not in raw_data:  # comentario
            raw_data['new_password2'] = (  # comentario
                data.get('new_password2')  # comentario
                or data.get('confirm_password')  # comentario
                or data.get('confirmPassword')  # comentario
                or ''  # comentario
            )  # comentario

        return super().to_internal_value(raw_data)  # comentario

    def validate(self, attrs):  # comentario
        new_password = attrs.get('new_password') or ''  # comentario
        new_password2 = attrs.get('new_password2') or ''  # comentario
        if len(new_password) < 8:  # comentario
            raise serializers.ValidationError({'new_password': 'La nueva contrasena debe tener minimo 8 caracteres.'})  # comentario
        if new_password2 and new_password != new_password2:  # comentario
            raise serializers.ValidationError({'new_password2': 'Las contrasenas no coinciden.'})  # comentario
        return attrs  # comentario


class RoleChangeRequestSerializer(serializers.ModelSerializer):  # comentario
    user = serializers.PrimaryKeyRelatedField(read_only=True)  # comentario

    class Meta:  # comentario
        model = RoleChangeRequest  # comentario
        fields = ['id', 'user', 'requested_role', 'reason', 'status', 'created_at', 'updated_at']  # comentario
        read_only_fields = ['id', 'user', 'status', 'created_at', 'updated_at']  # comentario

    def to_internal_value(self, data):  # comentario
        raw_data = data.copy() if hasattr(data, 'copy') else dict(data)  # comentario

        if 'requested_role' not in raw_data:  # comentario
            raw_data['requested_role'] = (  # comentario
                data.get('requested_role')  # comentario
                or data.get('role')  # comentario
                or data.get('nuevo_rol')  # comentario
                or ''  # comentario
            )  # comentario

        role = (raw_data.get('requested_role') or '').strip().lower()  # comentario
        role_map = {  # comentario
            'proveedor': 'provider',  # comentario
            'repartidor': 'driver',  # comentario
            'provider': 'provider',  # comentario
            'driver': 'driver',  # comentario
        }  # comentario
        if role:  # comentario
            raw_data['requested_role'] = role_map.get(role, role)  # comentario

        if 'reason' not in raw_data:  # comentario
            raw_data['reason'] = (  # comentario
                data.get('reason')  # comentario
                or data.get('motivo')  # comentario
                or data.get('description')  # comentario
                or ''  # comentario
            )  # comentario

        return super().to_internal_value(raw_data)  # comentario
