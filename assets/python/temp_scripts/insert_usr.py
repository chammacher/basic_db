#!/usr/bin/env python

import sqlite3

path = '/home/oper/qc/chance/mcusers/assets/db/SERVER-USR.db'
conn = sqlite3.connect(path)

out = conn.execute('select USRID from USERS;')
numbs = []
for ele in out.fetchall():
    numbs.append(ele[0])


summary = '/home/oper/datacenter/oper_admin/admin/summary'
f = open(summary, 'r')
temp = ''
l = []
dataset = ['null']

for line in f:
    line = line.replace('\n','')
    if ' ******' in line:
        
        if temp == line.split()[2]:
            l.append(line.split()[7])
        else:
            dataset = ['GROUP:'+(',').join(l), temp]
            l = []
            l.append(line.split()[7])
        temp = line.split()[2]
    elif 'YUAN' in line:
        pass
        #conn.execute("update USERS set DATASETS = 'ALL' where USRID like '"+line.split()[0]+"';")
        break
    else:
        if line.split()[0] in numbs:
            pass
            #conn.execute("update USERS set DATASETS = 'ALL' where USRID like '"+line.split()[0]+"';")
        else:
            pass
    if not dataset[0] == 'null':
        pass
        #conn.execute("update USERS set DATASETS = '"+dataset[0]+"' where USRID like '"+dataset[1]+"';")

test = '/home/oper/qc/chance/mcusers/assets/python/temp_scripts/temp.txt'
tester = open(test, 'w')
for line in f:
    tester.write(line)

#conn.commit()
