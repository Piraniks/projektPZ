from django.contrib import admin

from device.models import Device, File, Version


admin.site.register(Device)
admin.site.register(File)
admin.site.register(Version)
