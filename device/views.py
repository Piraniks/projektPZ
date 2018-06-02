from django.shortcuts import render, redirect
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.contenttypes.models import ContentType
from django.views import View
from django.db import transaction, IntegrityError
from django.utils import timezone

from projektPZ import status

from device.models import Device, Version
from device.forms import DeviceForm, VersionForm, DeviceEditForm
from device.mixins import DevicePermissionMixin


class DeviceView(DevicePermissionMixin, LoginRequiredMixin, View):
    TEMPLATE = 'device/device.html'

    def get(self, request, device_uuid):
        response = self.validate_user_for_device(request=request,
                                                 device_uuid=device_uuid)
        if response is not None:
            return response

        device = Device.objects.get(uuid=device_uuid)
        return render(request, self.TEMPLATE, context={'device': device})

    def post(self, request, device_uuid):
        response = self.validate_user_for_device(request=request,
                                                 device_uuid=device_uuid)
        if response is not None:
            return response

        device = Device.objects.get(uuid=device_uuid)
        device_form = DeviceEditForm(request.POST)

        if device_form.is_valid():
            device.name = device_form.cleaned_data.get('name', device.name)
            device.is_active = device_form.cleaned_data.get('is_active')
            device.save()

            if device.is_active:
                return render(request, self.TEMPLATE, context={'device': device})
            else:
                return redirect('device_list')

        else:
            context = {
                'device': device,
                'errors': device_form.errors.as_json()
            }
            return render(request, self.TEMPLATE, context=context, status=status.HTTP_400_BAD_REQUEST)


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
                'errors': device_form.errors.as_json()
            }
            return render(request, self.TEMPLATE, context=context, status=status.HTTP_400_BAD_REQUEST)


class VersionCreateView(DevicePermissionMixin, LoginRequiredMixin, View):
    TEMPLATE = 'device/version_create.html'
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

        device = Device.objects.get(uuid=device_uuid)
        version_form = VersionForm(data=request.POST, files=request.FILES)

        if version_form.is_valid() is False:
            context = {
                'errors': version_form.errors.as_json(),
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

        return redirect('version_list', device_uuid=device.uuid)


class VersionListView(DevicePermissionMixin, LoginRequiredMixin, View):
    TEMPLATE = 'device/version_list.html'

    def get(self, request, device_uuid):
        response = self.validate_user_for_device(request=request,
                                                 device_uuid=device_uuid)
        if response is not None:
            return response

        device = Device.objects.get(uuid=device_uuid)

        device_content_type = ContentType.objects.get_for_model(device)
        devices = Version.objects.filter(object_id=device.id,
                                         content_type=device_content_type)
        context = {
            'versions': devices,
            'device_uuid': device.uuid
        }
        return render(request, self.TEMPLATE, context=context)
