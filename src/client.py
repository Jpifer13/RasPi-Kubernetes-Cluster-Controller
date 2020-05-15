"""Remote host object to handle connections and actions."""
import sys
from loguru import logger
from os import system
from paramiko import SSHClient, AutoAddPolicy, RSAKey
from paramiko.auth_handler import AuthenticationException, SSHException
from scp import SCPClient, SCPException


logger.add(sys.stderr,
           format="{time} {level} {message}",
           filter="client",
           level="INFO")
logger.add('logs/log_{time:YYYY-MM-DD}.log',
           format="{time} {level} {message}",
           filter="client",
           level="ERROR")

class RemoteClient:
    """Client to interact with a remote host via SSH & SCP."""

    def __init__(self, host, user, ssh_key_filepath=None, remote_path=None):
        """
        """
        self.host = host
        self.user = user
        self.ssh_key_filepath = ssh_key_filepath
        self.remote_path = remote_path
        self.client = None
        self.scp = None
        self.__upload_ssh_key()

    def __connect(self):
        """Open connection to remote host."""
        try:
            self.client = SSHClient()
            # self.client.load_system_host_keys()
            # self.client.set_missing_host_key_policy(AutoAddPolicy())
            self.client.connect(self.host,
                                username=self.user,
                                key_filename=self.ssh_key_filepath,
                                look_for_keys=True,
                                timeout=5000)
            self.scp = SCPClient(self.client.get_transport())  # For later
        except AuthenticationException as error:
            logger.info('Authentication failed: did you remember to create an SSH key?')
            logger.error(error)
            raise error
        finally:
            return self.client

     def disconnect(self):
        """Close ssh connection."""
        self.client.close()
        self.scp.close()  # Coming later

    def execute_commands(self, commands):
        """Execute multiple commands in succession.
        
        Expects list of commands"""
        if self.client is None:
            self.client = self.__connect()
        for cmd in commands:
            stdin, stdout, stderr = self.client.exec_command(cmd)
            stdout.channel.recv_exit_status()
            response = stdout.readlines()
            for line in response:
                logger.info(f'INPUT: {cmd} | OUTPUT: {line}')