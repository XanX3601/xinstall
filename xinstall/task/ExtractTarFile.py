import tarfile

import xinstall.task as xtask


class ExtractTarFile(xtask.Task):
    """Exract a tarfile.

    Attributes:
        name: see `Task.name`.
        tarfile_path: where the tarfile is.
        extract_path: where extract the tarfile.
    """

    def __init__(self, tarfile_path, extract_path):
        """See `Task.__init__`."""
        super().__init__()
        self.tarfile_path = xtask.parse_path(tarfile_path)
        self.extract_path = xtask.parse_path(extract_path)

    def run(self):
        """See `Task.run`."""

        try:
            self._info("Opening tarfile {}".format(self.tarfile_path))
            tar = tarfile.open(self.tarfile_path)
        except Exception:
            self._exception("An error occured while opening the file")
            return False

        try:
            self._info("Extracting tarfile in {}".format(self.extract_path))
            tar.extractall(self.extract_path)
            return True
        except Exception:
            self._exception("An error occured during the extraction")
            return False
