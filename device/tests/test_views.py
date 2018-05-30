from uuid import uuid4

from django.core.files.uploadedfile import SimpleUploadedFile
from django.test import TransactionTestCase
from django.shortcuts import reverse
from rest_framework import status

from custom_auth.models import User
from device.models import Device, Version


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
        self.device = Device.objects.create(name='device', owner=self.device_owner)

    def test_allow_owner_to_see_device(self):
        self.client.force_login(self.device_owner)
        response = self.client.get(reverse('device', kwargs={'device_uuid': self.device.uuid}))

        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_not_owner_is_redirected_to_device_list_site(self):
        not_owner = User.objects.create_user(username='not_owner', password='password')

        self.client.force_login(not_owner)
        response = self.client.get(reverse('device', kwargs={'device_uuid': self.device.uuid}))

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
        new_name = 'new_name'

        self.client.force_login(not_owner)
        response = self.client.post(
            reverse('device', kwargs={'device_uuid': self.device.uuid}),
            {'name': new_name}
        )

        updated_device = Device.objects.get(pk=self.device.pk)

        self.assertEqual(updated_device.name, self.device.name)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_edit_as_owner_with_too_long_name(self):
        too_long_name = 'x' * 51

        self.client.force_login(self.device_owner)
        response = self.client.post(
            reverse('device', kwargs={'device_uuid': self.device.uuid}),
            {'name': too_long_name}
        )

        updated_device = Device.objects.get(pk=self.device.pk)

        self.assertEqual(updated_device.name, self.device.name)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_edit_as_owner_with_empty_string_name(self):
        too_long_name = ''

        self.client.force_login(self.device_owner)
        response = self.client.post(
            reverse('device', kwargs={'device_uuid': self.device.uuid}),
            {'name': too_long_name}
        )

        updated_device = Device.objects.get(pk=self.device.pk)

        self.assertEqual(updated_device.name, self.device.name)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_edit_as_owner_with_valid_name(self):
        new_name = 'new_name'

        self.client.force_login(self.device_owner)
        response = self.client.post(
            reverse('device', kwargs={'device_uuid': self.device.uuid}),
            {'name': new_name}
        )

        updated_device = Device.objects.get(pk=self.device.pk)

        self.assertEqual(updated_device.name, new_name)
        self.assertEqual(response.status_code, status.HTTP_200_OK)


class VersionTestCase(TransactionTestCase):
    def setUp(self):
        self.device_owner = User.objects.create_user(username='owner', password='password')
        self.device = Device.objects.create(name='device', owner=self.device_owner)
        self.version = Version.objects.create(name='version', versioned_object=self.device)
        self.device.version = self.version
        self.device.save()

    def test_list_versions_for_valid_device(self):
        self.client.force_login(self.device_owner)

        response = self.client.get(
            reverse('version_list', kwargs={'device_uuid': self.device.uuid})
        )

        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_list_versions_for_not_existing_device_uuid(self):
        self.client.force_login(self.device_owner)

        new_uuid = uuid4()

        response = self.client.get(
            reverse('version_list', kwargs={'device_uuid': str(new_uuid)})
        )

        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_list_versions_for_device_without_permissions(self):
        other_user = User.objects.create_user(username='user2', password='password')
        self.client.force_login(other_user)

        response = self.client.get(
            reverse('version_list', kwargs={'device_uuid': self.device.uuid})
        )

        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)


class CreateVersionTestCase(TransactionTestCase):
    def setUp(self):
        self.device_owner = User.objects.create_user(username='owner', password='password')
        self.device = Device.objects.create(name='device', owner=self.device_owner)

    def test_get_version_create_view_for_valid_device(self):
        self.client.force_login(self.device_owner)

        response = self.client.get(
            reverse('version_create', kwargs={'device_uuid': self.device.uuid})
        )

        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_get_version_create_view_for_not_existing_device_uuid(self):
        self.client.force_login(self.device_owner)

        new_uuid = uuid4()

        response = self.client.get(
            reverse('version_create', kwargs={'device_uuid': str(new_uuid)})
        )

        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_get_version_create_view_without_permissions(self):
        other_user = User.objects.create_user(username='user2', password='password')
        self.client.force_login(other_user)

        response = self.client.get(
            reverse('version_create', kwargs={'device_uuid': self.device.uuid})
        )

        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    # POST
    def test_post_without_version_file_and_name(self):
        self.client.force_login(self.device_owner)

        response = self.client.post(
            reverse('version_create', kwargs={'device_uuid': self.device.uuid}),
            data={}
        )

        device = Device.objects.get(pk=self.device.pk)

        self.assertIsNone(device.last_updated)
        self.assertIsNone(device.version)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_version_create_for_not_existing_device_uuid(self):
        self.client.force_login(self.device_owner)

        new_uuid = uuid4()
        version_name = 'version'
        version_file = SimpleUploadedFile('testfile.txt',
                                          b'example content')

        response = self.client.post(
            reverse('version_create', kwargs={'device_uuid': str(new_uuid)}),
            data={'name': version_name, 'file': version_file}
        )

        device = Device.objects.get(pk=self.device.pk)

        self.assertIsNone(device.last_updated)
        self.assertIsNone(device.version)
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_version_create_without_permissions(self):
        other_user = User.objects.create_user(username='user2', password='password')
        self.client.force_login(other_user)
        version_name = 'version'
        version_file = SimpleUploadedFile('testfile.txt',
                                          b'example content')

        response = self.client.post(
            reverse('version_create', kwargs={'device_uuid': self.device.uuid}),
            data={'name': version_name, 'file': version_file}
        )

        device = Device.objects.get(pk=self.device.pk)

        self.assertIsNone(device.last_updated)
        self.assertIsNone(device.version)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_post_with_valid_version_file_and_name(self):
        self.client.force_login(self.device_owner)
        version_name = 'version'
        version_file = SimpleUploadedFile('testfile.txt',
                                          b'example content')

        response = self.client.post(
            reverse('version_create', kwargs={'device_uuid': self.device.uuid}),
            data={'name': version_name, 'file': version_file}
        )

        device = Device.objects.get(pk=self.device.pk)

        self.assertRedirects(response,
                             reverse('device',
                                     kwargs={'device_uuid': self.device.uuid})
                             )
        self.assertIsNotNone(device.last_updated)
        self.assertIsNotNone(device.version)

    def test_post_with_existing_older_version(self):
        old_version_name = 'test'
        old_version = Version.objects.create(versioned_object=self.device,
                                             name=old_version_name)
        self.device.version = old_version
        self.device.save()

        self.client.force_login(self.device_owner)
        version_name = 'version'
        version_file = SimpleUploadedFile('testfile.txt',
                                          b'example content')

        response = self.client.post(
            reverse('version_create', kwargs={'device_uuid': self.device.uuid}),
            data={'name': version_name, 'file': version_file}
        )

        device = Device.objects.get(name=self.device.name)
        new_version = Version.objects.get(name=version_name)
        old_version = Version.objects.get(name=old_version_name)

        self.assertRedirects(response,
                             reverse('device',
                                     kwargs={'device_uuid': self.device.uuid})
                             )
        self.assertNotEqual(new_version.uuid, old_version.uuid)
        self.assertEqual(new_version.uuid, old_version.next.uuid)
        self.assertEqual(old_version.uuid, new_version.previous.uuid)
        self.assertIsNotNone(device.version)
