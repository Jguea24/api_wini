from rest_framework import serializers  # Importa serializers desde `rest_framework`.
from django.contrib.auth.models import Group, User  # Importa Group, User desde `django.contrib.auth.models`.
from .models import (  # Importa ( desde `.models`.
    Banner,  # Referencia `Banner` en la estructura/expresion.
    Category,  # Referencia `Category` en la estructura/expresion.
    Product,  # Referencia `Product` en la estructura/expresion.
    Cart,  # Referencia `Cart` en la estructura/expresion.
    UserProfile,  # Referencia `UserProfile` en la estructura/expresion.
    DeliveryAddress,  # Referencia `DeliveryAddress` en la estructura/expresion.
    RoleChangeRequest,  # Referencia `RoleChangeRequest` en la estructura/expresion.
    Order,  # Referencia `Order` en la estructura/expresion.
    OrderItem,  # Referencia `OrderItem` en la estructura/expresion.
    Shipment,  # Referencia `Shipment` en la estructura/expresion.
    ShipmentLocation,  # Referencia `ShipmentLocation` en la estructura/expresion.
)  # Cierra el bloque/estructura.


# =====================================================
# SERIALIZER DE REGISTRO DE USUARIO (SIN ROLES)
# =====================================================

class RegisterSerializer(serializers.ModelSerializer):  # Define la clase `RegisterSerializer`.
    full_name = serializers.CharField(write_only=True, required=False, allow_blank=True)  # Asigna a `full_name` un campo serializer `CharField`.
    phone = serializers.CharField(write_only=True, required=False, allow_blank=True)  # Asigna a `phone` un campo serializer `CharField`.
    address = serializers.CharField(write_only=True, required=False, allow_blank=True)  # Asigna a `address` un campo serializer `CharField`.
    username = serializers.CharField(required=False, allow_blank=True)  # Asigna a `username` un campo serializer `CharField`.
    role = serializers.CharField(write_only=True, required=False, allow_blank=True)  # Asigna a `role` un campo serializer `CharField`.
    role_reason = serializers.CharField(write_only=True, required=False, allow_blank=True)  # Asigna a `role_reason` un campo serializer `CharField`.
    password = serializers.CharField(write_only=True)  # Asigna a `password` un campo serializer `CharField`.
    password2 = serializers.CharField(write_only=True, required=False, allow_blank=True)  # Asigna a `password2` un campo serializer `CharField`.

    class Meta:  # Define la clase `Meta`.
        model = User  # Asigna un valor a `model`.
        fields = [  # Asigna un valor a `fields`.
            'full_name',  # Agrega un literal a la estructura.
            'email',  # Agrega un literal a la estructura.
            'phone',  # Agrega un literal a la estructura.
            'address',  # Agrega un literal a la estructura.
            'username',  # Agrega un literal a la estructura.
            'role',  # Agrega un literal a la estructura.
            'role_reason',  # Agrega un literal a la estructura.
            'password',  # Agrega un literal a la estructura.
            'password2',  # Agrega un literal a la estructura.
        ]  # Cierra el bloque/estructura.
        extra_kwargs = {  # Asigna un valor a `extra_kwargs`.
            'email': {'required': True},  # Asigna la clave `email` con un diccionario.
            'username': {'required': False},  # Asigna la clave `username` con un diccionario.
        }  # Cierra el bloque/estructura.

    def to_internal_value(self, data):  # Define la funcion `to_internal_value`.
        raw_data = data.copy()  # Asigna a `raw_data` el resultado de `data.copy`.

        if 'full_name' not in raw_data:  # Evalua la condicion del `if`.
            raw_data['full_name'] = (  # Asigna un valor a `raw_data['full_name']`.
                data.get('full_name')  # Ejecuta `data.get`.
                or data.get('name')  # Continua la expresion con `or`.
                or data.get('nombre')  # Continua la expresion con `or`.
                or data.get('fullName')  # Continua la expresion con `or`.
                or ''  # Continua la expresion con `or`.
            )  # Cierra el bloque/estructura.

        if 'phone' not in raw_data:  # Evalua la condicion del `if`.
            raw_data['phone'] = (  # Asigna un valor a `raw_data['phone']`.
                data.get('phone')  # Ejecuta `data.get`.
                or data.get('Phone')  # Continua la expresion con `or`.
                or data.get('telefono')  # Continua la expresion con `or`.
                or data.get('celular')  # Continua la expresion con `or`.
                or ''  # Continua la expresion con `or`.
            )  # Cierra el bloque/estructura.

        if 'address' not in raw_data:  # Evalua la condicion del `if`.
            raw_data['address'] = (  # Asigna un valor a `raw_data['address']`.
                data.get('address')  # Ejecuta `data.get`.
                or data.get('Address')  # Continua la expresion con `or`.
                or data.get('direccion')  # Continua la expresion con `or`.
                or data.get('dirección')  # Continua la expresion con `or`.
                or data.get('main_address')  # Continua la expresion con `or`.
                or data.get('direccion_principal')  # Continua la expresion con `or`.
                or data.get('address_line_1')  # Continua la expresion con `or`.
                or data.get('street')  # Continua la expresion con `or`.
                or ''  # Continua la expresion con `or`.
            )  # Cierra el bloque/estructura.

        if 'username' not in raw_data:  # Evalua la condicion del `if`.
            raw_data['username'] = (  # Asigna un valor a `raw_data['username']`.
                data.get('username')  # Ejecuta `data.get`.
                or data.get('usuario')  # Continua la expresion con `or`.
                or data.get('user')  # Continua la expresion con `or`.
                or ''  # Continua la expresion con `or`.
            )  # Cierra el bloque/estructura.

        if 'password' not in raw_data:  # Evalua la condicion del `if`.
            raw_data['password'] = data.get('password') or data.get('contrasena') or ''  # Asigna a `raw_data['password']` el resultado de `data.get`.

        if 'password2' not in raw_data:  # Evalua la condicion del `if`.
            raw_data['password2'] = (  # Asigna un valor a `raw_data['password2']`.
                data.get('password2')  # Ejecuta `data.get`.
                or data.get('confirm_password')  # Continua la expresion con `or`.
                or data.get('confirmPassword')  # Continua la expresion con `or`.
                or data.get('password_confirmation')  # Continua la expresion con `or`.
                or ''  # Continua la expresion con `or`.
            )  # Cierra el bloque/estructura.

        if 'role' not in raw_data:  # Evalua la condicion del `if`.
            raw_data['role'] = (  # Asigna un valor a `raw_data['role']`.
                data.get('role')  # Ejecuta `data.get`.
                or data.get('requested_role')  # Continua la expresion con `or`.
                or data.get('user_role')  # Continua la expresion con `or`.
                or ''  # Continua la expresion con `or`.
            )  # Cierra el bloque/estructura.

        if 'role_reason' not in raw_data:  # Evalua la condicion del `if`.
            raw_data['role_reason'] = (  # Asigna un valor a `raw_data['role_reason']`.
                data.get('role_reason')  # Ejecuta `data.get`.
                or data.get('reason')  # Continua la expresion con `or`.
                or data.get('motivo')  # Continua la expresion con `or`.
                or ''  # Continua la expresion con `or`.
            )  # Cierra el bloque/estructura.

        return super().to_internal_value(raw_data)  # Devuelve un valor (`return`).

    def validate(self, attrs):  # Define la funcion `validate`.
        password = attrs.get('password')  # Asigna a `password` el resultado de `attrs.get`.
        password2 = attrs.get('password2')  # Asigna a `password2` el resultado de `attrs.get`.
        email = (attrs.get('email') or '').strip().lower()  # Asigna un valor a `email`.
        username = (attrs.get('username') or '').strip()  # Asigna un valor a `username`.
        phone = (attrs.get('phone') or '').strip()  # Asigna un valor a `phone`.
        address = (attrs.get('address') or '').strip()  # Asigna un valor a `address`.
        role = (attrs.get('role') or '').strip().lower()  # Asigna un valor a `role`.

        if not password:  # Evalua la condicion del `if`.
            raise serializers.ValidationError({'password': 'Este campo es obligatorio.'})  # Lanza una excepcion (`raise`).

        if password2 and password != password2:  # Evalua la condicion del `if`.
            raise serializers.ValidationError({'password2': 'Las contrasenas no coinciden.'})  # Lanza una excepcion (`raise`).

        if not phone:  # Evalua la condicion del `if`.
            raise serializers.ValidationError({'phone': 'El telefono es obligatorio.'})  # Lanza una excepcion (`raise`).

        if not phone.isdigit():  # Evalua la condicion del `if`.
            raise serializers.ValidationError({'phone': 'El telefono solo debe contener numeros.'})  # Lanza una excepcion (`raise`).

        if len(phone) != 10:  # Evalua la condicion del `if`.
            raise serializers.ValidationError({'phone': 'El telefono debe tener exactamente 10 digitos.'})  # Lanza una excepcion (`raise`).

        if not phone.startswith('09'):  # Evalua la condicion del `if`.
            raise serializers.ValidationError({'phone': 'El telefono debe iniciar con 09.'})  # Lanza una excepcion (`raise`).

        if not address:  # Evalua la condicion del `if`.
            raise serializers.ValidationError({'address': 'La direccion es obligatoria.'})  # Lanza una excepcion (`raise`).

        if User.objects.filter(email=email).exists():  # Evalua la condicion del `if`.
            raise serializers.ValidationError({'email': 'Ya existe una cuenta con este correo.'})  # Lanza una excepcion (`raise`).

        if not username:  # Evalua la condicion del `if`.
            base_username = (email.split('@')[0] if email else 'usuario').replace(' ', '')  # Asigna un valor a `base_username`.
            username = base_username or 'usuario'  # Asigna un valor a `username`.
            suffix = 1  # Asigna un valor a `suffix`.
            candidate = username  # Asigna un valor a `candidate`.
            while User.objects.filter(username=candidate).exists():  # Itera en un bucle `while`.
                suffix += 1  # Incrementa `suffix` en 1.
                candidate = f'{username}{suffix}'  # Asigna un valor a `candidate`.
            attrs['username'] = candidate  # Asigna un valor a `attrs['username']`.
        elif User.objects.filter(username=username).exists():  # Evalua la condicion del `elif`.
            raise serializers.ValidationError({'username': 'Este usuario ya existe.'})  # Lanza una excepcion (`raise`).

        role_map = {  # Asigna un valor a `role_map`.
            'cliente': 'client',  # Agrega un literal a la estructura.
            'client': 'client',  # Agrega un literal a la estructura.
            'customer': 'client',  # Agrega un literal a la estructura.
            'usuario': 'client',  # Agrega un literal a la estructura.
            'user': 'client',  # Agrega un literal a la estructura.
            'repartidor': 'driver',  # Agrega un literal a la estructura.
            'driver': 'driver',  # Agrega un literal a la estructura.
            'proveedor': 'provider',  # Agrega un literal a la estructura.
            'provider': 'provider',  # Agrega un literal a la estructura.
        }  # Cierra el bloque/estructura.
        normalized_role = role_map.get(role, role)  # Asigna a `normalized_role` el resultado de `role_map.get`.
        if normalized_role and normalized_role not in {'client', 'driver', 'provider'}:  # Evalua la condicion del `if`.
            raise serializers.ValidationError({'role': 'Rol invalido. Usa client, driver o provider.'})  # Lanza una excepcion (`raise`).

        attrs['email'] = email  # Asigna un valor a `attrs['email']`.
        attrs['phone'] = phone  # Asigna un valor a `attrs['phone']`.
        attrs['address'] = address  # Asigna un valor a `attrs['address']`.
        attrs['role'] = normalized_role  # Asigna un valor a `attrs['role']`.
        return attrs  # Devuelve un valor (`return`).

    def create(self, validated_data):  # Define la funcion `create`.
        full_name = (validated_data.pop('full_name', '') or '').strip()  # Asigna un valor a `full_name`.
        phone = (validated_data.pop('phone', '') or '').strip()  # Asigna un valor a `phone`.
        address = (validated_data.pop('address', '') or '').strip()  # Asigna un valor a `address`.
        requested_role = validated_data.pop('role', '')  # Asigna a `requested_role` el resultado de `validated_data.pop`.
        role_reason = (validated_data.pop('role_reason', '') or '').strip()  # Asigna un valor a `role_reason`.
        validated_data.pop('password2', None)  # Ejecuta `validated_data.pop`.

        password = validated_data.pop('password')  # Asigna a `password` el resultado de `validated_data.pop`.
        user = User.objects.create_user(  # Asigna a `user` el resultado de `User.objects.create_user`.
            password=password,  # Asigna un valor a `password`.
            **validated_data  # Desempaqueta y mezcla el diccionario `validated_data`.
        )  # Cierra el bloque/estructura.

        if full_name:  # Evalua la condicion del `if`.
            name_parts = full_name.split(maxsplit=1)  # Asigna a `name_parts` el resultado de `full_name.split`.
            user.first_name = name_parts[0]  # Asigna un valor a `user.first_name`.
            user.last_name = name_parts[1] if len(name_parts) > 1 else ''  # Asigna un valor a `user.last_name`.
            user.save(update_fields=['first_name', 'last_name'])  # Ejecuta `user.save`.

        UserProfile.objects.update_or_create(  # Ejecuta `UserProfile.objects.update_or_create`.
            user=user,  # Asigna un valor a `user`.
            defaults={  # Asigna un valor a `defaults`.
                'phone': phone,  # Asigna la clave `phone` en un diccionario.
                'address': address,  # Asigna la clave `address` en un diccionario.
            }  # Cierra el bloque/estructura.
        )  # Cierra el bloque/estructura.

        # Rol base para todas las cuentas.
        cliente_group, _ = Group.objects.get_or_create(name='CLIENTE')  # Asigna a `cliente_group` y `_` el resultado de `Group.objects.get_or_create`.
        user.groups.add(cliente_group)  # Ejecuta `user.groups.add`.

        # Para roles operativos, crea solicitud pendiente en registro.
        if requested_role in {'driver', 'provider'}:  # Evalua la condicion del `if`.
            RoleChangeRequest.objects.create(  # Ejecuta `RoleChangeRequest.objects.create`.
                user=user,  # Asigna un valor a `user`.
                requested_role=requested_role,  # Asigna un valor a `requested_role`.
                reason=role_reason or 'Solicitud creada durante el registro.',  # Asigna un valor a `reason`.
                status='pending',  # Asigna un valor a `status`.
            )  # Cierra el bloque/estructura.

        return user  # Devuelve un valor (`return`).


class RegisteredUserSerializer(serializers.ModelSerializer):  # Define la clase `RegisteredUserSerializer`.
    full_name = serializers.SerializerMethodField()  # Asigna a `full_name` un campo serializer `SerializerMethodField`.
    phone = serializers.SerializerMethodField()  # Asigna a `phone` un campo serializer `SerializerMethodField`.
    address = serializers.SerializerMethodField()  # Asigna a `address` un campo serializer `SerializerMethodField`.
    avatar_url = serializers.SerializerMethodField()  # Asigna a `avatar_url` un campo serializer `SerializerMethodField`.
    roles = serializers.SerializerMethodField()  # Asigna a `roles` un campo serializer `SerializerMethodField`.

    class Meta:  # Define la clase `Meta`.
        model = User  # Asigna un valor a `model`.
        fields = [  # Asigna un valor a `fields`.
            'id',  # Agrega un literal a la estructura.
            'username',  # Agrega un literal a la estructura.
            'email',  # Agrega un literal a la estructura.
            'full_name',  # Agrega un literal a la estructura.
            'phone',  # Agrega un literal a la estructura.
            'address',  # Agrega un literal a la estructura.
            'avatar_url',  # Agrega un literal a la estructura.
            'roles',  # Agrega un literal a la estructura.
            'date_joined',  # Agrega un literal a la estructura.
            'is_active',  # Agrega un literal a la estructura.
        ]  # Cierra el bloque/estructura.
        read_only_fields = fields  # Asigna un valor a `read_only_fields`.

    def get_full_name(self, instance):  # Define la funcion `get_full_name`.
        return f'{instance.first_name} {instance.last_name}'.strip()  # Devuelve un valor (`return`).

    def get_phone(self, instance):  # Define la funcion `get_phone`.
        return getattr(getattr(instance, 'profile', None), 'phone', '')  # Devuelve un valor (`return`).

    def get_address(self, instance):  # Define la funcion `get_address`.
        return getattr(getattr(instance, 'profile', None), 'address', '')  # Devuelve un valor (`return`).

    def get_avatar_url(self, instance):  # Define la funcion `get_avatar_url`.
        avatar = getattr(getattr(instance, 'profile', None), 'avatar', None)  # Asigna a `avatar` el resultado de `getattr`.
        if not avatar:  # Evalua la condicion del `if`.
            return ''  # Devuelve un valor (`return`).
        request = self.context.get('request')  # Asigna a `request` el resultado de `self.context.get`.
        if request is None:  # Evalua la condicion del `if`.
            return avatar.url  # Devuelve un valor (`return`).
        return request.build_absolute_uri(avatar.url)  # Devuelve un valor (`return`).

    def get_roles(self, instance):  # Define la funcion `get_roles`.
        return sorted(list(instance.groups.values_list('name', flat=True)))  # Devuelve un valor (`return`).


# =====================================================
# SERIALIZER DE CATEGORIAS
# =====================================================

class CategorySerializer(serializers.ModelSerializer):  # Define la clase `CategorySerializer`.
    image_url = serializers.SerializerMethodField()  # Asigna a `image_url` un campo serializer `SerializerMethodField`.

    class Meta:  # Define la clase `Meta`.
        model = Category  # Asigna un valor a `model`.
        fields = ['id', 'name', 'order', 'image', 'image_url']  # Asigna un valor a `fields`.

    def get_image_url(self, obj):  # Define la funcion `get_image_url`.
        if not obj.image:  # Evalua la condicion del `if`.
            return ''  # Devuelve un valor (`return`).
        request = self.context.get('request')  # Asigna a `request` el resultado de `self.context.get`.
        if request is None:  # Evalua la condicion del `if`.
            return obj.image.url  # Devuelve un valor (`return`).
        return request.build_absolute_uri(obj.image.url)  # Devuelve un valor (`return`).


# =====================================================
# SERIALIZER DE BANNERS
# =====================================================

class BannerSerializer(serializers.ModelSerializer):  # Define la clase `BannerSerializer`.
    image_url = serializers.SerializerMethodField()  # Asigna a `image_url` un campo serializer `SerializerMethodField`.

    class Meta:  # Define la clase `Meta`.
        model = Banner  # Asigna un valor a `model`.
        fields = ['id', 'title', 'image', 'image_url', 'order']  # Asigna un valor a `fields`.

    def get_image_url(self, obj):  # Define la funcion `get_image_url`.
        if not obj.image:  # Evalua la condicion del `if`.
            return ''  # Devuelve un valor (`return`).
        request = self.context.get('request')  # Asigna a `request` el resultado de `self.context.get`.
        if request is None:  # Evalua la condicion del `if`.
            return obj.image.url  # Devuelve un valor (`return`).
        return request.build_absolute_uri(obj.image.url)  # Devuelve un valor (`return`).


# =====================================================
# SERIALIZER DE PRODUCTOS
# =====================================================

class ProductSerializer(serializers.ModelSerializer):  # Define la clase `ProductSerializer`.
    image_url = serializers.SerializerMethodField()  # Asigna a `image_url` un campo serializer `SerializerMethodField`.
    category_name = serializers.CharField(source='category.name', read_only=True)  # Asigna a `category_name` un campo serializer `CharField`.

    class Meta:  # Define la clase `Meta`.
        model = Product  # Asigna un valor a `model`.
        fields = [  # Asigna un valor a `fields`.
            'id',  # Agrega un literal a la estructura.
            'name',  # Agrega un literal a la estructura.
            'price',  # Agrega un literal a la estructura.
            'old_price',  # Agrega un literal a la estructura.
            'description',  # Agrega un literal a la estructura.
            'store_name',  # Agrega un literal a la estructura.
            'rating',  # Agrega un literal a la estructura.
            'reviews_count',  # Agrega un literal a la estructura.
            'stock',  # Agrega un literal a la estructura.
            'image',  # Agrega un literal a la estructura.
            'image_url',  # Agrega un literal a la estructura.
            'category',  # Agrega un literal a la estructura.
            'category_name',  # Agrega un literal a la estructura.
        ]  # Cierra el bloque/estructura.

    def get_image_url(self, obj):  # Define la funcion `get_image_url`.
        if not obj.image:  # Evalua la condicion del `if`.
            return ''  # Devuelve un valor (`return`).
        request = self.context.get('request')  # Asigna a `request` el resultado de `self.context.get`.
        if request is None:  # Evalua la condicion del `if`.
            return obj.image.url  # Devuelve un valor (`return`).
        return request.build_absolute_uri(obj.image.url)  # Devuelve un valor (`return`).


# =====================================================
# SERIALIZER DE CARRITO
# =====================================================

class CartSerializer(serializers.ModelSerializer):  # Define la clase `CartSerializer`.
    user = serializers.PrimaryKeyRelatedField(read_only=True)  # Asigna a `user` un campo serializer `PrimaryKeyRelatedField`.
    product_name = serializers.CharField(source='product.name', read_only=True)  # Asigna a `product_name` un campo serializer `CharField`.
    product_price = serializers.DecimalField(  # Asigna a `product_price` un campo serializer `DecimalField`.
        source='product.price',  # Asigna un valor a `source`.
        max_digits=8,  # Asigna un valor a `max_digits`.
        decimal_places=2,  # Asigna un valor a `decimal_places`.
        read_only=True,  # Asigna un valor a `read_only`.
    )  # Cierra el bloque/estructura.
    product_image_url = serializers.SerializerMethodField()  # Asigna a `product_image_url` un campo serializer `SerializerMethodField`.

    class Meta:  # Define la clase `Meta`.
        model = Cart  # Asigna un valor a `model`.
        fields = [  # Asigna un valor a `fields`.
            'id',  # Agrega un literal a la estructura.
            'user',  # Agrega un literal a la estructura.
            'product',  # Agrega un literal a la estructura.
            'quantity',  # Agrega un literal a la estructura.
            'product_name',  # Agrega un literal a la estructura.
            'product_price',  # Agrega un literal a la estructura.
            'product_image_url',  # Agrega un literal a la estructura.
        ]  # Cierra el bloque/estructura.
        read_only_fields = ['id', 'user', 'product_name', 'product_price', 'product_image_url']  # Asigna un valor a `read_only_fields`.

    def to_internal_value(self, data):  # Define la funcion `to_internal_value`.
        raw_data = data.copy() if hasattr(data, 'copy') else dict(data)  # Asigna a `raw_data` el resultado de `data.copy`.

        if 'product' not in raw_data:  # Evalua la condicion del `if`.
            raw_data['product'] = (  # Asigna un valor a `raw_data['product']`.
                data.get('product_id')  # Ejecuta `data.get`.
                or data.get('productId')  # Continua la expresion con `or`.
                or data.get('producto')  # Continua la expresion con `or`.
                or data.get('id_producto')  # Continua la expresion con `or`.
            )  # Cierra el bloque/estructura.

        if 'quantity' not in raw_data:  # Evalua la condicion del `if`.
            raw_data['quantity'] = (  # Asigna un valor a `raw_data['quantity']`.
                data.get('quantity')  # Ejecuta `data.get`.
                or data.get('cantidad')  # Continua la expresion con `or`.
                or data.get('qty')  # Continua la expresion con `or`.
                or 1  # Continua la expresion con `or`.
            )  # Cierra el bloque/estructura.

        return super().to_internal_value(raw_data)  # Devuelve un valor (`return`).

    def validate_quantity(self, value):  # Define la funcion `validate_quantity`.
        if value < 1:  # Evalua la condicion del `if`.
            raise serializers.ValidationError('La cantidad debe ser mayor a 0.')  # Lanza una excepcion (`raise`).
        return value  # Devuelve un valor (`return`).

    def get_product_image_url(self, obj):  # Define la funcion `get_product_image_url`.
        if not obj.product or not obj.product.image:  # Evalua la condicion del `if`.
            return ''  # Devuelve un valor (`return`).
        request = self.context.get('request')  # Asigna a `request` el resultado de `self.context.get`.
        if request is None:  # Evalua la condicion del `if`.
            return obj.product.image.url  # Devuelve un valor (`return`).
        return request.build_absolute_uri(obj.product.image.url)  # Devuelve un valor (`return`).


class OrderItemSerializer(serializers.ModelSerializer):  # Define la clase `OrderItemSerializer`.
    product = serializers.PrimaryKeyRelatedField(read_only=True)  # Asigna a `product` un campo serializer `PrimaryKeyRelatedField`.
    product_image_url = serializers.SerializerMethodField()  # Asigna a `product_image_url` un campo serializer `SerializerMethodField`.

    class Meta:  # Define la clase `Meta`.
        model = OrderItem  # Asigna un valor a `model`.
        fields = [  # Asigna un valor a `fields`.
            'id',  # Agrega un literal a la estructura.
            'product',  # Agrega un literal a la estructura.
            'product_name',  # Agrega un literal a la estructura.
            'product_price',  # Agrega un literal a la estructura.
            'quantity',  # Agrega un literal a la estructura.
            'subtotal',  # Agrega un literal a la estructura.
            'product_image_url',  # Agrega un literal a la estructura.
        ]  # Cierra el bloque/estructura.
        read_only_fields = fields  # Asigna un valor a `read_only_fields`.

    def get_product_image_url(self, obj):  # Define la funcion `get_product_image_url`.
        if not obj.product or not obj.product.image:  # Evalua la condicion del `if`.
            return ''  # Devuelve un valor (`return`).
        request = self.context.get('request')  # Asigna a `request` el resultado de `self.context.get`.
        if request is None:  # Evalua la condicion del `if`.
            return obj.product.image.url  # Devuelve un valor (`return`).
        return request.build_absolute_uri(obj.product.image.url)  # Devuelve un valor (`return`).


class OrderSerializer(serializers.ModelSerializer):  # Define la clase `OrderSerializer`.
    user = serializers.PrimaryKeyRelatedField(read_only=True)  # Asigna a `user` un campo serializer `PrimaryKeyRelatedField`.
    items = OrderItemSerializer(many=True, read_only=True)  # Asigna a `items` el resultado de `OrderItemSerializer`.
    status_label = serializers.CharField(source='get_status_display', read_only=True)  # Asigna a `status_label` un campo serializer `CharField`.

    class Meta:  # Define la clase `Meta`.
        model = Order  # Asigna un valor a `model`.
        fields = [  # Asigna un valor a `fields`.
            'id',  # Agrega un literal a la estructura.
            'user',  # Agrega un literal a la estructura.
            'delivery_address',  # Agrega un literal a la estructura.
            'delivery_main_address',  # Agrega un literal a la estructura.
            'delivery_secondary_street',  # Agrega un literal a la estructura.
            'delivery_apartment',  # Agrega un literal a la estructura.
            'delivery_city',  # Agrega un literal a la estructura.
            'delivery_latitude',  # Agrega un literal a la estructura.
            'delivery_longitude',  # Agrega un literal a la estructura.
            'delivery_instructions',  # Agrega un literal a la estructura.
            'status',  # Agrega un literal a la estructura.
            'status_label',  # Agrega un literal a la estructura.
            'total_amount',  # Agrega un literal a la estructura.
            'total_items',  # Agrega un literal a la estructura.
            'created_at',  # Agrega un literal a la estructura.
            'updated_at',  # Agrega un literal a la estructura.
            'items',  # Agrega un literal a la estructura.
        ]  # Cierra el bloque/estructura.
        read_only_fields = fields  # Asigna un valor a `read_only_fields`.


class OrderCreateSerializer(serializers.Serializer):  # Define la clase `OrderCreateSerializer`.
    delivery_address = serializers.PrimaryKeyRelatedField(  # Asigna a `delivery_address` un campo serializer `PrimaryKeyRelatedField`.
        queryset=DeliveryAddress.objects.all(),  # Asigna a `queryset` el resultado de `DeliveryAddress.objects.all`.
        required=False,  # Asigna un valor a `required`.
        allow_null=True,  # Asigna un valor a `allow_null`.
    )  # Cierra el bloque/estructura.

    def to_internal_value(self, data):  # Define la funcion `to_internal_value`.
        raw_data = data.copy() if hasattr(data, 'copy') else dict(data)  # Asigna a `raw_data` el resultado de `data.copy`.
        if 'delivery_address' not in raw_data:  # Evalua la condicion del `if`.
            raw_data['delivery_address'] = (  # Asigna un valor a `raw_data['delivery_address']`.
                data.get('delivery_address')  # Ejecuta `data.get`.
                or data.get('address_id')  # Continua la expresion con `or`.
                or data.get('address')  # Continua la expresion con `or`.
                or data.get('direccion_id')  # Continua la expresion con `or`.
            )  # Cierra el bloque/estructura.
        return super().to_internal_value(raw_data)  # Devuelve un valor (`return`).


class ShipmentLocationSerializer(serializers.ModelSerializer):  # Define la clase `ShipmentLocationSerializer`.
    class Meta:  # Define la clase `Meta`.
        model = ShipmentLocation  # Asigna un valor a `model`.
        fields = ['id', 'latitude', 'longitude', 'heading', 'speed', 'recorded_at']  # Asigna un valor a `fields`.
        read_only_fields = fields  # Asigna un valor a `read_only_fields`.


class ShipmentSerializer(serializers.ModelSerializer):  # Define la clase `ShipmentSerializer`.
    order = serializers.PrimaryKeyRelatedField(read_only=True)  # Asigna a `order` un campo serializer `PrimaryKeyRelatedField`.
    driver = serializers.PrimaryKeyRelatedField(read_only=True)  # Asigna a `driver` un campo serializer `PrimaryKeyRelatedField`.
    driver_name = serializers.SerializerMethodField()  # Asigna a `driver_name` un campo serializer `SerializerMethodField`.
    status_label = serializers.CharField(source='get_status_display', read_only=True)  # Asigna a `status_label` un campo serializer `CharField`.
    locations = serializers.SerializerMethodField()  # Asigna a `locations` un campo serializer `SerializerMethodField`.
    has_live_location = serializers.SerializerMethodField()  # Asigna a `has_live_location` un campo serializer `SerializerMethodField`.

    class Meta:  # Define la clase `Meta`.
        model = Shipment  # Asigna un valor a `model`.
        fields = [  # Asigna un valor a `fields`.
            'id',  # Agrega un literal a la estructura.
            'order',  # Agrega un literal a la estructura.
            'driver',  # Agrega un literal a la estructura.
            'driver_name',  # Agrega un literal a la estructura.
            'status',  # Agrega un literal a la estructura.
            'status_label',  # Agrega un literal a la estructura.
            'current_latitude',  # Agrega un literal a la estructura.
            'current_longitude',  # Agrega un literal a la estructura.
            'current_heading',  # Agrega un literal a la estructura.
            'current_speed',  # Agrega un literal a la estructura.
            'last_location_at',  # Agrega un literal a la estructura.
            'eta_minutes',  # Agrega un literal a la estructura.
            'notes',  # Agrega un literal a la estructura.
            'created_at',  # Agrega un literal a la estructura.
            'updated_at',  # Agrega un literal a la estructura.
            'has_live_location',  # Agrega un literal a la estructura.
            'locations',  # Agrega un literal a la estructura.
        ]  # Cierra el bloque/estructura.
        read_only_fields = fields  # Asigna un valor a `read_only_fields`.

    def get_driver_name(self, obj):  # Define la funcion `get_driver_name`.
        if not obj.driver:  # Evalua la condicion del `if`.
            return ''  # Devuelve un valor (`return`).
        full_name = f'{obj.driver.first_name} {obj.driver.last_name}'.strip()  # Asigna un valor a `full_name`.
        return full_name or obj.driver.username  # Devuelve un valor (`return`).

    def get_has_live_location(self, obj):  # Define la funcion `get_has_live_location`.
        return obj.current_latitude is not None and obj.current_longitude is not None  # Devuelve un valor (`return`).

    def get_locations(self, obj):  # Define la funcion `get_locations`.
        request = self.context.get('request')  # Asigna a `request` el resultado de `self.context.get`.
        try:  # Inicia un bloque `try`.
            raw_limit = request.query_params.get('points', 60) if request else 60  # Asigna a `raw_limit` el resultado de `request.query_params.get`.
            limit = int(raw_limit)  # Asigna a `limit` el resultado de `int`.
        except (TypeError, ValueError):  # Maneja una excepcion en `except`.
            limit = 60  # Asigna un valor a `limit`.
        limit = max(1, min(limit, 300))  # Asigna a `limit` el resultado de `max`.
        qs = obj.locations.all().order_by('-recorded_at', '-id')[:limit]  # Asigna a `qs` el resultado de `obj.locations.all`.
        return ShipmentLocationSerializer(qs, many=True).data  # Devuelve un valor (`return`).


class ShipmentLocationUpdateSerializer(serializers.Serializer):  # Define la clase `ShipmentLocationUpdateSerializer`.
    latitude = serializers.DecimalField(max_digits=9, decimal_places=6)  # Asigna a `latitude` un campo serializer `DecimalField`.
    longitude = serializers.DecimalField(max_digits=9, decimal_places=6)  # Asigna a `longitude` un campo serializer `DecimalField`.
    heading = serializers.DecimalField(max_digits=6, decimal_places=2, required=False, allow_null=True)  # Asigna a `heading` un campo serializer `DecimalField`.
    speed = serializers.DecimalField(max_digits=6, decimal_places=2, required=False, allow_null=True)  # Asigna a `speed` un campo serializer `DecimalField`.
    status = serializers.ChoiceField(choices=Shipment.STATUS_CHOICES, required=False)  # Asigna a `status` un campo serializer `ChoiceField`.
    eta_minutes = serializers.IntegerField(required=False, allow_null=True, min_value=0)  # Asigna a `eta_minutes` un campo serializer `IntegerField`.
    notes = serializers.CharField(required=False, allow_blank=True, max_length=255)  # Asigna a `notes` un campo serializer `CharField`.

    def to_internal_value(self, data):  # Define la funcion `to_internal_value`.
        raw_data = data.copy() if hasattr(data, 'copy') else dict(data)  # Asigna a `raw_data` el resultado de `data.copy`.

        if 'latitude' not in raw_data:  # Evalua la condicion del `if`.
            raw_data['latitude'] = data.get('lat') or data.get('current_latitude')  # Asigna a `raw_data['latitude']` el resultado de `data.get`.

        if 'longitude' not in raw_data:  # Evalua la condicion del `if`.
            raw_data['longitude'] = data.get('lng') or data.get('lon') or data.get('current_longitude')  # Asigna a `raw_data['longitude']` el resultado de `data.get`.

        if 'eta_minutes' not in raw_data:  # Evalua la condicion del `if`.
            raw_data['eta_minutes'] = (  # Asigna un valor a `raw_data['eta_minutes']`.
                data.get('eta_minutes')  # Ejecuta `data.get`.
                or data.get('eta')  # Continua la expresion con `or`.
                or data.get('eta_min')  # Continua la expresion con `or`.
            )  # Cierra el bloque/estructura.

        return super().to_internal_value(raw_data)  # Devuelve un valor (`return`).

    def validate_latitude(self, value):  # Define la funcion `validate_latitude`.
        if value < -90 or value > 90:  # Evalua la condicion del `if`.
            raise serializers.ValidationError('latitude debe estar entre -90 y 90.')  # Lanza una excepcion (`raise`).
        return value  # Devuelve un valor (`return`).

    def validate_longitude(self, value):  # Define la funcion `validate_longitude`.
        if value < -180 or value > 180:  # Evalua la condicion del `if`.
            raise serializers.ValidationError('longitude debe estar entre -180 y 180.')  # Lanza una excepcion (`raise`).
        return value  # Devuelve un valor (`return`).


class ShipmentAssignDriverSerializer(serializers.Serializer):  # Define la clase `ShipmentAssignDriverSerializer`.
    driver_id = serializers.IntegerField(required=False, allow_null=True)  # Asigna a `driver_id` un campo serializer `IntegerField`.
    auto_assign = serializers.BooleanField(required=False)  # Asigna a `auto_assign` un campo serializer `BooleanField`.

    def to_internal_value(self, data):  # Define la funcion `to_internal_value`.
        raw_data = data.copy() if hasattr(data, 'copy') else dict(data)  # Asigna a `raw_data` el resultado de `data.copy`.

        if 'driver_id' not in raw_data:  # Evalua la condicion del `if`.
            raw_data['driver_id'] = (  # Asigna un valor a `raw_data['driver_id']`.
                data.get('driver_id')  # Ejecuta `data.get`.
                or data.get('driver')  # Continua la expresion con `or`.
                or data.get('repartidor_id')  # Continua la expresion con `or`.
            )  # Cierra el bloque/estructura.

        if 'auto_assign' not in raw_data:  # Evalua la condicion del `if`.
            auto_value = (  # Asigna un valor a `auto_value`.
                data.get('auto_assign')  # Ejecuta `data.get`.
                if data.get('auto_assign') is not None  # Evalua la condicion del `if`.
                else data.get('autoAssign')  # Rama `else` del operador ternario.
            )  # Cierra el bloque/estructura.
            if auto_value is not None:  # Evalua la condicion del `if`.
                raw_data['auto_assign'] = auto_value  # Asigna un valor a `raw_data['auto_assign']`.

        # Si el cliente manda `auto_assign=true`, ignoramos cualquier driver_id (aunque venga en el body)
        # para evitar errores innecesarios en el frontend.
        auto_assign_raw = raw_data.get('auto_assign')  # Asigna a `auto_assign_raw` el resultado de `raw_data.get`.
        auto_assign_truthy = False  # Asigna un valor a `auto_assign_truthy`.
        if isinstance(auto_assign_raw, bool):  # Evalua la condicion del `if`.
            auto_assign_truthy = auto_assign_raw  # Asigna un valor a `auto_assign_truthy`.
        elif auto_assign_raw is not None:  # Evalua la condicion del `elif`.
            auto_assign_truthy = str(auto_assign_raw).strip().lower() in {  # Asigna a `auto_assign_truthy` el resultado de `str`.
                '1', 'true', 't', 'yes', 'y', 'on', 'si', 'sí'  # Agrega un literal a la estructura.
            }  # Cierra el bloque/estructura.
        if auto_assign_truthy:  # Evalua la condicion del `if`.
            raw_data.pop('driver_id', None)  # Ejecuta `raw_data.pop`.

        return super().to_internal_value(raw_data)  # Devuelve un valor (`return`).

    def validate_driver_id(self, value):  # Define la funcion `validate_driver_id`.
        if value is None:  # Evalua la condicion del `if`.
            return None  # Devuelve un valor (`return`).

        exists = User.objects.filter(id=value, is_active=True).exists()  # Asigna a `exists` el resultado de `User.objects.filter`.
        if not exists:  # Evalua la condicion del `if`.
            raise serializers.ValidationError('El repartidor no existe o esta inactivo.')  # Lanza una excepcion (`raise`).

        return value  # Devuelve un valor (`return`).

    def validate(self, attrs):  # Define la funcion `validate`.
        # El view resuelve la prioridad; no necesitamos ser estrictos aqui.
        return attrs  # Devuelve un valor (`return`).


class DeliveryAddressSerializer(serializers.ModelSerializer):  # Define la clase `DeliveryAddressSerializer`.
    user = serializers.PrimaryKeyRelatedField(read_only=True)  # Asigna a `user` un campo serializer `PrimaryKeyRelatedField`.

    class Meta:  # Define la clase `Meta`.
        model = DeliveryAddress  # Asigna un valor a `model`.
        fields = [  # Asigna un valor a `fields`.
            'id',  # Agrega un literal a la estructura.
            'user',  # Agrega un literal a la estructura.
            'main_address',  # Agrega un literal a la estructura.
            'secondary_street',  # Agrega un literal a la estructura.
            'apartment',  # Agrega un literal a la estructura.
            'city',  # Agrega un literal a la estructura.
            'latitude',  # Agrega un literal a la estructura.
            'longitude',  # Agrega un literal a la estructura.
            'delivery_instructions',  # Agrega un literal a la estructura.
            'is_default',  # Agrega un literal a la estructura.
            'created_at',  # Agrega un literal a la estructura.
            'updated_at',  # Agrega un literal a la estructura.
        ]  # Cierra el bloque/estructura.
        read_only_fields = ['id', 'user', 'created_at', 'updated_at']  # Asigna un valor a `read_only_fields`.

    def to_internal_value(self, data):  # Define la funcion `to_internal_value`.
        raw_data = data.copy() if hasattr(data, 'copy') else dict(data)  # Asigna a `raw_data` el resultado de `data.copy`.

        if 'main_address' not in raw_data:  # Evalua la condicion del `if`.
            raw_data['main_address'] = (  # Asigna un valor a `raw_data['main_address']`.
                data.get('direccion_principal')  # Ejecuta `data.get`.
                or data.get('direccionPrincipal')  # Continua la expresion con `or`.
                or data.get('address_line_1')  # Continua la expresion con `or`.
                or data.get('street')  # Continua la expresion con `or`.
                or ''  # Continua la expresion con `or`.
            )  # Cierra el bloque/estructura.

        if 'secondary_street' not in raw_data:  # Evalua la condicion del `if`.
            raw_data['secondary_street'] = (  # Asigna un valor a `raw_data['secondary_street']`.
                data.get('calle_secundaria')  # Ejecuta `data.get`.
                or data.get('calleSecundaria')  # Continua la expresion con `or`.
                or data.get('address_line_2')  # Continua la expresion con `or`.
                or ''  # Continua la expresion con `or`.
            )  # Cierra el bloque/estructura.

        if 'apartment' not in raw_data:  # Evalua la condicion del `if`.
            raw_data['apartment'] = (  # Asigna un valor a `raw_data['apartment']`.
                data.get('piso_departamento')  # Ejecuta `data.get`.
                or data.get('pisoDepartamento')  # Continua la expresion con `or`.
                or data.get('departamento')  # Continua la expresion con `or`.
                or ''  # Continua la expresion con `or`.
            )  # Cierra el bloque/estructura.

        if 'city' not in raw_data:  # Evalua la condicion del `if`.
            raw_data['city'] = (  # Asigna un valor a `raw_data['city']`.
                data.get('ciudad')  # Ejecuta `data.get`.
                or data.get('province')  # Continua la expresion con `or`.
                or data.get('provincia')  # Continua la expresion con `or`.
                or ''  # Continua la expresion con `or`.
            )  # Cierra el bloque/estructura.

        if 'latitude' not in raw_data:  # Evalua la condicion del `if`.
            raw_data['latitude'] = data.get('latitude') or data.get('lat')  # Asigna a `raw_data['latitude']` el resultado de `data.get`.

        if 'longitude' not in raw_data:  # Evalua la condicion del `if`.
            raw_data['longitude'] = (  # Asigna un valor a `raw_data['longitude']`.
                data.get('longitude')  # Ejecuta `data.get`.
                or data.get('lng')  # Continua la expresion con `or`.
                or data.get('lon')  # Continua la expresion con `or`.
            )  # Cierra el bloque/estructura.

        if 'delivery_instructions' not in raw_data:  # Evalua la condicion del `if`.
            raw_data['delivery_instructions'] = (  # Asigna un valor a `raw_data['delivery_instructions']`.
                data.get('indicaciones')  # Ejecuta `data.get`.
                or data.get('indicaciones_entrega')  # Continua la expresion con `or`.
                or data.get('reference')  # Continua la expresion con `or`.
                or data.get('notes')  # Continua la expresion con `or`.
                or ''  # Continua la expresion con `or`.
            )  # Cierra el bloque/estructura.

        if 'is_default' not in raw_data:  # Evalua la condicion del `if`.
            raw_data['is_default'] = (  # Asigna un valor a `raw_data['is_default']`.
                data.get('default')  # Ejecuta `data.get`.
                if data.get('default') is not None  # Evalua la condicion del `if`.
                else data.get('isDefault', False)  # Rama `else` del operador ternario.
            )  # Cierra el bloque/estructura.

        return super().to_internal_value(raw_data)  # Devuelve un valor (`return`).

    def validate_main_address(self, value):  # Define la funcion `validate_main_address`.
        value = (value or '').strip()  # Asigna un valor a `value`.
        if not value:  # Evalua la condicion del `if`.
            raise serializers.ValidationError('La direccion principal es obligatoria.')  # Lanza una excepcion (`raise`).
        return value  # Devuelve un valor (`return`).

    def validate_latitude(self, value):  # Define la funcion `validate_latitude`.
        if value is None:  # Evalua la condicion del `if`.
            return None  # Devuelve un valor (`return`).
        if value < -90 or value > 90:  # Evalua la condicion del `if`.
            raise serializers.ValidationError('latitude debe estar entre -90 y 90.')  # Lanza una excepcion (`raise`).
        return value  # Devuelve un valor (`return`).

    def validate_longitude(self, value):  # Define la funcion `validate_longitude`.
        if value is None:  # Evalua la condicion del `if`.
            return None  # Devuelve un valor (`return`).
        if value < -180 or value > 180:  # Evalua la condicion del `if`.
            raise serializers.ValidationError('longitude debe estar entre -180 y 180.')  # Lanza una excepcion (`raise`).
        return value  # Devuelve un valor (`return`).

    def validate_city(self, value):  # Define la funcion `validate_city`.
        value = (value or '').strip()  # Asigna un valor a `value`.
        if not value:  # Evalua la condicion del `if`.
            raise serializers.ValidationError('La ciudad es obligatoria.')  # Lanza una excepcion (`raise`).
        return value  # Devuelve un valor (`return`).


class MeSerializer(serializers.ModelSerializer):  # Define la clase `MeSerializer`.
    full_name = serializers.CharField(required=False, allow_blank=True)  # Asigna a `full_name` un campo serializer `CharField`.
    phone = serializers.CharField(required=False, allow_blank=True)  # Asigna a `phone` un campo serializer `CharField`.
    address = serializers.CharField(required=False, allow_blank=True)  # Asigna a `address` un campo serializer `CharField`.
    avatar = serializers.ImageField(required=False, allow_null=True)  # Asigna a `avatar` un campo serializer `ImageField`.
    avatar_url = serializers.SerializerMethodField()  # Asigna a `avatar_url` un campo serializer `SerializerMethodField`.
    role = serializers.SerializerMethodField()  # Asigna a `role` un campo serializer `SerializerMethodField`.
    roles = serializers.SerializerMethodField()  # Asigna a `roles` un campo serializer `SerializerMethodField`.
    pending_role_request = serializers.SerializerMethodField()  # Asigna a `pending_role_request` un campo serializer `SerializerMethodField`.

    class Meta:  # Define la clase `Meta`.
        model = User  # Asigna un valor a `model`.
        fields = [  # Asigna un valor a `fields`.
            'id',  # Agrega un literal a la estructura.
            'username',  # Agrega un literal a la estructura.
            'email',  # Agrega un literal a la estructura.
            'full_name',  # Agrega un literal a la estructura.
            'phone',  # Agrega un literal a la estructura.
            'address',  # Agrega un literal a la estructura.
            'avatar',  # Agrega un literal a la estructura.
            'avatar_url',  # Agrega un literal a la estructura.
            'role',  # Agrega un literal a la estructura.
            'roles',  # Agrega un literal a la estructura.
            'pending_role_request',  # Agrega un literal a la estructura.
        ]  # Cierra el bloque/estructura.
        read_only_fields = ['id', 'username', 'role', 'roles', 'pending_role_request']  # Asigna un valor a `read_only_fields`.

    def to_representation(self, instance):  # Define la funcion `to_representation`.
        data = super().to_representation(instance)  # Asigna a `data` el resultado de `super`.
        data['full_name'] = f'{instance.first_name} {instance.last_name}'.strip()  # Asigna un valor a `data['full_name']`.
        data['phone'] = getattr(getattr(instance, 'profile', None), 'phone', '')  # Asigna a `data['phone']` el resultado de `getattr`.
        data['address'] = getattr(getattr(instance, 'profile', None), 'address', '')  # Asigna a `data['address']` el resultado de `getattr`.
        data['avatar_url'] = self.get_avatar_url(instance)  # Asigna a `data['avatar_url']` el resultado de `self.get_avatar_url`.
        return data  # Devuelve un valor (`return`).

    def _resolve_primary_role(self, roles):  # Define la funcion `_resolve_primary_role`.
        role_set = set(roles)  # Asigna a `role_set` el resultado de `set`.
        if 'ADMIN' in role_set:  # Evalua la condicion del `if`.
            return 'admin'  # Devuelve un valor (`return`).
        if 'DRIVER' in role_set or 'REPARTIDOR' in role_set:  # Evalua la condicion del `if`.
            return 'driver'  # Devuelve un valor (`return`).
        if 'PROVIDER' in role_set:  # Evalua la condicion del `if`.
            return 'provider'  # Devuelve un valor (`return`).
        if 'CLIENTE' in role_set:  # Evalua la condicion del `if`.
            return 'client'  # Devuelve un valor (`return`).
        return 'user'  # Devuelve un valor (`return`).

    def get_roles(self, instance):  # Define la funcion `get_roles`.
        return sorted(list(instance.groups.values_list('name', flat=True)))  # Devuelve un valor (`return`).

    def get_role(self, instance):  # Define la funcion `get_role`.
        roles = self.get_roles(instance)  # Asigna a `roles` el resultado de `self.get_roles`.
        return self._resolve_primary_role(roles)  # Devuelve un valor (`return`).

    def get_pending_role_request(self, instance):  # Define la funcion `get_pending_role_request`.
        pending = instance.role_change_requests.filter(status='pending').order_by('-id').first()  # Asigna a `pending` el resultado de `instance.role_change_requests.filter`.
        if not pending:  # Evalua la condicion del `if`.
            return None  # Devuelve un valor (`return`).
        return {  # Devuelve un valor (`return`).
            'id': pending.id,  # Asigna la clave `id` en un diccionario.
            'requested_role': pending.requested_role,  # Asigna la clave `requested_role` en un diccionario.
            'status': pending.status,  # Asigna la clave `status` en un diccionario.
            'reason': pending.reason,  # Asigna la clave `reason` en un diccionario.
            'created_at': pending.created_at,  # Asigna la clave `created_at` en un diccionario.
        }  # Cierra el bloque/estructura.

    def get_avatar_url(self, instance):  # Define la funcion `get_avatar_url`.
        avatar = getattr(getattr(instance, 'profile', None), 'avatar', None)  # Asigna a `avatar` el resultado de `getattr`.
        if not avatar:  # Evalua la condicion del `if`.
            return ''  # Devuelve un valor (`return`).
        request = self.context.get('request')  # Asigna a `request` el resultado de `self.context.get`.
        if request is None:  # Evalua la condicion del `if`.
            return avatar.url  # Devuelve un valor (`return`).
        return request.build_absolute_uri(avatar.url)  # Devuelve un valor (`return`).

    def to_internal_value(self, data):  # Define la funcion `to_internal_value`.
        raw_data = data.copy() if hasattr(data, 'copy') else dict(data)  # Asigna a `raw_data` el resultado de `data.copy`.

        if 'full_name' not in raw_data:  # Evalua la condicion del `if`.
            raw_data['full_name'] = (  # Asigna un valor a `raw_data['full_name']`.
                data.get('full_name')  # Ejecuta `data.get`.
                or data.get('name')  # Continua la expresion con `or`.
                or data.get('nombre')  # Continua la expresion con `or`.
                or data.get('fullName')  # Continua la expresion con `or`.
                or ''  # Continua la expresion con `or`.
            )  # Cierra el bloque/estructura.

        if 'phone' not in raw_data:  # Evalua la condicion del `if`.
            raw_data['phone'] = (  # Asigna un valor a `raw_data['phone']`.
                data.get('phone')  # Ejecuta `data.get`.
                or data.get('telefono')  # Continua la expresion con `or`.
                or data.get('celular')  # Continua la expresion con `or`.
                or ''  # Continua la expresion con `or`.
            )  # Cierra el bloque/estructura.

        if 'address' not in raw_data:  # Evalua la condicion del `if`.
            raw_data['address'] = (  # Asigna un valor a `raw_data['address']`.
                data.get('address')  # Ejecuta `data.get`.
                or data.get('direccion')  # Continua la expresion con `or`.
                or ''  # Continua la expresion con `or`.
            )  # Cierra el bloque/estructura.

        return super().to_internal_value(raw_data)  # Devuelve un valor (`return`).

    def validate_email(self, value):  # Define la funcion `validate_email`.
        email = (value or '').strip().lower()  # Asigna un valor a `email`.
        user = self.instance  # Asigna un valor a `user`.
        if User.objects.filter(email=email).exclude(id=user.id).exists():  # Evalua la condicion del `if`.
            raise serializers.ValidationError('Ya existe una cuenta con este correo.')  # Lanza una excepcion (`raise`).
        return email  # Devuelve un valor (`return`).

    def validate_phone(self, value):  # Define la funcion `validate_phone`.
        value = (value or '').strip()  # Asigna un valor a `value`.
        if not value:  # Evalua la condicion del `if`.
            return value  # Devuelve un valor (`return`).
        if not value.isdigit():  # Evalua la condicion del `if`.
            raise serializers.ValidationError('El telefono solo debe contener numeros.')  # Lanza una excepcion (`raise`).
        if len(value) != 10:  # Evalua la condicion del `if`.
            raise serializers.ValidationError('El telefono debe tener exactamente 10 digitos.')  # Lanza una excepcion (`raise`).
        if not value.startswith('09'):  # Evalua la condicion del `if`.
            raise serializers.ValidationError('El telefono debe iniciar con 09.')  # Lanza una excepcion (`raise`).
        return value  # Devuelve un valor (`return`).

    def update(self, instance, validated_data):  # Define la funcion `update`.
        full_name = validated_data.pop('full_name', None)  # Asigna a `full_name` el resultado de `validated_data.pop`.
        phone = validated_data.pop('phone', None)  # Asigna a `phone` el resultado de `validated_data.pop`.
        address = validated_data.pop('address', None)  # Asigna a `address` el resultado de `validated_data.pop`.
        avatar = validated_data.pop('avatar', serializers.empty)  # Asigna a `avatar` el resultado de `validated_data.pop`.

        if 'email' in validated_data:  # Evalua la condicion del `if`.
            instance.email = validated_data['email']  # Asigna un valor a `instance.email`.

        if full_name is not None:  # Evalua la condicion del `if`.
            full_name = full_name.strip()  # Asigna a `full_name` el resultado de `full_name.strip`.
            name_parts = full_name.split(maxsplit=1) if full_name else []  # Asigna a `name_parts` el resultado de `full_name.split`.
            instance.first_name = name_parts[0] if len(name_parts) > 0 else ''  # Asigna un valor a `instance.first_name`.
            instance.last_name = name_parts[1] if len(name_parts) > 1 else ''  # Asigna un valor a `instance.last_name`.

        instance.save()  # Ejecuta `instance.save`.

        if phone is not None or address is not None or avatar is not serializers.empty:  # Evalua la condicion del `if`.
            profile, _ = UserProfile.objects.get_or_create(user=instance)  # Asigna a `profile` y `_` el resultado de `UserProfile.objects.get_or_create`.
            if phone is not None:  # Evalua la condicion del `if`.
                profile.phone = phone.strip()  # Asigna a `profile.phone` el resultado de `phone.strip`.
            if address is not None:  # Evalua la condicion del `if`.
                profile.address = (address or '').strip()  # Asigna un valor a `profile.address`.
            if avatar is not serializers.empty:  # Evalua la condicion del `if`.
                profile.avatar = avatar  # Asigna un valor a `profile.avatar`.
            profile.save()  # Ejecuta `profile.save`.

        return instance  # Devuelve un valor (`return`).


class ChangePasswordSerializer(serializers.Serializer):  # Define la clase `ChangePasswordSerializer`.
    current_password = serializers.CharField(required=True, write_only=True)  # Asigna a `current_password` un campo serializer `CharField`.
    new_password = serializers.CharField(required=True, write_only=True)  # Asigna a `new_password` un campo serializer `CharField`.
    new_password2 = serializers.CharField(required=False, allow_blank=True, write_only=True)  # Asigna a `new_password2` un campo serializer `CharField`.

    def to_internal_value(self, data):  # Define la funcion `to_internal_value`.
        raw_data = data.copy() if hasattr(data, 'copy') else dict(data)  # Asigna a `raw_data` el resultado de `data.copy`.

        if 'current_password' not in raw_data:  # Evalua la condicion del `if`.
            raw_data['current_password'] = (  # Asigna un valor a `raw_data['current_password']`.
                data.get('current_password')  # Ejecuta `data.get`.
                or data.get('old_password')  # Continua la expresion con `or`.
                or data.get('actual_password')  # Continua la expresion con `or`.
                or ''  # Continua la expresion con `or`.
            )  # Cierra el bloque/estructura.

        if 'new_password' not in raw_data:  # Evalua la condicion del `if`.
            raw_data['new_password'] = (  # Asigna un valor a `raw_data['new_password']`.
                data.get('new_password')  # Ejecuta `data.get`.
                or data.get('password')  # Continua la expresion con `or`.
                or data.get('nueva_password')  # Continua la expresion con `or`.
                or ''  # Continua la expresion con `or`.
            )  # Cierra el bloque/estructura.

        if 'new_password2' not in raw_data:  # Evalua la condicion del `if`.
            raw_data['new_password2'] = (  # Asigna un valor a `raw_data['new_password2']`.
                data.get('new_password2')  # Ejecuta `data.get`.
                or data.get('confirm_password')  # Continua la expresion con `or`.
                or data.get('confirmPassword')  # Continua la expresion con `or`.
                or ''  # Continua la expresion con `or`.
            )  # Cierra el bloque/estructura.

        return super().to_internal_value(raw_data)  # Devuelve un valor (`return`).

    def validate(self, attrs):  # Define la funcion `validate`.
        new_password = attrs.get('new_password') or ''  # Asigna a `new_password` el resultado de `attrs.get`.
        new_password2 = attrs.get('new_password2') or ''  # Asigna a `new_password2` el resultado de `attrs.get`.
        if len(new_password) < 8:  # Evalua la condicion del `if`.
            raise serializers.ValidationError({'new_password': 'La nueva contrasena debe tener minimo 8 caracteres.'})  # Lanza una excepcion (`raise`).
        if new_password2 and new_password != new_password2:  # Evalua la condicion del `if`.
            raise serializers.ValidationError({'new_password2': 'Las contrasenas no coinciden.'})  # Lanza una excepcion (`raise`).
        return attrs  # Devuelve un valor (`return`).


class RoleChangeRequestSerializer(serializers.ModelSerializer):  # Define la clase `RoleChangeRequestSerializer`.
    user = serializers.PrimaryKeyRelatedField(read_only=True)  # Asigna a `user` un campo serializer `PrimaryKeyRelatedField`.

    class Meta:  # Define la clase `Meta`.
        model = RoleChangeRequest  # Asigna un valor a `model`.
        fields = ['id', 'user', 'requested_role', 'reason', 'status', 'created_at', 'updated_at']  # Asigna un valor a `fields`.
        read_only_fields = ['id', 'user', 'status', 'created_at', 'updated_at']  # Asigna un valor a `read_only_fields`.

    def to_internal_value(self, data):  # Define la funcion `to_internal_value`.
        raw_data = data.copy() if hasattr(data, 'copy') else dict(data)  # Asigna a `raw_data` el resultado de `data.copy`.

        if 'requested_role' not in raw_data:  # Evalua la condicion del `if`.
            raw_data['requested_role'] = (  # Asigna un valor a `raw_data['requested_role']`.
                data.get('requested_role')  # Ejecuta `data.get`.
                or data.get('role')  # Continua la expresion con `or`.
                or data.get('nuevo_rol')  # Continua la expresion con `or`.
                or ''  # Continua la expresion con `or`.
            )  # Cierra el bloque/estructura.

        role = (raw_data.get('requested_role') or '').strip().lower()  # Asigna un valor a `role`.
        role_map = {  # Asigna un valor a `role_map`.
            'proveedor': 'provider',  # Agrega un literal a la estructura.
            'repartidor': 'driver',  # Agrega un literal a la estructura.
            'provider': 'provider',  # Agrega un literal a la estructura.
            'driver': 'driver',  # Agrega un literal a la estructura.
        }  # Cierra el bloque/estructura.
        if role:  # Evalua la condicion del `if`.
            raw_data['requested_role'] = role_map.get(role, role)  # Asigna a `raw_data['requested_role']` el resultado de `role_map.get`.

        if 'reason' not in raw_data:  # Evalua la condicion del `if`.
            raw_data['reason'] = (  # Asigna un valor a `raw_data['reason']`.
                data.get('reason')  # Ejecuta `data.get`.
                or data.get('motivo')  # Continua la expresion con `or`.
                or data.get('description')  # Continua la expresion con `or`.
                or ''  # Continua la expresion con `or`.
            )  # Cierra el bloque/estructura.

        return super().to_internal_value(raw_data)  # Devuelve un valor (`return`).
