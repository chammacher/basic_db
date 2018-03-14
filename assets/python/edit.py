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
#arguments.append(fs.getvalue('data'))


##checkDate( dates ) ##
## checkDate: gets date input and checks if valid date 
## returns valid date to query database with
def checkDate(check):
    try:
        valid = datetime.datetime.strptime(check, "%Y-%m-%d")
        valid = valid.strftime("%Y-%m-%d")
    except ValueError:
        valid = 'NULL'
    return valid

tableU = {'1':'USRID', '2':'DATE_ADDED', '3':'STATUS','4':'EXPIRATION', '5':'NAME', '6':'ORGANIZATION','7':'EMAIL','8':'PHONE','9':'DATASETS'}
tableP = {'1':'PROJID', '2':'DATE_ADDED', '3':'STATUS','4':'EXPIRATION', '5':'NAME', '6':'CONTACT','7':'DATASETS'}

count = 0
for val in arguments:
    if val[0:5] == '+new+':
        new_val = val[5:len(val)]
        ind = count
        arguments[ind] = arguments[int(len(arguments)-1)] 
    count +=1

tablename = arguments[0]
ID = arguments[1]

if tablename == 'USERS':
    cond = "USRID LIKE '"+ID+"'"
    col = tableU[str(ind)]
else:
    cond = "PROJID LIKE '"+ID+"'"
    col = tableP[str(ind)]

success = False
## use ind for case to check input at least a little bit along with secure sqlite command ##
if ind == 1 and tablename == 'USERS':
    if new_val.isalpha() and len(new_val) <= 4:
        success = True
elif ind == 1 and tablename == "PROJECTS":
    if new_val.isdigit() and len(new_val) <= 4:
        success = True
elif ind in [2, 4]:
    if ' to ' in new_val:
        date_range = new_val.split(' to ')
        first = checkDate(date_range[0])
        second = checkDate(date_range[1])
        if first == 'NULL' or second == "NULL":
            new_val = "NULL"
        else:
            success = True
    else:
        exact = checkDate(new_val)
        if not exact == "NULL":
            success = True    
elif ind == 3:
    if new_val.lower() == 'enabled' or new_val.lower() == 'disabled':
        new_val = new_val.upper()
        success = True
else:
    success = True
#still to do

new_val = new_val.replace("'", "")
new_val = new_val.replace("\n", "")
new_val = new_val.replace("\r", "")

#### change this to make it "secure" for sqlite ####
try:
    if success:
        output = conn.execute("UPDATE "+tablename+" SET "+col+" = ? WHERE "+cond+";", (new_val,))
    else:
        print 'error'
except sqlite3.Error as er:
    print er.message

conn.commit()
conn.close()

