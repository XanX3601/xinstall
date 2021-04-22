import xinstall.task as xtask
import subprocess


class Bootstrap(xtask.Task):
    """Invoke bootstrap script inside a directory."""

    def __init__(self, directory_path, *args):
        """See Task.__init__"""
        super().__init__()
        self.directory_path = xtask.parse_path(directory_path)

        self.args = [xtask.task_variables_to_value(arg) for arg in args]

    def run(self):
        """See Task.run"""
        args = ["./bootstrap"] + self.args

        if not self.directory_path.exists():
            self._error("Location {} does not exist".format(self.directory_path))
            return False

        self._info(
            "Calling '{}' in directory {}".format(" ".join(args), self.directory_path)
        )

        try:
            results = subprocess.run(
                args, cwd=self.directory_path, capture_output=True, text=True
            )
        except Exception:
            self._exception("Something went wrong while calling bootstrap")
            return False

        if results.returncode != 0:
            self._error("Something went wrong during the bootstraping")
            self._error(results.stderr)
            return False

        return True
