from django import forms

from device.models import Device


class DeviceForm(forms.ModelForm):
    uuid = forms.UUIDField(disabled=True, required=False)
    last_updated = forms.DateTimeField(disabled=True, required=False)

    version = forms.IntegerField(disabled=True, min_value=0, required=False)
    owner = forms.IntegerField(disabled=True, min_value=0, required=False)

    class Meta:
        model = Device
        exclude = ['id']
