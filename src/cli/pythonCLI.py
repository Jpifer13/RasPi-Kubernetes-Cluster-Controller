"""
This is a cli utility to check status' of raspberry pi's on local network

The repo that is being used can be found here: https://github.com/Jpifer13/python-cli
"""
import click
import requests
import paramiko
import os
import subprocess

from cli.functions import connect, \
    change_master
from cli.values import user, \
    password, \
    master

@click.group()
@click.option('--ip', '-i', help='This is the ip address of the device you wish to connect to.')
@click.option('--new_ip', '-ni', help='This is the ip address of the new device.', default="")
@click.option('--password', '-p', help='The password of the device you are trying to connect to.',)
@click.option('--user', '-u', help='The username of the device you are trying to connect to.',)
@click.option('--command', '-c', help='The command you wish to run on each device.',)
@click.option('--syspass', '-sp', help='The new system password')
@click.option('--sysuser', '-su', help='The new system username')
@click.option('--bulk', '-b', help='States whether this is a bulk action.', type=bool, default=False)
@click.option('--newmas', '-nm', help='This tag is used if you are changing the master node ip.', default=master)
@click.pass_context
def cli(ctx, ip, user, password, command, sysuser, syspass, bulk, new_ip, newmas):
    """
    CLI tool used for SSH into rpi 4's and using commands
    """

    ctx.obj['BULK'] = bulk
    if(new_ip):
        newDevice = {
            'USER': user,
            'PASSWORD': password
        }
        ctx.obj[str(ip)] = newDevice
    if(ip):
        if(ctx.obj[ip] == None):
            newDevice = {
            'USER': user,
            'PASSWORD': password
            }
            ctx.obj[str(ip)] = newDevice
        else:
            ctx.obj['IP'] = ip
    if(command):
        ctx.obj['COMMAND'] = command
    if(sysuser):
        ctx.obj['SYSUSER'] = sysuser
    if(syspass):
        ctx.obj['SYSPASS'] = syspass
    if(newmas != master):
        ctx.obj['MASTER'] = newmas
    elif(newmas == master):
        ctx.obj['MASTER'] = master

@cli.command()
@click.pass_context
def pingnodes(ctx):
    """
    Ping all nodes and returns true is hits false if doesn't
    """

    for key in ctx.obj:
        if(key != 'BULK' and key != "MASTER"):
            try:
                response = os.system("ping -c 1 " + key)

                if(response == 0):
                    print(key, "is up!")
                else:
                    print(key, "is down!")
            except:
                print("Couldn't connect to: " + key)
                pass


@cli.command()
@click.pass_context
def testconn(ctx):
    """
    Test connection to rpi's'. This will currently print out the date if connected. 
    """
    # This loops through the dict of devices and connects and shows the temp for each one
    for key in ctx.obj:
        try:
            ssh = connect(str(key), ctx.obj[str(key)]
                        ['USER'], ctx.obj[str(key)]['PASSWORD'])

            stdin, stdout, stderr = ssh.exec_command(
                'date')

            print(*stdout.readlines(), sep='\n')
        except:
            pass


@cli.command()
@click.pass_context
def cmd(ctx):
    """
    This will loop through selected devices, bulk or individual, and do the command given to it.
    """

    # Check if bulk tag is absent or not
    if(ctx.obj['BULK']):
        # This loops through the dict of devices and runs the inputted command for each one
        for key in ctx.obj:
            try:  # Check to make sure that the current iteration is an IP
                ssh = connect(str(key), ctx.obj[str(key)]
                              ['USER'], ctx.obj[str(key)]['PASSWORD'])

                stdin, stdout, stderr = ssh.exec_command(
                    str(ctx.obj['COMMAND']))

                print(*stdout.readlines(), sep='\n')
            except:
                pass
    # Bulk tab is absent
    else:
        # Check to make sure that IP address is present
        try:
            ssh = connect(ctx.obj['IP'], ctx.obj[ctx.obj['IP']]
                          ['USER'], ctx.obj[ctx.obj['IP']]['PASSWORD'])

            stdin, stdout, stderr = ssh.exec_command(str(ctx.obj['COMMAND']))

            print(*stdout.readlines(), sep='\n')
        except: # IP address and bulk tag are not present so state so
            print("No IP address given and one is needed when not using bulk tag.")


@cli.command()
@click.pass_context
def masdo(ctx):
    """
    This is for master node commands only
    """
    # This is to make sure login uses correct master node hostname in case we change master node
    ctx.obj['MASTER']['USER'] = 'kmaster'
    
    try:
        ssh = connect(ctx.obj['MASTER'], ctx.obj[ctx.obj['MASTER']]
                        ['USER'], ctx.obj[ctx.obj['MASTER']]['PASSWORD'])

        stdin, stdout, stderr = ssh.exec_command(str(ctx.obj['COMMAND']))

        print(*stdout.readlines(), sep='\n')
    except:
        print("Could not connect to master node or invalid command. " + stderr)

# @cli.command()
# @click.pass_context
# def supop(ctx):
#     """
#     This is used to change the systems default username or password
#     """
#     if(ctx.obj['SYSUSER']):
#         os.system('powershell.exe $Env:PI_USER = ' + "'" + str(ctx.obj['SYSUSER']) + "'")
#         click.echo('This is the new systems username: ' + ctx.obj['SYSUSER'])
#     elif(ctx.obj['SYSPASS']):
#         os.system('powershell.exe [$Env:PI_PASS = ' + ctx.obj['SYSPASS'] + ']')
#         click.echo('This is the new systems password: ' + ctx.obj['SYSPASS'])


if __name__ == '__main__':
    cli(obj={
        '192.168.1.146': {
            'USER': user,
            'PASSWORD': password
        },
        '192.168.1.148': {
            'USER': user,
            'PASSWORD': password
        },
        '192.168.1.149': {
            'USER': user,
            'PASSWORD': password
        }
    }
    )
