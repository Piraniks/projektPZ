from django import forms

from device.models import Device


class DeviceForm(forms.ModelForm):
    uuid = forms.UUIDField(disabled=True)
    last_updated = forms.DateTimeField(disabled=True)

    latest_version = forms.IntegerField(disabled=True, min_value=0)
    owner = forms.IntegerField(disabled=True, min_value=0)

    class Meta:
        model = Device
        fields = '__all__'
