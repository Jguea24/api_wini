from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.contrib.auth.models import User
from django.utils.html import format_html
from .models import (
    Banner,
    Category,
    Product,
    Cart,
    UserProfile,
    DeliveryAddress,
    RoleChangeRequest,
    Order,
    OrderItem,
    Shipment,
    ShipmentLocation,
)

# Register your models here.

@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'order', 'image_preview')
    ordering = ('order', 'name')
    search_fields = ('name',)
    readonly_fields = ('image_preview',)

    @admin.display(description='Imagen')
    def image_preview(self, obj):
        if not obj.image:
            return '-'
        return format_html(
            '<img src="{}" style="height:40px;width:40px;object-fit:cover;border-radius:6px;" />',
            obj.image.url
        )


@admin.register(Banner)
class BannerAdmin(admin.ModelAdmin):
    list_display = ('title', 'order', 'is_active', 'image_preview')
    list_filter = ('is_active',)
    ordering = ('order', 'id')
    search_fields = ('title',)
    readonly_fields = ('image_preview',)

    @admin.display(description='Imagen')
    def image_preview(self, obj):
        if not obj.image:
            return '-'
        return format_html(
            '<img src="{}" style="height:56px;width:120px;object-fit:cover;border-radius:8px;" />',
            obj.image.url
        )


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = (
        'name',
        'category',
        'short_description',
        'price',
        'old_price',
        'rating',
        'reviews_count',
        'stock',
        'image_preview',
    )
    search_fields = ('name', 'description', 'category__name')
    list_filter = ('category', 'price',)
    readonly_fields = ('image_preview',)

    @admin.display(description='Imagen')
    def image_preview(self, obj):
        if not obj.image:
            return '-'
        return format_html(
            '<img src="{}" style="height:40px;width:40px;object-fit:cover;border-radius:6px;" />',
            obj.image.url
        )

    @admin.display(description='Descripcion')
    def short_description(self, obj):
        text = (obj.description or '').strip()
        if len(text) <= 40:
            return text
        return f'{text[:40]}...'

@admin.register(Cart)
class CartAdmin(admin.ModelAdmin):
    list_display = ('user', 'product', 'quantity')
    search_fields = ('user__username', 'product__name')


@admin.register(UserProfile)
class UserProfileAdmin(admin.ModelAdmin):
    list_display = ('user', 'phone', 'address')
    search_fields = ('user__username', 'user__email', 'phone', 'address')


@admin.register(DeliveryAddress)
class DeliveryAddressAdmin(admin.ModelAdmin):
    list_display = ('user', 'main_address', 'city', 'is_default', 'created_at')
    list_filter = ('city', 'is_default')
    search_fields = ('user__username', 'user__email', 'main_address', 'secondary_street', 'apartment', 'city')


@admin.register(RoleChangeRequest)
class RoleChangeRequestAdmin(admin.ModelAdmin):
    list_display = ('user', 'requested_role', 'status', 'created_at')
    list_filter = ('requested_role', 'status')
    search_fields = ('user__username', 'user__email', 'reason')


class OrderItemInline(admin.TabularInline):
    model = OrderItem
    extra = 0
    can_delete = False
    fields = ('product', 'product_name', 'product_price', 'quantity', 'subtotal')
    readonly_fields = ('product', 'product_name', 'product_price', 'quantity', 'subtotal')


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'status', 'total_items', 'total_amount', 'created_at')
    list_filter = ('status', 'created_at')
    search_fields = (
        'id',
        'user__username',
        'user__email',
        'delivery_main_address',
        'delivery_city',
    )
    readonly_fields = ('created_at', 'updated_at')
    inlines = (OrderItemInline,)


@admin.register(OrderItem)
class OrderItemAdmin(admin.ModelAdmin):
    list_display = ('order', 'product_name', 'quantity', 'product_price', 'subtotal')
    list_filter = ('order__status',)
    search_fields = ('order__id', 'product_name', 'order__user__username')


class ShipmentLocationInline(admin.TabularInline):
    model = ShipmentLocation
    extra = 0
    can_delete = False
    readonly_fields = ('latitude', 'longitude', 'heading', 'speed', 'recorded_at')
    fields = ('latitude', 'longitude', 'heading', 'speed', 'recorded_at')


@admin.register(Shipment)
class ShipmentAdmin(admin.ModelAdmin):
    list_display = (
        'id',
        'order',
        'driver',
        'status',
        'current_latitude',
        'current_longitude',
        'last_location_at',
        'updated_at',
    )
    list_filter = ('status', 'updated_at')
    search_fields = ('order__id', 'order__user__username', 'driver__username')
    readonly_fields = ('created_at', 'updated_at', 'last_location_at')
    inlines = (ShipmentLocationInline,)


@admin.register(ShipmentLocation)
class ShipmentLocationAdmin(admin.ModelAdmin):
    list_display = ('shipment', 'latitude', 'longitude', 'heading', 'speed', 'recorded_at')
    list_filter = ('recorded_at',)
    search_fields = ('shipment__order__id', 'shipment__order__user__username')


class UserProfileInline(admin.StackedInline):
    model = UserProfile
    can_delete = False
    extra = 0
    fk_name = 'user'


class UserAdmin(BaseUserAdmin):
    inlines = (UserProfileInline,)
    list_display = BaseUserAdmin.list_display + ('role', 'phone', 'address')

    def get_queryset(self, request):
        return super().get_queryset(request).select_related('profile').prefetch_related('groups')

    @admin.display(description='Rol')
    def role(self, obj):
        roles = list(obj.groups.values_list('name', flat=True))
        return ', '.join(roles) if roles else '-'

    @admin.display(description='Phone')
    def phone(self, obj):
        return getattr(getattr(obj, 'profile', None), 'phone', '')

    @admin.display(description='Address')
    def address(self, obj):
        return getattr(getattr(obj, 'profile', None), 'address', '')


admin.site.unregister(User)
admin.site.register(User, UserAdmin)
