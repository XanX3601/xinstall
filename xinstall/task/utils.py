import xinstall.task as xtask


def str_to_task(string_task):
    """Inits a task from a string.

    The expected format of the string is the following:

        TaskType task_name [args...]

    Args:
        string_task: the string containing the task to read.

    Raises:
        NotATask: if the type of the taks is unknown.
        WrongTaskArgs: if a task cannot be instanciated from the string.

    Retuns:
        A task.
    """
    string_task = string_task.split()

    if not string_task:
        raise ValueError("Received empty string")

    task_class_name = string_task[0]

    try:
        task_class = getattr(xtask, task_class_name)
    except AttributeError as exception:
        raise xtask.NotATask(task_class_name)

    try:
        task = task_class(*string_task[1:])
    except TypeError as exception:
        raise xtask.WrongTaskArgs(task_class_name, string_task[1:])

    return task
