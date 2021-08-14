import xinstall.task as xtask
import importlib.resources as pkg_resources
import xinstall.resources as xresources
import shutil


class CopyResource(xtask.Task):
    """Copy a resource to a given destination."""

    def __init__(self, resource_name, destination_path):
        """See `Task.__init__`"""
        super().__init__()
        self.resource_name = resource_name
        self.destination_path = xtask.parse_path(destination_path)

    def run(self):
        """See `Task.run`"""
        if not pkg_resources.is_resource(xresources, self.resource_name):
            self._error("Resource '{}' does not exist".format(self.resource_name))
            return False

        with pkg_resources.path(xresources, self.resource_name) as path:
            self._info(
                "Copying resources '{}' to {}".format(
                    self.resource_name, self.destination_path
                )
            )

            try:
                shutil.copyfile(path, self.destination_path)
            except Exception:
                self._exception("An error occured during the copy")
                return False
