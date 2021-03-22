import xinstall.worker as xworker
import xinstall.installer as xinstaller


class Configurator:
    """Configure a package."""

    def __init__(self, package):
        """Inits a configurator."""
        self.package = package

    def config(self):
        """Configs the package."""
        worker = xworker.Worker(self.package.config_tasks())
        worker.work()
        worker.wait_till_work_done()

        if not worker.success:
            raise xinstaller.ConfigurationIncomplete(self.package)
