from uuid import uuid4

from django.test import TestCase, TransactionTestCase
from django.shortcuts import reverse
from rest_framework import status

from custom_auth.models import User
from device.models import Device


class DeviceListTestCase(TestCase):
    def setUp(self):
        self.device_owner = User.objects.create_user(username='owner', password='password')


class DeviceCreateTestCase(TransactionTestCase):
    def setUp(self):
        self.device_owner = User.objects.create_user(username='owner', password='password')

    def test_create_device_with_valid_data_redirects_to_new_device_site(self):
        device_name = 'device'

        self.client.force_login(self.device_owner)
        response = self.client.post(reverse('device_create'), {'name': device_name})

        device = Device.objects.filter(name=device_name).first()

        self.assertIsNotNone(device)
        self.assertEqual(device.owner, self.device_owner)
        self.assertEqual(device.name, device_name)
        self.assertRedirects(response, reverse('device_list'))

    def test_create_device_with_empty_string_name(self):
        device_name = ''

        self.client.force_login(self.device_owner)
        response = self.client.post(reverse('device_create'), {'name': device_name})

        device = Device.objects.filter(name=device_name).first()

        self.assertIsNone(device)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)


class DeviceTestCase(TransactionTestCase):
    def setUp(self):
        self.device_owner = User.objects.create_user(username='owner', password='password')

    def test_allow_owner_to_see_device(self):
        device = Device.objects.create(name='device', owner=self.device_owner)

        self.client.force_login(self.device_owner)
        response = self.client.get(reverse('device', kwargs={'device_uuid': device.uuid}))

        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_not_owner_is_redirected_to_device_list_site(self):
        not_owner = User.objects.create_user(username='not_owner', password='password')
        device = Device.objects.create(name='device', owner=self.device_owner)

        self.client.force_login(not_owner)
        response = self.client.get(reverse('device', kwargs={'device_uuid': device.uuid}))

        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_not_existing_device_redirects_authenticated_user_to_404(self):
        not_existing_uuid = uuid4()

        self.client.force_login(self.device_owner)
        response = self.client.get(reverse('device', kwargs={'device_uuid': not_existing_uuid}))

        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_edit_not_existing_device_redirects_authenticated_user_to_404(self):
        not_existing_uuid = uuid4()
        new_name = 'new_name'

        self.client.force_login(self.device_owner)
        response = self.client.post(
            reverse('device', kwargs={'device_uuid': not_existing_uuid}),
            {'name': new_name}
        )

        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_edit_device_not_as_owner(self):
        not_owner = User.objects.create_user(username='not_owner', password='password')
        device = Device.objects.create(name='device', owner=self.device_owner)
        new_name = 'new_name'

        self.client.force_login(not_owner)
        response = self.client.post(
            reverse('device', kwargs={'device_uuid': device.uuid}),
            {'name': new_name}
        )

        updated_device = Device.objects.get(pk=device.pk)

        self.assertEqual(updated_device.name, device.name)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_edit_as_owner_with_too_long_name(self):
        device = Device.objects.create(name='device', owner=self.device_owner)
        too_long_name = 'x' * 51

        self.client.force_login(self.device_owner)
        response = self.client.post(
            reverse('device', kwargs={'device_uuid': device.uuid}),
            {'name': too_long_name}
        )

        updated_device = Device.objects.get(pk=device.pk)

        self.assertEqual(updated_device.name, device.name)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_edit_as_owner_with_empty_string_name(self):
        device = Device.objects.create(name='device', owner=self.device_owner)
        too_long_name = ''

        self.client.force_login(self.device_owner)
        response = self.client.post(
            reverse('device', kwargs={'device_uuid': device.uuid}),
            {'name': too_long_name}
        )

        updated_device = Device.objects.get(pk=device.pk)

        self.assertEqual(updated_device.name, device.name)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_edit_as_owner_with_valid_name(self):
        device = Device.objects.create(name='device', owner=self.device_owner)
        new_name = 'new_name'

        self.client.force_login(self.device_owner)
        response = self.client.post(
            reverse('device', kwargs={'device_uuid': device.uuid}),
            {'name': new_name}
        )

        updated_device = Device.objects.get(pk=device.pk)

        self.assertEqual(updated_device.name, new_name)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
