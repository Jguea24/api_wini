from django.db import models  # comentario
from django.contrib.auth.models import Group, User  # comentario
from django.db.models.signals import post_save  # comentario
from django.dispatch import receiver  # comentario


class Category(models.Model):  # comentario
    name = models.CharField(max_length=100, unique=True)  # comentario
    order = models.PositiveIntegerField(default=0)  # comentario
    image = models.ImageField(upload_to='categories/', blank=True, null=True)  # comentario

    class Meta:  # comentario
        ordering = ['order', 'name']  # comentario

    def __str__(self):  # comentario
        return self.name  # comentario


class Banner(models.Model):  # comentario
    title = models.CharField(max_length=120, blank=True)  # comentario
    image = models.ImageField(upload_to='banners/')  # comentario
    order = models.PositiveIntegerField(default=0)  # comentario
    is_active = models.BooleanField(default=True)  # comentario

    class Meta:  # comentario
        ordering = ['order', 'id']  # comentario

    def __str__(self):  # comentario
        return self.title or f'Banner {self.id}'  # comentario


class Product(models.Model):  # comentario
    name = models.CharField(max_length=100)  # comentario
    price = models.DecimalField(max_digits=8, decimal_places=2)  # comentario
    old_price = models.DecimalField(max_digits=8, decimal_places=2, null=True, blank=True)  # comentario
    description = models.TextField(blank=True)  # comentario
    store_name = models.CharField(max_length=120, blank=True)  # comentario
    rating = models.DecimalField(max_digits=3, decimal_places=1, null=True, blank=True)  # comentario
    reviews_count = models.PositiveIntegerField(default=0)  # comentario
    stock = models.IntegerField()  # comentario
    image = models.ImageField(upload_to='products/', blank=True, null=True)  # comentario
    category = models.ForeignKey(  # comentario
        Category,  # comentario
        on_delete=models.SET_NULL,  # comentario
        null=True,  # comentario
        blank=True,  # comentario
        related_name='products'  # comentario
    )  # comentario

    def __str__(self):  # comentario
        return self.name  # comentario


class Cart(models.Model):  # comentario
    user = models.ForeignKey(User, on_delete=models.CASCADE)  # comentario
    product = models.ForeignKey(Product, on_delete=models.CASCADE)  # comentario
    quantity = models.IntegerField(default=1)  # comentario

    def __str__(self):  # comentario
        return f"{self.user.username} - {self.product.name}"  # comentario


class UserProfile(models.Model):  # comentario
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profile')  # comentario
    phone = models.CharField(max_length=20, blank=True)  # comentario
    address = models.CharField(max_length=255, blank=True)  # comentario
    avatar = models.ImageField(upload_to='avatars/', blank=True, null=True)  # comentario

    def __str__(self):  # comentario
        return f"Perfil de {self.user.username}"  # comentario


class DeliveryAddress(models.Model):  # comentario
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='delivery_addresses')  # comentario
    main_address = models.CharField(max_length=255)  # comentario
    secondary_street = models.CharField(max_length=255, blank=True)  # comentario
    apartment = models.CharField(max_length=120, blank=True)  # comentario
    city = models.CharField(max_length=120)  # comentario
    latitude = models.DecimalField(max_digits=9, decimal_places=6, null=True, blank=True)  # comentario
    longitude = models.DecimalField(max_digits=9, decimal_places=6, null=True, blank=True)  # comentario
    delivery_instructions = models.TextField(blank=True)  # comentario
    is_default = models.BooleanField(default=False)  # comentario
    created_at = models.DateTimeField(auto_now_add=True)  # comentario
    updated_at = models.DateTimeField(auto_now=True)  # comentario

    class Meta:  # comentario
        ordering = ['-is_default', '-id']  # comentario

    def __str__(self):  # comentario
        return f"{self.user.username} - {self.main_address} ({self.city})"  # comentario


class RoleChangeRequest(models.Model):  # comentario
    ROLE_CHOICES = [  # comentario
        ('provider', 'Proveedor'),  # comentario
        ('driver', 'Repartidor'),  # comentario
    ]  # comentario
    STATUS_CHOICES = [  # comentario
        ('pending', 'Pendiente'),  # comentario
        ('approved', 'Aprobada'),  # comentario
        ('rejected', 'Rechazada'),  # comentario
    ]  # comentario

    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='role_change_requests')  # comentario
    requested_role = models.CharField(max_length=20, choices=ROLE_CHOICES)  # comentario
    reason = models.TextField(blank=True)  # comentario
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')  # comentario
    created_at = models.DateTimeField(auto_now_add=True)  # comentario
    updated_at = models.DateTimeField(auto_now=True)  # comentario

    class Meta:  # comentario
        ordering = ['-id']  # comentario

    def __str__(self):  # comentario
        return f"{self.user.username} -> {self.requested_role} ({self.status})"  # comentario


class Order(models.Model):  # comentario
    STATUS_CHOICES = [  # comentario
        ('pending', 'Pendiente'),  # comentario
        ('confirmed', 'Confirmado'),  # comentario
        ('preparing', 'En preparacion'),  # comentario
        ('on_the_way', 'En camino'),  # comentario
        ('delivered', 'Entregado'),  # comentario
        ('cancelled', 'Cancelado'),  # comentario
    ]  # comentario

    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='orders')  # comentario
    delivery_address = models.ForeignKey(  # comentario
        DeliveryAddress,  # comentario
        on_delete=models.SET_NULL,  # comentario
        null=True,  # comentario
        blank=True,  # comentario
        related_name='orders',  # comentario
    )  # comentario
    delivery_main_address = models.CharField(max_length=255)  # comentario
    delivery_secondary_street = models.CharField(max_length=255, blank=True)  # comentario
    delivery_apartment = models.CharField(max_length=120, blank=True)  # comentario
    delivery_city = models.CharField(max_length=120)  # comentario
    delivery_latitude = models.DecimalField(max_digits=9, decimal_places=6, null=True, blank=True)  # comentario
    delivery_longitude = models.DecimalField(max_digits=9, decimal_places=6, null=True, blank=True)  # comentario
    delivery_instructions = models.TextField(blank=True)  # comentario
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')  # comentario
    total_amount = models.DecimalField(max_digits=10, decimal_places=2, default=0)  # comentario
    total_items = models.PositiveIntegerField(default=0)  # comentario
    created_at = models.DateTimeField(auto_now_add=True)  # comentario
    updated_at = models.DateTimeField(auto_now=True)  # comentario

    class Meta:  # comentario
        ordering = ['-id']  # comentario

    def __str__(self):  # comentario
        return f"Pedido #{self.id} - {self.user.username} ({self.status})"  # comentario


class OrderItem(models.Model):  # comentario
    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name='items')  # comentario
    product = models.ForeignKey(  # comentario
        Product,  # comentario
        on_delete=models.SET_NULL,  # comentario
        null=True,  # comentario
        blank=True,  # comentario
        related_name='order_items',  # comentario
    )  # comentario
    product_name = models.CharField(max_length=100)  # comentario
    product_price = models.DecimalField(max_digits=8, decimal_places=2)  # comentario
    quantity = models.PositiveIntegerField(default=1)  # comentario
    subtotal = models.DecimalField(max_digits=10, decimal_places=2, default=0)  # comentario

    class Meta:  # comentario
        ordering = ['id']  # comentario

    def __str__(self):  # comentario
        return f"{self.order_id} - {self.product_name} x{self.quantity}"  # comentario


class Shipment(models.Model):  # comentario
    STATUS_CHOICES = [  # comentario
        ('pending_assignment', 'Pendiente de asignacion'),  # comentario
        ('assigned', 'Asignado'),  # comentario
        ('picked_up', 'Recogido'),  # comentario
        ('on_the_way', 'En camino'),  # comentario
        ('nearby', 'Cerca del destino'),  # comentario
        ('delivered', 'Entregado'),  # comentario
        ('cancelled', 'Cancelado'),  # comentario
    ]  # comentario

    order = models.OneToOneField(Order, on_delete=models.CASCADE, related_name='shipment')  # comentario
    driver = models.ForeignKey(  # comentario
        User,  # comentario
        on_delete=models.SET_NULL,  # comentario
        null=True,  # comentario
        blank=True,  # comentario
        related_name='shipments_assigned',  # comentario
    )  # comentario
    status = models.CharField(max_length=30, choices=STATUS_CHOICES, default='pending_assignment')  # comentario
    current_latitude = models.DecimalField(max_digits=9, decimal_places=6, null=True, blank=True)  # comentario
    current_longitude = models.DecimalField(max_digits=9, decimal_places=6, null=True, blank=True)  # comentario
    current_heading = models.DecimalField(max_digits=6, decimal_places=2, null=True, blank=True)  # comentario
    current_speed = models.DecimalField(max_digits=6, decimal_places=2, null=True, blank=True)  # comentario
    last_location_at = models.DateTimeField(null=True, blank=True)  # comentario
    eta_minutes = models.PositiveIntegerField(null=True, blank=True)  # comentario
    notes = models.CharField(max_length=255, blank=True)  # comentario
    created_at = models.DateTimeField(auto_now_add=True)  # comentario
    updated_at = models.DateTimeField(auto_now=True)  # comentario

    class Meta:  # comentario
        ordering = ['-id']  # comentario

    def __str__(self):  # comentario
        return f"Envio #{self.id} - Pedido #{self.order_id} ({self.status})"  # comentario


class ShipmentLocation(models.Model):  # comentario
    shipment = models.ForeignKey(Shipment, on_delete=models.CASCADE, related_name='locations')  # comentario
    latitude = models.DecimalField(max_digits=9, decimal_places=6)  # comentario
    longitude = models.DecimalField(max_digits=9, decimal_places=6)  # comentario
    heading = models.DecimalField(max_digits=6, decimal_places=2, null=True, blank=True)  # comentario
    speed = models.DecimalField(max_digits=6, decimal_places=2, null=True, blank=True)  # comentario
    recorded_at = models.DateTimeField(auto_now_add=True)  # comentario

    class Meta:  # comentario
        ordering = ['-recorded_at', '-id']  # comentario

    def __str__(self):  # comentario
        return f"{self.shipment_id} @ {self.latitude},{self.longitude}"  # comentario


@receiver(post_save, sender=User)  # comentario
def create_user_profile(sender, instance, created, **kwargs):  # comentario
    if created:  # comentario
        UserProfile.objects.get_or_create(user=instance)  # comentario


@receiver(post_save, sender=RoleChangeRequest)  # comentario
def sync_user_groups_on_role_approval(sender, instance, **kwargs):  # comentario
    if instance.status != 'approved':  # comentario
        return  # comentario

    user = instance.user  # comentario
    cliente_group, _ = Group.objects.get_or_create(name='CLIENTE')  # comentario
    user.groups.add(cliente_group)  # comentario

    if instance.requested_role == 'driver':  # comentario
        driver_group, _ = Group.objects.get_or_create(name='DRIVER')  # comentario
        user.groups.add(driver_group)  # comentario
        return  # comentario

    if instance.requested_role == 'provider':  # comentario
        provider_group, _ = Group.objects.get_or_create(name='PROVIDER')  # comentario
        user.groups.add(provider_group)  # comentario
