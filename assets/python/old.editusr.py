#!/usr/bin/env python

#####################################################
## Script written by Chance Hammacher
## Contact the SSEC Satellite Date Services for help
#####################################################

import os, sqlite3, cgi, datetime

## checkHost( machine, host, send ) ##
# take host which is a string input to check against sqlite db send to server.usr file on specific machine
# machine is the sever to send to 
# send is if the file is to create SERVER.USR file
# returns 1 or 0 depending on if it finishes
def checkHost(machine, host, send):
    #open server.usr file to read and temp to write to
    if send:
        s = trycatch(cvs_path+'SERVER'+table, 'r')
        t = trycatch(temp_path+'SERVER'+table+'.temp', 'w+')
    #open host.special.temp file that needs to be changed
    update = trycatch(temp_path+host+table+'.SPECIAL.temp', 'w+')
    # write changes to temp files if not disabled
    if 'DISABLED' in arguments:
        pass
    else:
        update.write('\t'.join(arguments[1:len(arguments)])+'\n')
        if send:
            t.write('\t'.join(arguments[1:len(arguments)])+'\n')     

    #check if host.special file exists to update and read from
    if os.path.isfile(cvs_path+host+table+'.SPECIAL'):
        #open file to read
        h = trycatch(cvs_path+host+table+'.SPECIAL', 'r')
        for line in h:
            #if updated user already in file dont write to new file
            if arguments[1] == line.split()[0]:
                pass
            else:
                update.write(line)
                if send:
                    t.write(line)
        ## end loop ##
        h.close()
    update.close()
    tryscp(temp_path+host+table+'.SPECIAL.temp', host, host+table+'.SPECIAL', False)
    if send:
        #read all of the server.usr file to the temp file
        for line in s:
            if arguments[1] == line.split()[0]:
                pass
            else:
                #else write to new file
                t.write(line)
        ## end loop ##
        s.close()
        t.close()
        #next get all alias .usr.special files and add them to server.usr.temp
        #get list of alias from sqlite
        alias = conn.execute("select ALIASES from HOSTS where SERVER like '"+host+"';")
        alias = alias.fetchall()
        a = alias[0][0].split(',')
        a_list = []
        for ali in a:
            a_list.append(ali)

        readAlias(temp_path+'SERVER'+table+'.temp', a_list)
        tryscp(temp_path+'SERVER'+table+'.temp', machine, 'SERVER'+table, False)        


## readAlias ( temp, alias ) ##
# temp is open temp filename | alias is the list of aliases to read from
# uses host to get its alias and updates temp with data from all those
def readAlias(temp, alias):
    #for each alias that exists update temp
    for ali in alias:
        #check if ali exists
        if os.path.isfile(cvs_path+ali+table+'.SPECIAL'):
            #if it does open to read 
            a = trycatch(cvs_path+ali+table+'.SPECIAL', 'r')
            #open temp to read and to write
            t = trycatch(temp, 'r')
            #create empty array of existing users
            existing = []
            #for each line in server.temp check if a users already exists
            for l in t:
                u = l.split()[0]
                for line in a:
                    if line.split()[0] == u:
                        existing.append(u)
                ## end loop ##
                a.seek(0)
            ## end loop ##
            # open temp up to write 
            tw = trycatch(temp, 'a')
            #read alias file in
            for line in a:
                if line.split()[0] in existing:
                    pass
                else:
                    tw.write(line)
            #close any open files
            t.close()
            a.close()
            tw.close()
    ## end loop ##     

## trycatch( filename , p ) ##
# take filename and permission on the file
# returns a file that was attempted to be opened
def trycatch(filename, p):
    r = ''
    try:
        r = open(filename, p)
    except Exception, e:
        print str(e)
    
    return r


## tryscp( file_path_temp, file_path, host, remove ) ##
# takes temp file and real file and host that file will be sent to 
# remove: remove ending or not
# returns nothing but trys to send file to a specific machine and logs results
def tryscp(file_path_temp, host, scp_file, remove):
    if remove:
        file_path_temp_temp = ".".join(file_path_temp.split('.')[:-1])
        os.system("mv {0} {1}".format(file_path_temp_temp, file_path_temp)) 
        file_path_temp = file_path_temp_temp
    try:
        os.system("mv {0} {1}/{2}.{3}".format(file_path_temp, check_path, host, scp_file))
        #os.system("rm {0}".format(file_path_temp))
    except Exception, e:
        print str(e)
   

## setGroup( host ) ##
# takes a host name of a special group and sends all the needed group files to the machine
# returns
def setGroups(host):
    grp_array = []
    grp_file = open(temp_path+host[0]+'.GRP.SPECIAL.temp', 'r')
    hsplit = host[1].split(',')
    ## for each group in file create a separate file and send it to that machine
    for line in grp_file:
        a = line.split()
        if a[len(a)-1] in host[1]:
            if os.path.isfile(temp_path+a[len(a)-1]+'.USR'):
                grp = open(temp_path+a[len(a)-1]+'.USR', 'a')
            else:
                grp = open(temp_path+a[len(a)-1]+'.USR', 'w+')
                grp_array.append(a[len(a)-1])
            grp.write('\t'.join(a[:len(a)-1])+'\n')
            grp.close()
    #for each group file that was created scp it to host
    for ele in grp_array:
        tryscp(temp_path+ele+'.USR', host[0], ele+'.USR', False)
        
    grp_file.close()

print "Content-type: text/html\n"

# get cgi params from js script
#s = cgi.FieldStorage()
#rguments = fs.getvalue('data')
#print arguments

##### TEST INPUT LINES ######
#arguments = ['USERS','CHAN','empty','ENABLED','empty','Chance Hammacher','SSEC','empty','empty','SERVER:indoex,msg,msgbak - GROUP:IND3HR,IODC3HR,MSG3HR,MSG-GT24']
arguments = ['USERS','CHAN','empty','ENABLED','empty','Chance Hammacher','SSEC','empty','empty','ALL']
#arguments = ['USERS','CHAN','empty','ENABLED','empty','Chance Hammacher','SSEC','empty','empty','SERVER:indoex - GROUP:IND3HR,END3HR']
#############################

#connect to database and get list of hosts####################################
conn = sqlite3.connect('/home/oper/qc/chance/mcusers/assets/db/SERVER-USR.db')
out = conn.execute('select SERVER from HOSTS;')
hosts = out.fetchall()

#check for users or projects then set up file paths
table = '.PRJ'

if len(arguments) == 10:
    table = '.USR'

#path to SERVER.USR
cvs_path = '/home/oper/datacenter/oper_admin/admin/'
################################################################
temp_path = '/home/oper/qc/chance/mcusers/assets/admin/'
check_path = os.path.join(temp_path, 'check')
server = os.path.join(cvs_path, 'SERVER'+table)
temp = os.path.join(temp_path, 'SERVER'+table+'.temp')


dataset = arguments[len(arguments)-1]
arguments.remove(arguments[len(arguments)-1])

while 'empty' in arguments:
        arguments.remove('empty')

## generate log file each time this script is called########################
curr_time = datetime.datetime.now().strftime('%Y%j%H%M')

## Just a layout for now not real values
if dataset == 'ALL':
    print 'in the ALL check'    
    #if it is ALL update SERVER.USR to correct values and send to ALL machines
    su = trycatch(server,'r')


    #permission denied here
    tu = trycatch(temp, 'w+')

    prev = False
    ## copy server.usr to temp file to push changes 
    for line in su:
        #########if line contains data to be changed, change it########
        if arguments[1] == line.split()[0]:
            prev = True
            if 'DISABLED' in arguments:
                pass
            else:
                tu.write('\t'.join(arguments[1:len(arguments)])+'\n')
        else:
            #else write to new file
            tu.write(line)
        # check if user was previously in file
    if not prev:
        if 'DISABLED' in arguments:
            pass
        else:
            tu.write('\t'.join(arguments[1:len(arguments)])+'\n')
    su.close()
    tu.close()
    check_array = []
    #find all active machines 
    for host in hosts:
        out = conn.execute("select CURRENT_ALIAS from HOSTS where SERVER like '"+host[0]+"';")
        out = out.fetchall()[0]        
        if not out in check_array:
            check_array.append(out[0].split('.')[0])
            
    print check_array
    for h in check_array:
        #get alias for each machine
        #get list of alias from sqlite
        alias = conn.execute("select ALIASES from HOSTS where SERVER like '"+h+"';")
        alias = alias.fetchall()
        a = alias[0][0].split(',')
        a_list = []
        for ali in a:
            a_list.append(ali)
       
        checkHost(h, h, True)
        #readAlias(temp+'.'+h[0].split('.')[0], a_list) 
        #######scp file to all machines######
        #tryscp(temp+'.'+h.split('.')[0], h[0].split('.')[0], 'SERVER'+table, True)
    
else:
    ##make changes to special file?
    if 'SERVER' in dataset:
        dataset = dataset.split(' - ')
        ## dataset[0] should be server
        ## dataset[1] should be groups
        if len(dataset) == 1:
            if 'SERVER' in dataset[0]:
                servers = dataset[0].split(':')[1].split(',')
                check_array = []
                for host in servers:
                    out = conn.execute("select CURRENT_ALIAS from HOSTS where SERVER like '"+host+"';")
                    out = out.fetchall()[0]
                    if not out in check_array:
                        check_array.append(out)
                        checkHost(out[0].split('.')[0], host, True)
                    else:
                        checkHost(None, host, False)
        else:
            #### check grp file and send to GRP.USR
            #dataset[0] is servers dataset[1] is groups
            servers = dataset[0].split(':')[1].split(',')
            groups = dataset[1].split(':')[1].split(',')
            check_array = []
            ## get list of servers and their groups
            host_db = conn.execute("select * from HOSTS;")
            host_db = host_db.fetchall()
            # loop through all the servers and check groups
            for host in host_db:
                #if host in list of server
                if host[0] in servers:
                    # set variable to check if server has groups in it.
                    check = False
                    # for each group in this server
                    for group in groups:
                        # check if group goes with host
                        if group in host[1]: 
                            check = True
                            
                            # create temp file to make changes too
                            group_temp = trycatch(temp_path+host[0]+'.GRP.SPECIAL.temp', 'a+')
                            # if no special group file already create one.
                            if not group_temp == '': 
                                # check if user should be disabled or not
                                if 'DISABLED' in arguments:
                                    pass
                                else:
                                    group_temp.write('\t'.join(arguments[1:len(arguments)])+' '+group+'\n')
                             
                    # if groups are present for server update temp file
                    if check:
                        if os.path.isfile(cvs_path+host[0]+'.GRP.SPECIAL'):
                            #if file exists read its contents to temp file and remove old
                            gf = trycatch(cvs_path+host[0]+'.GRP.SPECIAL', 'r')
                            
                            # for each line check if user changed is present to remove old permissions
                            for line in gf:
                                if line.split()[0] == arguments[1]:
                                    pass
                                else:
                                    if not group_temp == '':
                                        group_temp.write(line)
                            gf.close()
                            if not group_temp == '':
                                group_temp.close()
                            setGroups(host)
                            ### replace grp file
                            tryscp(temp_path+host[0]+'.GRP.SPECIAL.temp', host[0], host[0]+'.GRP.SPECIAL', False)
                    # if server without group just make special usr file
                    if not check:
                        out = conn.execute("select CURRENT_ALIAS from HOSTS where SERVER like '"+host+"';")
                        out = out.fetchall()[0]
                        if not out in check_array:
                            check_array.append(out)
                            checkHost(out.split('.')[0], host, True)
                        else:
                            checkHost(None, host, False)

conn.close()
