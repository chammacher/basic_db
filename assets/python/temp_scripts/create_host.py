#!/usr/bin/env python

import sqlite3

path = '/home/oper/qc/chance/mcusers/assets/db/SERVER-USR.db'
conn = sqlite3.connect(path)

host = '/home/oper/qc/chance/mcusers/assets/db/temp.txt'
f = open(host, 'r')

for line in f:
    serv_name = line.split(':')[0]
    grp_name = line.split(':')[1].replace('\n','')
    for name in serv_name.split(','):
        print name, grp_name 
        out = conn.execute("update HOSTS set GROUPS = "+grp_name+" where SERVER like '"+name+"';")

conn.commit()
