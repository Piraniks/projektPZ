import uuid

from django.db import models
from django.contrib.auth import get_user_model
from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.models import ContentType
from django.utils import timezone


User = get_user_model()


class File(models.Model):
    uuid = models.UUIDField(default=uuid.uuid4, unique=True)
    name = models.CharField(max_length=50)
    data = models.BinaryField()
    timestamp = models.DateTimeField(auto_now_add=True)

    uploader = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)

    class Meta:
        ordering = ['-id']
        get_latest_by = 'timestamp'

    def __str__(self):
        return self.name


class Version(models.Model):
    uuid = models.UUIDField(default=uuid.uuid4, unique=True)
    name = models.CharField(max_length=50)
    timestamp = models.DateTimeField(auto_now_add=True)

    # TODO: Figure out better names for the relation.
    content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE, null=True)
    object_id = models.PositiveIntegerField(null=True)
    versioned_object = GenericForeignKey('content_type', 'object_id')

    file = models.ForeignKey(File, on_delete=models.SET_NULL, null=True)
    creator = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)

    previous = models.ForeignKey('self', on_delete=models.SET_NULL, null=True, blank=True, related_name='+')
    next = models.ForeignKey('self', on_delete=models.SET_NULL, null=True, blank=True, related_name='+')

    class Meta:
        ordering = ['-id']
        get_latest_by = 'timestamp'

    def __str__(self):
        return self.name


class Device(models.Model):
    uuid = models.UUIDField(default=uuid.uuid4, unique=True)
    name = models.CharField(max_length=50)
    is_standalone = models.BooleanField(default=True)
    is_active = models.BooleanField(default=True)

    last_updated = models.DateTimeField(null=True, blank=True)
    version = models.ForeignKey(Version, on_delete=models.SET_NULL, related_name='devices',
                                       null=True, blank=True)

    owner = models.ForeignKey(User, on_delete=models.SET_NULL, related_name='devices', null=True)

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

        if version.next is None:
            return True

        return False

    def raise_version(self):
        if self.is_up_to_date:
            return False

        current_version = self.version
        if current_version is None:
            raise Exception('Version for the device is not specified.')

        next_version = current_version.next
        if next_version is None:
            raise Exception(
                'Version { current_version.name }({ current_version.uuid }) '
                'is not considered latest while there is no next version.'
            )

        self.version = next_version
        self.last_updated = timezone.now()
        self.save()

        return True

    def update(self):
        while self.is_up_to_date is False:
            self.raise_version()
