from django.urls import path

from device.views import (
    DeviceView, DeviceListView, DeviceCreateView
)


urlpatterns = [
    path('device/', DeviceListView.as_view(), name='device_list'),
    path('device/create/', DeviceCreateView.as_view(), name='device_create'),
    path('device/<uuid:device_uuid>/', DeviceView.as_view(), name='device'),
]
