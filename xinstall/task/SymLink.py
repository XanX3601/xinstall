import os

import xinstall.task as xtask

class SymLink(xtask.Task):
    """Create a symbolic link."""
    
    def __init__(self, link_location, link_target):
        """See `Task.__init__`."""
        super().__init__()
        self.link_location = xtask.parse_path(link_location)
        self.link_target = xtask.parse_path(link_target)

    def run(self):
        """See `Task.run`."""
        if not self.link_target.exists():
            self._error("Location {} does not exist.""".format(self.link_target))
            return False

        if self.link_location.exists():
            self._error("Location {} already exists.""".format(self.link_location))
            return False

        self._info("Linking {} to {}".format(self.link_location, self.link_target))

        try:
            os.symlink(self.link_target, self.link_location)
            return True
        except Exception:
            self._exception("An error occured during linking")
            return False

