from django.shortcuts import render, redirect
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.contenttypes.models import ContentType
from django.views import View
from django.db import transaction, IntegrityError

from projektPZ import status
from projektPZ import TEMPLATE_404, TEMPLATE_403

from device.models import Device, Version
from device.forms import DeviceForm, VersionForm


class DeviceView(LoginRequiredMixin, View):
    TEMPLATE = 'device/device.html'

    def get(self, request, device_uuid):
        try:
            device = Device.objects.get(uuid=device_uuid, is_active=True)
            if request.user == device.owner:
                return render(request, self.TEMPLATE, context={'device': device})
            else:
                return render(request, TEMPLATE_403, status=status.HTTP_403_FORBIDDEN)
        except Device.DoesNotExist:
            return render(request, TEMPLATE_404, status=status.HTTP_404_NOT_FOUND)

    def post(self, request, device_uuid):
        try:
            device = Device.objects.get(uuid=device_uuid, is_active=True)

            if request.user != device.owner:
                return render(request, TEMPLATE_403, status=status.HTTP_403_FORBIDDEN)

            device_form = DeviceForm(request.POST)

            if device_form.is_valid():
                device.name = device_form.cleaned_data.get('name', device.name)
                device.is_standalone = device_form.cleaned_data.get(
                    'is_standalone', device.is_standalone)
                device.save()

                return render(request, self.TEMPLATE, context={'device': device})
            else:
                context = {
                    'device': device,
                    'errors': device_form.errors.as_json()
                }
                return render(request, self.TEMPLATE, context=context, status=status.HTTP_400_BAD_REQUEST)

        except Device.DoesNotExist:
            return render(request, TEMPLATE_404, status=status.HTTP_404_NOT_FOUND)


class DeviceListView(LoginRequiredMixin, View):
    TEMPLATE = 'device/device_list.html'

    def get(self, request):
        devices = Device.objects.filter(owner=request.user,
                                        is_active=True).order_by('timestamp')
        return render(request, self.TEMPLATE, context={'devices': devices})


class DeviceCreateView(LoginRequiredMixin, View):
    TEMPLATE = 'device/create_device.html'

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


class VersionCreateView(LoginRequiredMixin, View):
    TEMPLATE = 'device/create_version.html'
    INTEGRITY_ERROR_MESSAGE = ('Integrity error has been encountered. '
                               'Contact the service administrator.')

    def get(self, request, device_uuid):
        device = Device.objects.filter(uuid=device_uuid, is_active=True).first()

        if device is None:
            return render(request, TEMPLATE_404, status=status.HTTP_404_NOT_FOUND)

        if request.user != device.owner:
            return render(request, TEMPLATE_403, status=status.HTTP_403_FORBIDDEN)

        return render(request, self.TEMPLATE, context={'device_uuid': device_uuid})

    def post(self, request, device_uuid):
        device = Device.objects.filter(uuid=device_uuid, is_active=True).first()

        if device is None:
            return render(request, TEMPLATE_404, status=status.HTTP_404_NOT_FOUND)

        if request.user != device.owner:
            return render(request, TEMPLATE_403, status=status.HTTP_403_FORBIDDEN)

        version_form = VersionForm(data=request.POST, files=request.FILES)

        if version_form.is_valid() is False:
            context = {
                'errors': version_form.errors.as_json(),
                'device_uuid': device.uuid
            }

            return render(request, self.TEMPLATE,
                          context=context, status=status.HTTP_400_BAD_REQUEST)

        new_version = version_form.save(commit=False)
        old_version = device.version

        new_version.creator = request.user
        new_version.versioned_object = device
        new_version.previous = old_version

        try:
            with transaction.atomic():
                new_version.save()

                if old_version is not None:
                    old_version.next = new_version
                    old_version.save()

                device.last_updated = timezone.now()
                device.version = new_version
                device.save()

        except IntegrityError:
            context = {
                "errors": {
                    "data": [{
                        "message": self.INTEGRITY_ERROR_MESSAGE
                    }],
                },
                'device_uuid': device.uuid
            }
            return render(request, self.TEMPLATE, context=context)

        return redirect('device', device_uuid=device.uuid)


class VersionListView(LoginRequiredMixin, View):
    TEMPLATE = 'device/version_list.html'

    def get(self, request, device_uuid):
        device = Device.objects.filter(uuid=device_uuid, is_active=True).first()

        if device is None:
            return render(request, TEMPLATE_404, status=status.HTTP_404_NOT_FOUND)

        if request.user != device.owner:
            return render(request, TEMPLATE_403, status=status.HTTP_403_FORBIDDEN)

        device_content_type = ContentType.objects.get_for_model(device)
        devices = Version.objects.filter(object_id=device.id,
                                         content_type=device_content_type)
        return render(request, self.TEMPLATE, context={'versions': devices})
