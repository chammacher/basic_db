#!/usr/bin/env python

#####################################################
## Script written by Chance Hammacher
## Contact the SSEC Satellite Date Services for help
#####################################################
import os, sqlite3, cgi, datetime, shutil

print "Content-type: text/html\n"

# get cgi params from js script
fs = cgi.FieldStorage()
arguments = fs.getvalue('data')
#print arguments


################### methods ####################
## create_file ( string: server )
# server: name of a server to get its aliases
# return: returns an open file contianing users specific to that machine or None if no file is opened.
def create_file(server):
    try:
        f = open(check_path_temp+server+".SERVER"+file_table, 'w+')
    except:
        return None

    # query host list to get all alias of server
    alist = conn.execute("select ALIASES from HOSTS where SERVER like '"+server+"';")
    alist = alist.fetchall()
    
    slist = []
    for ele in alist:
        for e in ele[0].split(','):
            if not e in slist:
                slist.append(e)
    #slist at this point contains the server names that corrispond to a used alias
     
    # create list of users using slist of server aliases 
    ulist = []
    uNamelist = []
    for s in slist:
        
        # query the database for all users that have the server in their dataset.
        pUsers = conn.execute("select * from "+table+" where DATASETS like '%{0}%' and STATUS like 'enabled'".format(s))
        pUsers = pUsers.fetchall()
        #add all unique users to a list
        for t in pUsers:
            # t is a tuple of a user
	    if not t[0] in uNamelist: 
                ulist.append(t)
                uNamelist.append(t[0])
    
    
    # check for each users if they a) just have that server b) are in a group on that server c) no users so do nothing
    for ele in ulist:
        ele = filter(None, ele)
        
        # this is the variable used to hold the info on the dataset of each user.
        datasets = ele[len(ele)-1]
        valid = check_dataset_server(datasets, server)
        if valid:
            # if valid is true then the user should be added to the file
            ele = filter(None, ele)
            f.write('\t'.join(ele[0:-1])+'\n')

    return f


## check_dataset_server ( string:datasets , server)
# datasets: string in the form SERVER:____ - GROUP:_____ | server: a server to check for
# return: true if this dataset matches server given. (sister method checks if a group is in a dataset.)
def check_dataset_server(datasets, server):
    dataset = datasets.split('-', 1)
    dlist = False
    # if no group present return true
    if len(dataset) == 1:
	dlist = True
    else:
        # next check if the server is associated with a group
        server_list = dataset[0].split(':')[1].split(',')
        group_list = dataset[1].split(':')[1].split(',')
	
	# query database for all servers in server_list and check their groups.
        server_query = conn.execute("select GROUPS from HOSTS where SERVER like '" + server + "';")
	server_query = server_query.fetchall()
        
        if  len(server_query) == 0 or server_query[0][0] == None:
            return True
        # for each element returned from query, check if it has groups in group_list
        if len(set(group_list).intersection(server_query[0][0].split(','))) == 0:
            dlist = True
        else:
            dlist = False
        
    return dlist

## check_dataset_group ( string:datasets , group)
# datasets: string in the form SERVER:____ - GROUP:_____ | group: a group to check for
# return: list of all servers associated with this group in the dataset if not return empty list
def check_dataset_group(datasets, group):
    dataset = datasets.split('-', 1)
    dlist = []
    # if no group present return true
    if len(dataset) == 1:
        dlist = []
        return dlist
    else:
        # next check if the group associated with a server
        server_list = dataset[0].split(':')[1].split(',')
        server_list[len(server_list)-1] = server_list[len(server_list)-1].split()[0]
        #group_list = dataset[1].split(':')[1].split(',')

        # query database for all servers in server_list and check their groups.
        server_query = conn.execute("select SERVER from HOSTS where GROUPS like '%" + group + "%';")
        server_query = server_query.fetchall()
        server_query = [i[0] for i in server_query]
        
        if len(server_query) == 0:
            dlist = []
            return dlist
        # for each element returned from query, check if it has groups in group_list
        intersect = set(server_list).intersection(server_query)
        
        if len(intersect) == 0:
            dlist = []
            return dlist
        else:
            for s in intersect:
                dlist.append(s)

    return dlist

## find_backup ( string:server )
# server is a string of a server that is used to find its server
# returns a backup server string for the server param
def find_backup(server):
    # start by getting all of the possibly aliasses for the server
    al = conn.execute("select ALIASES from HOSTS where SERVER like '"+server+"';")
    al = al.fetchall()
    
    # next get the current alias of the server
    curr = conn.execute("select CURRENT_ALIAS from HOSTS where SERVER like '"+server+"';")
    curr = curr.fetchall()

    # contains a list of aliases with no duplicates
    slist = []
    for ele in al:
        for e in ele[0].split(','):
            if not e in slist:
                slist.append(e)
    
    # for each alias check if its current alias is the same as the servers, if not it is the back up...
    for ele in slist:
        check = conn.execute("select CURRENT_ALIAS from HOSTS where SERVER like '"+ele+"';")
        check = check.fetchall()
       
        if not check == curr:
            return check[0]
    return ''


## move_file()
# moves all the new files created from temp directory to normal directory to be processed by the deamon
def move_file():
    direc = os.listdir(check_path_temp)
    #for each file in directory move it to finshed dir
    for f in direc:
        if file_table in f:
            os.rename(check_path_temp+f, check_path+f)


##### TEST INPUT LINES ######
#arguments = ['USERS','CHAN','empty','ENABLED','empty','Chance Hammacher','SSEC','empty','empty','SERVER:indoex,msg,msgbak - GROUP:IND3HR,IODC3HR,MSG3HR,MSG-GT24']
#arguments = ['USERS','CHAN','empty','ENABLED','empty','Chance Hammacher','SSEC','empty','empty','ALL']
#arguments = ['USERS','CHAN','empty','ENABLED','empty','Chance Hammacher','SSEC','empty','empty','SERVER:msg,dcserve1']
#############################

#check for users or projects then set up file paths
file_table = '.PRJ'
table = arguments[0]

if len(arguments) == 10:
    file_table = '.USR'

# get the dataset from the input and remove it from the list
dataset = arguments[len(arguments)-1]
arguments.remove(arguments[len(arguments)-1])

# remove all empty arguments from list
while 'empty' in arguments:
        arguments.remove('empty')


################################################################
temp_path = '/home/oper/qc/chance/mcusers/assets/admin/'
log_path = os.path.join(temp_path, 'log/')
check_path = os.path.join(temp_path, 'check/')
check_path_temp = os.path.join(temp_path, 'temp/')
################################################################


#connect to database and get list of hosts####################################
conn = sqlite3.connect('/home/oper/qc/chance/mcusers/assets/db/SERVER-USR.db')
#out = conn.execute('select * from USERS;')
#ALL = out.fetchall()


## Open Log file ###############################################
try:
    log = open(log_path+'editusr.log', 'a+')
except:
    print 'caught error while openning log'


# first figure out which files need to be created ie: ALL or specific server or special group or a combination
if dataset == 'ALL':
    #if dataset is all get list of dataset that are all AND.....
    out = conn.execute("select * from "+table+" where DATASETS like 'ALL' and STATUS like 'enabled'")
    out = out.fetchall()
    # get list of servers in use to send files too
    curr_server = conn.execute("select CURRENT_ALIAS from HOSTS;")
    curr_server = curr_server.fetchall()
    # create a list containing only unique servers
    servers = []
    for ele in curr_server:
        if not ele[0] in servers and not ele[0] == None:
            servers.append(ele[0])

    # for each server get server access users to a file to add with all users
    for ele in servers:
        #call function that takes a server name and creates a file with specific users for all its aliases.
        # should return a file that can be used to add all the rest of the ALL users.
        filename = create_file(ele.split('.')[0]) 
        #check if filename was opened correctly
        if filename is None:
            now = datetime.datetime.now().strftime('%Y%j %H%M%S')
            log.write("Unable to create file for {0} at {1}\n".format(ele, now))
            exit()
        
        for row in out:
            row = filter(None, row)
            filename.write('\t'.join(row[0:-1])+'\n')
        filename.close()
    

# if not in all must check for either server or group or both.
else:
    # split dataset on '-' to see if special group file needs to be created
    dataset_check = dataset.split('-', 1)
    
    #check if just server or has group involved
    if len(dataset_check) == 1:
        out = conn.execute("select * from "+table+" where DATASETS like 'ALL' and STATUS like 'enabled'")
        out = out.fetchall()
        #this should be just server
        curr_server = dataset_check[0].split(':')[1].split(',')
        for ele in curr_server:
            filename = create_file(ele.split('.')[0])
            backup = find_backup(ele.split('.')[0])[0].split('.')[0]
   
            #check if filename was opened correctly
            if filename is None:
                now = datetime.datetime.now().strftime('%Y%j %H%M%S')
                log.write("Unable to create file for {0} at {1}\n".format(ele, now))
                exit()
            #add users under ALL category to server file
            for row in out: 
                row = filter(None, row)
                filename.write('\t'.join(row[0:-1])+'\n')
            filename.close()
            ## copy file with backup as the prefix instead
            shutil.copy(check_path_temp+ele.split('.')[0]+'.SERVER'+file_table, check_path_temp+backup+'.SERVER'+file_table)
        
    else:
        #this should have a group
        #dataset[0] is servers dataset[1] is groups
        servers = dataset_check[0].split(':')[1].split(',')
        groups = dataset_check[1].split(':')[1].split(',')
        #one for loop on each to check for unique values
        # check for servers that dont have a group 
        serv = []
        for ele in servers:
            if check_dataset_server(dataset, ele.split()[0]):
                serv.append(ele)
        # create file for servers with no group
        for s in serv:
            filename = create_file(s.split('.')[0])
            backup = find_backup(s.split('.')[0])[0].split('.')[0]

            #check if filename was opened correctly
            if filename is None:
                now = datetime.datetime.now().strftime('%Y%j %H%M%S')
                log.write("Unable to create file for {0} at {1}\n".format(ele, now))
                exit()
            #add users under ALL category to server file
            for row in out:
                row = filter(None, row)
                filename.write('\t'.join(row[0:-1])+'\n')
            filename.close()
            ## Copy file with backup as the prefix instead
            shutil.copy(check_path_temp+s.split('.')[0]+'.SERVER'+file_table, check_path_temp+backup+'.SERVER'+file_table)

        # next check servers with group and create file
        for g in groups:
            # this returns list of SERVER, group, group1, group2.....
            sGroup = check_dataset_group(dataset, g)
                
            if len(sGroup) == 0:
                now = datetime.datetime.now().strftime('%Y%j %H%M%S')
                log.write("Error finding group values for {0} at {1}\n".format(g, now))
                exit()
            
            for ele in sGroup:
                #not get all the users that have this group and check if they have a server that goes with the current server
                user_potential = conn.execute("select * from "+table+" where DATASETS like '%"+g+"%' and DATASETS like '%,"+ele+",%' and STATUS like 'enabled'")
                user_potential = user_potential.fetchall()                 

                #try and open file for group to 
                try:
                    filename = open(check_path_temp+ele+'.'+g+file_table , 'w+')
                except: 
                    #write to log couldn't open file
                    now = datetime.datetime.now().strftime('%Y%j %H%M%S')
                    log.write("Unable to open file for group {0} at {1}\n".format(g, now))
                    exit()
                 
                # find back up for g here and create its file as well...
                backup = find_backup(g)[0].split('.')[0]

                # for each user add them to the file
                for u in user_potential:
                    u = filter(None, u)
                    filename.write('\t'.join(u[0:-1])+'\n')

                filename.close()
                ## copy file with backup as the prefix here 
                shutil.copy(check_path_temp+ele+'.'+g+file_table, check_path_temp+backup+'.'+g+file_table)

move_file() 
