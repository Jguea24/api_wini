from django.contrib.auth.models import User  # comentario
from django.test import TestCase  # comentario
from decimal import Decimal  # comentario

from rest_framework.test import APIClient  # comentario

from django.contrib.auth.models import Group  # comentario

from app.models import Order, RoleChangeRequest, Shipment  # comentario
from app.serializers import RegisterSerializer, ShipmentAssignDriverSerializer  # comentario


class RegisterRoleFlowTests(TestCase):  # comentario
    def test_register_assigns_cliente_group_by_default(self):  # comentario
        serializer = RegisterSerializer(data={  # comentario
            'email': 'cliente1@example.com',  # comentario
            'phone': '0999999999',  # comentario
            'address': 'Av. Siempre Viva 123',  # comentario
            'password': 'password123',  # comentario
            'password2': 'password123',  # comentario
        })  # comentario
        self.assertTrue(serializer.is_valid(), serializer.errors)  # comentario
        user = serializer.save()  # comentario

        self.assertTrue(user.groups.filter(name='CLIENTE').exists())  # comentario
        self.assertFalse(RoleChangeRequest.objects.filter(user=user).exists())  # comentario

    def test_register_driver_role_creates_pending_request(self):  # comentario
        serializer = RegisterSerializer(data={  # comentario
            'email': 'driver1@example.com',  # comentario
            'phone': '0999999998',  # comentario
            'address': 'Av. Siempre Viva 124',  # comentario
            'password': 'password123',  # comentario
            'password2': 'password123',  # comentario
            'role': 'driver',  # comentario
            'role_reason': 'Tengo moto propia',  # comentario
        })  # comentario
        self.assertTrue(serializer.is_valid(), serializer.errors)  # comentario
        user = serializer.save()  # comentario

        self.assertTrue(user.groups.filter(name='CLIENTE').exists())  # comentario
        self.assertFalse(user.groups.filter(name='DRIVER').exists())  # comentario

        request = RoleChangeRequest.objects.get(user=user)  # comentario
        self.assertEqual(request.requested_role, 'driver')  # comentario
        self.assertEqual(request.status, 'pending')  # comentario
        self.assertEqual(request.reason, 'Tengo moto propia')  # comentario

    def test_register_rejects_invalid_role(self):  # comentario
        serializer = RegisterSerializer(data={  # comentario
            'email': 'rolinvalido@example.com',  # comentario
            'phone': '0999999997',  # comentario
            'address': 'Av. Siempre Viva 125',  # comentario
            'password': 'password123',  # comentario
            'password2': 'password123',  # comentario
            'role': 'admin',  # comentario
        })  # comentario
        self.assertFalse(serializer.is_valid())  # comentario
        self.assertIn('role', serializer.errors)  # comentario

    def test_approved_driver_request_adds_driver_group(self):  # comentario
        user = User.objects.create_user(username='driverx', email='driverx@example.com', password='password123')  # comentario
        role_request = RoleChangeRequest.objects.create(  # comentario
            user=user,  # comentario
            requested_role='driver',  # comentario
            status='pending',  # comentario
        )  # comentario

        role_request.status = 'approved'  # comentario
        role_request.save(update_fields=['status'])  # comentario
        user.refresh_from_db()  # comentario

        self.assertTrue(user.groups.filter(name='CLIENTE').exists())  # comentario
        self.assertTrue(user.groups.filter(name='DRIVER').exists())  # comentario

    def test_approved_provider_request_adds_provider_group(self):  # comentario
        user = User.objects.create_user(username='providerx', email='providerx@example.com', password='password123')  # comentario
        role_request = RoleChangeRequest.objects.create(  # comentario
            user=user,  # comentario
            requested_role='provider',  # comentario
            status='pending',  # comentario
        )  # comentario

        role_request.status = 'approved'  # comentario
        role_request.save(update_fields=['status'])  # comentario
        user.refresh_from_db()  # comentario

        self.assertTrue(user.groups.filter(name='CLIENTE').exists())  # comentario
        self.assertTrue(user.groups.filter(name='PROVIDER').exists())  # comentario


class OrderTrackingMapTests(TestCase):  # comentario
    def setUp(self):  # comentario
        self.client = APIClient()  # comentario
        self.user = User.objects.create_user(  # comentario
            username='cliente1',  # comentario
            email='cliente1@example.com',  # comentario
            password='password123',  # comentario
        )  # comentario
        self.client.force_authenticate(user=self.user)  # comentario

    def test_tracking_include_map_accepts_destination_query_params(self):  # comentario
        order = Order.objects.create(  # comentario
            user=self.user,  # comentario
            delivery_address=None,  # comentario
            delivery_main_address='Av. Siempre Viva 123',  # comentario
            delivery_secondary_street='',  # comentario
            delivery_apartment='',  # comentario
            delivery_city='Quito',  # comentario
            delivery_instructions='',  # comentario
            status='confirmed',  # comentario
            total_amount=Decimal('0.00'),  # comentario
            total_items=0,  # comentario
        )  # comentario
        Shipment.objects.create(  # comentario
            order=order,  # comentario
            status='assigned',  # comentario
            current_latitude=Decimal('-0.210000'),  # comentario
            current_longitude=Decimal('-78.490000'),  # comentario
        )  # comentario

        resp = self.client.get(  # comentario
            f'/orders/{order.id}/tracking/?include_map=1&dest_lat=-0.205000&dest_lng=-78.500000'  # comentario
        )  # comentario
        self.assertEqual(resp.status_code, 200, resp.data)  # comentario
        self.assertIn('map', resp.data)  # comentario
        self.assertEqual(resp.data['map']['destination']['lat'], -0.205)  # comentario
        self.assertEqual(resp.data['map']['destination']['lng'], -78.5)  # comentario
        self.assertIsNone(resp.data['map']['route'])  # comentario
        self.assertIsNone(resp.data['map']['geocode'])  # comentario

    def test_tracking_include_map_uses_order_stored_destination_coords(self):  # comentario
        order = Order.objects.create(  # comentario
            user=self.user,  # comentario
            delivery_address=None,  # comentario
            delivery_main_address='Av. Siempre Viva 123',  # comentario
            delivery_secondary_street='',  # comentario
            delivery_apartment='',  # comentario
            delivery_city='Quito',  # comentario
            delivery_latitude=Decimal('-0.205000'),  # comentario
            delivery_longitude=Decimal('-78.500000'),  # comentario
            delivery_instructions='',  # comentario
            status='confirmed',  # comentario
            total_amount=Decimal('0.00'),  # comentario
            total_items=0,  # comentario
        )  # comentario
        Shipment.objects.create(  # comentario
            order=order,  # comentario
            status='assigned',  # comentario
            current_latitude=Decimal('-0.210000'),  # comentario
            current_longitude=Decimal('-78.490000'),  # comentario
        )  # comentario

        resp = self.client.get(f'/orders/{order.id}/tracking/?include_map=1')  # comentario
        self.assertEqual(resp.status_code, 200, resp.data)  # comentario
        self.assertEqual(resp.data['map']['destination']['lat'], -0.205)  # comentario
        self.assertEqual(resp.data['map']['destination']['lng'], -78.5)  # comentario
        self.assertIsNone(resp.data['map']['geocode'])  # comentario


class ShipmentAssignDriverSerializerTests(TestCase):  # comentario
    def test_auto_assign_allows_driver_id_null(self):  # comentario
        s = ShipmentAssignDriverSerializer(data={'driver_id': None, 'auto_assign': True})  # comentario
        self.assertTrue(s.is_valid(), s.errors)  # comentario

    def test_auto_assign_rejects_driver_id_value(self):  # comentario
        driver = User.objects.create_user(username='driver1', email='driver1@example.com', password='password123')  # comentario
        s = ShipmentAssignDriverSerializer(data={'driver_id': driver.id, 'auto_assign': True})  # comentario
        self.assertTrue(s.is_valid(), s.errors)  # comentario
        self.assertNotIn('driver_id', s.validated_data)  # comentario


class OrderAssignDriverPermissionTests(TestCase):  # comentario
    def setUp(self):  # comentario
        self.client = APIClient()  # comentario
        self.owner = User.objects.create_user(  # comentario
            username='cliente2',  # comentario
            email='cliente2@example.com',  # comentario
            password='password123',  # comentario
        )  # comentario
        self.driver = User.objects.create_user(  # comentario
            username='driver2',  # comentario
            email='driver2@example.com',  # comentario
            password='password123',  # comentario
        )  # comentario
        group, _ = Group.objects.get_or_create(name='DRIVER')  # comentario
        self.driver.groups.add(group)  # comentario

        self.order = Order.objects.create(  # comentario
            user=self.owner,  # comentario
            delivery_address=None,  # comentario
            delivery_main_address='Av. Siempre Viva 222',  # comentario
            delivery_secondary_street='',  # comentario
            delivery_apartment='',  # comentario
            delivery_city='Quito',  # comentario
            delivery_instructions='',  # comentario
            status='pending',  # comentario
            total_amount=Decimal('0.00'),  # comentario
            total_items=0,  # comentario
        )  # comentario
        Shipment.objects.create(order=self.order, status='pending_assignment')  # comentario

    def test_owner_can_auto_assign(self):  # comentario
        self.client.force_authenticate(user=self.owner)  # comentario
        resp = self.client.post(  # comentario
            f'/orders/{self.order.id}/tracking/assign-driver/',  # comentario
            data={'auto_assign': True},  # comentario
            format='json',  # comentario
        )  # comentario
        self.assertEqual(resp.status_code, 200, resp.data)  # comentario
        self.assertEqual(resp.data.get('driver'), self.driver.id)  # comentario

    def test_owner_cannot_manual_assign(self):  # comentario
        self.client.force_authenticate(user=self.owner)  # comentario
        resp = self.client.post(  # comentario
            f'/orders/{self.order.id}/tracking/assign-driver/',  # comentario
            data={'driver_id': self.driver.id},  # comentario
            format='json',  # comentario
        )  # comentario
        self.assertEqual(resp.status_code, 403, resp.data)  # comentario
