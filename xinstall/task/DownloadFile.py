import requests

import xinstall.task as xtask


class DownloadFile(xtask.Task):
    """Download a file.

    Attributes:
        name: see `Task`.
        file_link: the link to the file to download
        file_path: where to download the file
    """

    def __init__(self, file_link, file_path):
        """See `Task.__init__`."""
        super().__init__()
        self.file_link = file_link
        self.file_path = xtask.parse_path(file_path)

    def run(self):
        """See `Task.run`."""

        try:
            self._info("Requesting file {}".format(self.file_link))
            request = requests.get(self.file_link)

            if not request.ok:
                self._error("Could not request file")
                return False

            self._info("Downloading file to {}".format(self.file_path))
            with open(self.file_path, "wb") as file:
                file.write(request.content)

            return True
        except Exception:
            self._exception("An error occured during the download")
            return False
