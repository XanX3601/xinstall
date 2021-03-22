class ConfigurationIncomplete(Exception):
    """Raised when the configuration of a package is incomplete."""

    def __init__(self, package):
        self.package = package

    def __str__(self):
        return "Configuration of package {} is incomplete".format(self.package.name)

    def __repr__(self):
        return str(self)
