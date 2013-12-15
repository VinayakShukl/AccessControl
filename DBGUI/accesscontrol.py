import pyodbc
from operator import itemgetter
import operator

import django_tables2 as tables
from django_tables2_reports.tables import TableReport

from models import *


server = '192.168.138.5'
port = '1433'
database = 'WIN-PAK PRO'
uid = 'sa'
connection = ''

reqDict = {}
listTable = []


class NameTable(TableReport):
    time = tables.DateTimeColumn()
    name = tables.Column()
    action = tables.Column()
    #room = tables.Column()

    class Meta:
        attrs = {"class": "paleblue"}


def generate_queries(infodict):
    global reqDict
    reqDict = {}
    reqDict = infodict

    room = infodict['room']
    sTime = "'" + infodict['sTime'].strftime('%Y%m%d %H:%M:%S') + "'"
    eTime = "'" + infodict['eTime'].strftime('%Y%m%d %H:%M:%S') + "'"
    res = RoomDevice.objects.filter(room=room.id)

    if res[0].device.dType == 0:
        reader = "'" + str(res[0].device.name) + "'"
        button = "'" + str(res[1].device.name) + "'"
    else:
        reader = "'" + str(res[1].device.name) + "'"
        button = "'" + str(res[0].device.name) + "'"

    readerquery = ('SELECT HR.Timestamp, C.FirstName, C.LastName, HW.Name '
                   'FROM dbo.CardHolder as C, dbo.HWIndependentDevices as HW, dbo.HistoryReport as HR, dbo.CardEx as CE '
                   'WHERE HR.Link3 = C.RecordID '
                   'AND HR.Link1 = HW.DeviceID '
                   'AND CE.CardHolderID = C.RecordID '
                   "AND HW.Name = " + reader + " "
                                               "AND HR.Timestamp BETWEEN " + sTime + " AND " + eTime + " ")
    buttonquery = ('SELECT HR.Timestamp, HW.Name '
                   'FROM dbo.HistoryReport as HR, dbo.HWIndependentDevices as HW '
                   'WHERE HR.Link1 = HW.DeviceID '
                   'AND HR.Link3 = 0'
                   'AND HR.Param1 = 2'
                   "AND HW.Name = " + button + " "
                                               "AND HR.Timestamp BETWEEN " + sTime + " AND " + eTime + " ")

    return readerquery, buttonquery


def get_http_resonse(infoDict):
    global listTable
    listTable = []

    cursor = get_login_cursor()
    queries = generate_queries(infoDict)

    row1 = run_query(cursor, queries[0])
    addToTable(row1, 'Reader')

    row2 = run_query(cursor, queries[1])
    addToTable(row2, 'Button')

    close_connection()

    jslist = createJSlist(row1, row2)

    #print listTable
    return NameTable(listTable), jslist


def get_login_cursor():
    global connection
    connection = pyodbc.connect(
        'DRIVER={FreeTDS};SERVER=' + server + ';PORT=' + port + ';' + 'DATABASE=' + database + ';UID=' + uid)
    cursor = connection.cursor()
    return cursor


def close_connection():
    global connection
    connection.close()


def createJSlist(r1, r2):
    temp = []
    numPeople = 0
    for r in r1:
        dateUTC = int(r[0].strftime('%s')) * 1000
        temp.append([dateUTC, 'reader'])

    for r in r2:
        dateUTC = int(r[0].strftime('%s')) * 1000
        temp.append([dateUTC, 'button'])
    temp = sorted(temp, key=itemgetter(0))

    final = []
    for ele in temp:
        if ele[1] == 'reader':
            numPeople += 1
            final.append([ele[0], numPeople])
        else:
            numPeople -= 1
            final.append([ele[0], numPeople])
    return final


def addToTable(rows, type):
    global listTable
    #room = RoomDevice.objects.filter(room=reqDict['room'].id)[0].room
    if type == 'Reader':
        for r in rows:
            listTable.append({'time': r[0], 'name': r[1] + ' ' + r[2], 'action': 'Room Entered'})
            #print 'time:' + str(r[0]) + ' name:' +  r[1]
        #print listTable
        return
    elif type == 'Button':
        for r in rows:
            listTable.append({'time': r[0], 'name': 'NA', 'action': 'Room Exited'})
        return


def run_query(cursor, query):
    cursor.execute(query)
    print query
    rows = cursor.fetchall()
    #print rows
    return rows
