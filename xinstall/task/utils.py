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

        TaskType [args...]

    Args:
        string_task: the string containing the task to read.

    Raises:
        NotATask: if the type of the taks is unknown.
        WrongTaskArgs: if a task cannot be instanciated from the string.
        WrongTaskFormat: if the string task is wrongly formatted

    Retuns:
        A task.
    """
    string_task = split_string_task(string_task)

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


def split_string_task(string_task):
    """Splits a string task by cutting the space characters.

    The string task is plit around spaces so the expected format is:

        TaskType [args...]

    An arg put in quotes will keep its spaces and quotes will be removed
    An arg put in double quotes will keep its spaces.
    Every quotes in a double quoted arg are escaped.
    Every double quotes in a quoted arg are escaped.

    Args:
        string_task: the string task to split

    Raises:
        WrongTaskFormat: if a quoted argument is not properly opened or closed

    Returns:
        the string task split as a list of arguments
    """
    string_task_split_input = string_task.split()
    string_task_split_output = []

    quoted_arg = None
    double_quoted_arg = None

    for arg in string_task_split_input:
        if quoted_arg is not None:
            quoted_arg = "{} {}".format(quoted_arg, arg)

            if arg.endswith("'"):
                quoted_arg = quoted_arg.replace("'", "")
                string_task_split_output.append(quoted_arg)
                quoted_arg = None
            elif arg.startswith("'"):
                raise xtask.WrongTaskFormat(
                    "Quoted argument is not properly closed", string_task
                )

        elif double_quoted_arg is not None:
            double_quoted_arg = "{} {}".format(double_quoted_arg, arg)

            if arg.endswith('"'):
                string_task_split_output.append(double_quoted_arg)
                double_quoted_arg = None
            elif arg.startswith('"'):
                raise xtask.WrongTaskArgs(
                    "Double quoted argument is not properly closed", string_task
                )

        elif arg.startswith("'"):
            quoted_arg = arg

        elif arg.startswith('"'):
            double_quoted_arg = arg

        else:
            string_task_split_output.append(arg)

    if quoted_arg is not None:
        raise xtask.WrongTaskFormat(
            "Quoted argument is not properly closed", string_task
        )

    if double_quoted_arg is not None:
        raise xtask.WrongTaskArgs(
            "Double quoted argument is not properly closed", string_task
        )

    return string_task_split_output
