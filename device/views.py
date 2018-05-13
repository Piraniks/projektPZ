from django.shortcuts import render, redirect
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views import View
from django.utils import timezone
from rest_framework import status

from projektPZ import TEMPLATE_404, TEMPLATE_403
from device.models import Device
from device.forms import DeviceForm


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
                device.name = device_form.cleaned_data.get('name')
                device.save()

                return render(request, self.TEMPLATE, context={'device': device})
            else:
                context = {
                    'device': device,
                    'errors': device_form.errors.as_json()
                }
                return render(request, self.TEMPLATE, context=context)

        except Device.DoesNotExist:
            return render(request, TEMPLATE_404, status=status.HTTP_404_NOT_FOUND)


class DeviceViewList(LoginRequiredMixin, View):
    TEMPLATE = 'device/device_list.html'

    def get(self, request):
        devices = Device.objects.filter(owner=request.user, is_active=True)
        return render(request, self.TEMPLATE, context={'devices': devices})


class DeviceCreateView(LoginRequiredMixin, View):
    TEMPLATE = 'device/create_device.html'

    def get(self, request):
        return render(request, self.TEMPLATE)

    def post(self, request):
        device_form = DeviceForm(data=request.POST)

        if device_form.is_valid():
            new_device = device_form.save(commit=False)

            new_device.last_updated = timezone.now()
            new_device.owner = request.user
            new_device.is_active = True

            new_device.save()

            return redirect('device', device_uuid=str(new_device.uuid))
        else:
            return redirect('device_list')
