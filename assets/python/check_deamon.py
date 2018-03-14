#!/usr/bin/env python

#####################################################
## Script written by Chance Hammacher
## Contact the SSEC Satellite Date Services for help
#####################################################

import time, os, sqlite3, datetime

# sid machine list
sdi = ['sdilambda', 'sdimu', 'sdidelta', 'sdiepsilon', 'wallops', 'gilmore', 'sdigamma', 'goes14', 'sdizeta', 'sdiiota', 'sdieta', 'sdibeta', 'goes15', 'sditheta', 'sdikappa', 'eastl', 'easts', 'westl', 'wests']

## tryscp( file_path_temp, file_path, host ) ##
# takes temp file and real file and host that file will be sent to 
# returns nothing but trys to send file to a specific machine and logs results
def tryscp(file_path_temp, host, scp_filename):
    log = open(log_path+scp_filename+'_'+host+'.log', 'a+')
    now = datetime.datetime.now().strftime('%Y%j-%H:%M')
    try:
        if host in sdi:
            os.system("scp -q {0} root@{1}:/data/{2}".format(file_path_temp, host, scp_filename))
        else:
            os.system("scp -q {0} mcadde@{1}:/home/mcadde/mcidas/data/{2}".format(file_path_temp, host, scp_filename))
    except Exception, e:
        #print str(e)
        log.write(str(e)+' '+now+'\n')
        
    else:
        #print "scp to host: {0} successfull".format(host)
        log.write("scp to host: {0} successfull "+now+"\n".format(host))
    log.close()


#get list of hosts for sending to ALL
conn = sqlite3.connect('/home/oper/qc/chance/mcusers/assets/db/SERVER-USR.db')


#paths
path = '/home/oper/qc/chance/mcusers/assets/admin/check/'
log_path = '/home/oper/qc/chance/mcusers/assets/admin/log/'
qc_path = '/home/oper/datacenter/oper_admin/admin/'

test=True
#start the deamon
while test:
    #get list of hosts for sending to ALL
    conn = sqlite3.connect('/home/oper/qc/chance/mcusers/assets/db/SERVER-USR.db')
    #check directory for files
    while not os.listdir(path) == []:
        #get the first file in list and split it to host, filename
        first_fname = os.listdir(path)[0]

        ## info[0] is host to send to info[1] is the end filename
        info = first_fname.split('.', 1)
           
        fname_info = info[1].split('.')
 
        ##############check the current alias of each alias to be sure to only send to a machine once###########
        if fname_info[1] in ['USR', 'PRJ']:
            tryscp(path+first_fname, info[0], info[1])

    conn.close()
    time.sleep(120)
