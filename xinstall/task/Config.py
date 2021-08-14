import subprocess

import xinstall.task as xtask


class Config(xtask.Task):
    """Invoke configure script inside a directory."""

    def __init__(self, directory_path, *args):
        """See Task.__init__"""
        super().__init__()
        self.directory_path = xtask.parse_path(directory_path)

        self.args = [xtask.task_variables_to_value(arg) for arg in args]

    def run(self):
        """See Task.run"""
        if not self.directory_path.exists():
            self._error("Location {} does not exist".format(self.directory_path))
            return False

        if (self.directory_path / "configure").is_file():
            args = ["./configure"] + self.args
        elif (self.directory_path / "config").is_file():
            args = ["./config"] + self.args
        else:
            self._error("No configure file found in {}".format(self.directory_path))

        self._info(
            "Calling '{}' in directory {}".format(" ".join(args), self.directory_path)
        )
        try:
            results = subprocess.run(
                args,
                cwd=self.directory_path,
                capture_output=True,
                text=True,
            )
        except Exception:
            self._exception("An error occured during the call")
            return False

        returncode = results.returncode

        if returncode != 0:
            self._error("Something went wrong during the configuration")
            self._error(results.stderr)
            return False

        return True
