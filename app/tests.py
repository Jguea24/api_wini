from django.contrib.auth.models import User  # Importa User desde `django.contrib.auth.models`.
from django.test import TestCase  # Importa TestCase desde `django.test`.
from decimal import Decimal  # Importa Decimal desde `decimal`.
from datetime import date, timedelta  # Importa utilidades de fecha desde `datetime`.

from rest_framework.test import APIClient  # Importa APIClient desde `rest_framework.test`.

from django.contrib.auth.models import Group  # Importa Group desde `django.contrib.auth.models`.

from app.models import (  # Importa modelos desde `app.models`.
    ChocolateLot,  # Referencia `ChocolateLot` en la estructura/expresion.
    CocoaInfo,  # Referencia `CocoaInfo` en la estructura/expresion.
    LotTraceEvent,  # Referencia `LotTraceEvent` en la estructura/expresion.
    Order,  # Referencia `Order` en la estructura/expresion.
    Product,  # Referencia `Product` en la estructura/expresion.
    RoleChangeRequest,  # Referencia `RoleChangeRequest` en la estructura/expresion.
    Shipment,  # Referencia `Shipment` en la estructura/expresion.
)  # Cierra el bloque/estructura.
from app.serializers import RegisterSerializer, ShipmentAssignDriverSerializer  # Importa RegisterSerializer, ShipmentAssignDriverSerializer desde `app.serializers`.


class RegisterRoleFlowTests(TestCase):  # Define la clase `RegisterRoleFlowTests`.
    def test_register_assigns_cliente_group_by_default(self):  # Define la funcion `test_register_assigns_cliente_group_by_default`.
        serializer = RegisterSerializer(data={  # Asigna a `serializer` el resultado de `RegisterSerializer`.
            'email': 'cliente1@example.com',  # Agrega un literal a la estructura.
            'phone': '0999999999',  # Agrega un literal a la estructura.
            'address': 'Av. Siempre Viva 123',  # Agrega un literal a la estructura.
            'password': 'password123',  # Agrega un literal a la estructura.
            'password2': 'password123',  # Agrega un literal a la estructura.
        })  # Cierra la estructura.
        self.assertTrue(serializer.is_valid(), serializer.errors)  # Ejecuta `self.assertTrue`.
        user = serializer.save()  # Asigna a `user` el resultado de `serializer.save`.

        self.assertTrue(user.groups.filter(name='CLIENTE').exists())  # Ejecuta `self.assertTrue`.
        self.assertFalse(RoleChangeRequest.objects.filter(user=user).exists())  # Ejecuta `self.assertFalse`.

    def test_register_driver_role_creates_pending_request(self):  # Define la funcion `test_register_driver_role_creates_pending_request`.
        serializer = RegisterSerializer(data={  # Asigna a `serializer` el resultado de `RegisterSerializer`.
            'email': 'driver1@example.com',  # Agrega un literal a la estructura.
            'phone': '0999999998',  # Agrega un literal a la estructura.
            'address': 'Av. Siempre Viva 124',  # Agrega un literal a la estructura.
            'password': 'password123',  # Agrega un literal a la estructura.
            'password2': 'password123',  # Agrega un literal a la estructura.
            'role': 'driver',  # Agrega un literal a la estructura.
            'role_reason': 'Tengo moto propia',  # Agrega un literal a la estructura.
        })  # Cierra la estructura.
        self.assertTrue(serializer.is_valid(), serializer.errors)  # Ejecuta `self.assertTrue`.
        user = serializer.save()  # Asigna a `user` el resultado de `serializer.save`.

        self.assertTrue(user.groups.filter(name='CLIENTE').exists())  # Ejecuta `self.assertTrue`.
        self.assertFalse(user.groups.filter(name='DRIVER').exists())  # Ejecuta `self.assertFalse`.

        request = RoleChangeRequest.objects.get(user=user)  # Asigna a `request` el resultado de `RoleChangeRequest.objects.get`.
        self.assertEqual(request.requested_role, 'driver')  # Ejecuta `self.assertEqual`.
        self.assertEqual(request.status, 'pending')  # Ejecuta `self.assertEqual`.
        self.assertEqual(request.reason, 'Tengo moto propia')  # Ejecuta `self.assertEqual`.

    def test_register_rejects_invalid_role(self):  # Define la funcion `test_register_rejects_invalid_role`.
        serializer = RegisterSerializer(data={  # Asigna a `serializer` el resultado de `RegisterSerializer`.
            'email': 'rolinvalido@example.com',  # Agrega un literal a la estructura.
            'phone': '0999999997',  # Agrega un literal a la estructura.
            'address': 'Av. Siempre Viva 125',  # Agrega un literal a la estructura.
            'password': 'password123',  # Agrega un literal a la estructura.
            'password2': 'password123',  # Agrega un literal a la estructura.
            'role': 'admin',  # Agrega un literal a la estructura.
        })  # Cierra la estructura.
        self.assertFalse(serializer.is_valid())  # Ejecuta `self.assertFalse`.
        self.assertIn('role', serializer.errors)  # Ejecuta `self.assertIn`.

    def test_approved_driver_request_adds_driver_group(self):  # Define la funcion `test_approved_driver_request_adds_driver_group`.
        user = User.objects.create_user(username='driverx', email='driverx@example.com', password='password123')  # Asigna a `user` el resultado de `User.objects.create_user`.
        role_request = RoleChangeRequest.objects.create(  # Asigna a `role_request` el resultado de `RoleChangeRequest.objects.create`.
            user=user,  # Asigna un valor a `user`.
            requested_role='driver',  # Asigna un valor a `requested_role`.
            status='pending',  # Asigna un valor a `status`.
        )  # Cierra el bloque/estructura.

        role_request.status = 'approved'  # Asigna un valor a `role_request.status`.
        role_request.save(update_fields=['status'])  # Ejecuta `role_request.save`.
        user.refresh_from_db()  # Ejecuta `user.refresh_from_db`.

        self.assertTrue(user.groups.filter(name='CLIENTE').exists())  # Ejecuta `self.assertTrue`.
        self.assertTrue(user.groups.filter(name='DRIVER').exists())  # Ejecuta `self.assertTrue`.

    def test_approved_provider_request_adds_provider_group(self):  # Define la funcion `test_approved_provider_request_adds_provider_group`.
        user = User.objects.create_user(username='providerx', email='providerx@example.com', password='password123')  # Asigna a `user` el resultado de `User.objects.create_user`.
        role_request = RoleChangeRequest.objects.create(  # Asigna a `role_request` el resultado de `RoleChangeRequest.objects.create`.
            user=user,  # Asigna un valor a `user`.
            requested_role='provider',  # Asigna un valor a `requested_role`.
            status='pending',  # Asigna un valor a `status`.
        )  # Cierra el bloque/estructura.

        role_request.status = 'approved'  # Asigna un valor a `role_request.status`.
        role_request.save(update_fields=['status'])  # Ejecuta `role_request.save`.
        user.refresh_from_db()  # Ejecuta `user.refresh_from_db`.

        self.assertTrue(user.groups.filter(name='CLIENTE').exists())  # Ejecuta `self.assertTrue`.
        self.assertTrue(user.groups.filter(name='PROVIDER').exists())  # Ejecuta `self.assertTrue`.


class OrderTrackingMapTests(TestCase):  # Define la clase `OrderTrackingMapTests`.
    def setUp(self):  # Define la funcion `setUp`.
        self.client = APIClient()  # Asigna a `self.client` el resultado de `APIClient`.
        self.user = User.objects.create_user(  # Asigna a `self.user` el resultado de `User.objects.create_user`.
            username='cliente1',  # Asigna un valor a `username`.
            email='cliente1@example.com',  # Asigna un valor a `email`.
            password='password123',  # Asigna un valor a `password`.
        )  # Cierra el bloque/estructura.
        self.client.force_authenticate(user=self.user)  # Ejecuta `self.client.force_authenticate`.

    def test_tracking_include_map_accepts_destination_query_params(self):  # Define la funcion `test_tracking_include_map_accepts_destination_query_params`.
        order = Order.objects.create(  # Asigna a `order` el resultado de `Order.objects.create`.
            user=self.user,  # Asigna un valor a `user`.
            delivery_address=None,  # Asigna un valor a `delivery_address`.
            delivery_main_address='Av. Siempre Viva 123',  # Asigna un valor a `delivery_main_address`.
            delivery_secondary_street='',  # Asigna un valor a `delivery_secondary_street`.
            delivery_apartment='',  # Asigna un valor a `delivery_apartment`.
            delivery_city='Quito',  # Asigna un valor a `delivery_city`.
            delivery_instructions='',  # Asigna un valor a `delivery_instructions`.
            status='confirmed',  # Asigna un valor a `status`.
            total_amount=Decimal('0.00'),  # Asigna a `total_amount` el resultado de `Decimal`.
            total_items=0,  # Asigna un valor a `total_items`.
        )  # Cierra el bloque/estructura.
        Shipment.objects.create(  # Ejecuta `Shipment.objects.create`.
            order=order,  # Asigna un valor a `order`.
            status='assigned',  # Asigna un valor a `status`.
            current_latitude=Decimal('-0.210000'),  # Asigna a `current_latitude` el resultado de `Decimal`.
            current_longitude=Decimal('-78.490000'),  # Asigna a `current_longitude` el resultado de `Decimal`.
        )  # Cierra el bloque/estructura.

        resp = self.client.get(  # Asigna a `resp` el resultado de `self.client.get`.
            f'/orders/{order.id}/tracking/?include_map=1&dest_lat=-0.205000&dest_lng=-78.500000'  # Agrega un literal a la estructura.
        )  # Cierra el bloque/estructura.
        self.assertEqual(resp.status_code, 200, resp.data)  # Ejecuta `self.assertEqual`.
        self.assertIn('map', resp.data)  # Ejecuta `self.assertIn`.
        self.assertEqual(resp.data['map']['destination']['lat'], -0.205)  # Ejecuta `self.assertEqual`.
        self.assertEqual(resp.data['map']['destination']['lng'], -78.5)  # Ejecuta `self.assertEqual`.
        self.assertIsNone(resp.data['map']['route'])  # Ejecuta `self.assertIsNone`.
        self.assertIsNone(resp.data['map']['geocode'])  # Ejecuta `self.assertIsNone`.

    def test_tracking_include_map_uses_order_stored_destination_coords(self):  # Define la funcion `test_tracking_include_map_uses_order_stored_destination_coords`.
        order = Order.objects.create(  # Asigna a `order` el resultado de `Order.objects.create`.
            user=self.user,  # Asigna un valor a `user`.
            delivery_address=None,  # Asigna un valor a `delivery_address`.
            delivery_main_address='Av. Siempre Viva 123',  # Asigna un valor a `delivery_main_address`.
            delivery_secondary_street='',  # Asigna un valor a `delivery_secondary_street`.
            delivery_apartment='',  # Asigna un valor a `delivery_apartment`.
            delivery_city='Quito',  # Asigna un valor a `delivery_city`.
            delivery_latitude=Decimal('-0.205000'),  # Asigna a `delivery_latitude` el resultado de `Decimal`.
            delivery_longitude=Decimal('-78.500000'),  # Asigna a `delivery_longitude` el resultado de `Decimal`.
            delivery_instructions='',  # Asigna un valor a `delivery_instructions`.
            status='confirmed',  # Asigna un valor a `status`.
            total_amount=Decimal('0.00'),  # Asigna a `total_amount` el resultado de `Decimal`.
            total_items=0,  # Asigna un valor a `total_items`.
        )  # Cierra el bloque/estructura.
        Shipment.objects.create(  # Ejecuta `Shipment.objects.create`.
            order=order,  # Asigna un valor a `order`.
            status='assigned',  # Asigna un valor a `status`.
            current_latitude=Decimal('-0.210000'),  # Asigna a `current_latitude` el resultado de `Decimal`.
            current_longitude=Decimal('-78.490000'),  # Asigna a `current_longitude` el resultado de `Decimal`.
        )  # Cierra el bloque/estructura.

        resp = self.client.get(f'/orders/{order.id}/tracking/?include_map=1')  # Asigna a `resp` el resultado de `self.client.get`.
        self.assertEqual(resp.status_code, 200, resp.data)  # Ejecuta `self.assertEqual`.
        self.assertEqual(resp.data['map']['destination']['lat'], -0.205)  # Ejecuta `self.assertEqual`.
        self.assertEqual(resp.data['map']['destination']['lng'], -78.5)  # Ejecuta `self.assertEqual`.
        self.assertIsNone(resp.data['map']['geocode'])  # Ejecuta `self.assertIsNone`.


class ShipmentAssignDriverSerializerTests(TestCase):  # Define la clase `ShipmentAssignDriverSerializerTests`.
    def test_auto_assign_allows_driver_id_null(self):  # Define la funcion `test_auto_assign_allows_driver_id_null`.
        s = ShipmentAssignDriverSerializer(data={'driver_id': None, 'auto_assign': True})  # Asigna a `s` el resultado de `ShipmentAssignDriverSerializer`.
        self.assertTrue(s.is_valid(), s.errors)  # Ejecuta `self.assertTrue`.

    def test_auto_assign_rejects_driver_id_value(self):  # Define la funcion `test_auto_assign_rejects_driver_id_value`.
        driver = User.objects.create_user(username='driver1', email='driver1@example.com', password='password123')  # Asigna a `driver` el resultado de `User.objects.create_user`.
        s = ShipmentAssignDriverSerializer(data={'driver_id': driver.id, 'auto_assign': True})  # Asigna a `s` el resultado de `ShipmentAssignDriverSerializer`.
        self.assertTrue(s.is_valid(), s.errors)  # Ejecuta `self.assertTrue`.
        self.assertNotIn('driver_id', s.validated_data)  # Ejecuta `self.assertNotIn`.


class OrderAssignDriverPermissionTests(TestCase):  # Define la clase `OrderAssignDriverPermissionTests`.
    def setUp(self):  # Define la funcion `setUp`.
        self.client = APIClient()  # Asigna a `self.client` el resultado de `APIClient`.
        self.owner = User.objects.create_user(  # Asigna a `self.owner` el resultado de `User.objects.create_user`.
            username='cliente2',  # Asigna un valor a `username`.
            email='cliente2@example.com',  # Asigna un valor a `email`.
            password='password123',  # Asigna un valor a `password`.
        )  # Cierra el bloque/estructura.
        self.driver = User.objects.create_user(  # Asigna a `self.driver` el resultado de `User.objects.create_user`.
            username='driver2',  # Asigna un valor a `username`.
            email='driver2@example.com',  # Asigna un valor a `email`.
            password='password123',  # Asigna un valor a `password`.
        )  # Cierra el bloque/estructura.
        group, _ = Group.objects.get_or_create(name='DRIVER')  # Asigna a `group` y `_` el resultado de `Group.objects.get_or_create`.
        self.driver.groups.add(group)  # Ejecuta `self.driver.groups.add`.

        self.order = Order.objects.create(  # Asigna a `self.order` el resultado de `Order.objects.create`.
            user=self.owner,  # Asigna un valor a `user`.
            delivery_address=None,  # Asigna un valor a `delivery_address`.
            delivery_main_address='Av. Siempre Viva 222',  # Asigna un valor a `delivery_main_address`.
            delivery_secondary_street='',  # Asigna un valor a `delivery_secondary_street`.
            delivery_apartment='',  # Asigna un valor a `delivery_apartment`.
            delivery_city='Quito',  # Asigna un valor a `delivery_city`.
            delivery_instructions='',  # Asigna un valor a `delivery_instructions`.
            status='pending',  # Asigna un valor a `status`.
            total_amount=Decimal('0.00'),  # Asigna a `total_amount` el resultado de `Decimal`.
            total_items=0,  # Asigna un valor a `total_items`.
        )  # Cierra el bloque/estructura.
        Shipment.objects.create(order=self.order, status='pending_assignment')  # Ejecuta `Shipment.objects.create`.

    def test_owner_can_auto_assign(self):  # Define la funcion `test_owner_can_auto_assign`.
        self.client.force_authenticate(user=self.owner)  # Ejecuta `self.client.force_authenticate`.
        resp = self.client.post(  # Asigna a `resp` el resultado de `self.client.post`.
            f'/orders/{self.order.id}/tracking/assign-driver/',  # Agrega un literal a la estructura.
            data={'auto_assign': True},  # Asigna un valor a `data`.
            format='json',  # Asigna un valor a `format`.
        )  # Cierra el bloque/estructura.
        self.assertEqual(resp.status_code, 200, resp.data)  # Ejecuta `self.assertEqual`.
        self.assertEqual(resp.data.get('driver'), self.driver.id)  # Ejecuta `self.assertEqual`.

    def test_owner_cannot_manual_assign(self):  # Define la funcion `test_owner_cannot_manual_assign`.
        self.client.force_authenticate(user=self.owner)  # Ejecuta `self.client.force_authenticate`.
        resp = self.client.post(  # Asigna a `resp` el resultado de `self.client.post`.
            f'/orders/{self.order.id}/tracking/assign-driver/',  # Agrega un literal a la estructura.
            data={'driver_id': self.driver.id},  # Asigna un valor a `data`.
            format='json',  # Asigna un valor a `format`.
        )  # Cierra el bloque/estructura.
        self.assertEqual(resp.status_code, 403, resp.data)  # Ejecuta `self.assertEqual`.


class TraceabilityByQrViewTests(TestCase):  # Define la clase `TraceabilityByQrViewTests`.
    def setUp(self):  # Define la funcion `setUp`.
        self.client = APIClient()  # Asigna a `self.client` el resultado de `APIClient`.
        self.product = Product.objects.create(  # Asigna a `self.product` el resultado de `Product.objects.create`.
            name='Chocolate 70%',  # Asigna un valor a `name`.
            price=Decimal('4.50'),  # Asigna a `price` el resultado de `Decimal`.
            stock=12,  # Asigna un valor a `stock`.
        )  # Cierra el bloque/estructura.
        CocoaInfo.objects.create(  # Ejecuta `CocoaInfo.objects.create`.
            product=self.product,  # Asigna un valor a `product`.
            cacao_variety='Nacional',  # Asigna un valor a `cacao_variety`.
            origin_country='Ecuador',  # Asigna un valor a `origin_country`.
            origin_region='Los Rios',  # Asigna un valor a `origin_region`.
            farm_name='Finca El Cacao',  # Asigna un valor a `farm_name`.
            fermentation_hours=72,  # Asigna un valor a `fermentation_hours`.
            drying_days=7,  # Asigna un valor a `drying_days`.
            roasting_profile='Ligero',  # Asigna un valor a `roasting_profile`.
            story='Cacao de pequeños productores.',  # Asigna un valor a `story`.
        )  # Cierra el bloque/estructura.
        self.lot = ChocolateLot.objects.create(  # Asigna a `self.lot` el resultado de `ChocolateLot.objects.create`.
            product=self.product,  # Asigna un valor a `product`.
            lot_code='LOT-CHOC-001',  # Asigna un valor a `lot_code`.
            qr_code='QR-CHOC-001',  # Asigna un valor a `qr_code`.
            production_date=date.today() - timedelta(days=5),  # Asigna un valor a `production_date`.
            expiration_date=date.today() + timedelta(days=360),  # Asigna un valor a `expiration_date`.
            cacao_percentage=Decimal('70.00'),  # Asigna a `cacao_percentage` el resultado de `Decimal`.
            bean_origin='Quevedo',  # Asigna un valor a `bean_origin`.
            notes='Lote premium',  # Asigna un valor a `notes`.
            is_active=True,  # Asigna un valor a `is_active`.
        )  # Cierra el bloque/estructura.

    def test_qr_traceability_returns_full_payload(self):  # Define la funcion `test_qr_traceability_returns_full_payload`.
        LotTraceEvent.objects.create(  # Ejecuta `LotTraceEvent.objects.create`.
            lot=self.lot,  # Asigna un valor a `lot`.
            step='Fermentacion',  # Asigna un valor a `step`.
            status='completed',  # Asigna un valor a `status`.
            location='Los Rios',  # Asigna un valor a `location`.
            details='72 horas',  # Asigna un valor a `details`.
        )  # Cierra el bloque/estructura.
        LotTraceEvent.objects.create(  # Ejecuta `LotTraceEvent.objects.create`.
            lot=self.lot,  # Asigna un valor a `lot`.
            step='Tostado',  # Asigna un valor a `step`.
            status='completed',  # Asigna un valor a `status`.
            location='Planta Quito',  # Asigna un valor a `location`.
            details='Perfil ligero',  # Asigna un valor a `details`.
        )  # Cierra el bloque/estructura.

        resp = self.client.get('/trace/qr/QR-CHOC-001/')  # Asigna a `resp` el resultado de `self.client.get`.
        self.assertEqual(resp.status_code, 200, resp.data)  # Ejecuta `self.assertEqual`.
        self.assertEqual(resp.data['qr_code'], 'QR-CHOC-001')  # Ejecuta `self.assertEqual`.
        self.assertEqual(resp.data['lot']['lot_code'], 'LOT-CHOC-001')  # Ejecuta `self.assertEqual`.
        self.assertEqual(resp.data['product']['name'], 'Chocolate 70%')  # Ejecuta `self.assertEqual`.
        self.assertEqual(resp.data['cocoa_info']['origin_country'], 'Ecuador')  # Ejecuta `self.assertEqual`.
        self.assertEqual(len(resp.data['traceability']), 2)  # Ejecuta `self.assertEqual`.

    def test_qr_traceability_fallbacks_to_lot_code(self):  # Define la funcion `test_qr_traceability_fallbacks_to_lot_code`.
        resp = self.client.get('/trace/qr/LOT-CHOC-001/')  # Asigna a `resp` el resultado de `self.client.get`.
        self.assertEqual(resp.status_code, 200, resp.data)  # Ejecuta `self.assertEqual`.
        self.assertEqual(resp.data['lot']['lot_code'], 'LOT-CHOC-001')  # Ejecuta `self.assertEqual`.

    def test_qr_traceability_returns_404_when_not_found(self):  # Define la funcion `test_qr_traceability_returns_404_when_not_found`.
        resp = self.client.get('/trace/qr/NO-EXISTE/')  # Asigna a `resp` el resultado de `self.client.get`.
        self.assertEqual(resp.status_code, 404, resp.data)  # Ejecuta `self.assertEqual`.
        self.assertIn('error', resp.data)  # Ejecuta `self.assertIn`.

    def test_qr_traceability_returns_404_for_inactive_lot(self):  # Define la funcion `test_qr_traceability_returns_404_for_inactive_lot`.
        self.lot.is_active = False  # Asigna un valor a `self.lot.is_active`.
        self.lot.save(update_fields=['is_active'])  # Ejecuta `self.lot.save`.

        resp = self.client.get('/trace/qr/QR-CHOC-001/')  # Asigna a `resp` el resultado de `self.client.get`.
        self.assertEqual(resp.status_code, 404, resp.data)  # Ejecuta `self.assertEqual`.
