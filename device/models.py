import uuid

from django.db import models
from django.contrib.auth import get_user_model
from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.models import ContentType
from django.utils import timezone

from device.utils import (checksum, uploaded_file_path,
                          update_device, update_device_group)


User = get_user_model()


class Version(models.Model):
    uuid = models.UUIDField(default=uuid.uuid4, unique=True)
    name = models.CharField(max_length=50)
    timestamp = models.DateTimeField(auto_now_add=True)

    content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE,
                                     null=True)
    object_id = models.PositiveIntegerField(null=True)
    versioned_object = GenericForeignKey('content_type', 'object_id')

    file = models.FileField(null=True, upload_to=uploaded_file_path)
    file_checksum = models.BinaryField(blank=True)

    creator = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)

    previous = models.ForeignKey('self', on_delete=models.SET_NULL,
                                 null=True, blank=True, related_name='+')
    next = models.ForeignKey('self', on_delete=models.SET_NULL,
                             null=True, blank=True, related_name='+')

    class Meta:
        ordering = ['-id']
        get_latest_by = 'timestamp'

    def __str__(self):
        return self.name

    def generate_checksum(self):
        file_checksum = checksum(self.file.file.name).digest()
        self.file_checksum = file_checksum
        self.save()
        return self.file_checksum


class Device(models.Model):
    uuid = models.UUIDField(default=uuid.uuid4, unique=True)
    name = models.CharField(max_length=50)
    is_active = models.BooleanField(default=True)
    timestamp = models.DateTimeField(auto_now_add=True)
    last_edited = models.DateTimeField(auto_now=True)
    ip_address = models.GenericIPAddressField()

    last_updated = models.DateTimeField(null=True, blank=True)
    version = models.OneToOneField(Version, on_delete=models.SET_NULL,
                                   related_name='devices',
                                   null=True, blank=True)

    owner = models.ForeignKey(User, on_delete=models.SET_NULL,
                              related_name='devices', null=True)

    class Meta:
        ordering = ['-id']
        get_latest_by = 'timestamp'

    def __str__(self):
        return self.name

    @property
    def is_up_to_date(self):
        version = self.version
        if version is None:
            return True

        if version.next is None or version.uuid == version.next.uuid:
            return True

        return False

    def raise_version(self):
        if self.is_up_to_date:
            return False

        next_version = self.version.next
        if next_version is None:
            return None

        self.version = next_version
        self.last_updated = timezone.now()
        self.save()

        return True

    def save(self, *args, **kwargs):
        update_device(self.ip_address)
        return super().save(*args, **kwargs)


class DeviceGroup(models.Model):
    uuid = models.UUIDField(default=uuid.uuid4, unique=True)
    name = models.CharField(max_length=50)
    is_active = models.BooleanField(default=True)
    timestamp = models.DateTimeField(auto_now_add=True)
    last_edited = models.DateTimeField(auto_now=True)

    last_updated = models.DateTimeField(null=True, blank=True)
    _version = models.OneToOneField(Version, on_delete=models.SET_NULL,
                                    null=True, blank=True)

    owner = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    devices = models.ManyToManyField(Device, related_name='groups', blank=True)

    def __init__(self, *args, **kwargs):
        self._updated_devices = []
        super().__init__(*args, **kwargs)

    @property
    def version(self):
        return self._version

    @version.setter
    def version(self, version):
        self._version = version
        for device in self.devices.filter(is_active=True):
            new_version = Version.objects.create(name=version.name,
                                                 file=version.file,
                                                 file_checksum=version.file_checksum)

            device.version = new_version
            self._updated_devices.append(device)

    def save(self, *args, **kwargs):
        for device in self._updated_devices:
            device.save()

            new_version = device.version
            new_version.versioned_object = device
            new_version.save()

        update_device_group(self.uuid)
        return super().save(*args, **kwargs)
