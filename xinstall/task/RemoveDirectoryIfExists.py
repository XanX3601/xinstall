import shutil

import xinstall.task as xtask


class RemoveDirectoryIfExists(xtask.Task):
    """Remove a directory if it exists."""

    def __init__(self, directory_path):
        """See Task.__init__"""
        super().__init__()
        self.directory_path = xtask.parse_path(directory_path)

    def run(self):
        """See Task.run"""
        if not self.directory_path.exists():
            self._info(
                "Doing nothing: Location '{}' does not exist".format(
                    self.directory_path
                )
            )
            return True

        if not self.directory_path.is_dir():
            self._info(
                "Doing nothing: Location '{}' is not a directory".format(
                    self.directory_path
                )
            )
            return True

        self._info("Removing directory '{}'".format(self.directory_path))
        try:
            shutil.rmtree(self.directory_path)
        except Exception:
            self._exception("An error occured during removal")
            return False

        return True
