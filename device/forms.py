from django import forms

from device.models import Device, Version


class DeviceForm(forms.ModelForm):
    uuid = forms.UUIDField(disabled=True, required=False)
    last_updated = forms.DateTimeField(disabled=True, required=False)

    version = forms.IntegerField(disabled=True, min_value=0, required=False)
    owner = forms.IntegerField(disabled=True, min_value=0, required=False)

    class Meta:
        model = Device
        exclude = ['id']


class VersionForm(forms.ModelForm):
    uuid = forms.UUIDField(disabled=True, required=False)
    timestamp = forms.DateTimeField(disabled=True, required=False)

    name = forms.CharField(max_length=50)
    creator = forms.IntegerField(disabled=True, min_value=0, required=False)

    class Meta:
        model = Version
        exclude = ['id', 'versioned_object', 'object_id', 'content_type']
