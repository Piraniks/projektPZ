from django import forms

from device.models import Device, Version, DeviceGroup


class DeviceForm(forms.ModelForm):
    uuid = forms.UUIDField(disabled=True, required=False)
    last_updated = forms.DateTimeField(disabled=True, required=False)

    version = forms.IntegerField(disabled=True, min_value=0, required=False)
    owner = forms.IntegerField(disabled=True, min_value=0, required=False)

    class Meta:
        model = Device
        exclude = ['id']


class DeviceEditForm(forms.ModelForm):
    uuid = forms.UUIDField(disabled=True, required=False)
    last_updated = forms.DateTimeField(disabled=True, required=False)

    version = forms.IntegerField(disabled=True, min_value=0, required=False)
    owner = forms.IntegerField(disabled=True, min_value=0, required=False)
    ip_address = forms.GenericIPAddressField(required=False, disabled=True)

    class Meta:
        model = Device
        exclude = ['id']


class VersionForm(forms.ModelForm):
    uuid = forms.UUIDField(disabled=True, required=False)
    timestamp = forms.DateTimeField(disabled=True, required=False)
    file_checksum = forms.Field(disabled=True, required=False)

    name = forms.CharField(max_length=50)
    creator = forms.IntegerField(disabled=True, min_value=0, required=False)

    class Meta:
        model = Version
        exclude = ['id', 'versioned_object', 'object_id', 'content_type']


class DeviceGroupForm(forms.ModelForm):
    uuid = forms.UUIDField(disabled=True, required=False)
    last_updated = forms.DateTimeField(disabled=True, required=False)

    version = forms.IntegerField(disabled=True, min_value=0, required=False)
    owner = forms.IntegerField(disabled=True, min_value=0, required=False)

    class Meta:
        model = DeviceGroup
        exclude = ['id']


class DeviceGroupDeviceForm(forms.Form):
    device_uuid = forms.UUIDField()
