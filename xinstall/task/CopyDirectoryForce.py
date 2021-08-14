import shutil
import os
import pathlib

import xinstall.task as xtask


class CopyDirectoryForce(xtask.Task):
    """Copy a directory recursively and overwrite files."""

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

        for dirpath, dirnames, filenames in os.walk(self.directory_path):
            dir_path = pathlib.Path(dirpath)
            destination_dir_path = pathlib.Path(
                dirpath.replace(
                    str(self.directory_path), str(self.target_directory_path)
                )
            )

            if not destination_dir_path.exists():
                self._info("Creating directory {}".format(destination_dir_path))
                os.makedirs(destination_dir_path)

            for filename in filenames:
                file_path = dir_path.joinpath(filename)
                destination_path = destination_dir_path.joinpath(filename)

                self._info("Copying {} to {}".format(file_path, destination_path))

                try:
                    shutil.copy(file_path, destination_path)
                except Exception:
                    self._exception("An error occured during the copy of {} to {}.".format(file_path, destination_path))
                    return False

        return True
