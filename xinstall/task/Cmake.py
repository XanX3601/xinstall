import subprocess

import xinstall.task as xtask


class Cmake(xtask.Task):
    """Call cmake inside a directory."""

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

        args = ["cmake"] + self.args

        self._info(
            "Calling '{}' in directory {}".format(" ".join(args), self.directory_path)
        )

        try:
            results = subprocess.run(
                args, cwd=self.directory_path, capture_output=True, text=True
            )
        except Exception:
            self._exception("Something went wrong during the call to cmake")
            return False

        returncode = results.returncode

        if returncode != 0:
            self._error("Something went wrong during the cmaking")
            self._error(results.stderr)
            return False

        return True
