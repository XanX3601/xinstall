class NotATask(Exception):
    """Raised when an object does not match any task."""

    def __init__(self, not_a_task_name):
        super().__init__()
        self.not_a_task_name = not_a_task_name

    def __str__(self):
        return "{} is not a task".format(self.not_a_task_name)
