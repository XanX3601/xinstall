class WrongTaskArgs(Exception):
    """Raised when a task is initiated with the wrong arguments."""

    def __init__(self, task_type, args):
        super().__init__()
        self.task_type = task_type
        self.args = args

    def __str__(self):
        return "Wrong arguments received for task {}: {}".format(
            self.task_type, self.args
        )
