from django.contrib import admin  # comentario
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin  # comentario
from django.contrib.auth.models import User  # comentario
from django.utils.html import format_html  # comentario
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

# Register your models here.

@admin.register(Category)  # comentario
class CategoryAdmin(admin.ModelAdmin):  # comentario
    list_display = ('name', 'order', 'image_preview')  # comentario
    ordering = ('order', 'name')  # comentario
    search_fields = ('name',)  # comentario
    readonly_fields = ('image_preview',)  # comentario

    @admin.display(description='Imagen')  # comentario
    def image_preview(self, obj):  # comentario
        if not obj.image:  # comentario
            return '-'  # comentario
        return format_html(  # comentario
            '<img src="{}" style="height:40px;width:40px;object-fit:cover;border-radius:6px;" />',  # comentario
            obj.image.url  # comentario
        )  # comentario


@admin.register(Banner)  # comentario
class BannerAdmin(admin.ModelAdmin):  # comentario
    list_display = ('title', 'order', 'is_active', 'image_preview')  # comentario
    list_filter = ('is_active',)  # comentario
    ordering = ('order', 'id')  # comentario
    search_fields = ('title',)  # comentario
    readonly_fields = ('image_preview',)  # comentario

    @admin.display(description='Imagen')  # comentario
    def image_preview(self, obj):  # comentario
        if not obj.image:  # comentario
            return '-'  # comentario
        return format_html(  # comentario
            '<img src="{}" style="height:56px;width:120px;object-fit:cover;border-radius:8px;" />',  # comentario
            obj.image.url  # comentario
        )  # comentario


@admin.register(Product)  # comentario
class ProductAdmin(admin.ModelAdmin):  # comentario
    list_display = (  # comentario
        'name',  # comentario
        'category',  # comentario
        'short_description',  # comentario
        'price',  # comentario
        'old_price',  # comentario
        'rating',  # comentario
        'reviews_count',  # comentario
        'stock',  # comentario
        'image_preview',  # comentario
    )  # comentario
    search_fields = ('name', 'description', 'category__name')  # comentario
    list_filter = ('category', 'price',)  # comentario
    readonly_fields = ('image_preview',)  # comentario

    @admin.display(description='Imagen')  # comentario
    def image_preview(self, obj):  # comentario
        if not obj.image:  # comentario
            return '-'  # comentario
        return format_html(  # comentario
            '<img src="{}" style="height:40px;width:40px;object-fit:cover;border-radius:6px;" />',  # comentario
            obj.image.url  # comentario
        )  # comentario

    @admin.display(description='Descripcion')  # comentario
    def short_description(self, obj):  # comentario
        text = (obj.description or '').strip()  # comentario
        if len(text) <= 40:  # comentario
            return text  # comentario
        return f'{text[:40]}...'  # comentario

@admin.register(Cart)  # comentario
class CartAdmin(admin.ModelAdmin):  # comentario
    list_display = ('user', 'product', 'quantity')  # comentario
    search_fields = ('user__username', 'product__name')  # comentario


@admin.register(UserProfile)  # comentario
class UserProfileAdmin(admin.ModelAdmin):  # comentario
    list_display = ('user', 'avatar_preview', 'phone', 'address')  # comentario
    search_fields = ('user__username', 'user__email', 'phone', 'address')  # comentario
    readonly_fields = ('avatar_preview',)  # comentario
    fields = ('user', 'phone', 'address', 'avatar', 'avatar_preview')  # comentario

    @admin.display(description='Foto')  # comentario
    def avatar_preview(self, obj):  # comentario
        if not obj.avatar:  # comentario
            return '-'  # comentario
        return format_html(  # comentario
            '<img src="{}" style="height:40px;width:40px;object-fit:cover;border-radius:50%;" />',  # comentario
            obj.avatar.url  # comentario
        )  # comentario


@admin.register(DeliveryAddress)  # comentario
class DeliveryAddressAdmin(admin.ModelAdmin):  # comentario
    list_display = ('user', 'main_address', 'city', 'is_default', 'created_at')  # comentario
    list_filter = ('city', 'is_default')  # comentario
    search_fields = ('user__username', 'user__email', 'main_address', 'secondary_street', 'apartment', 'city')  # comentario


@admin.register(RoleChangeRequest)  # comentario
class RoleChangeRequestAdmin(admin.ModelAdmin):  # comentario
    list_display = ('user', 'requested_role', 'status', 'created_at')  # comentario
    list_filter = ('requested_role', 'status')  # comentario
    search_fields = ('user__username', 'user__email', 'reason')  # comentario


class OrderItemInline(admin.TabularInline):  # comentario
    model = OrderItem  # comentario
    extra = 0  # comentario
    can_delete = False  # comentario
    fields = ('product', 'product_name', 'product_price', 'quantity', 'subtotal')  # comentario
    readonly_fields = ('product', 'product_name', 'product_price', 'quantity', 'subtotal')  # comentario


@admin.register(Order)  # comentario
class OrderAdmin(admin.ModelAdmin):  # comentario
    list_display = ('id', 'user', 'status', 'total_items', 'total_amount', 'created_at')  # comentario
    list_filter = ('status', 'created_at')  # comentario
    search_fields = (  # comentario
        'id',  # comentario
        'user__username',  # comentario
        'user__email',  # comentario
        'delivery_main_address',  # comentario
        'delivery_city',  # comentario
    )  # comentario
    readonly_fields = ('created_at', 'updated_at')  # comentario
    inlines = (OrderItemInline,)  # comentario


@admin.register(OrderItem)  # comentario
class OrderItemAdmin(admin.ModelAdmin):  # comentario
    list_display = ('order', 'product_name', 'quantity', 'product_price', 'subtotal')  # comentario
    list_filter = ('order__status',)  # comentario
    search_fields = ('order__id', 'product_name', 'order__user__username')  # comentario


class ShipmentLocationInline(admin.TabularInline):  # comentario
    model = ShipmentLocation  # comentario
    extra = 0  # comentario
    can_delete = False  # comentario
    readonly_fields = ('latitude', 'longitude', 'heading', 'speed', 'recorded_at')  # comentario
    fields = ('latitude', 'longitude', 'heading', 'speed', 'recorded_at')  # comentario


@admin.register(Shipment)  # comentario
class ShipmentAdmin(admin.ModelAdmin):  # comentario
    list_display = (  # comentario
        'id',  # comentario
        'order',  # comentario
        'driver',  # comentario
        'status',  # comentario
        'current_latitude',  # comentario
        'current_longitude',  # comentario
        'last_location_at',  # comentario
        'updated_at',  # comentario
    )  # comentario
    list_filter = ('status', 'updated_at')  # comentario
    search_fields = ('order__id', 'order__user__username', 'driver__username')  # comentario
    readonly_fields = ('created_at', 'updated_at', 'last_location_at')  # comentario
    inlines = (ShipmentLocationInline,)  # comentario


@admin.register(ShipmentLocation)  # comentario
class ShipmentLocationAdmin(admin.ModelAdmin):  # comentario
    list_display = ('shipment', 'latitude', 'longitude', 'heading', 'speed', 'recorded_at')  # comentario
    list_filter = ('recorded_at',)  # comentario
    search_fields = ('shipment__order__id', 'shipment__order__user__username')  # comentario


class UserProfileInline(admin.StackedInline):  # comentario
    model = UserProfile  # comentario
    can_delete = False  # comentario
    extra = 0  # comentario
    fk_name = 'user'  # comentario
    fields = ('phone', 'address', 'avatar', 'avatar_preview')  # comentario
    readonly_fields = ('avatar_preview',)  # comentario

    @admin.display(description='Foto actual')  # comentario
    def avatar_preview(self, obj):  # comentario
        if not obj or not obj.avatar:  # comentario
            return '-'  # comentario
        return format_html(  # comentario
            '<img src="{}" style="height:96px;width:96px;object-fit:cover;border-radius:50%;" />',  # comentario
            obj.avatar.url  # comentario
        )  # comentario


class UserAdmin(BaseUserAdmin):  # comentario
    inlines = (UserProfileInline,)  # comentario
    list_display = BaseUserAdmin.list_display + ('avatar_preview', 'role', 'phone', 'address')  # comentario

    def get_queryset(self, request):  # comentario
        return super().get_queryset(request).select_related('profile').prefetch_related('groups')  # comentario

    @admin.display(description='Rol')  # comentario
    def role(self, obj):  # comentario
        roles = list(obj.groups.values_list('name', flat=True))  # comentario
        return ', '.join(roles) if roles else '-'  # comentario

    @admin.display(description='Phone')  # comentario
    def phone(self, obj):  # comentario
        return getattr(getattr(obj, 'profile', None), 'phone', '')  # comentario

    @admin.display(description='Address')  # comentario
    def address(self, obj):  # comentario
        return getattr(getattr(obj, 'profile', None), 'address', '')  # comentario

    @admin.display(description='Foto')  # comentario
    def avatar_preview(self, obj):  # comentario
        avatar = getattr(getattr(obj, 'profile', None), 'avatar', None)  # comentario
        if not avatar:  # comentario
            return '-'  # comentario
        return format_html(  # comentario
            '<img src="{}" style="height:32px;width:32px;object-fit:cover;border-radius:50%;" />',  # comentario
            avatar.url  # comentario
        )  # comentario


admin.site.unregister(User)  # comentario
admin.site.register(User, UserAdmin)  # comentario
