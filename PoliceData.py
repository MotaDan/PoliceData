import sqlite3
import tablib

connection = sqlite3.connect("2014-12-snapshot.sqlite3db")
cursor = connection.cursor()

sql_command = """SELECT COUNT(*), calls.*, nicenames.desc FROM calls LEFT JOIN nicenames ON calls.address LIKE '%' || nicenames.address || '%' WHERE nicenames.address IS NULL GROUP BY calls.address ORDER BY COUNT(*) DESC LIMIT 50;"""
cursor.execute(sql_command)
incidents = cursor.fetchall()

book = tablib.Databook()

data = tablib.Dataset(title = "Incident Count")
#data.headers = ["Incidents", "Name", "Street"]

for incident in incidents:
    data.append(incident)

book.add_sheet(data)

sql_command = """SELECT nicenames.desc, calls.address, COUNT(calls.address) FROM calls LEFT JOIN nicenames ON calls.address LIKE '%' || nicenames.address || '%' GROUP BY nicenames.desc, CASE WHEN nicenames.desc IS NULL THEN calls.address ELSE 0 END ORDER BY COUNT(calls.address) DESC LIMIT 100;"""
cursor.execute(sql_command)
incidents = cursor.fetchall()

data = tablib.Dataset(title = "Incident Count Nice Names")

for incident in incidents:
    data.append(incident)
    
book.add_sheet(data)

# Writing the items information to an excel file with multiple sheets
with open('PoliceData.xls', 'wb') as f:
    f.write(book.xls)