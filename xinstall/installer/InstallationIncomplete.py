class InstallationIncomplete(Exception):
    """Raised when the installation of a package is incomplete."""

    def __init__(self, package):
        self.package = package

    def __str__(self):
        return "Installation of package {} is incomplete.".format(self.package.name)

    def __repr__(self):
        return str(self)
