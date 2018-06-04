from django.urls import path

from device.views import (
    DeviceView, DeviceListView, DeviceCreateView, DeviceDeleteView,
    VersionCreateView, VersionListView,
    DeviceGroupCreateView, DeviceGroupDeleteView,
    DeviceGroupAddDeviceView, DeviceGroupRemoveDeviceView,
    DeviceGroupListView, DeviceGroupView
)


urlpatterns = [
    path('devices/', DeviceListView.as_view(), name='device_list'),
    path('devices/create/', DeviceCreateView.as_view(), name='device_create'),
    path('devices/<uuid:device_uuid>/', DeviceView.as_view(), name='device'),
    path('devices/<uuid:device_uuid>/delete/',
         DeviceDeleteView.as_view(), name='device_delete'),

    path('groups/', DeviceGroupListView.as_view(), name='group_list'),
    path('groups/create/', DeviceGroupCreateView.as_view(), name='group_create'),
    path('groups/<uuid:group_uuid>/', DeviceGroupView.as_view(), name='group'),
    path('groups/<uuid:group_uuid>/delete/',
         DeviceGroupDeleteView.as_view(), name='group_delete'),
    path('groups/<uuid:group_uuid>/add/',
         DeviceGroupAddDeviceView.as_view(), name='group_add'),
    path('groups/<uuid:group_uuid>/remove/',
         DeviceGroupRemoveDeviceView.as_view(), name='group_remove'),

    path('devices/<uuid:device_uuid>/versions/create/',
         VersionCreateView.as_view(), name='version_create'),
    path('devices/<uuid:device_uuid>/versions/',
         VersionListView.as_view(), name='version_list'),
]
