import xinstall.task as xtask
import pexpect


class Process(xtask.Task):
    """Handle processes.

    To start a process:
        process process_name start directory command [args...]

    To search for a pattern:
        process process_name search pattern

    To send a line:
        process process_name send line

    To send a line if a pattern is found:
        process process_name if pattern then line

    To wait for a process:
        process process_name wait

    To check for process terminated with success:
        process process_name success
    """

    _processes = {}

    def __init__(self, *args):
        """See Task.__init__"""
        super().__init__()
        self.args = [xtask.task_variables_to_value(arg) for arg in args]

    @staticmethod
    def is_running(process_name):
        """Checks if a process has been started and is still alive."""
        return (
            process_name in Process._processes
            and Process._processes[process_name].isalive()
        )

    def start(self, process_name, *args):
        """Starts a process."""
        if Process.is_running(process_name):
            self._error("Process '{}' is already running".format(process_name))
            return False

        if len(args) < 2:
            self._error("'directory' and 'command' arguments not given but mandatory")
            return False

        directory_path = xtask.parse_path(args[0])

        if not directory_path.exists():
            self._error("Location {} does not exist".format(directory_path))
            return False

        command = args[1]
        args = list(args[2:])

        if pexpect.which(command) is None:
            self._error("Unknown command '{}'".format(command))
            return False

        try:
            self._info(
                "Starting process '{}' by calling '{} {}' in directory {}".format(
                    process_name, command, " ".join(args), directory_path
                )
            )
            process = pexpect.spawn(command, args, cwd=directory_path, timeout=5)
            Process._processes[process_name] = process
        except Exception:
            self._exception(
                "Something went wrong while starting process '{}'".format(process_name)
            )
            return False

        return True

    def search(self, process_name, *args):
        """Search for a pattern."""
        if not Process.is_running(process_name):
            self._error("Process '{}' is not running".format(process_name))
            return False

        if not args:
            self._error("No pattern given but mandatory")
            return False

        process = Process._processes[process_name]
        pattern = " ".join(args)

        try:
            self._info(
                "Searching for '{}' in process '{}'".format(pattern, process_name)
            )
            index = process.expect([pattern, pexpect.TIMEOUT])

            if index != 0:
                self._error("Could not find given pattern")
                return False
        except Exception:
            self._exception("Something went wrong while searching for the pattern")
            return False

        return True

    def send(self, process_name, *args):
        """Send a line."""
        if not Process.is_running(process_name):
            self._error("Process '{}' is not running".format(process_name))
            return False

        process = Process._processes[process_name]
        line = " ".join(args)

        try:
            self._info("Sending '{}' to process '{}'".format(line, process_name))
            process.sendline(line)
        except Exception:
            self._exception("Something went wrong while sending the line")
            return False

        return True

    def ifthen(self, process_name, *args):
        """Sends a line if a pattern is found."""
        if not Process.is_running(process_name):
            self._error("Process '{}' is not running".format(process_name))
            return False

        if "then" not in args:
            self._error(
                "Wrong arg format received. Expected 'if pattern then line'. Could not find 'then'"
            )
            return False

        then_index = args.index("then")

        pattern = args[:then_index]

        if not pattern:
            self._error(
                "Wrong arg format received. Expected 'if pattern then line'. Could not find pattern"
            )
            return False

        pattern = " ".join(pattern)
        line = " ".join(args[then_index + 1 :])
        process = Process._processes[process_name]

        try:
            self._info(
                "Searching for '{}' in process '{}'".format(pattern, process_name)
            )
            index = process.expect([pattern, pexpect.TIMEOUT])
        except Exception:
            self._exception("Something went wrong while searching for the pattern")
            return False

        if index != 0:
            self._info("Could not find given pattern")
            return True

        try:
            self._info("Sending '{}' to process '{}'".format(line, process_name))
            process.sendline(line)
        except Exception:
            self._exception("Something went wrong while sending the line")
            return False

        return True

    def wait(self, process_name, *args):
        """Waits for a process to terminate."""
        if not Process.is_running(process_name):
            self._error("Process '{}' is not running".format(process_name))
            return False

        process = Process._processes[process_name]
        process.timeout = 3600

        try:
            self._info("Waiting for process '{}' to terminate".format(process_name))
            while not process.terminated:
                line = process.readline().decode()
                print(line)

            process.wait()
        except Exception:
            self._exception(
                "Something went wrong while waiting for the process to terminate"
            )
            return False

        return True

    def success(self, process_name, *args):
        """Checks if a process is terminated with success."""
        if process_name not in Process._processes:
            self._error("Process '{}' does no exist".format(process_name))
            return False

        process = Process._processes[process_name]

        if process.isalive():
            self._error("Process '{}' is still running".format(process_name))
            return False

        self._info(
            "Checking wether process '{}' terminated with success".format(process_name)
        )

        if process.exitstatus != 0:
            self._error(
                "Process '{}' did not terminate with success".format(process_name)
            )
            return False

        self._info("Process '{}' terminated with success".format(process_name))

        return True

    def run(self):
        """See Task.run"""
        if len(self.args) < 2:
            self._error(
                "'process_name' and 'command' arguments not given but mandatory"
            )
            return False

        commands = {
            "start": self.start,
            "search": self.search,
            "send": self.send,
            "if": self.ifthen,
            "wait": self.wait,
            "success": self.success,
        }

        process_name = self.args[0]
        command = self.args[1]

        if not command in commands:
            self._error("Unknown command '{}'".format(command))
            return False

        return commands[command](process_name, *self.args[2:])
