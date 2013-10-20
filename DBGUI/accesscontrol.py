import pyodbc
from prettytable import PrettyTable
import datetime
import json
from time import mktime

con = pyodbc.connect('DRIVER={FreeTDS};SERVER=192.168.138.5;PORT=1433;DATABASE=WIN-PAK PRO;UID=sa')
cur = con.cursor()
results = []
STARTDATE = "'20131014 00:00:00'"
ENDDATE = "'20131021 00:00:00'"


# logins by XYZ in last 24hrs
'''
cur.execute("SELECT HR.TimeStamp, HR.FirstName, HW.RecordID \
			 FROM dbo.HistoryReport as HR, dbo.HWIndependentDevices as HW \
			 WHERE HR.FirstName='inder' \
			 AND HR.Link1 = HW.DeviceID \
             AND HR.TimeStamp BETWEEN '20101007 00:00:00' \
					              AND '20131008 00:00:00'")
'''

# number of logins by name
'''
cur.execute("SELECT distinct C.FirstName, C.LastName, count(*) as cnt\
			 FROM dbo.HistoryReport as H, dbo.CardHolder as C \
			 WHERE H.Link3 = C.RecordID \
			 GROUP BY C.FirstName, C.LastName \
             ORDER BY cnt")
'''

# records in last 24 hrs
'''
cur.execute("SELECT * \
			 FROM dbo.HistoryReport \
			 WHERE Timestamp BETWEEN '20131017 00:00:00' \
							     AND '20131018 00:00:00'")
rows = cur.fetchall()'''

# available devices
cur.execute("SELECT distinct(Name) \
			 FROM dbo.HWIndependentDevices")

rows = cur.fetchall()
for r in rows:
	print r[0]

# who, where and when - logins of past 24 hrs
cur.execute("SELECT HR.Timestamp, C.FirstName, C.LastName, HW.Name, CE.Name, HR.Param1, HR.Param3\
			 FROM dbo.CardHolder as C, dbo.HWIndependentDevices as HW, dbo.HistoryReport as HR, dbo.CardEx as CE \
			 WHERE HR.Link3 = C.RecordID \
			 AND HR.Link1 = HW.DeviceID \
			 AND CE.CardHolderID = C.RecordID \
             AND HR.Timestamp BETWEEN " + STARTDATE + " \
							      AND " + ENDDATE)

rows = cur.fetchall()
x = PrettyTable(["Time", "Name", "Location", "Access", "Param1", "Misc"])
x.align["Time"] = "c" 
x.align["Name"] = "l"
x.padding_width = 3

for r in rows:
	row = [r[0].strftime('%H:%M:%S (%d, %b %Y)'), (r[1].title() + " " + r[2].title()), r[3], r[4], r[5], r[6]]
	x.add_row(row)
	results.append(dict(zip(["TimeStamp", "FirstName", "LastName", "Name", "Param1", "Param3"], r)))

# logouts
# Param1 = 1 --> Opened, Param1 = 2 --> Closed
cur.execute("SELECT HR.Timestamp, HW.Name, HR.Param1, Param3 \
				 FROM dbo.HistoryReport as HR, dbo.HWIndependentDevices as HW \
				 WHERE HR.Timestamp BETWEEN " + STARTDATE + " \
										AND " + ENDDATE + " \
				 AND HR.Link1 = HW.DeviceID \
				 AND HR.Link3 = 0 \
				 AND HR.Param1 = 1")
rows = cur.fetchall()
for r in rows:
	row = [r[0].strftime('%H:%M:%S (%d, %b %Y)'), "Opened from Inside", r[1], "NA", r[2], r[3]]
	x.add_row(row)
	results.append(dict(zip(["TimeStamp", "Name", "Param1", "Param3"], r)))

# door closed
cur.execute("SELECT HR.Timestamp, HW.Name, HR.Param1, Param3 \
				 FROM dbo.HistoryReport as HR, dbo.HWIndependentDevices as HW \
				 WHERE HR.Timestamp BETWEEN " + STARTDATE + " \
								        AND " + ENDDATE + " \
				 AND HR.Link1 = HW.DeviceID \
				 AND HR.Param1 = 2")		
rows = cur.fetchall()
for r in rows:
	row = [r[0].strftime('%H:%M:%S (%d, %b %Y)'), "Closed", r[1], "NA", r[2], r[3]]
	x.add_row(row)
	results.append(dict(zip(["TimeStamp", "Name", "Param1", "Param3"], r)))	

class MyEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, datetime.datetime):
            return int(mktime(obj.timetuple()))

        return json.JSONEncoder.default(self, obj)

#sortResults = sorted(results, key=lambda k: k['TimeStamp']) 
#with open('data.txt', 'w') as outfile:
#	json.dump(sortResults, outfile, cls = MyEncoder, indent=4, sort_keys=True)
 
#print x.get_string(sortby="Time")
