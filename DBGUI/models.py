from datetime import datetime

from django.db import models


class Room(models.Model):
    name = models.CharField(max_length=60, primary_key=True)
    building_choices = (
        ('A', 'Academic'),
        ('L', 'Library'),
        ('M', 'Mess'),
    )
    floor_choices = (
        ('0', 'Ground'),
        ('1', 'First'),
        ('2', 'Second'),
        ('3', 'Third'),
        ('4', 'Fourth'),
        ('5', 'Fifth'),
    )

    wing_choices = (
        ('0', 'NA'),
        ('A', 'A'),
        ('B', 'B'),
    )

    building = models.CharField(max_length=1, choices=building_choices, blank=False)
    floor = models.CharField(max_length=1, choices=floor_choices, blank=False)
    wing = models.CharField(max_length=1, choices=wing_choices, blank=False)

    def __unicode__(self):
        return "%s | %s building, %s floor, %s wing" % (self.name, self.get_building_display(), self.get_floor_display(), self.wing)


class Device(models.Model):
    inRoom = models.ForeignKey(Room)
    tag = models.CharField(max_length=60, blank=False, verbose_name="Name in DB")

    def __unicode__(self):
        return "In room: %s Tag: %s" % (self.inRoom, self.tag)


class DataRequest(models.Model):
    start_time = models.DateTimeField(blank=False, verbose_name="Start Time")
    end_time = models.DateTimeField(blank=False, verbose_name="End Time")
    room = models.ForeignKey(Room, blank=False, verbose_name="Room")

    request_time = models.DateTimeField(default=datetime.now(), blank=False)
    request_IP = models.IPAddressField(blank=False)

    def __unicode__(self):
        return "%s Start: %s End: %s" % (
            self.room, self.start_time.strftime("%d/%m/%Y"), self.end_time.strftime("%d/%m/%Y"))