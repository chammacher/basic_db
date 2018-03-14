#!/usr/bin/env python

import os, sqlite3

#get list of hosts for sending to ALL
conn = sqlite3.connect('/home/oper/qc/chance/mcusers/assets/db/SERVER-USR.db')
output = conn.execute('select SERVER,GROUPS from HOSTS;')
hosts = output.fetchall()
conn.close()

print "Content-type: text/html\n"
print "{"

# for each host check the current host and update the database
for host in hosts:
    # host[0] gets the host name
    if host[1] == None:
        print '"'+host[0]+'": [],'
    else:
	groups = host[1].split(',')
        data = '", "'.join(groups)
        print '"'+host[0]+'": ["'+data+'"],'
print '"ALL": []'
print "}"
    
