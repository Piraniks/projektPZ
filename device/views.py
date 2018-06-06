import json

from django.http import JsonResponse
from django.shortcuts import render, redirect
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.contenttypes.models import ContentType
from django.views import View
from django.db import transaction, IntegrityError
from django.utils import timezone

from projektPZ import status

from device.models import Device, Version, DeviceGroup
from device.forms import (DeviceForm, VersionForm, DeviceEditForm,
                          DeviceGroupForm, DeviceGroupDeviceForm)
from device.mixins import DevicePermissionMixin, DeviceGroupsPermissionMixin


class DeviceDetailsView(DevicePermissionMixin, LoginRequiredMixin, View):
    TEMPLATE = 'device/device_details.html'

    def get(self, request, device_uuid):
        response = self.validate_user_for_device(request=request,
                                                 device_uuid=device_uuid)
        if response is not None:
            return response

        device = Device.objects.get(uuid=device_uuid, is_active=True)
        return render(request, self.TEMPLATE, context={'device': device})

    def post(self, request, device_uuid):
        response = self.validate_user_for_device(request=request,
                                                 device_uuid=device_uuid)
        if response is not None:
            return response

        device = Device.objects.get(uuid=device_uuid, is_active=True)
        device_form = DeviceEditForm(request.POST)

        if device_form.is_valid():
            device.name = device_form.cleaned_data.get('name', device.name)
            device.save()

            return render(request, self.TEMPLATE, context={'device': device})

        else:
            context = {
                'device': device,
                'errors': json.loads(device_form.errors.as_json())
            }
            return render(request, self.TEMPLATE, context=context,
                          status=status.HTTP_400_BAD_REQUEST)


class DeviceListView(LoginRequiredMixin, View):
    TEMPLATE = 'device/device_list.html'

    def get(self, request):
        devices = Device.objects.filter(owner=request.user,
                                        is_active=True).order_by('timestamp')
        return render(request, self.TEMPLATE, context={'devices': devices})


class DeviceCreateView(LoginRequiredMixin, View):
    TEMPLATE = 'device/device_create.html'

    def get(self, request):
        return render(request, self.TEMPLATE)

    def post(self, request):
        device_form = DeviceForm(data=request.POST)

        if device_form.is_valid():
            new_device = device_form.save(commit=False)

            new_device.owner = request.user
            new_device.is_active = True

            new_device.save()

            return redirect('device_list')
        else:
            context = {
                'errors': json.loads(device_form.errors.as_json())
            }
            return render(request, self.TEMPLATE, context=context,
                          status=status.HTTP_400_BAD_REQUEST)


class DeviceDeleteView(DevicePermissionMixin, LoginRequiredMixin, View):
    def post(self, request, device_uuid):
        response = self.validate_user_for_device(request=request,
                                                 device_uuid=device_uuid)
        if response is not None:
            return response

        device = Device.objects.get(uuid=device_uuid, is_active=True)
        device.is_active = False
        device.save()

        return redirect('device_list')


class DeviceVersionCreateView(DevicePermissionMixin, LoginRequiredMixin, View):
    TEMPLATE = 'device/device_version_create.html'
    INTEGRITY_ERROR_MESSAGE = ('Integrity error has been encountered. '
                               'Contact the service administrator.')

    def get(self, request, device_uuid):
        response = self.validate_user_for_device(request=request,
                                                 device_uuid=device_uuid)
        if response is not None:
            return response

        context = {'device_uuid': device_uuid}
        return render(request, self.TEMPLATE, context=context)

    def post(self, request, device_uuid):
        response = self.validate_user_for_device(request=request,
                                                 device_uuid=device_uuid)
        if response is not None:
            return response

        device = Device.objects.get(uuid=device_uuid, is_active=True)
        version_form = VersionForm(data=request.POST, files=request.FILES)

        if version_form.is_valid() is False:
            context = {
                'errors': json.loads(version_form.errors.as_json()),
                'device_uuid': device.uuid
            }

            return render(request, self.TEMPLATE,
                          context=context,
                          status=status.HTTP_400_BAD_REQUEST)

        new_version = version_form.save(commit=False)
        old_version = device.version

        new_version.creator = request.user
        new_version.versioned_object = device
        new_version.previous = old_version

        try:
            with transaction.atomic():
                new_version.save()

                # Add checksum for already created file.
                new_version.generate_checksum()

                if old_version is not None:
                    old_version.next = new_version
                    old_version.save()

                device.last_updated = timezone.now()
                device.version = new_version
                device.save()

        except IntegrityError:
            # If any integrity error is raised inform the user but
            # don't blow up. Just for when we become next Facebook.
            context = {
                "errors": {
                    "data": [{
                        "message": self.INTEGRITY_ERROR_MESSAGE
                    }],
                },
                'device_uuid': device.uuid
            }
            return render(request, self.TEMPLATE, context=context)

        return redirect('device_version_list', device_uuid=device.uuid)


class GroupVersionCreateView(DevicePermissionMixin, LoginRequiredMixin, View):
    TEMPLATE = 'device/group_version_create.html'
    INTEGRITY_ERROR_MESSAGE = ('Integrity error has been encountered. '
                               'Contact the service administrator.')

    def get(self, request, device_uuid):
        response = self.validate_user_for_device(request=request,
                                                 device_uuid=device_uuid)
        if response is not None:
            return response

        context = {'device_uuid': device_uuid}
        return render(request, self.TEMPLATE, context=context)

    def post(self, request, device_uuid):
        response = self.validate_user_for_device(request=request,
                                                 device_uuid=device_uuid)
        if response is not None:
            return response

        device = Device.objects.get(uuid=device_uuid, is_active=True)
        version_form = VersionForm(data=request.POST, files=request.FILES)

        if version_form.is_valid() is False:
            context = {
                'errors': json.loads(version_form.errors.as_json()),
                'device_uuid': device.uuid
            }

            return render(request, self.TEMPLATE,
                          context=context,
                          status=status.HTTP_400_BAD_REQUEST)

        new_version = version_form.save(commit=False)
        old_version = device.version

        new_version.creator = request.user
        new_version.versioned_object = device
        new_version.previous = old_version

        try:
            with transaction.atomic():
                new_version.save()

                # Add checksum for already created file.
                new_version.generate_checksum()

                if old_version is not None:
                    old_version.next = new_version
                    old_version.save()

                device.last_updated = timezone.now()
                device.version = new_version
                device.save()

        except IntegrityError:
            # If any integrity error is raised inform the user but
            # don't blow up. Just for when we become next Facebook.
            context = {
                "errors": {
                    "data": [{
                        "message": self.INTEGRITY_ERROR_MESSAGE
                    }],
                },
                'device_uuid': device.uuid
            }
            return render(request, self.TEMPLATE, context=context)

        return redirect('device_version_list', device_uuid=device.uuid)


class DeviceVersionListView(DevicePermissionMixin, LoginRequiredMixin, View):
    TEMPLATE = 'device/device_version_list.html'

    def get(self, request, device_uuid):
        response = self.validate_user_for_device(request=request,
                                                 device_uuid=device_uuid)
        if response is not None:
            return response

        device = Device.objects.get(uuid=device_uuid, is_active=True)

        device_content_type = ContentType.objects.get_for_model(device)
        devices = Version.objects.filter(object_id=device.id,
                                         content_type=device_content_type)
        context = {
            'versions': devices,
            'device': device
        }
        return render(request, self.TEMPLATE, context=context)


class GroupVersionListView(DevicePermissionMixin, LoginRequiredMixin, View):
    TEMPLATE = 'device/group_version_list.html'

    def get(self, request, device_uuid):
        response = self.validate_user_for_device(request=request,
                                                 device_uuid=device_uuid)
        if response is not None:
            return response

        device = Device.objects.get(uuid=device_uuid, is_active=True)

        device_content_type = ContentType.objects.get_for_model(device)
        devices = Version.objects.filter(object_id=device.id,
                                         content_type=device_content_type)
        context = {
            'versions': devices,
            'device': device
        }
        return render(request, self.TEMPLATE, context=context)


class DeviceGroupListView(LoginRequiredMixin, View):
    TEMPLATE = 'device/group_list.html'

    def get(self, request):
        groups = DeviceGroup.objects.filter(owner=request.user,
                                            is_active=True).order_by('timestamp')

        context = {'groups': groups}
        return render(request, self.TEMPLATE, context=context)


class DeviceGroupCreateView(LoginRequiredMixin, View):
    TEMPLATE = 'device/group_create.html'

    def get(self, request):
        return render(request, self.TEMPLATE)

    def post(self, request):
        group_form = DeviceGroupForm(data=request.POST)

        if group_form.is_valid():
            new_group = group_form.save(commit=False)

            new_group.owner = request.user
            new_group.is_active = True

            new_group.save()

            return redirect('group_list')
        else:
            context = {
                'errors': json.loads(group_form.errors.as_json())
            }
            return render(request, self.TEMPLATE, context=context,
                          status=status.HTTP_400_BAD_REQUEST)


class DeviceGroupDetailsView(DeviceGroupsPermissionMixin, LoginRequiredMixin, View):
    TEMPLATE = 'device/group_details.html'

    def get(self, request, group_uuid):
        response = self.validate_user_for_group(request=request,
                                                group_uuid=group_uuid)
        if response is not None:
            return response

        group = DeviceGroup.objects.get(uuid=group_uuid, is_active=True)

        context = {'group': group}
        return render(request, self.TEMPLATE, context=context)

    def post(self, request, group_uuid):
        response = self.validate_user_for_group(request=request,
                                                group_uuid=group_uuid)
        if response is not None:
            return response

        group = DeviceGroup.objects.get(uuid=group_uuid, is_active=True)

        group_form = DeviceGroupForm(request.POST)

        if group_form.is_valid():
            group.name = group_form.cleaned_data.get('name', group.name)
            group.save()

            return render(request, self.TEMPLATE, context={'group': group})

        else:
            context = {
                'group': group,
                'errors': json.loads(group_form.errors.as_json())
            }
            return render(request, self.TEMPLATE, context=context,
                          status=status.HTTP_400_BAD_REQUEST)


class DeviceGroupAddDeviceView(DeviceGroupsPermissionMixin,
                               DevicePermissionMixin,
                               LoginRequiredMixin, View):

    def post(self, request, group_uuid):
        response = self.validate_user_for_group(request=request,
                                                group_uuid=group_uuid)
        if response is not None:
            return response

        group = DeviceGroup.objects.get(uuid=group_uuid, is_active=True)

        group_form = DeviceGroupDeviceForm(request.POST)

        # If anyone used the endpoint directly
        if group_form.is_valid() is False:
            data = {
                'errors': json.loads(group_form.errors.as_json())
            }

            return JsonResponse(data=data, status=status.HTTP_400_BAD_REQUEST)

        device_uuid = group_form.cleaned_data.get('device_uuid')
        response = self.validate_user_for_device(request=request,
                                                 device_uuid=device_uuid)
        if response is not None:
            return response

        device = Device.objects.get(uuid=device_uuid, is_active=True)
        if device not in group.devices.all():
            group.devices.add(device)

        return redirect('group_details', group_uuid=group_uuid)


class DeviceGroupRemoveDeviceView(DeviceGroupsPermissionMixin,
                                  DevicePermissionMixin,
                                  LoginRequiredMixin, View):

    def post(self, request, group_uuid):
        response = self.validate_user_for_group(request=request,
                                                group_uuid=group_uuid)
        if response is not None:
            return response

        group = DeviceGroup.objects.get(uuid=group_uuid, is_active=True)

        group_form = DeviceGroupDeviceForm(request.POST)

        # If anyone used the endpoint directly
        if group_form.is_valid() is False:
            data = {
                'errors': json.loads(group_form.errors.as_json())
            }

            return JsonResponse(data=data, status=status.HTTP_400_BAD_REQUEST)

        device_uuid = group_form.cleaned_data.get('device_uuid')
        response = self.validate_user_for_device(request=request,
                                                 device_uuid=device_uuid)
        if response is not None:
            return response

        device = Device.objects.get(uuid=device_uuid, is_active=True)
        if device in group.devices.all():
            group.devices.remove(device)

        return redirect('group_details', group_uuid=group_uuid)


class DeviceGroupAddedDeviceView(DeviceGroupsPermissionMixin,
                                 LoginRequiredMixin, View):
    TEMPLATE = 'device/group_added_devices.html'

    def get(self, request, group_uuid):
        response = self.validate_user_for_group(request=request,
                                                group_uuid=group_uuid)
        if response is not None:
            return response

        group = DeviceGroup.objects.get(uuid=group_uuid, is_active=True)
        devices = group.devices.exclude(is_active=False)

        context = {
            'devices': devices,
            'group': group
        }
        return render(request, self.TEMPLATE, context=context)


class DeviceGroupAvailableDeviceView(DeviceGroupsPermissionMixin,
                                     LoginRequiredMixin, View):
    TEMPLATE = 'device/group_available_devices.html'

    def get(self, request, group_uuid):
        response = self.validate_user_for_group(request=request,
                                                group_uuid=group_uuid)
        if response is not None:
            return response

        group = DeviceGroup.objects.get(uuid=group_uuid, is_active=True)
        devices = Device.objects.exclude(groups=group).exclude(is_active=False).filter(owner=group.owner)

        context = {
            'devices': devices,
            'group': group
        }
        return render(request, self.TEMPLATE, context=context)


class DeviceGroupDeleteView(DeviceGroupsPermissionMixin,
                            LoginRequiredMixin, View):

    def post(self, request, group_uuid):
        response = self.validate_user_for_group(request=request,
                                                group_uuid=group_uuid)
        if response is not None:
            return response

        group = DeviceGroup.objects.get(uuid=group_uuid, is_active=True)
        group.is_active = False
        group.save()

        return redirect('group_list')
