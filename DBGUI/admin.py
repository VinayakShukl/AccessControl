from django.contrib import admin
from models import Room, DataRequest, Building, Floor, Device, RoomDevice

admin.site.register(Room)
admin.site.register(DataRequest)
admin.site.register(Building)
admin.site.register(Floor)
admin.site.register(Device)
admin.site.register(RoomDevice)