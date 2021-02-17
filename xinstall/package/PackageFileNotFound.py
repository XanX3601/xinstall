class PackageFileNotFound(Exception):
    """Raised when a package does not have its corresponding package file in the
    resources."""

    def __init__(self, package):
        super().__init__()
        self.package = package

    def __str__(self):
        return "Package file not found for package {}".format(self.package.name)

    def __repr__(self):
        return str(self)
