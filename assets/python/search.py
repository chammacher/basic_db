#!/usr/bin/env python

#####################################################
## Script written by Chance Hammacher
## Contact the SSEC Satellite Date Services for help
#####################################################

import os, sqlite3, datetime, cgi, json

#need this line for ajax output
print "Content-type: text/html\n"

conn = sqlite3.connect('/home/oper/qc/chance/mcusers/assets/db/SERVER-USR.db')

# get cgi params from js script
fs = cgi.FieldStorage()
arguments = {}
for key in fs.keys():
    arguments[key] = fs.getvalue(key)


## List of common words in org names
common = ['on','in','to','with','and','of','at','be','from','working','for','-','or', '']

## checkTable( TABLE name, column, input to check ##
## checkTable: receives all elements from column and check for matches/similarities with input and returns
def checkTable(tableName, column, check): 
    rows = conn.execute('select '+column+' FROM '+tableName+';')
    checks = rows.fetchall()
    searches = []
    for row in checks:
      if not row[0] is None:
        if check.lower() in row[0].lower():
            if not row[0].lower() in searches:
                searches.append(row[0].lower())
        vari = check.split()
        if len(vari) > 1:
            for ele in vari:
                if ele.lower() in row[0].lower() and not row[0].lower() in searches and not ele.lower() in common:
                    searches.append(row[0].lower())
    return searches;

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
 
#init params before assigning data to it
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
    #get option if it exists
    option=''
    if value == "  ":
        pass
    elif not value == 'NULL':
        test = value.split()
        if test[len(test)-1] == 'OR':
            option = ' OR'
            value = value[0:len(value)-3]
        if test[len(test)-1] == 'AND':
            option = ' AND'
            value = value[0:len(value)-4]
    if value == '' or value == '  ':
        params[key] = key+" LIKE '%'"+option
    elif key == "USRID":
        if not value == 'NULL':
            if value.isalpha() and len(value) <= 4:
                value = "USRID LIKE '%"+value+"%'"+option
            else:
                value = "NULL"
        else:
            value = ""
        params[key] = value
    
    elif key == "PROJID":
        if not value == 'NULL':
            if value.isdigit() and len(value) <= 4:
                value = "PROJID LIKE '%"+value+"%'"+option
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
                    value = key+" BETWEEN '"+first+"' AND '"+second+"'"+option
            else:
                exact = checkDate(value)
                if exact == "NULL":
                    value = "NULL"
                else:
                    value = key+" = date('"+exact+"')"+option
        params[key] = value

    elif key == "STATUS":
        if not value == 'NULL':
            if value.lower() == 'enabled' or value.lower() == 'disabled':
                status_test = value.upper()
                value = "STATUS LIKE '"+status_test+"'"+option
            else:
                value = "NULL"
        else:
            value = ""
        params[key] = value

    elif key in ["PHONE", "EMAIL", "ORGANIZATION", "NAME", "CONTACT", "DATASETS"]:
        if not value == 'NULL':
            check = checkTable(arguments['TABLE'], key, value)
            if not len(check) == 0:
                q = []
                for ele in check:
                    q.append(key+" LIKE '%"+ele+"%'")
                value = " OR ".join(q)+option
            else:
                value = ""
        else:
            value = ""
        params[key] = value

##############################
## check for any NULL values signaling there was a wrong input
verify = False
count = 0
for key in key_order:
    value = params[key]
    if not value == False:
        if value == "":
            count += 1
        if value == 'NULL':
            #FIGURE OUT THE CORRECT OUTPUT METHOD
            params[key] = 'not a valid input'
            verify = True
    else:
        params[key] = key+" LIKE '%'"

#check if valid input or not
if verify:
    print json.dumps(params)
    exit()

q = []
for key in key_order:
    value = params[key]
    if value == '':
        pass
    else: 
        q.append(value)

#query = ' '.join(str(value) for key, value in params.items())
query = ' '.join(q)

#if count is 9 on users or 7 on projects select * from table
if arguments['TABLE'] == 'USERS' and count == 9:
    output = conn.execute("SELECT * FROM "+arguments['TABLE']+";")
elif arguments['TABLE'] == 'PROJECTS' and count == 7:
    output = conn.execute("SELECT * FROM "+arguments['TABLE']+";")
else: 
    output = conn.execute("SELECT * FROM "+arguments['TABLE']+" WHERE "+query+";" )

print json.dumps(output.fetchall())

conn.close()
