import importlib.resources as pkg_resources
import logging

import xinstall.package as xpackage
import xinstall.resources.packages as xpackages
import xinstall.task as xtask


class LazyPackage(xpackage.Package):
    """Represents a package to be installed.

    A lazy package is a package for which its tasks and dependencies are only
    instantiated when required.
    """

    INSTALL_TASKS_TOKEN = "INSTALL_TASKS:"
    CONFIG_TASKS_TOKEN = "CONFIG_TASKS:"
    DEPENDENCIES_TOKEN = "DEPENDENCIES:"

    def __init__(self, name):
        self.name = name
        self._install_tasks = None
        self._config_tasks = None
        self._dependencies = None
        self.__package_file_name = "{}.pkg".format(self.name)

    def __get_package_file_path(self):
        """Returns the path to this package file.

        Checks if the package file exists and if so, returns the path to the
        file as a context manager.

        Raises:
            PackageFileNotFound: when the package file cannot be found.
        """
        if not pkg_resources.is_resource(xpackages, self.__package_file_name):
            raise xpackage.PackageFileNotFound(self)

        return pkg_resources.path(xpackages, self.__package_file_name)

    def __read_install_tasks(self):
        """Reads the install tasks in the file related to the package.

        Raises:
            PackageFileNotFound: when the correspong package file cannot be found.
            ReadingTasksError: when something goes wrong while reading the tasks
              from the package file.
        """
        self._install_tasks = []

        with self.__get_package_file_path() as path:
            with open(path, "r") as file:
                expecting_install_task = False

                for line in file:
                    line = line.strip()

                    if line == LazyPackage.INSTALL_TASKS_TOKEN:
                        expecting_install_task = True

                    elif any(
                        line == token
                        for token in [
                            LazyPackage.CONFIG_TASKS_TOKEN,
                            LazyPackage.DEPENDENCIES_TOKEN,
                        ]
                    ):
                        expecting_install_task = False

                    elif expecting_install_task:
                        try:
                            task = xtask.str_to_task(line)
                            task.name = self.name
                            self._install_tasks.append(task)
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
        self._dependencies = []

        with self.__get_package_file_path() as path:
            with open(path, "r") as file:
                expecting_dependencies = False

                for line in file:
                    line = line.strip()

                    if line == LazyPackage.DEPENDENCIES_TOKEN:
                        expecting_dependencies = True

                    elif any(
                        line == token
                        for token in [
                            LazyPackage.INSTALL_TASKS_TOKEN,
                            LazyPackage.CONFIG_TASKS_TOKEN,
                        ]
                    ):
                        expecting_dependencies = False

                    elif expecting_dependencies and line:
                        self._dependencies.append(LazyPackage(line))

    def __read_config_tasks(self):
        """Reads the config tasks in the file related to the package.

        Raises:
            PackageFileNotFound: when the correspong package file cannot be found.
            ReadingTasksError: when something goes wrong while reading the tasks
              from the package file.
        """
        self._config_tasks = []

        with self.__get_package_file_path() as path:
            with open(path, "r") as file:
                expecting_config_task = False

                for line in file:
                    line = line.strip()

                    if line == LazyPackage.CONFIG_TASKS_TOKEN:
                        expecting_config_task = True

                    elif any(
                        line == token
                        for token in [
                            LazyPackage.INSTALL_TASKS_TOKEN,
                            LazyPackage.DEPENDENCIES_TOKEN,
                        ]
                    ):
                        expecting_config_task = False

                    elif expecting_config_task:
                        try:
                            task = xtask.str_to_task(line)
                            task.name = self.name
                            self._config_tasks.append(task)
                        except ValueError as exception:
                            pass
                        except xtask.NotATask as exception:
                            pass
                        except xtask.WrongTaskArgs as exception:
                            raise xpackage.ReadingTasksError(
                                "Could not read config tasks of package {}".format(
                                    self.name
                                )
                            )

    def install_tasks(self):
        """See ``Package.install_tasks``"""
        if self._install_tasks is None:
            self.__read_install_tasks()
        return self._install_tasks

    def config_tasks(self):
        """See ``Package.config_tasks``"""
        if self._config_tasks is None:
            self.__read_config_tasks()
        return self._config_tasks

    def dependencies(self):
        """See ``Package.dependencies``"""
        if self._dependencies is None:
            self.__read_dependencies()
        return self._dependencies
