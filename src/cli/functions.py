import paramiko
import os

def connect(ip, user, password):
    ssh = paramiko.SSHClient()
    ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    ssh.connect(hostname=str(ip), username=str(user), password=str(password))
    return ssh

def change_master(newmas):
    try:
        os.environ['MASTER_NODE'] = newmas
        print("Master node changed to: " + newmas)
    except:
        print('Master node ip was not changed')