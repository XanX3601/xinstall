import os

import xinstall.task as xtask


class CreateDirectoryIfNotExist(xtask.Task):
    """Create a directory if it does not exist."""

    def __init__(self, directory_path):
        """See `Task.__init__`."""
        super().__init__()
        self.directory_path = xtask.parse_path(directory_path)

    def run(self):
        """See `Task.run`."""
        if self.directory_path.exists():
            self._info("Location {} already exists".format(self.directory_path))
            return True

        self._info("Creating directory '{}'".format(self.directory_path))
        try:
            os.mkdir(self.directory_path)
            return True
        except Exception:
            self._exception("An error occured during the creation of the directory")
            return False
