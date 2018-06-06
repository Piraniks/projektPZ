from django.shortcuts import render

from device.models import Device, DeviceGroup

from projektPZ import TEMPLATE_404, TEMPLATE_403
from projektPZ import status


class DevicePermissionMixin:
    """
    Mixin which implements method to check if device exists and if so
    if user should be allowed to see it.
    """

    @staticmethod
    def validate_user_for_device(request, device_uuid):
        device = Device.objects.filter(uuid=device_uuid, is_active=True).first()

        if device is None:
            return render(request, TEMPLATE_404, status=status.HTTP_404_NOT_FOUND)

        if request.user != device.owner:
            return render(request, TEMPLATE_403, status=status.HTTP_403_FORBIDDEN)

        return None


class DeviceGroupsPermissionMixin:
    """
    Mixin which implements method to check if device group exists and if so
    if user should be allowed to see it.
    """

    @staticmethod
    def validate_user_for_group(request, group_uuid):
        group = DeviceGroup.objects.filter(uuid=group_uuid, is_active=True).first()

        if group is None:
            return render(request, TEMPLATE_404, status=status.HTTP_404_NOT_FOUND)

        if request.user != group.owner:
            return render(request, TEMPLATE_403, status=status.HTTP_403_FORBIDDEN)

        return None
