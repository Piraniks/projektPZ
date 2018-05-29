from django.test import TransactionTestCase

from custom_auth.models import User
from device.models import Device, Version


class DeviceTestCase(TransactionTestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='user',
                                             password='password')
        self.device = Device.objects.create()

    def test_is_up_to_date_with_none_version(self):
        pass