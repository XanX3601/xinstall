class Task:
    """A task in an installation process.

    Attributes:
        name: the name of the task
    """

    def __init__(self, name):
        """Inits a task."""
        self.name = name

    def __eq__(self, other):
        """Test wether two tasks are equal."""
        return self.name == other.name

    def __hash__(self):
        """Returns the hash value of this task."""
        return hash(self.name)

    def run(self):
        """Runs the task.

        Returns:
            True if the task is successful, False otherwise.
        """
        return True
