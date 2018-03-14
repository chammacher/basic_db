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
arguments = {}
for key in fs.keys():
    arguments[key] = fs.getvalue(key)


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

params = {}
key_order = []
if arguments['TABLE'] == 'USERS':
    params = {
        'USRID': False,
        'DATE_ADDED': False,
        'STATUS': False,
        'EXPIRATION': False,
        'NAME': False,
        'ORGANIZATION': False,
        'EMAIL': False,
        'PHONE': False,
        'DATASETS': False
    }
    key_order = ['USRID','DATE_ADDED','STATUS','EXPIRATION','NAME','ORGANIZATION','EMAIL','PHONE','DATASETS']
if arguments['TABLE'] == 'PROJECTS':
    params = {
        'PROJID': False,
        'DATE_ADDED': False,
        'STATUS': False,
        'EXPIRATION': False,
        'NAME': False,
        'CONTACT': False,
        'DATASETS': False
    }
    key_order = ['PROJID','DATE_ADDED','STATUS','EXPIRATION','NAME','CONTACT','DATASETS']



for key, value in arguments.iteritems():
    if value == "  ":
        pass
    if value == '' or value == '  ':
        params[key] = True
    elif key == "USRID":
        if not value == 'NULL':
            if value.isalpha() and len(value) <= 4:
                value = True
            else:
                value = "NULL"
        else:
            value = ""
        params[key] = value

    elif key == "PROJID":
        if not value == 'NULL':
            if value.isdigit() and len(value) <= 4:
                value = True
            else:
                value = "NULL"
        else:
            value = ""
        params[key] = value

    elif key in ["DATE_ADDED", "EXPIRATION"]:
        if  value== 'NULL':
            value = ''
        else:
            if ' to ' in value:
                date_range = value.split(' to ')
                first = checkDate(date_range[0])
                second = checkDate(date_range[1])
                if first == 'NULL' or second == "NULL":
                    value = "NULL"
                else:
                    #value = key+" BETWEEN '"+first+"' AND '"+second+"'"
                    value = True
            else:
                exact = checkDate(value)
                if exact == "NULL":
                    value = "NULL"
                else:
                    #value = key+" = date('"+exact+"')"
                    value = True
        params[key] = value

    elif key == "STATUS":
        if not value == 'NULL':
            if value.lower() == 'enabled' or value.lower() == 'disabled':
                status_test = value.upper()
                value = True
            else:
                value = "NULL"
        else:
            value = ""
        params[key] = value

    elif key in ["PHONE", "EMAIL", "ORGANIZATION", "NAME", "CONTACT"]:
        if not value == 'NULL':
            value = True
        else:
            value = ""
        params[key] = value
    elif key == 'DATASETS':
        if not value == 'NULL':
            value = True
            if value == "":
                ## dataset default to ALL
                arguments[key] = 'ALL'
        else:
            value == ""
        params[key] = value


val = []
fields = []
for ele in key_order:
    if params[ele]:
        fields.append(ele)
	val.append("'"+arguments[ele].replace("'","")+"'")
    
f_group = ','.join(fields)
v_group = ','.join(val)
#v_group = v_group.replace("'", "")

end = False
for key in params:
    if params[key] == "NULL":
        end = True
        print "Invalid "+key+" input"

if end:
    quit()

try:
    conn.execute("INSERT INTO "+arguments['TABLE']+" ("+f_group+") VALUES (%s);" % v_group)
except sqlite3.Error as er:
    print er.message

conn.commit()
conn.close()

