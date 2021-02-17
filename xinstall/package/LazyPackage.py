import importlib.resources as pkg_resources
import xinstall.package as xpackage
import xinstall.resources.packages as xpackages
import xinstall.task as xtask
import logging


class LazyPackage(xpackage.Package):
    """Represents a package to be installed.

    A lazy package is a package for which its tasks and dependencies are only
    instantiated when required.
    """

    def __init__(self, name):
        self.name = name
        self._tasks = None
        self._dependencies = None
        self.__package_file_name = "{}.pkg".format(self.name)

    def __read_tasks(self):
        """Reads the tasks in the file related to the package.

        Raises:
            PackageFileNotFound: when the correspong package file cannot be found.
            ReadingTasksError: when something goes wrong while reading the tasks
              from the package file.
        """
        if not pkg_resources.is_resource(xpackages, self.__package_file_name):
            raise xpackage.PackageFileNotFound(self)

        self._tasks = []

        with pkg_resources.path(
            xpackages, self.__package_file_name
        ) as path:
            with open(path, "r") as file:
                expecting_task = False

                for line in file:
                    line = line.strip()

                    if line == "TASKS:":
                        expecting_task = True

                    elif line == "DEPENDENCIES:":
                        expecting_task = False

                    elif expecting_task:
                        try:
                            task = xtask.str_to_task(line)
                            self._tasks.append(task)
                        except ValueError as exception:
                            pass
                        except xtask.NotATask as exception:
                            pass
                        except xtask.WrongTaskArgs as exception:
                            raise xpackage.ReadingTasksError(
                                "Could not read tasks of package {}".format(self.name)
                            )

    def __read_dependencies(self):
        """Reads the dependencies in the file related to the package."""
        if not pkg_resources.is_resource(xpackages, self.__package_file_name):
            raise xpackage.PackageFileNotFound(self)

        self._dependencies = []

        with pkg_resources.path(xpackages, self.__package_file_name) as path:
            with open(path, "r") as file:
                expecting_dependencies = False

                for line in file:
                    line = line.strip()

                    if line == "DEPENDENCIES:":
                        expecting_depenencies = True

                    elif line == "TASKS:":
                        expecting_dependencies = False

                    elif expecting_dependencies and line:
                        self._dependencies.append(LazyPackage(line))

    def tasks(self):
        """See ``Package.tasks``"""
        if self._tasks is None:
            self.__read_tasks()
        return self._tasks

    def dependencies(self):
        """See ``Package.dependencies``"""
        if self._dependencies is None:
            self.__read_dependencies()
        return self._dependencies
