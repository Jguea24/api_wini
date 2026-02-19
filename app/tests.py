from django.contrib.auth.models import User
from django.test import TestCase

from app.models import RoleChangeRequest
from app.serializers import RegisterSerializer


class RegisterRoleFlowTests(TestCase):
    def test_register_assigns_cliente_group_by_default(self):
        serializer = RegisterSerializer(data={
            'email': 'cliente1@example.com',
            'phone': '0999999999',
            'password': 'password123',
            'password2': 'password123',
        })
        self.assertTrue(serializer.is_valid(), serializer.errors)
        user = serializer.save()

        self.assertTrue(user.groups.filter(name='CLIENTE').exists())
        self.assertFalse(RoleChangeRequest.objects.filter(user=user).exists())

    def test_register_driver_role_creates_pending_request(self):
        serializer = RegisterSerializer(data={
            'email': 'driver1@example.com',
            'phone': '0999999998',
            'password': 'password123',
            'password2': 'password123',
            'role': 'driver',
            'role_reason': 'Tengo moto propia',
        })
        self.assertTrue(serializer.is_valid(), serializer.errors)
        user = serializer.save()

        self.assertTrue(user.groups.filter(name='CLIENTE').exists())
        self.assertFalse(user.groups.filter(name='DRIVER').exists())

        request = RoleChangeRequest.objects.get(user=user)
        self.assertEqual(request.requested_role, 'driver')
        self.assertEqual(request.status, 'pending')
        self.assertEqual(request.reason, 'Tengo moto propia')

    def test_register_rejects_invalid_role(self):
        serializer = RegisterSerializer(data={
            'email': 'rolinvalido@example.com',
            'phone': '0999999997',
            'password': 'password123',
            'password2': 'password123',
            'role': 'admin',
        })
        self.assertFalse(serializer.is_valid())
        self.assertIn('role', serializer.errors)

    def test_approved_driver_request_adds_driver_group(self):
        user = User.objects.create_user(username='driverx', email='driverx@example.com', password='password123')
        role_request = RoleChangeRequest.objects.create(
            user=user,
            requested_role='driver',
            status='pending',
        )

        role_request.status = 'approved'
        role_request.save(update_fields=['status'])
        user.refresh_from_db()

        self.assertTrue(user.groups.filter(name='CLIENTE').exists())
        self.assertTrue(user.groups.filter(name='DRIVER').exists())

    def test_approved_provider_request_adds_provider_group(self):
        user = User.objects.create_user(username='providerx', email='providerx@example.com', password='password123')
        role_request = RoleChangeRequest.objects.create(
            user=user,
            requested_role='provider',
            status='pending',
        )

        role_request.status = 'approved'
        role_request.save(update_fields=['status'])
        user.refresh_from_db()

        self.assertTrue(user.groups.filter(name='CLIENTE').exists())
        self.assertTrue(user.groups.filter(name='PROVIDER').exists())
