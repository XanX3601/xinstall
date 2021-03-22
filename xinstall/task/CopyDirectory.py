import shutil

import xinstall.task as xtask


class CopyDirectory(xtask.Task):
    """Copy a directory recursively."""

    def __init__(self, directory_path, target_directory_path):
        """See `Task.__init__`"""
        super().__init__()
        self.directory_path = xtask.parse_path(directory_path)
        self.target_directory_path = xtask.parse_path(target_directory_path)

    def run(self):
        """See `Task.run`."""
        if not self.directory_path.exists():
            self._error("Location {} does not exist.".format(self.directory_path))
            return False

        if self.target_directory_path.exists():
            self._error("Location {} already exists".format(self.target_directory_path))
            return False

        self._info(
            "Copying {} to {}".format(self.directory_path, self.target_directory_path)
        )

        try:
            shutil.copytree(self.directory_path, self.target_directory_path)
            return True
        except Exception:
            self._exception("An error occured during copy")
            return False
