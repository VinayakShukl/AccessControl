from datetime import datetime

from django.db import models


class Building(models.Model):
    name = models.CharField(max_length=60, primary_key=True)

    def __unicode__(self):
        return "%s" % self.name


class Floor(models.Model):
    bID = models.ForeignKey(Building, null=False, verbose_name="Building")
    floor = models.PositiveSmallIntegerField(default=0, null=False)

    def __unicode__(self):
        return "%s, %d floor" % (self.bID.name, self.floor)


class Room(models.Model):
    fID = models.ForeignKey(Floor, null=False, verbose_name="Floor")
    name = models.CharField(max_length=60)

    def __unicode__(self):
        return "%s - %s" % (self.fID, self.name)


class Device(models.Model):
    """ type 0: Reader, type 1: In
    """
    name = models.CharField(max_length=30, primary_key=True, verbose_name="MSSQL Name")
    dType = models.SmallIntegerField(null=False, default=0, verbose_name="Device Type [0: reader, 1: in]")

    def __unicode__(self):
        return "%s - Type %d" % (self.name, self.dType)


class RoomDevice(models.Model):
    room = models.ForeignKey(Room, null=False)
    device = models.ForeignKey(Device, null=False)

    def __unicode__(self):
        return "%s" % (self.device)

class DataRequestManager(models.Manager):
    def create_req(self, start, end, room, rTime, rIP):
        req = self.create(start_time=start, end_time=end, room=room, request_time=rTime, request_IP=rIP)
        return req


class DataRequest(models.Model):
    start_date = models.DateTimeField(blank=False, verbose_name="Start Date")
    end_date = models.DateTimeField(blank=False, verbose_name="End Date")
    start_time = models.TimeField(blank=False, verbose_name="Start Time")
    end_time = models.TimeField(blank=False, verbose_name="End Time")
    room = models.ForeignKey(Room, blank=False, verbose_name="Room")
    request_time = models.DateTimeField(default=datetime.now(), blank=False)
    request_IP = models.IPAddressField(blank=False)

    objects = DataRequestManager()

    def __unicode__(self):
        return "%s Start: %s End: %s" % (
            self.room, self.start_time.strftime("%d/%m/%Y"), self.end_time.strftime("%d/%m/%Y"))
