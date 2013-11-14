import pyodbc
import datetime

from django.shortcuts import render
import django_tables2 as tables
from django_tables2 import RequestConfig

from models import *
from forms import DataRequestForm1


def process_form(form, rIP):
    building_name = form.cleaned_data['room']
    startDate = form.cleaned_data['startDate']
    startTime = form.cleaned_data['startTime']
    endDate = form.cleaned_data['endDate']
    endTime = form.cleaned_data['endTime']
    info = {}
    info['room'] = building_name
    info['sTime'] = datetime.datetime.combine(startDate, startTime)
    info['eTime'] = datetime.datetime.combine(endDate, endTime)
    info['rTime'] = datetime.datetime.now()
    info['rIP'] = rIP
    print str(info['room']) + " -> " + str(info['sTime']) + " TO " + str(info['eTime']) + " | " + str(
        info['rTime']) + "@" + str(info['rIP'])
    return info


def home(request):
    form = DataRequestForm1()
    if request.method == 'POST':
        form = DataRequestForm1(request.POST, request)
        if form.is_valid():
            print "valid"
            uRoom = form.cleaned_data['room']
            for x in RoomDevice.objects.filter(room=uRoom.id):
                print x
                #info = process_form(form, request.META.get('REMOTE_ADDR'))
                #print info['room'], type(info['room'])
                #DataRequest.objects.create_req(info['sTime'], info['eTime'], info['room'], info['rTime'], info['rIP'])
                #DataRequest.objects.create_req(info['sDate'])
                #return details(request, info)
        else:
            print form.errors
    return render(request, 'RequestForm.html', {'form': form, 'title': "Access Control"})


class NameTable(tables.Table):
    time = tables.DateTimeColumn()
    f = tables.Column()
    l = tables.Column()
    d = tables.Column()

    class Meta:
        attrs = {"class": "paleblue"}


def details(request):
    con = pyodbc.connect('DRIVER={FreeTDS};SERVER=192.168.138.5;PORT=1433;DATABASE=WIN-PAK PRO;UID=sa')
    cur = con.cursor()
    cur.execute(
        "SELECT HR.Timestamp, C.FirstName, C.LastName, HW.Name, CE.Name, HR.Param1, HR.Param3 FROM dbo.CardHolder as C, dbo.HWIndependentDevices as HW, dbo.HistoryReport as HR, dbo.CardEx as CE WHERE HR.Link3 = C.RecordID AND HR.Link1 = HW.DeviceID AND CE.CardHolderID = C.RecordID AND HR.Timestamp BETWEEN " + "'20131114 00:00:00'" + "AND " + "'20141114 23:59:59'")
    rows = cur.fetchall()
    l = []
    for r in rows:
        l.append({'time': r[0], 'f': r[1], 'l': r[2], 'd': r[3]})
    t = NameTable(l)
    RequestConfig(request).configure(t)
    #print type(rows)
    con.close()
    return render(request, 'details.html', {'title': "Details", 'info': t})
