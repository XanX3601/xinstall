import xinstall.worker as xworker
import xinstall.installer as xinstaller
import logging


class Installer:
    """Install a package with or without its dependencies."""

    def __init__(self, package, with_dependencies=True):
        """Inits an installer."""
        self.package = package
        self.with_dependencies = with_dependencies

    def install_dict(self):
        """Computes a dictionnary mapping deep to a list of packages.

        It gives the order in which packages should be installed. The deeper a
        package is, the earliest it needs to be installed.
        """

        def rec(package, deep=0):
            for dependency in package.dependencies():
                rec(dependency, deep + 1)

            if package not in packages_set:
                packages_set.add(package)

                if deep not in packages:
                    packages[deep] = []

                packages[deep].append(package)

        packages = {}
        packages_set = set()

        if self.with_dependencies:
            rec(self.package)
        else:
            packages = {0: [self.package]}

        return packages

    def install(self):
        """Installs the package."""
        try:
            install_dict = self.install_dict()
        except Exception as e:
            logging.critical(str(e))
            exit(0)

        for deep in range(len(install_dict) - 1, -1, -1):
            packages = install_dict[deep]
            workers = []

            for package in packages:
                worker = xworker.Worker(package.tasks())
                workers.append(worker)
                worker.work()

            for worker in workers:
                worker.wait_till_work_done()

            if any(not worker.success for worker in workers):
                raise xinstaller.InstallationIncomplete(self.package)
