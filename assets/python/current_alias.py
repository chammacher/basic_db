#!/usr/bin/env python

import os, sqlite3

#get list of hosts for sending to ALL
conn = sqlite3.connect('/home/oper/qc/chance/mcusers/assets/db/SERVER-USR.db')
output = conn.execute('select SERVER from HOSTS;')
hosts = output.fetchall()

# for each host check the current host and update the database
for host in hosts:
    # host[0] gets the host name
    try:
        #vari = os.system("ssh {0} hostname".format(host[0]))
        vari = os.popen("ssh {0} hostname".format(host[0])).read()
        out = vari.replace('\n', '')
        
        # update sqlite with out as current
        update = conn.execute("update HOSTS set CURRENT_ALIAS = ? where SERVER like '"+host[0]+"';", (out,))
    except Exception, e:
        print str(e)

conn.commit()
conn.close()
