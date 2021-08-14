import xinstall.task as xtask

class RemoveFileIfExists(xtask.Task):
    """Remove a file if it exists."""

    def __init__(self, file_path):
        """See `Task.__init__`."""
        super().__init__()
        self.file_path = xtask.parse_path(file_path)

    def run(self):
        """See `Task.run`."""
        if not self.file_path.exists():
            self._info("Doing nothing: Location {} does not exist.""".format(self.file_path))
            return True

        if not self.file_path.is_file():
            self._info("Doing nothing: Location {} is not a file.".format(self.file_path))
            return True

        self._info("Removing file {}".format(self.file_path))
        try:
            self.file_path.unlink()
        except Exception:
            self._exception("An error occured during removal.")
            return False

        return True
