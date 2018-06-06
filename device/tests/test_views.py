from uuid import uuid4

from django.core.files.uploadedfile import SimpleUploadedFile
from django.test import TransactionTestCase
from django.shortcuts import reverse

from projektPZ import status

from custom_auth.models import User

from device.models import Device, Version, DeviceGroup


class DeviceCreateTestCase(TransactionTestCase):
    def setUp(self):
        self.device_owner = User.objects.create_user(username='owner',
                                                     password='password')

        self.client.force_login(self.device_owner)

    def test_create_device_with_valid_data_redirects_to_new_device_site(self):
        device_name = 'device'
        ip_address = '192.168.1.1'

        request_data = {
            'name': device_name,
            'ip_address': ip_address
        }
        response = self.client.post(reverse('device_create'), request_data)

        device = Device.objects.filter(name=device_name).first()

        self.assertIsNotNone(device)
        self.assertEqual(device.owner, self.device_owner)
        self.assertEqual(device.name, device_name)
        self.assertRedirects(response, reverse('device_list'))

    def test_create_device_with_empty_string_name(self):
        device_name = ''
        ip_address = '192.168.1.1'

        request_data = {
            'name': device_name,
            'ip_address': ip_address
        }
        response = self.client.post(reverse('device_create'), request_data)

        device = Device.objects.filter(name=device_name).first()

        self.assertIsNone(device)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_create_device_with_empty_ip_address(self):
        device_name = 'device'
        ip_address = ''

        request_data = {
            'name': device_name,
            'ip_address': ip_address
        }
        response = self.client.post(reverse('device_create'), request_data)

        device = Device.objects.filter(name=device_name).first()

        self.assertIsNone(device)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)


class DeviceTestCase(TransactionTestCase):
    def setUp(self):
        self.device_owner = User.objects.create_user(username='owner',
                                                     password='password')

        self.device = Device.objects.create(name='device',
                                            owner=self.device_owner,
                                            ip_address='192.168.1.1')

    def test_allow_owner_to_see_device(self):
        self.client.force_login(self.device_owner)
        response = self.client.get(reverse('device_details', kwargs={'device_uuid': self.device.uuid}))

        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_not_owner_is_redirected_to_device_list_site(self):
        not_owner = User.objects.create_user(username='not_owner', password='password')

        self.client.force_login(not_owner)
        response = self.client.get(reverse('device_details', kwargs={'device_uuid': self.device.uuid}))

        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_not_existing_device_redirects_authenticated_user_to_404(self):
        not_existing_uuid = uuid4()

        self.client.force_login(self.device_owner)
        response = self.client.get(reverse('device_details', kwargs={'device_uuid': not_existing_uuid}))

        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_inactive_device_redirects_authenticated_user_to_404(self):
        self.client.force_login(self.device_owner)

        self.device.is_active = False
        self.device.save()

        response = self.client.get(reverse('device_details', kwargs={'device_uuid': self.device.uuid}))

        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_edit_not_existing_device_redirects_authenticated_user_to_404(self):
        not_existing_uuid = uuid4()
        new_name = 'new_name'

        self.client.force_login(self.device_owner)

        request_data = {
            'name': new_name,
            'ip_address': self.device.ip_address
        }
        response = self.client.post(
            reverse('device_details', kwargs={'device_uuid': not_existing_uuid}),
            request_data
        )

        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_edit_device_not_as_owner(self):
        not_owner = User.objects.create_user(username='not_owner', password='password')
        new_name = 'new_name'

        self.client.force_login(not_owner)

        request_data = {
            'name': new_name,
            'ip_address': self.device.ip_address
        }
        response = self.client.post(
            reverse('device_details', kwargs={'device_uuid': self.device.uuid}),
            request_data
        )

        updated_device = Device.objects.get(pk=self.device.pk)

        self.assertEqual(updated_device.name, self.device.name)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_edit_as_owner_with_too_long_name(self):
        new_name = 'x' * 51

        self.client.force_login(self.device_owner)

        request_data = {
            'name': new_name,
            'ip_address': self.device.ip_address
        }
        response = self.client.post(
            reverse('device_details', kwargs={'device_uuid': self.device.uuid}),
            request_data
        )

        updated_device = Device.objects.get(pk=self.device.pk)

        self.assertEqual(updated_device.name, self.device.name)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_edit_as_owner_with_empty_string_name(self):
        new_name = ''

        self.client.force_login(self.device_owner)

        request_data = {
            'name': new_name,
            'ip_address': self.device.ip_address
        }
        response = self.client.post(
            reverse('device_details', kwargs={'device_uuid': self.device.uuid}),
            request_data
        )

        updated_device = Device.objects.get(pk=self.device.pk)

        self.assertEqual(updated_device.name, self.device.name)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_edit_ip_addess_with_new_ip_address(self):
        new_ip_address = '8.8.8.8'

        self.client.force_login(self.device_owner)

        request_data = {
            'name': self.device.name,
            'ip_address': new_ip_address,
            'is_active': True
        }
        response = self.client.post(
            reverse('device_details', kwargs={'device_uuid': self.device.uuid}),
            request_data
        )

        updated_device = Device.objects.get(pk=self.device.pk)

        self.assertEqual(updated_device.ip_address, self.device.ip_address)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_edit_as_owner_with_valid_name(self):
        new_name = 'new_name'

        self.client.force_login(self.device_owner)

        request_data = {
            'name': new_name,
            'ip_address': self.device.ip_address,
            'is_active': True
        }
        response = self.client.post(
            reverse('device_details', kwargs={'device_uuid': self.device.uuid}),
            request_data
        )

        updated_device = Device.objects.get(pk=self.device.pk)

        self.assertEqual(updated_device.name, new_name)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_delete_device(self):
        self.client.force_login(self.device_owner)

        response = self.client.post(
            reverse('device_delete', kwargs={'device_uuid': self.device.uuid})
        )

        updated_device = Device.objects.get(pk=self.device.pk)

        self.assertFalse(updated_device.is_active)
        self.assertRedirects(response, reverse('device_list'))

    def test_delete_not_existing_device(self):
        not_existing_device_uuid = uuid4()
        self.client.force_login(self.device_owner)

        response = self.client.post(
            reverse('device_delete', kwargs={'device_uuid': not_existing_device_uuid})
        )

        device = Device.objects.get(pk=self.device.pk)

        self.assertTrue(device.is_active)
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_delete_not_owned_device(self):
        not_owner = User.objects.create_user(username='not_owner', password='password')
        self.client.force_login(not_owner)

        response = self.client.post(
            reverse('device_delete', kwargs={'device_uuid': self.device.uuid})
        )

        device = Device.objects.get(pk=self.device.pk)

        self.assertTrue(device.is_active)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)


class DeviceVersionTestCase(TransactionTestCase):
    def setUp(self):
        self.device_owner = User.objects.create_user(username='owner',
                                                     password='password')

        self.device = Device.objects.create(name='device',
                                            owner=self.device_owner,
                                            ip_address='192.168.1.1')

        self.version = Version.objects.create(name='version',
                                              versioned_object=self.device)

        self.device.version = self.version
        self.device.save()

    def test_list_versions_for_valid_device(self):
        self.client.force_login(self.device_owner)

        response = self.client.get(
            reverse('device_version_list', kwargs={'device_uuid': self.device.uuid})
        )

        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_list_versions_for_not_existing_device_uuid(self):
        self.client.force_login(self.device_owner)

        new_uuid = uuid4()

        response = self.client.get(
            reverse('device_version_list', kwargs={'device_uuid': str(new_uuid)})
        )

        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_list_versions_for_device_without_permissions(self):
        other_user = User.objects.create_user(username='user2', password='password')
        self.client.force_login(other_user)

        response = self.client.get(
            reverse('device_version_list', kwargs={'device_uuid': self.device.uuid})
        )

        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)


class CreateDeviceVersionTestCase(TransactionTestCase):
    def setUp(self):
        self.device_owner = User.objects.create_user(username='owner',
                                                     password='password')

        self.device = Device.objects.create(name='device',
                                            owner=self.device_owner,
                                            ip_address='192.168.1.1')

    def test_get_version_create_view_for_valid_device(self):
        self.client.force_login(self.device_owner)

        response = self.client.get(
            reverse('device_version_create', kwargs={'device_uuid': self.device.uuid})
        )

        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_get_version_create_view_for_not_existing_device_uuid(self):
        self.client.force_login(self.device_owner)

        new_uuid = uuid4()

        response = self.client.get(
            reverse('device_version_create', kwargs={'device_uuid': str(new_uuid)})
        )

        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_get_version_create_view_without_permissions(self):
        other_user = User.objects.create_user(username='user2', password='password')
        self.client.force_login(other_user)

        response = self.client.get(
            reverse('device_version_create', kwargs={'device_uuid': self.device.uuid})
        )

        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    # POST
    def test_post_without_version_file_and_name(self):
        self.client.force_login(self.device_owner)

        response = self.client.post(
            reverse('device_version_create', kwargs={'device_uuid': self.device.uuid}),
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
            reverse('device_version_create', kwargs={'device_uuid': str(new_uuid)}),
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
            reverse('device_version_create', kwargs={'device_uuid': self.device.uuid}),
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
            reverse('device_version_create', kwargs={'device_uuid': self.device.uuid}),
            data={'name': version_name, 'file': version_file}
        )

        version_created = Version.objects.filter(name=version_name).first()

        self.assertRedirects(response,
                             reverse('device_version_list',
                                     kwargs={'device_uuid': self.device.uuid})
                             )
        self.assertIsNotNone(version_created)
        self.assertEqual(version_created.versioned_object.id, self.device.id)

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
            reverse('device_version_create', kwargs={'device_uuid': self.device.uuid}),
            data={'name': version_name, 'file': version_file}
        )

        device = Device.objects.get(name=self.device.name)
        new_version = Version.objects.get(name=version_name)
        old_version = Version.objects.get(name=old_version_name)

        self.assertRedirects(response,
                             reverse('device_version_list',
                                     kwargs={'device_uuid': self.device.uuid})
                             )
        self.assertNotEqual(new_version.uuid, old_version.uuid)
        self.assertEqual(new_version.uuid, old_version.next.uuid)
        self.assertEqual(old_version.uuid, new_version.previous.uuid)
        self.assertIsNotNone(device.version)


class DeviceGroupTestCase(TransactionTestCase):
    def setUp(self):
        self.owner = User.objects.create_user(username='owner',
                                              password='password')

        self.device = Device.objects.create(name='device',
                                            owner=self.owner,
                                            ip_address='192.168.1.1')

        self.device_group = DeviceGroup.objects.create(name='device_group',
                                                       owner=self.owner)

    def test_get_group_details_as_owner(self):
        self.client.force_login(self.owner)
        response = self.client.get(
            reverse('group_details', kwargs={'group_uuid': self.device_group.uuid})
        )

        updated_device_group = DeviceGroup.objects.get(uuid=self.device_group.uuid)

        self.assertEqual(updated_device_group.name, self.device_group.name)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_get_group_details_for_not_existing_group(self):
        device_group_uuid = uuid4()

        self.client.force_login(self.owner)
        response = self.client.get(
            reverse('group_details', kwargs={'group_uuid': device_group_uuid})
        )

        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_edit_group_with_too_long_name(self):
        new_group_name = 'x' * 100

        self.client.force_login(self.owner)
        response = self.client.post(
            reverse('group_details', kwargs={'group_uuid': self.device_group.uuid}),
            data={'name': new_group_name}
        )

        updated_device_group = DeviceGroup.objects.get(uuid=self.device_group.uuid)

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(updated_device_group.name, self.device_group.name)

    def test_edit_group_with_empty_name(self):
        new_group_name = ''

        self.client.force_login(self.owner)
        response = self.client.post(
            reverse('group_details', kwargs={'group_uuid': self.device_group.uuid}),
            data={'name': new_group_name}
        )

        updated_device_group = DeviceGroup.objects.get(uuid=self.device_group.uuid)

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(updated_device_group.name, self.device_group.name)

    def test_edit_group_with_valid_new_name(self):
        new_group_name = 'new'

        self.client.force_login(self.owner)
        response = self.client.post(
            reverse('group_details', kwargs={'group_uuid': self.device_group.uuid}),
            data={'name': new_group_name}
        )

        updated_device_group = DeviceGroup.objects.get(uuid=self.device_group.uuid)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(updated_device_group.name, new_group_name)

    def test_get_group_details_not_as_owner(self):
        not_owner = User.objects.create(username='user', password='password')

        self.client.force_login(not_owner)
        response = self.client.get(
            reverse('group_details', kwargs={'group_uuid': self.device_group.uuid})
        )

        updated_device_group = DeviceGroup.objects.get(uuid=self.device_group.uuid)

        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        self.assertEqual(updated_device_group.name, self.device_group.name)

    def test_edit_group_details_not_as_owner(self):
        new_group_name = 'new'
        not_owner = User.objects.create(username='user', password='password')

        self.client.force_login(not_owner)
        response = self.client.post(
            reverse('group_details', kwargs={'group_uuid': self.device_group.uuid}),
            data={'name': new_group_name}
        )

        updated_device_group = DeviceGroup.objects.get(uuid=self.device_group.uuid)

        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        self.assertEqual(updated_device_group.name, self.device_group.name)


class DeviceGroupDeleteTestCase(TransactionTestCase):
    def setUp(self):
        self.owner = User.objects.create_user(username='owner',
                                              password='password')

        self.device = Device.objects.create(name='device',
                                            owner=self.owner,
                                            ip_address='192.168.1.1')

        self.device_group = DeviceGroup.objects.create(name='device_group',
                                                       owner=self.owner)

    def test_delete_group_as_owner(self):
        self.client.force_login(self.owner)
        response = self.client.post(
            reverse('group_delete', kwargs={'group_uuid': self.device_group.uuid})
        )

        updated_device_group = DeviceGroup.objects.get(uuid=self.device_group.uuid)

        self.assertEqual(updated_device_group.is_active, False)
        self.assertRedirects(response, reverse('group_list'))

    def test_delete_group_not_as_owner(self):
        not_owner = User.objects.create(username='user', password='password')

        self.client.force_login(not_owner)
        response = self.client.post(
            reverse('group_delete', kwargs={'group_uuid': self.device_group.uuid})
        )

        updated_device_group = DeviceGroup.objects.get(uuid=self.device_group.uuid)

        self.assertEqual(updated_device_group.is_active, True)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_delete_not_existing_group(self):
        group_uuid = uuid4()

        self.client.force_login(self.owner)
        response = self.client.post(
            reverse('group_delete', kwargs={'group_uuid': group_uuid})
        )

        updated_device_group = DeviceGroup.objects.get(uuid=self.device_group.uuid)

        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
        self.assertEqual(updated_device_group.is_active, True)


class DeviceGroupCreateTestCase(TransactionTestCase):
    def setUp(self):
        self.owner = User.objects.create_user(username='owner',
                                              password='password')

        self.device = Device.objects.create(name='device',
                                            owner=self.owner,
                                            ip_address='192.168.1.1')

    def test_create_group_with_valid_name(self):
        new_group_name = 'new'

        self.client.force_login(self.owner)
        response = self.client.post(reverse('group_create'),
                                    data={'name': new_group_name})

        new_device_group = DeviceGroup.objects.get(owner=self.owner)

        self.assertRedirects(response, reverse('group_list'))
        self.assertEqual(new_device_group.name, new_group_name)
        self.assertEqual(new_device_group.is_active, True)

    def test_create_group_with_too_long_name(self):
        new_group_name = 'x' * 100

        self.client.force_login(self.owner)
        response = self.client.post(reverse('group_create'),
                                    data={'name': new_group_name})

        new_device_group = DeviceGroup.objects.filter(owner=self.owner).first()

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIsNone(new_device_group)


class DeviceGroupAvailableDeviceTestCase(TransactionTestCase):
    def setUp(self):
        self.owner = User.objects.create_user(username='owner',
                                              password='password')

        self.device = Device.objects.create(name='device',
                                            owner=self.owner,
                                            ip_address='192.168.1.1')

        self.device_group = DeviceGroup.objects.create(name='device_group',
                                                       owner=self.owner)

    def test_get_group_details_as_owner(self):
        self.client.force_login(self.owner)
        response = self.client.get(
            reverse('group_available', kwargs={'group_uuid': self.device_group.uuid})
        )

        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_get_group_details_not_as_owner(self):
        not_owner = User.objects.create(username='user', password='password')

        self.client.force_login(not_owner)
        response = self.client.get(
            reverse('group_available', kwargs={'group_uuid': self.device_group.uuid})
        )

        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_get_group_details_for_not_existing_group(self):
        new_uuid = uuid4()

        self.client.force_login(self.owner)
        response = self.client.get(
            reverse('group_available', kwargs={'group_uuid': new_uuid})
        )

        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)


class DeviceGroupAddedDeviceTestCase(TransactionTestCase):
    def setUp(self):
        self.owner = User.objects.create_user(username='owner',
                                              password='password')

        self.device = Device.objects.create(name='device',
                                            owner=self.owner,
                                            ip_address='192.168.1.1')

        self.device_group = DeviceGroup.objects.create(name='device_group',
                                                       owner=self.owner)

    def test_get_group_details_as_owner(self):
        self.client.force_login(self.owner)
        response = self.client.get(
            reverse('group_added', kwargs={'group_uuid': self.device_group.uuid})
        )

        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_get_group_details_not_as_owner(self):
        not_owner = User.objects.create(username='user', password='password')

        self.client.force_login(not_owner)
        response = self.client.get(
            reverse('group_added', kwargs={'group_uuid': self.device_group.uuid})
        )

        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_get_group_details_for_not_existing_group(self):
        new_uuid = uuid4()

        self.client.force_login(self.owner)
        response = self.client.get(
            reverse('group_added', kwargs={'group_uuid': new_uuid})
        )

        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)


class DeviceGroupRemoveDeviceTestCase(TransactionTestCase):
    def setUp(self):
        self.owner = User.objects.create_user(username='owner',
                                              password='password')

        self.device = Device.objects.create(name='device',
                                            owner=self.owner,
                                            ip_address='192.168.1.1')

        self.device_group = DeviceGroup.objects.create(name='device_group',
                                                       owner=self.owner)

        self.device_group.devices.add(self.device)
        self.device_group.save()

    def test_remove_device_as_owner(self):
        self.client.force_login(self.owner)
        response = self.client.post(
            reverse('group_remove', kwargs={'group_uuid': self.device_group.uuid}),
            data={'device_uuid': self.device.uuid}
        )

        device = Device.objects.filter(groups__uuid=self.device_group.uuid).first()

        self.assertRedirects(response,
                             reverse('group_added',
                                     kwargs={'group_uuid': self.device_group.uuid})
                             )
        self.assertIsNone(device)

    def test_remove_device_not_as_owner(self):
        not_owner = User.objects.create_user(username='user', password='password')

        self.client.force_login(not_owner)
        response = self.client.post(
            reverse('group_remove', kwargs={'group_uuid': self.device_group.uuid}),
            data={'device_uuid': self.device.uuid}
        )

        device = Device.objects.filter(groups__uuid=self.device_group.uuid).first()

        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        self.assertIsNotNone(device)

    def test_remove_device_for_not_existing_group(self):
        new_uuid = uuid4()

        self.client.force_login(self.owner)
        response = self.client.post(
            reverse('group_remove', kwargs={'group_uuid': new_uuid}),
            data={'device_uuid': self.device.uuid}
        )

        device = Device.objects.filter(groups__uuid=self.device_group.uuid).first()

        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
        self.assertIsNotNone(device)

    def test_add_not_existing_device(self):
        new_uuid = uuid4()

        self.client.force_login(self.owner)
        response = self.client.post(
            reverse('group_remove', kwargs={'group_uuid': self.device_group.uuid}),
            data={'device_uuid': new_uuid}
        )

        device = Device.objects.filter(groups__uuid=self.device_group.uuid).first()

        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
        self.assertIsNotNone(device)

    def test_add_not_owned_device(self):
        not_owner = User.objects.create_user(username='user', password='password')
        not_owned_device = Device.objects.create(name='not_owned',
                                                 owner=not_owner,
                                                 ip_address='192.168.1.1')

        self.client.force_login(self.owner)
        response = self.client.post(
            reverse('group_remove', kwargs={'group_uuid': self.device_group.uuid}),
            data={'device_uuid': not_owned_device.uuid}
        )

        device = Device.objects.filter(groups__uuid=self.device_group.uuid).first()

        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        self.assertIsNotNone(device)

    def test_add_with_invalid_form_data(self):
        self.client.force_login(self.owner)
        response = self.client.post(
            reverse('group_remove', kwargs={'group_uuid': self.device_group.uuid})
        )

        device = Device.objects.filter(groups__uuid=self.device_group.uuid).first()

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIsNotNone(device)


class DeviceGroupAddDeviceTestCase(TransactionTestCase):
    def setUp(self):
        self.owner = User.objects.create_user(username='owner',
                                              password='password')

        self.device = Device.objects.create(name='device',
                                            owner=self.owner,
                                            ip_address='192.168.1.1')

        self.device_group = DeviceGroup.objects.create(name='device_group',
                                                       owner=self.owner)

    def test_add_device_as_owner(self):
        self.client.force_login(self.owner)
        response = self.client.post(
            reverse('group_add', kwargs={'group_uuid': self.device_group.uuid}),
            data={'device_uuid': self.device.uuid}
        )

        device = Device.objects.filter(groups__uuid=self.device_group.uuid).first()

        self.assertRedirects(response,
                             reverse('group_added',
                                     kwargs={'group_uuid': self.device_group.uuid})
                             )
        self.assertIsNotNone(device)

    def test_remove_device_not_as_owner(self):
        not_owner = User.objects.create_user(username='user', password='password')

        self.client.force_login(not_owner)
        response = self.client.post(
            reverse('group_add', kwargs={'group_uuid': self.device_group.uuid}),
            data={'device_uuid': self.device.uuid}
        )

        device = Device.objects.filter(groups__uuid=self.device_group.uuid).first()

        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        self.assertIsNone(device)

    def test_remove_device_for_not_existing_group(self):
        new_uuid = uuid4()

        self.client.force_login(self.owner)
        response = self.client.post(
            reverse('group_add', kwargs={'group_uuid': new_uuid}),
            data={'device_uuid': self.device.uuid}
        )

        device = Device.objects.filter(groups__uuid=self.device_group.uuid).first()

        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
        self.assertIsNone(device)

    def test_add_not_existing_device(self):
        new_uuid = uuid4()

        self.client.force_login(self.owner)
        response = self.client.post(
            reverse('group_add', kwargs={'group_uuid': self.device_group.uuid}),
            data={'device_uuid': new_uuid}
        )

        device = Device.objects.filter(groups__uuid=self.device_group.uuid).first()

        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
        self.assertIsNone(device)

    def test_add_not_owned_device(self):
        not_owner = User.objects.create_user(username='user', password='password')
        not_owned_device = Device.objects.create(name='not_owned',
                                                 owner=not_owner,
                                                 ip_address='192.168.1.1')

        self.client.force_login(self.owner)
        response = self.client.post(
            reverse('group_add', kwargs={'group_uuid': self.device_group.uuid}),
            data={'device_uuid': not_owned_device.uuid}
        )

        device = Device.objects.filter(groups__uuid=self.device_group.uuid).first()

        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        self.assertIsNone(device)

    def test_add_with_invalid_form_data(self):
        self.client.force_login(self.owner)
        response = self.client.post(
            reverse('group_add', kwargs={'group_uuid': self.device_group.uuid})
        )

        device = Device.objects.filter(groups__uuid=self.device_group.uuid).first()

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIsNone(device)


class GroupVersionTestCase(TransactionTestCase):
    def setUp(self):
        self.owner = User.objects.create_user(username='owner',
                                              password='password')

        self.device_group = DeviceGroup.objects.create(name='device_group',
                                                       owner=self.owner)

        self.version = Version.objects.create(name='version',
                                              versioned_object=self.device_group)

        self.device_group.version = self.version
        self.device_group.save()

    def test_list_versions_for_valid_device(self):
        self.client.force_login(self.owner)

        response = self.client.get(
            reverse('group_version_list',
                    kwargs={'group_uuid': self.device_group.uuid})
        )

        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_list_versions_for_not_existing_device_uuid(self):
        self.client.force_login(self.owner)

        new_uuid = uuid4()

        response = self.client.get(
            reverse('group_version_list',
                    kwargs={'group_uuid': new_uuid})
        )

        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_list_versions_for_device_without_permissions(self):
        other_user = User.objects.create_user(username='user2', password='password')
        self.client.force_login(other_user)

        response = self.client.get(
            reverse('group_version_list',
                    kwargs={'group_uuid': self.device_group.uuid})
        )

        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)


class CreateGroupVersionTestCase(TransactionTestCase):
    def setUp(self):
        self.owner = User.objects.create_user(username='owner',
                                              password='password')

        self.device_group = DeviceGroup.objects.create(name='device_group',
                                                       owner=self.owner)

    def test_get_version_create_view_for_valid_device(self):
        self.client.force_login(self.owner)

        response = self.client.get(
            reverse('group_version_create',
                    kwargs={'group_uuid': self.device_group.uuid})
        )

        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_get_version_create_view_for_not_existing_device_uuid(self):
        self.client.force_login(self.owner)

        new_uuid = uuid4()

        response = self.client.get(
            reverse('group_version_create',
                    kwargs={'group_uuid': new_uuid})
        )

        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_get_version_create_view_without_permissions(self):
        other_user = User.objects.create_user(username='user2', password='password')
        self.client.force_login(other_user)

        response = self.client.get(
            reverse('group_version_create',
                    kwargs={'group_uuid': self.device_group.uuid})
        )

        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    # POST
    def test_post_without_version_file_and_name(self):
        self.client.force_login(self.owner)

        response = self.client.post(
            reverse('group_version_create',
                    kwargs={'group_uuid': self.device_group.uuid}),
            data={}
        )

        device_group = DeviceGroup.objects.get(pk=self.device_group.pk)

        self.assertIsNone(device_group.last_updated)
        self.assertIsNone(device_group.version)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_version_create_for_not_existing_device_uuid(self):
        self.client.force_login(self.owner)

        new_uuid = uuid4()
        version_name = 'version'
        version_file = SimpleUploadedFile('testfile.txt',
                                          b'example content')

        response = self.client.post(
            reverse('group_version_create',
                    kwargs={'group_uuid': new_uuid}),
            data={'name': version_name, 'file': version_file}
        )

        device_group = DeviceGroup.objects.get(pk=self.device_group.pk)

        self.assertIsNone(device_group.last_updated)
        self.assertIsNone(device_group.version)
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_version_create_without_permissions(self):
        other_user = User.objects.create_user(username='user2', password='password')
        self.client.force_login(other_user)
        version_name = 'version'
        version_file = SimpleUploadedFile('testfile.txt',
                                          b'example content')

        response = self.client.post(
            reverse('group_version_create',
                    kwargs={'group_uuid': self.device_group.uuid}),
            data={'name': version_name, 'file': version_file}
        )

        device_group = DeviceGroup.objects.get(pk=self.device_group.pk)

        self.assertIsNone(device_group.last_updated)
        self.assertIsNone(device_group.version)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_post_with_valid_version_file_and_name(self):
        self.client.force_login(self.owner)
        version_name = 'version'
        version_file = SimpleUploadedFile('testfile.txt',
                                          b'example content')

        response = self.client.post(
            reverse('group_version_create',
                    kwargs={'group_uuid': self.device_group.uuid}),
            data={'name': version_name, 'file': version_file}
        )

        version_created = Version.objects.filter(name=version_name).first()

        self.assertRedirects(response,
                             reverse('group_version_list',
                                     kwargs={'group_uuid': self.device_group.uuid})
                             )
        self.assertIsNotNone(version_created)
        self.assertEqual(version_created.versioned_object.id,
                         self.device_group.id)

    def test_post_with_existing_older_version(self):
        old_version_name = 'test'
        old_version = Version.objects.create(versioned_object=self.device_group,
                                             name=old_version_name)
        self.device_group.version = old_version
        self.device_group.save()

        self.client.force_login(self.owner)
        version_name = 'version'
        version_file = SimpleUploadedFile('testfile.txt',
                                          b'example content')

        response = self.client.post(
            reverse('group_version_create',
                    kwargs={'group_uuid': self.device_group.uuid}),
            data={'name': version_name, 'file': version_file}
        )

        device_group = DeviceGroup.objects.get(name=self.device_group.name)
        new_version = Version.objects.get(name=version_name)
        old_version = Version.objects.get(name=old_version_name)

        self.assertRedirects(response,
                             reverse('group_version_list',
                                     kwargs={'group_uuid': self.device_group.uuid})
                             )
        self.assertNotEqual(new_version.uuid, old_version.uuid)
        self.assertEqual(new_version.uuid, old_version.next.uuid)
        self.assertEqual(old_version.uuid, new_version.previous.uuid)
        self.assertIsNotNone(device_group.version)
