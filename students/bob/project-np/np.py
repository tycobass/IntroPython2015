#!/usr/bin/python



# np partial, broken down into individual functions:

import nmap # http://xael.org/pages/python-nmap-en.html
import paramiko # http://www.paramiko.org/
import getpass # https://docs.python.org/3/library/getpass.html

def np():
    
    hosts = input(
'''
Enter nmap-friendly address or range. 
(e.g. 127.0.0.1-255 or 127.0.0.0/24)
Input address or range: '''
    )

    user = input('Input username for ssh: ')
    pw = getpass.getpass('Input password for ssh: ')
    commands = input("Input commands, (e.g. 'hostname ; uptime'): ")

    lh, dh, nossh = mapper(hosts)  # calls the nmap portion
    
    pusher(lh, user, pw, commands) # call the paramiko portion


def mapper(hosts):
    ''' 
Take nmap-formatted IP address range,
and return 3 lists: hosts listening on p22,
                    offline hosts, and
                    online hosts with p22 closed  
    '''
    nm = nmap.PortScanner()

    lh = [] # listening hosts
    dh = [] # down hosts
    nossh = [] # closed 

    nm.scan(hosts, '22', '-vv') # run nmap scan against hosts on tcp.22

    ### Future expansion: add something for error scan:
    ### Test existance of the following key to know if something went wrong : ['nmap']['scaninfo']['error']

    for i in nm.all_hosts(): # for all hosts in scanned range
        if nm[i]['status']['state'] == 'up':
            if nm[i]['tcp'][22]['state'] == 'open':
                lh.append(i)
            else:
                nossh.append(i)
        else: 
                dh.append(i) 
    return(lh,dh,nossh)

def pusher(lh,user,pw,commands):

    output = dict()

    ssh = paramiko.SSHClient()
    ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy()) # allow/auto-add all hosts attempted

    print(
'''
Warning: this module automatically adds 
all listed hosts to the known_hosts file.  
Only use this in lab or on trusted networks.\n'''  # probably not the best place for this warning to go...
    )

    for i in lh:
        #try:
            ssh.connect(hostname=i,username=user,password=pw,timeout=10.0) #timeout hardcoded to 2s
            
            stdin, stdout, stderr = ssh.exec_command(commands)
            #print(stderr.readlines())
            for line in stdout:
                line = stdout.readline()
                if i not in output:
                    output[i] = [line]
                else:
                    output[i].append(line)
        #except BadAuthenticationException:     #  <-- got a NameError?
        #    print ('Bad username or password for', i) 
        #    ## write this to log
        #except timeout:
        #    print ('Connection timed out after 2 seconds.  Is {} really up?'.format(i))
        #except SSHException:
        #    print ('Session not active......')
    print(output) # do something fancier with this in the next revision


if __name__=='__main__':
    print(np())