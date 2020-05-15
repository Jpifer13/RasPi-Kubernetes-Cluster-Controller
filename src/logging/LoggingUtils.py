import os
import logging
import getpass
import platform
import sys
from datetime import datetime, timedelta

class LogFileCreationError( Exception ):
    """
    This is my custom exception class to be thrown when there is an error when creating a log file

    Arguments:
        Exception {[type]} -- [description]
    """
    def __init__(self, filespec):
        self.filespec = filespec

class LoggingUtils:
    """
    A utility class to create a logging object with nicer formatting
    """

    def __init__(self, application_name, log_file: str = None, file_level: int = logging.NOTSET, console_level: int = logging.NOTSET):
        self.app_name = application_name
        self._filename = log_file
        self._file_level = file_level
        self._console_level = console_level
        self._logger = None
        self._file_handler = None
        self._console_handler = None
        self._username = getpass.getuser()
        self._hostname = platform.node()
        self._start_datetime = datetime.now()
        self._finish_datetime = None
        self._datetime_format = '%d%b%Y %H:%M:%S'
        self._time_with_milliseconds = '%H:%M:%S.%f'

        formatter = logging.Formatter(
            '[%(asctime)s.%(msecs)03d] - $(module)s - %(levelname)s - %(message)s', self._datetime_format
        )

        self._logger = logging.getLogger()

        self._logger.setLevel(logging.DEBUG)

        # Set up level logging
        if file_level:
            if not self._filename:
                self._filename = os.path.join(self._app_name + '.log')
            
            try:
                self._file_handler = logging.FileHandler(self._filename, encoding='UTF-8')
            except IOError:
                raise LogFileCreationError(self._filename)

            self._file_handler.setLevel(self._file_level)

            self._file_handler.setFormatter(formatter)

        if console_level:
            self._console_handler = logging.StreamHandler()
            self._console_handler.setLevel(self._console_level)
            self._console_handler.setFormatter(formatter)
            self._logger.addHandler(self._console_handler)

    def logApplicationStart(self):
        """
        Log the start of an application. This inserts a standard set of information:
            * User name
            * Host name
            * Command used to run the application
            * Application name
            * Start time
        """
        command = ' '.join(sys.argv)
        start = self._formatDateTime(self._startDateTime)
        self._logger.info("**************************************************************")
        self._logger.info(f"  User         = {self._username}" )
        self._logger.info(f"  Hostname     = {self._hostname}" )
        self._logger.info(f"  Command      = {command}" )
        self._logger.info(f"  Application  = {self._appName}" )
        self._logger.info(f"  Start        = {start}" )
        self._logger.info("**************************************************************")
    
    def logApplicationFinish(self):
        """
        Log the finish of an application. This inserts the following information:
            * Finish time
            * Elapsed time
        """
        self._finishDateTime = datetime.now()
        finish = self._formatDateTime(self._finishDateTime)
        elapsedTime = self._finishDateTime - self._startDateTime
        self._logger.info("**************************************************************")
        self._logger.info(f"{self._appName} finished.")
        self._logger.info(f"  Finish time  = {finish}")
        self._logger.info(f"  Elapsed time = {str(elapsedTime)}")
        self._logger.info("**************************************************************")
    

    def _formatDateTime(self, rawDateTime):
        """
        Formats a time value in a human-readable format.

        Args:
            :param rawTime
                A floating point value returned from datetime.now(). 

        Returns:
            A string in human readable format with days, hours, minutes, seconds, and microseconds.
            Example: "2 days, 0:00:00.000678
        """
        return rawDateTime.strftime(self._timeWithMilleseconds)
