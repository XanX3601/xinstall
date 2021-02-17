class ReadingTasksError(Exception):
    """Raised when an error occurs while reading a package's tasks."""

    def __init__(self, package):
        super().__init__()
        self.package = package

    def __str__(self):
        return "Could not read tasks for package {}".format(self.package.name)
