from django.contrib import admin  # Importa admin desde `django.contrib`.



from django.contrib.auth.admin import UserAdmin as BaseUserAdmin  # Importa UserAdmin as BaseUserAdmin desde `django.contrib.auth.admin`.



from django.contrib.auth.models import User  # Importa User desde `django.contrib.auth.models`.



from django.utils.html import format_html  # Importa format_html desde `django.utils.html`.



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







# Register your models here.







@admin.register(Category)  # Aplica el decorador `admin.register`.



class CategoryAdmin(admin.ModelAdmin):  # Define la clase `CategoryAdmin`.



    list_display = ('name', 'order', 'image_preview')  # Asigna un valor a `list_display`.



    ordering = ('order', 'name')  # Asigna un valor a `ordering`.



    search_fields = ('name',)  # Asigna un valor a `search_fields`.



    readonly_fields = ('image_preview',)  # Asigna un valor a `readonly_fields`.







    @admin.display(description='Imagen')  # Aplica el decorador `admin.display`.



    def image_preview(self, obj):  # Define la funcion `image_preview`.



        if not obj.image:  # Evalua la condicion del `if`.



            return '-'  # Devuelve un valor (`return`).



        return format_html(  # Devuelve un valor (`return`).



            '<img src="{}" style="height:40px;width:40px;object-fit:cover;border-radius:6px;" />',  # Agrega un literal a la estructura.



            obj.image.url  # Referencia `obj.image.url` en la estructura/expresion.



        )  # Cierra el bloque/estructura.











@admin.register(Banner)  # Aplica el decorador `admin.register`.



class BannerAdmin(admin.ModelAdmin):  # Define la clase `BannerAdmin`.



    list_display = ('title', 'order', 'is_active', 'image_preview')  # Asigna un valor a `list_display`.



    list_filter = ('is_active',)  # Asigna un valor a `list_filter`.



    ordering = ('order', 'id')  # Asigna un valor a `ordering`.



    search_fields = ('title',)  # Asigna un valor a `search_fields`.



    readonly_fields = ('image_preview',)  # Asigna un valor a `readonly_fields`.







    @admin.display(description='Imagen')  # Aplica el decorador `admin.display`.



    def image_preview(self, obj):  # Define la funcion `image_preview`.



        if not obj.image:  # Evalua la condicion del `if`.



            return '-'  # Devuelve un valor (`return`).



        return format_html(  # Devuelve un valor (`return`).



            '<img src="{}" style="height:56px;width:120px;object-fit:cover;border-radius:8px;" />',  # Agrega un literal a la estructura.



            obj.image.url  # Referencia `obj.image.url` en la estructura/expresion.



        )  # Cierra el bloque/estructura.











@admin.register(Product)  # Aplica el decorador `admin.register`.



class ProductAdmin(admin.ModelAdmin):  # Define la clase `ProductAdmin`.



    list_display = (  # Asigna un valor a `list_display`.



        'name',  # Agrega un literal a la estructura.



        'category',  # Agrega un literal a la estructura.



        'short_description',  # Agrega un literal a la estructura.



        'price',  # Agrega un literal a la estructura.



        'old_price',  # Agrega un literal a la estructura.



        'rating',  # Agrega un literal a la estructura.



        'reviews_count',  # Agrega un literal a la estructura.



        'stock',  # Agrega un literal a la estructura.



        'image_preview',  # Agrega un literal a la estructura.



    )  # Cierra el bloque/estructura.



    search_fields = ('name', 'description', 'category__name')  # Asigna un valor a `search_fields`.



    list_filter = ('category', 'price',)  # Asigna un valor a `list_filter`.



    readonly_fields = ('image_preview',)  # Asigna un valor a `readonly_fields`.







    @admin.display(description='Imagen')  # Aplica el decorador `admin.display`.



    def image_preview(self, obj):  # Define la funcion `image_preview`.



        if not obj.image:  # Evalua la condicion del `if`.



            return '-'  # Devuelve un valor (`return`).



        return format_html(  # Devuelve un valor (`return`).



            '<img src="{}" style="height:40px;width:40px;object-fit:cover;border-radius:6px;" />',  # Agrega un literal a la estructura.



            obj.image.url  # Referencia `obj.image.url` en la estructura/expresion.



        )  # Cierra el bloque/estructura.







    @admin.display(description='Descripcion')  # Aplica el decorador `admin.display`.



    def short_description(self, obj):  # Define la funcion `short_description`.



        text = (obj.description or '').strip()  # Asigna un valor a `text`.



        if len(text) <= 40:  # Evalua la condicion del `if`.



            return text  # Devuelve un valor (`return`).



        return f'{text[:40]}...'  # Devuelve un valor (`return`).







@admin.register(Cart)  # Aplica el decorador `admin.register`.



class CartAdmin(admin.ModelAdmin):  # Define la clase `CartAdmin`.



    list_display = ('user', 'product', 'quantity')  # Asigna un valor a `list_display`.



    search_fields = ('user__username', 'product__name')  # Asigna un valor a `search_fields`.











@admin.register(UserProfile)  # Aplica el decorador `admin.register`.



class UserProfileAdmin(admin.ModelAdmin):  # Define la clase `UserProfileAdmin`.



    list_display = ('user', 'avatar_preview', 'phone', 'address')  # Asigna un valor a `list_display`.



    search_fields = ('user__username', 'user__email', 'phone', 'address')  # Asigna un valor a `search_fields`.



    readonly_fields = ('avatar_preview',)  # Asigna un valor a `readonly_fields`.



    fields = ('user', 'phone', 'address', 'avatar', 'avatar_preview')  # Asigna un valor a `fields`.







    @admin.display(description='Foto')  # Aplica el decorador `admin.display`.



    def avatar_preview(self, obj):  # Define la funcion `avatar_preview`.



        if not obj.avatar:  # Evalua la condicion del `if`.



            return '-'  # Devuelve un valor (`return`).



        return format_html(  # Devuelve un valor (`return`).



            '<img src="{}" style="height:40px;width:40px;object-fit:cover;border-radius:50%;" />',  # Agrega un literal a la estructura.



            obj.avatar.url  # Referencia `obj.avatar.url` en la estructura/expresion.



        )  # Cierra el bloque/estructura.











@admin.register(DeliveryAddress)  # Aplica el decorador `admin.register`.



class DeliveryAddressAdmin(admin.ModelAdmin):  # Define la clase `DeliveryAddressAdmin`.



    list_display = ('user', 'main_address', 'city', 'is_default', 'created_at')  # Asigna un valor a `list_display`.



    list_filter = ('city', 'is_default')  # Asigna un valor a `list_filter`.



    search_fields = ('user__username', 'user__email', 'main_address', 'secondary_street', 'apartment', 'city')  # Asigna un valor a `search_fields`.











@admin.register(RoleChangeRequest)  # Aplica el decorador `admin.register`.



class RoleChangeRequestAdmin(admin.ModelAdmin):  # Define la clase `RoleChangeRequestAdmin`.



    list_display = ('user', 'requested_role', 'status', 'created_at')  # Asigna un valor a `list_display`.



    list_filter = ('requested_role', 'status')  # Asigna un valor a `list_filter`.



    search_fields = ('user__username', 'user__email', 'reason')  # Asigna un valor a `search_fields`.











class OrderItemInline(admin.TabularInline):  # Define la clase `OrderItemInline`.



    model = OrderItem  # Asigna un valor a `model`.



    extra = 0  # Asigna un valor a `extra`.



    can_delete = False  # Asigna un valor a `can_delete`.



    fields = ('product', 'product_name', 'product_price', 'quantity', 'subtotal')  # Asigna un valor a `fields`.



    readonly_fields = ('product', 'product_name', 'product_price', 'quantity', 'subtotal')  # Asigna un valor a `readonly_fields`.











@admin.register(Order)  # Aplica el decorador `admin.register`.



class OrderAdmin(admin.ModelAdmin):  # Define la clase `OrderAdmin`.



    list_display = ('id', 'user', 'status', 'total_items', 'total_amount', 'created_at')  # Asigna un valor a `list_display`.



    list_filter = ('status', 'created_at')  # Asigna un valor a `list_filter`.



    search_fields = (  # Asigna un valor a `search_fields`.



        'id',  # Agrega un literal a la estructura.



        'user__username',  # Agrega un literal a la estructura.



        'user__email',  # Agrega un literal a la estructura.



        'delivery_main_address',  # Agrega un literal a la estructura.



        'delivery_city',  # Agrega un literal a la estructura.



    )  # Cierra el bloque/estructura.



    readonly_fields = ('created_at', 'updated_at')  # Asigna un valor a `readonly_fields`.



    inlines = (OrderItemInline,)  # Asigna un valor a `inlines`.











@admin.register(OrderItem)  # Aplica el decorador `admin.register`.



class OrderItemAdmin(admin.ModelAdmin):  # Define la clase `OrderItemAdmin`.



    list_display = ('order', 'product_name', 'quantity', 'product_price', 'subtotal')  # Asigna un valor a `list_display`.



    list_filter = ('order__status',)  # Asigna un valor a `list_filter`.



    search_fields = ('order__id', 'product_name', 'order__user__username')  # Asigna un valor a `search_fields`.











class ShipmentLocationInline(admin.TabularInline):  # Define la clase `ShipmentLocationInline`.



    model = ShipmentLocation  # Asigna un valor a `model`.



    extra = 0  # Asigna un valor a `extra`.



    can_delete = False  # Asigna un valor a `can_delete`.



    readonly_fields = ('latitude', 'longitude', 'heading', 'speed', 'recorded_at')  # Asigna un valor a `readonly_fields`.



    fields = ('latitude', 'longitude', 'heading', 'speed', 'recorded_at')  # Asigna un valor a `fields`.











@admin.register(Shipment)  # Aplica el decorador `admin.register`.



class ShipmentAdmin(admin.ModelAdmin):  # Define la clase `ShipmentAdmin`.



    list_display = (  # Asigna un valor a `list_display`.



        'id',  # Agrega un literal a la estructura.



        'order',  # Agrega un literal a la estructura.



        'driver',  # Agrega un literal a la estructura.



        'status',  # Agrega un literal a la estructura.



        'current_latitude',  # Agrega un literal a la estructura.



        'current_longitude',  # Agrega un literal a la estructura.



        'last_location_at',  # Agrega un literal a la estructura.



        'updated_at',  # Agrega un literal a la estructura.



    )  # Cierra el bloque/estructura.



    list_filter = ('status', 'updated_at')  # Asigna un valor a `list_filter`.



    search_fields = ('order__id', 'order__user__username', 'driver__username')  # Asigna un valor a `search_fields`.



    readonly_fields = ('created_at', 'updated_at', 'last_location_at')  # Asigna un valor a `readonly_fields`.



    inlines = (ShipmentLocationInline,)  # Asigna un valor a `inlines`.











@admin.register(ShipmentLocation)  # Aplica el decorador `admin.register`.



class ShipmentLocationAdmin(admin.ModelAdmin):  # Define la clase `ShipmentLocationAdmin`.



    list_display = ('shipment', 'latitude', 'longitude', 'heading', 'speed', 'recorded_at')  # Asigna un valor a `list_display`.



    list_filter = ('recorded_at',)  # Asigna un valor a `list_filter`.



    search_fields = ('shipment__order__id', 'shipment__order__user__username')  # Asigna un valor a `search_fields`.











class UserProfileInline(admin.StackedInline):  # Define la clase `UserProfileInline`.



    model = UserProfile  # Asigna un valor a `model`.



    can_delete = False  # Asigna un valor a `can_delete`.



    extra = 0  # Asigna un valor a `extra`.



    fk_name = 'user'  # Asigna un valor a `fk_name`.



    fields = ('phone', 'address', 'avatar', 'avatar_preview')  # Asigna un valor a `fields`.



    readonly_fields = ('avatar_preview',)  # Asigna un valor a `readonly_fields`.







    @admin.display(description='Foto actual')  # Aplica el decorador `admin.display`.



    def avatar_preview(self, obj):  # Define la funcion `avatar_preview`.



        if not obj or not obj.avatar:  # Evalua la condicion del `if`.



            return '-'  # Devuelve un valor (`return`).



        return format_html(  # Devuelve un valor (`return`).



            '<img src="{}" style="height:96px;width:96px;object-fit:cover;border-radius:50%;" />',  # Agrega un literal a la estructura.



            obj.avatar.url  # Referencia `obj.avatar.url` en la estructura/expresion.



        )  # Cierra el bloque/estructura.











class UserAdmin(BaseUserAdmin):  # Define la clase `UserAdmin`.



    inlines = (UserProfileInline,)  # Asigna un valor a `inlines`.



    list_display = BaseUserAdmin.list_display + ('avatar_preview', 'role', 'phone', 'address')  # Asigna un valor a `list_display`.







    def get_queryset(self, request):  # Define la funcion `get_queryset`.



        return super().get_queryset(request).select_related('profile').prefetch_related('groups')  # Devuelve un valor (`return`).







    @admin.display(description='Rol')  # Aplica el decorador `admin.display`.



    def role(self, obj):  # Define la funcion `role`.



        roles = list(obj.groups.values_list('name', flat=True))  # Asigna a `roles` el resultado de `list`.



        return ', '.join(roles) if roles else '-'  # Devuelve un valor (`return`).







    @admin.display(description='Phone')  # Aplica el decorador `admin.display`.



    def phone(self, obj):  # Define la funcion `phone`.



        return getattr(getattr(obj, 'profile', None), 'phone', '')  # Devuelve un valor (`return`).







    @admin.display(description='Address')  # Aplica el decorador `admin.display`.



    def address(self, obj):  # Define la funcion `address`.



        return getattr(getattr(obj, 'profile', None), 'address', '')  # Devuelve un valor (`return`).







    @admin.display(description='Foto')  # Aplica el decorador `admin.display`.



    def avatar_preview(self, obj):  # Define la funcion `avatar_preview`.



        avatar = getattr(getattr(obj, 'profile', None), 'avatar', None)  # Asigna a `avatar` el resultado de `getattr`.



        if not avatar:  # Evalua la condicion del `if`.



            return '-'  # Devuelve un valor (`return`).



        return format_html(  # Devuelve un valor (`return`).



            '<img src="{}" style="height:32px;width:32px;object-fit:cover;border-radius:50%;" />',  # Agrega un literal a la estructura.



            avatar.url  # Referencia `avatar.url` en la estructura/expresion.



        )  # Cierra el bloque/estructura.











admin.site.unregister(User)  # Ejecuta `admin.site.unregister`.



admin.site.register(User, UserAdmin)  # Ejecuta `admin.site.register`.



