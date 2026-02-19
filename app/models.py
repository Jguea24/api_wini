from django.db import models
from django.contrib.auth.models import Group, User
from django.db.models.signals import post_save
from django.dispatch import receiver


class Category(models.Model):
    name = models.CharField(max_length=100, unique=True)
    order = models.PositiveIntegerField(default=0)
    image = models.ImageField(upload_to='categories/', blank=True, null=True)

    class Meta:
        ordering = ['order', 'name']

    def __str__(self):
        return self.name


class Banner(models.Model):
    title = models.CharField(max_length=120, blank=True)
    image = models.ImageField(upload_to='banners/')
    order = models.PositiveIntegerField(default=0)
    is_active = models.BooleanField(default=True)

    class Meta:
        ordering = ['order', 'id']

    def __str__(self):
        return self.title or f'Banner {self.id}'


class Product(models.Model):
    name = models.CharField(max_length=100)
    price = models.DecimalField(max_digits=8, decimal_places=2)
    old_price = models.DecimalField(max_digits=8, decimal_places=2, null=True, blank=True)
    description = models.TextField(blank=True)
    store_name = models.CharField(max_length=120, blank=True)
    rating = models.DecimalField(max_digits=3, decimal_places=1, null=True, blank=True)
    reviews_count = models.PositiveIntegerField(default=0)
    stock = models.IntegerField()
    image = models.ImageField(upload_to='products/', blank=True, null=True)
    category = models.ForeignKey(
        Category,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='products'
    )

    def __str__(self):
        return self.name


class Cart(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.IntegerField(default=1)

    def __str__(self):
        return f"{self.user.username} - {self.product.name}"


class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profile')
    phone = models.CharField(max_length=20, blank=True)
    address = models.CharField(max_length=255, blank=True)

    def __str__(self):
        return f"Perfil de {self.user.username}"


class DeliveryAddress(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='delivery_addresses')
    main_address = models.CharField(max_length=255)
    secondary_street = models.CharField(max_length=255, blank=True)
    apartment = models.CharField(max_length=120, blank=True)
    city = models.CharField(max_length=120)
    delivery_instructions = models.TextField(blank=True)
    is_default = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-is_default', '-id']

    def __str__(self):
        return f"{self.user.username} - {self.main_address} ({self.city})"


class RoleChangeRequest(models.Model):
    ROLE_CHOICES = [
        ('provider', 'Proveedor'),
        ('driver', 'Repartidor'),
    ]
    STATUS_CHOICES = [
        ('pending', 'Pendiente'),
        ('approved', 'Aprobada'),
        ('rejected', 'Rechazada'),
    ]

    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='role_change_requests')
    requested_role = models.CharField(max_length=20, choices=ROLE_CHOICES)
    reason = models.TextField(blank=True)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-id']

    def __str__(self):
        return f"{self.user.username} -> {self.requested_role} ({self.status})"


class Order(models.Model):
    STATUS_CHOICES = [
        ('pending', 'Pendiente'),
        ('confirmed', 'Confirmado'),
        ('preparing', 'En preparacion'),
        ('on_the_way', 'En camino'),
        ('delivered', 'Entregado'),
        ('cancelled', 'Cancelado'),
    ]

    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='orders')
    delivery_address = models.ForeignKey(
        DeliveryAddress,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='orders',
    )
    delivery_main_address = models.CharField(max_length=255)
    delivery_secondary_street = models.CharField(max_length=255, blank=True)
    delivery_apartment = models.CharField(max_length=120, blank=True)
    delivery_city = models.CharField(max_length=120)
    delivery_instructions = models.TextField(blank=True)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')
    total_amount = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    total_items = models.PositiveIntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-id']

    def __str__(self):
        return f"Pedido #{self.id} - {self.user.username} ({self.status})"


class OrderItem(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name='items')
    product = models.ForeignKey(
        Product,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='order_items',
    )
    product_name = models.CharField(max_length=100)
    product_price = models.DecimalField(max_digits=8, decimal_places=2)
    quantity = models.PositiveIntegerField(default=1)
    subtotal = models.DecimalField(max_digits=10, decimal_places=2, default=0)

    class Meta:
        ordering = ['id']

    def __str__(self):
        return f"{self.order_id} - {self.product_name} x{self.quantity}"


class Shipment(models.Model):
    STATUS_CHOICES = [
        ('pending_assignment', 'Pendiente de asignacion'),
        ('assigned', 'Asignado'),
        ('picked_up', 'Recogido'),
        ('on_the_way', 'En camino'),
        ('nearby', 'Cerca del destino'),
        ('delivered', 'Entregado'),
        ('cancelled', 'Cancelado'),
    ]

    order = models.OneToOneField(Order, on_delete=models.CASCADE, related_name='shipment')
    driver = models.ForeignKey(
        User,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='shipments_assigned',
    )
    status = models.CharField(max_length=30, choices=STATUS_CHOICES, default='pending_assignment')
    current_latitude = models.DecimalField(max_digits=9, decimal_places=6, null=True, blank=True)
    current_longitude = models.DecimalField(max_digits=9, decimal_places=6, null=True, blank=True)
    current_heading = models.DecimalField(max_digits=6, decimal_places=2, null=True, blank=True)
    current_speed = models.DecimalField(max_digits=6, decimal_places=2, null=True, blank=True)
    last_location_at = models.DateTimeField(null=True, blank=True)
    eta_minutes = models.PositiveIntegerField(null=True, blank=True)
    notes = models.CharField(max_length=255, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-id']

    def __str__(self):
        return f"Envio #{self.id} - Pedido #{self.order_id} ({self.status})"


class ShipmentLocation(models.Model):
    shipment = models.ForeignKey(Shipment, on_delete=models.CASCADE, related_name='locations')
    latitude = models.DecimalField(max_digits=9, decimal_places=6)
    longitude = models.DecimalField(max_digits=9, decimal_places=6)
    heading = models.DecimalField(max_digits=6, decimal_places=2, null=True, blank=True)
    speed = models.DecimalField(max_digits=6, decimal_places=2, null=True, blank=True)
    recorded_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-recorded_at', '-id']

    def __str__(self):
        return f"{self.shipment_id} @ {self.latitude},{self.longitude}"


@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        UserProfile.objects.get_or_create(user=instance)


@receiver(post_save, sender=RoleChangeRequest)
def sync_user_groups_on_role_approval(sender, instance, **kwargs):
    if instance.status != 'approved':
        return

    user = instance.user
    cliente_group, _ = Group.objects.get_or_create(name='CLIENTE')
    user.groups.add(cliente_group)

    if instance.requested_role == 'driver':
        driver_group, _ = Group.objects.get_or_create(name='DRIVER')
        user.groups.add(driver_group)
        return

    if instance.requested_role == 'provider':
        provider_group, _ = Group.objects.get_or_create(name='PROVIDER')
        user.groups.add(provider_group)
