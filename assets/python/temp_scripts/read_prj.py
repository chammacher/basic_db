#!/usr/bin/env python

import urllib, datetime, sqlite3

path = '/home/oper/qc/chance/mcusers/assets/db/SERVER-USR.db'
conn = sqlite3.connect(path)

out = conn.execute('select PROJID from PROJECTS;')
numbs = []
for ele in out.fetchall():
    numbs.append(ele[0].replace(' ',''))



link = "https://www.ssec.wisc.edu/accounting/projlist.htm"
f = urllib.urlopen(link)
myfile = f.read()
mylist = myfile.split('\n')
while '\r' in mylist:
    mylist.remove('\r');    

for line in mylist[22:len(mylist)-3]:
    line = line.replace('</TD>', '')
    sline = line.split('<TD>')
    prj = sline[2]
    name = sline[4]
    contact = sline[5]
    if not contact == '':
        contact = ' '.join(contact.split(',')[::-1])
    date = sline[6]
    if not date == '':
        try:
            if len(date.split()[0]) == 1:
                date= '0'+date
            date = datetime.datetime.strptime(date, '%d %b %y')
            date = date.strftime('%Y-%m-%d')
        except ValueError:
            pass
    if prj in numbs:
        if "'" in name:
            name = name.replace("'", "")
        print prj, name, contact, date
        if not date == '':
            #use date in update query
            conn.execute("UPDATE PROJECTS SET NAME = '"+name+"', CONTACT = '"+contact+"', EXPIRATION = '"+date+"' WHERE PROJID LIKE '"+prj+"';")
        else:
            #dont use date in query
            conn.execute("UPDATE PROJECTS SET NAME = '"+name+"', CONTACT = '"+contact+"' WHERE PROJID LIKE '"+prj+"';")


conn.commit()
