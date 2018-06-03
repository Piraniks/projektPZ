from django.urls import path

from device.views import (
    DeviceView, DeviceListView, DeviceCreateView, DeviceDeleteView,
    VersionCreateView, VersionListView
)


urlpatterns = [
    path('device/', DeviceListView.as_view(), name='device_list'),
    path('device/create/', DeviceCreateView.as_view(), name='device_create'),
    path('device/<uuid:device_uuid>/', DeviceView.as_view(), name='device'),
    path('device/<uuid:device_uuid>/delete', DeviceDeleteView.as_view(), name='device_delete'),

    path('device/<uuid:device_uuid>/version/create',
         VersionCreateView.as_view(), name='version_create'),
    path('device/<uuid:device_uuid>/version/',
         VersionListView.as_view(), name='version_list'),
]
