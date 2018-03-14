#!/usr/bin/env python

import os, sqlite3, sys

# make a script that can be used to easily update database host/group lists

#print no args given if no arguments given....
if len(sys.argv) == 1:
    print "no arguments specified"
    print "use '-h' for help options"
    exit()

# -h help menu
if sys.argv[1] == '-h':
    print 'updateHost.py is a simple tool for editting a database\n'
    print 'Usage: updateHost.py [-h ]'
    print 'Usage: updateHost.py [-list] [-remove host] [-update oldhost newhost] [-add host groups aliases currentalias]\n       [-addgroup host group] [-addalias host alias] [-editgroup host oldgroups newgroups] [-editalias host oldalias newalias]'
    #print what each command does
    print '\nOptions:'
    print '  -add:           adds a new row to the database | -add host groups aliases current_alias'
    print '                  (if no value for group,aliases,current_alias enter \'none\')'
    print '  -addalias:      adds a single alias to the list of aliases for a host | -addalias host alias'
    print '  -addgroup:      adds a single group to the list of groups for a host | -addgroup host group'
    print '  -replacealias:  replaces list of aliases for a host with a new list | -editalias host alias'
    print '  -replacegroup:  replaces list of groups for a host with a new list | -editgroup host group'
    print '  -h:             display help message and exit'
    print '  -list:          display the contents of the host table in the database'
    print '  -remove:        remove a certain host and all its data from the database | -remove host'
    print '  -update:        change a host name | -update oldHost newHost'
    exit()


def maxChar(temp):
    lines = []
    while len(temp) > 34:
        line = temp[:33]
        sp = line.rsplit(',', 1)
        line = sp[0]+','
        space = 34 - len(line)
        line += ' ' * space
        lines.append(line)
        temp = sp[1] + temp[33:]
    else:
        space = 34 - len(temp)
        temp += ' ' * space
        lines.append(temp)
    return lines


conn = sqlite3.connect('/home/oper/qc/chance/mcusers/assets/db/SERVER-USR.db')
null = True
# set up if statement that checks which command is called 
if sys.argv[1] == '-add':
    null = False
    if not len(sys.argv) == 6:
        print 'invalid number of arguments'
        print 'Usage: -add host groups aliases current_alias'
        print '        (if no value for group,aliases,current_alias enter \'none\')'
        exit()
    else:
        host = sys.argv[2]
        group = sys.argv[3]
        alias = sys.argv[4]
        curr = sys.argv[5]
        if group == 'none':
            group = ''
        if alias == 'none':
            alias = ''
        if curr == 'none':
            curr = ''
        conn.execute("INSERT INTO HOSTS (SERVER,GROUPS,ALIASES,CURRENT_ALIAS) VALUES ('"+host+"','"+group+"','"+alias+"','"+curr+"');")

#add new alias to the current list of aliases for a certain host    
if sys.argv[1] == '-addalias':
    null = False
    if not len(sys.argv) == 4:
        print 'invalid number of arguments'
        print 'Usage: -addalias host alias'
        exit()
    else:
        host = sys.argv[2]
        alias = sys.argv[3]
        prev = conn.execute("select ALIASES from HOSTS where SERVER like '"+host+"';")
        prev = prev.fetchall()[0][0]
        newAlias = prev+','+alias
        conn.execute("UPDATE HOSTS SET ALIASES = '"+newAlias+"' WHERE SERVER like '"+host+"';")

#add new group to the current list of group for a certain host
if sys.argv[1] == '-addgroup':
    null = False
    if not len(sys.argv) == 4:
        print 'invalid number of arguments'
        print 'Usage: -addgroup host group'
        exit()
    else:
        host = sys.argv[2]
        group = sys.argv[3]
        prev = conn.execute("select GROUPS from HOSTS where SERVER like '"+host+"';")
        prev = prev.fetchall()[0][0]
        newGroup = prev+','+group
        conn.execute("UPDATE HOSTS SET GROUPS = '"+newGroup+"' WHERE SERVER like '"+host+"';")
 
#replace the alias list of a host with a new list    
if sys.argv[1] == '-replacealias':
    null = False
    if not len(sys.argv) == 4:
        print 'invalid number of arguments'
        print 'Usage: -replacealias host alias'
        exit()
    else:
        host = sys.argv[2]
        alias = sys.argv[3]
        conn.execute("UPDATE HOSTS SET ALIASES = '"+alias+"' WHERE SERVER like '"+host+"';")

#replace the group list of a host with a new list
if sys.argv[1] == '-replacegroup':
    null = False
    if not len(sys.argv) == 4:
        print 'invalid number of arguments'
        print 'Usage: -replacegroup host group'
        exit()
    else:
        host = sys.argv[2]
        group = sys.argv[3]
        conn.execute("UPDATE HOSTS SET GROUPS = '"+group+"' WHERE SERVER like '"+host+"';")

#display the database in a viewer friendly form
if sys.argv[1] == '-list':
    null = False
    if not len(sys.argv) == 2:
        print 'invalid number of arguments'
        print 'Usage: -list'
    output = conn.execute("select * from HOSTS;")
    output = output.fetchall()

    #print the database for easy viewing
    print '---------      --------                           ---------                          ---------------'
    print '|SERVERS|      |GROUPS|                           |ALIASES|                          |CURRENT_ALIAS|'
    print '---------      --------                           ---------                          ---------------'
    for ele in output:
        if ele[1] == None:
            group = ''
            group += ' ' * 34
        else:
            group = ele[1]
        if None == ele[2]:
            alias = ''
            alias += ' ' * 34
        else:
            alias = ele[2]
        #set up server element 
        server = ele[0]
        space = 14 - len(server)
        server += ' ' * space
        #set up group element
        groups = maxChar(group)
        #set up alias element
        aliases = maxChar(alias)

        if len(groups) == 1 and len(aliases) == 1:
            print ' '+ server +' '+groups[0]+' '+aliases[0]+' '+ele[3]
        else:  
            print ' '+ server +' '+groups[0]+' '+aliases[0]+' '+ele[3]
            loop = max(len(groups), len(aliases))
            server = '              '
            placehold = ''
            placehold += ' ' * 34
            size = len(groups)
            while size < loop:
                groups.append(placehold)
                size = len(groups)
            size = len(aliases)
            while size < loop:
                aliases.append(placehold)
                size = len(aliases)
            for i in range(1, loop):
                print ' '+ server +' '+groups[i]+' '+aliases[i]
              
#run remove command and check for correct number of inputs  
if sys.argv[1] == '-remove':
    null = False
    if not len(sys.argv) == 3:
        print 'invalid number of arguments'
        print 'Usage: -remove host'
        exit()
    else:
        host = sys.argv[2]
        confirm = raw_input('Are you sure you wish to remove '+host+' from the database y/n? ')
        if str(confirm[0]) == 'y':
            conn.execute("DELETE from HOSTS where SERVER like '"+host+"';")
        else:
            print host+' not removed'

#run update command and check for correct number of inputs    
if sys.argv[1] == '-update':
    null = False
    if not len(sys.argv) == 4:
        print 'invalid number of arguments'
        print 'Usage: -update oldHost newHost'
        exit()
    else:
        new_val = sys.argv[3]
        old_val = sys.argv[2]
        conn.execute("UPDATE HOSTS SET SERVER = '"+new_val+"' WHERE SERVER like '"+old_val+"';")

if null:
    print 'no valid argument was given'

conn.commit()
conn.close()
