from rest_framework import serializers
from django.contrib.auth.models import User
from .models import Product, Cart


# =====================================================
# SERIALIZER DE REGISTRO DE USUARIO (SIN ROLES)
# =====================================================

class RegisterSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)

    class Meta:
        model = User
        fields = ['username', 'email', 'password']

    def create(self, validated_data):
        user = User.objects.create_user(
            username=validated_data['username'],
            email=validated_data.get('email'),
            password=validated_data['password']
        )
        return user


# =====================================================
# SERIALIZER DE PRODUCTOS
# =====================================================

class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = '__all__'


# =====================================================
# SERIALIZER DE CARRITO
# =====================================================

class CartSerializer(serializers.ModelSerializer):
    class Meta:
        model = Cart
        fields = '__all__'
