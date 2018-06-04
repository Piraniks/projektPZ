from django.urls import path

from device.views import (
    DeviceView, DeviceListView, DeviceCreateView, DeviceDeleteView,
    VersionCreateView, VersionListView,
    DeviceGroupCreateView, DeviceGroupDeleteView, DeviceGroupAddDeviceView,
    DeviceGroupListView, DeviceGroupView
)


urlpatterns = [
    path('device/', DeviceListView.as_view(), name='device_list'),
    path('device/create/', DeviceCreateView.as_view(), name='device_create'),
    path('device/<uuid:device_uuid>/', DeviceView.as_view(), name='device'),
    path('device/<uuid:device_uuid>/delete',
         DeviceDeleteView.as_view(), name='device_delete'),

    path('group/', DeviceGroupListView.as_view(), name='group_list'),
    path('group/create/', DeviceGroupCreateView.as_view(), name='group_create'),
    path('group/<uuid:group_uuid>/', DeviceGroupView.as_view(), name='group'),
    path('group/<uuid:group_uuid>/delete',
         DeviceGroupDeleteView.as_view(), name='group_delete'),
    path('group/<uuid:group_uuid>/add/<uuid:device_uuid>/',
         DeviceGroupAddDeviceView.as_view(), name='group_add'),

    path('device/<uuid:device_uuid>/version/create',
         VersionCreateView.as_view(), name='version_create'),
    path('device/<uuid:device_uuid>/version/',
         VersionListView.as_view(), name='version_list'),
]
