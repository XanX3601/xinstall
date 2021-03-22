import importlib.resources as pkg_resources
import multiprocessing

import xinstall.resources.descriptions as xdescriptions


class Package:
    """Represents a package to be installed.

    Attributes:
        name: a string containing the name of the package.
    """

    def __init__(self, name, install_tasks, dependencies, config_tasks):
        """Inits a package with given parameters.

        Args:
            name: a string containing the package name.
            tasks: a list of tasks necessary to install the package.
            dependencies: a set of package that the current package depends on.
              Aka, packages that need to be installed before the current one.
        """
        self.name = name
        self._install_tasks = install_tasks
        self._dependencies = dependencies
        self._config_tasks = config_tasks

    def install_tasks(self):
        """Returns the list of tasks to install the package."""
        return self._install_tasks

    def dependencies(self):
        """Returns the set of dependencies of the package."""
        return self._dependencies

    def __eq__(self, other):
        """Tests if two packages are equal."""
        return self.name == other.name

    def __hash__(self):
        """Returns the hash value of the package."""
        return hash(self.name)

    def description(self):
        """Returns a description of the package.

        The description is a markdown text extracted from
        ``xconfigurator.resources.descriptions``. The description is expected to
        be in a file named ``package_name.md``.
        """
        if not pkg_resources.is_resource(xdescriptions, "{}.md".format(self.name)):
            return "No description available."

        with pkg_resources.path(xdescriptions, "{}.md".format(self.name)) as path:
            return path.read_text(encoding="utf-8")

    def __str__(self):
        return self.name

    def __repr__(self):
        return self.name

    def config_tasks(self):
        """Returns the list of tasks to configure the package."""
        return self._config_tasks
