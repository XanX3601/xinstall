import multiprocessing


class Worker:
    """Runs a list of task asynchronously.

    Attributes:
        tasks: the list of tasks to run.
    """

    def __init__(self, tasks):
        """Inits a worker."""
        self.tasks = tasks
        self.__process = None
        self.success = None

    def work(self):
        """Launches the worker."""

        def __work(tasks):
            for task in tasks:
                success = task.run()
                if not success:
                    self.success = False
                    return
            self.success = True

        self.__process = multiprocessing.Process(target=__work, args=(self.tasks,))
        self.__process.run()

    def wait_till_work_done(self):
        """Waits for the worker to end its tasks."""
        if self.__process is not None and self.__process.is_alive():
            self.__process.join()
