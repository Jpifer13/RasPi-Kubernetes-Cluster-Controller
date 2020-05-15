"""Remote host object to handle connections and actions."""
import os
import sys
import time
from datetime import datetime
import logging
from os import system
from paramiko import SSHClient, AutoAddPolicy, RSAKey
from paramiko.auth_handler import AuthenticationException, SSHException
# from scp import SCPClient, SCPException
from argparse import ArgumentParser, RawTextHelpFormatter


from logging.LoggingUtils import LoggingUtils

# user = os.environ.get('K8S_USERNAME')
# password = os.environ.get('K8S_PASSWORD')

__version__ = 'v1.0'
__application__ = 'Kubernetes Cluster Controller'


class RemoteClient:
    """Client to interact with a remote host via SSH & SCP."""

    def __init__(self, host, user, logLevel=None, ssh_key_filepath=None, remote_path=None):
        """
        """
        self.host = host
        self.user = user
        self.ssh_key_filepath = ssh_key_filepath
        self.remote_path = remote_path
        self.client = None
        self.scp = None
        self.__upload_ssh_key()

        # Initialize logger
        try:
            self._loggingUtils = self._initLogging(fileLogLevel=logLevel)
            self._loggingUtils.logApplicationStart()
        except Exception as err:
            setErrorAndExit(f"Unable to initialize the logger. Error: {err}")

    def __connect(self):
        """Open connection to remote host."""
        try:
            logger = logging.getLogger()
            logging.info("Connecting...")

            self.client = SSHClient()
            # self.client.load_system_host_keys()
            # self.client.set_missing_host_key_policy(AutoAddPolicy())
            self.client.connect(self.host,
                                username=self.user,
                                key_filename=self.ssh_key_filepath,
                                look_for_keys=True,
                                timeout=5000)
            # self.scp = SCPClient(self.client.get_transport())  # For later

            logging.info("Connected...")
        except AuthenticationException as error:
            logger.exception(f'Authentication failed: {error}')
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
        logger = logging.getLogger()

        if self.client is None:
            self.client = self.__connect()
        for cmd in commands:
            stdin, stdout, stderr = self.client.exec_command(cmd)
            stdout.channel.recv_exit_status()
            response = stdout.readlines()
            for line in response:
                logger.info(f'INPUT: {cmd} | OUTPUT: {line}')

    def _initLogging(self, fileLogLevel=None, consoleLogLevel=None):
        """
        _initLogging uses the LoggingUtils module to configure logging. This provides consistent
        formatting for all of our log files.

        Parameters
        ----------
            fileLogLevel : number or str
                Optional: specifies the level of messages to log to the log file.
                Example: logging.DEBUG, 'DEBUG', logging.ERROR, 'ERROR'
            consoleLogLevel : str
                Optional: specifies the level of messages to log to the console file.
                Example: logging.DEBUG, 'DEBUG', logging.ERROR, 'ERROR'

        Returns
        ----------
            LoggingUtils
                Returns an instance of the LoggingUtils class.

        """
        # Exceptions are handled by the caller.
        timestamp = time.strftime("%Y%m%d%H%M%S")
        loggingFile = f"logs/{__application__}-{timestamp}.log"
        loggingUtils = LoggingUtils(__application__,
                                    logFile=loggingFile,
                                    fileLevel=fileLogLevel,
                                    consoleLevel=consoleLogLevel)
        return loggingUtils


def parseArgs():
    """
    Parse the command line arguments for this program.

    Returns
    ----------
        dictionary
            A dictionary with the command line arguments and values. 

    """
  
    USAGE = f"""
    {__application__}, {__version__}
    Description of functionality...
    """

    parser = ArgumentParser(description=__application__, 
                            formatter_class=RawTextHelpFormatter, epilog=USAGE)
    parser.add_argument('--debug', action='store_true', required=False, default=False,
                        help='Sets log level to DEBUG')
    parser.add_argument('-v', '--version', action='version', 
                        version=f"{__application__}, {__version__}\n")
    # parser.add_argument('-f', '--fileSpec', action='fileSPec')
    return parser.parse_args()


##---------------------------------------------------------------------------------------------------------------------

def setErrorAndExit(error):
    """
    Reports the specified error and terminates the program..

    Parameters
    ----------
        error : str
            The error message to report.

    """
    sys.stderr.write("Error: " + error + "\n")
    sys.stderr.write("Program exiting.")
    sys.exit(1)


##---------------------------------------------------------------------------------------------------------------------
## Main function
##---------------------------------------------------------------------------------------------------------------------

def main():
    """
    This is the main function for this program. It parses the command line arguments,
    instantiates an instance of the controller class, and invokes the run method.
    """

    try:
        # Get the command line arguments
        args = parseArgs()
            
        # Set up logging level
        if args.debug:
            logLevel = logging.DEBUG
        else:
            logLevel = logging.INFO


        # Initiate controller and run it.
        # Do NOT pass the args dictionary into the controller. That would tightly couple the 
        # controller to being invoked via a command line. Testing is improved by passing individual
        # values as parameters to the constructor. 

        # controller = LimsSampleManipulationController(logLevel)
        # controller.run()

    except Exception as exc:
        print(f"exc = {exc}")
        execptionType, exceptionObj, exceptionTraceback = sys.exc_info()
        fname = os.path.split(exceptionTraceback.tb_frame.f_code.co_filename)[1]
        errorInfo = f"{str(exceptionObj)} {str(execptionType)}, file={fname} , line={str(exceptionTraceback.tb_lineno)}"
        setErrorAndExit(errorInfo)

    finally:
        # Clean up any resources
        pass

    sys.exit(0)

##---------------------------------------------------------------------------------------------------------------------

if __name__ == '__main__':
    main()

##---------------------------------------------------------------------------------------------------------------------
