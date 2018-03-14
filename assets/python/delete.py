#!/usr/bin/env python

#####################################################
## Script written by Chance Hammacher
## Contact the SSEC Satellite Date Services for help
#####################################################

import os, sqlite3, cgi, datetime

print "Content-type: text/html\n"

conn = sqlite3.connect('/home/oper/qc/chance/mcusers/assets/db/SERVER-USR.db')
# get cgi params from js script
fs = cgi.FieldStorage()
arguments = fs.getvalue('data')


tableU = {'1':'USRID', '2':'DATE_ADDED', '3':'STATUS','4':'EXPIRATION', '5':'NAME', '6':'ORGANIZATION','7':'EMAIL','8':'PHONE','9':'DATASETS'}
tableP = {'1':'PROJID', '2':'DATE_ADDED', '3':'STATUS','4':'EXPIRATION', '5':'NAME', '6':'CONTACT','7':'DATASETS'}

tablename = arguments[0]

preQ = []
if tablename == 'USERS':
    # use tableU
    for idx, ele in enumerate(arguments):
        if not idx == 0:
            if not ele == 'empty':
                preQ.append(tableU[str(idx)]+" LIKE '"+ele+"'")
else:
    # use tableP
    for idx, ele in enumerate(arguments):
        if not idx == 0:
            if not ele == 'empty':
                preQ.append(tableP[str(idx)]+" LIKE '"+ele+"'")

query = preQ[0]
print query
#### change this to make it "secure" for sqlite ####
try:
    output = conn.execute("DELETE FROM "+tablename+" WHERE "+query+";")
except sqlite3.Error as er:
    print er.message


conn.commit()
conn.close()
