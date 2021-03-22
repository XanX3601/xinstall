import xinstall.resources.logger as xlogger


class Task:
    """A task in an installation process."""

    def __init__(self, name=None):
        """Inits a task."""
        self.name = name
        self.logger = xlogger.get_xinstall_logger()

    def run(self):
        """Runs the task.

        Returns:
            True if the task is successful, False otherwise.
        """
        return True

    @property
    def __log_start(self):
        if self.name is None:
            return "[{}]".format(self.__class__.__name__)

        return "[{}] [{}]".format(self.__class__.__name__, self.name)

    def _info(self, msg):
        """Logs an info message.

        Args:
            msg: the message to log
        """
        self.logger.info("{} {}".format(self.__log_start, msg))

    def _exception(self, msg):
        """Logs an exception message.

        Args:
            msg: the message to log
        """
        self.logger.exception("{} {}".format(self.__log_start, msg))

    def _error(self, msg):
        """Logs an error message.

        Args:
            msg: the message to log.
        """
        self.logger.error("{} {}".format(self.__log_start, msg))
