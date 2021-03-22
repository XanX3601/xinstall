import pathlib
import tempfile

import xinstall.resources.paths as xpaths
import xinstall.task as xtask


def str_to_task_class(task_class_name):
    """Parse a string to a task class

    The expected format of the string can be one of the following:

        TaskClass
        task_class
        task-class

    Args:
        task_class_name: the string to parse.

    Raises:
        NotATask: if the task class cannot be retrieved

    Returns:
        A task class.
    """
    split_char = None
    if "-" in task_class_name:
        split_char = "-"

    elif "_" in task_class_name:
        split_char = "_"

    if split_char is not None:
        task_class_name = task_class_name.split(split_char)
        for i in range(len(task_class_name)):
            component = task_class_name[i]
            component = component[0].upper() + component[1:]
            task_class_name[i] = component
        task_class_name = "".join(task_class_name)
    elif not task_class_name[0].isupper():
        task_class_name = task_class_name[0].upper() + task_class_name[1:]

    try:
        task_class = getattr(xtask, task_class_name)
    except AttributeError as exception:
        raise xtask.NotATask(task_class_name)

    return task_class


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

    task_class = str_to_task_class(task_class_name)

    try:
        task = task_class(*string_task[1:])
    except TypeError as exception:
        raise xtask.WrongTaskArgs(task_class_name, string_task[1:])

    return task


def parse_path(path):
    """Creates a path from a string.

    Replaces any task variables to its corresponding value.
    """
    path = task_variables_to_value(path)
    path = pathlib.Path(path)
    return path


def task_variables_to_value(string):
    """Replaces any task variables in a string by its corresponding values."""
    for variable, value in xtask.task_variables.items():
        string = string.replace(variable, value)

    return string
