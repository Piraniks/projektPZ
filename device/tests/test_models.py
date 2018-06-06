from django.test import TransactionTestCase

from custom_auth.models import User
from device.models import Device, Version, DeviceGroup


class DeviceTestCase(TransactionTestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='user',
                                             password='password')
        self.device = Device.objects.create(name='device',
                                            owner=self.user,
                                            ip_address='192.168.1.1')

    def test_is_up_to_date_with_none_version(self):
        is_up_to_date = self.device.is_up_to_date

        self.assertTrue(is_up_to_date)

    def test_is_up_to_date_with_newest_version(self):
        new_version = Version.objects.create(versioned_object=self.device,
                                             name='new_version')
        self.device.version = new_version
        self.device.save()

        is_up_to_date = self.device.is_up_to_date

        self.assertTrue(is_up_to_date)

    def test_is_up_to_date_with_old_version(self):
        new_version = Version.objects.create(versioned_object=self.device,
                                             name='new_version')
        old_version = Version.objects.create(versioned_object=self.device,
                                             name='new_version')

        new_version.previous = old_version
        old_version.next = new_version
        new_version.save()
        old_version.save()

        self.device.version = old_version
        self.device.save()

        is_up_to_date = self.device.is_up_to_date

        self.assertFalse(is_up_to_date)

    def test_raise_version_with_none_as_latest(self):
        result = self.device.raise_version()

        self.assertFalse(result)

    def test_raise_version_with_latest_version_already(self):
        new_version = Version.objects.create(versioned_object=self.device,
                                             name='new_version')
        self.device.version = new_version
        self.device.save()

        result = self.device.raise_version()

        self.assertFalse(result)

    def test_raise_version_with_version_raising(self):
        new_version = Version.objects.create(versioned_object=self.device,
                                             name='new_version')
        old_version = Version.objects.create(versioned_object=self.device,
                                             name='new_version')

        new_version.previous = old_version
        old_version.next = new_version
        new_version.save()
        old_version.save()

        self.device.version = old_version
        self.device.save()

        result = self.device.raise_version()

        self.assertTrue(result)


class DeviceGroupTestCase(TransactionTestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='user',
                                             password='password')

        self.device_group = DeviceGroup.objects.create(name='device_group',
                                                       owner=self.user)

    def test_if_versions_for_devices_in_group_is_not_created_needlessly(self):
        device = Device.objects.create(name='device',
                                       owner=self.user,
                                       ip_address='192.168.1.1')

        self.device_group.devices.add(device)
        self.device_group.save()

        device_after_save = Device.objects.get(pk=device.pk)

        self.assertIsNone(device_after_save.version)


    def test_add_group_version_creates_device_versions(self):
        device = Device.objects.create(name='device',
                                       owner=self.user,
                                       ip_address='192.168.1.1')

        self.device_group.devices.add(device)
        self.device_group.save()

        new_version = Version.objects.create(versioned_object=self.device_group,
                                             name='new_version')

        self.device_group.version = new_version
        self.device_group.save()

        device_after_save = Device.objects.get(pk=device.pk)

        self.assertIsNotNone(device_after_save.version)
        self.assertEqual(device_after_save.version.name, new_version.name)
        self.assertEqual(device_after_save.version.file_checksum,
                         new_version.file_checksum)
