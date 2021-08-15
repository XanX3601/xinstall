class WrongTaskFormat(Exception):
    """Raised when a task string is malformed."""

    def __init__(self, explanation, task_string):
        self.explanation = explanation
        self.task_string = task_string

    def __str__(self):
        return "Malformed task '{}': {}".format(self.task_string, self.explanation)
