import logging

import git
import git.exc

import xinstall.task as xtask


class GitCloneIfNotExists(xtask.Task):
    """Clone a git repository.

    Attributes:
        repo_link: the link to the repository
        repo_path: where download the repository
    """

    def __init__(self, repo_link, repo_path):
        """See `Task.__init__`"""
        super().__init__()
        self.repo_link = repo_link
        self.repo_path = xtask.parse_path(repo_path)

    def run(self):
        """See `Task.run`"""

        if self.repo_path.exists():
            self._info("Location '{}' already exists".format(self.repo_path))
            return True

        try:
            self._info(
                "Cloning repository '{}' to ".format(self.repo_link, self.repo_path)
            )
            git.Repo.clone_from(self.repo_link, self.repo_path)
            return True
        except Exception:
            self._exception("Exception during cloning".format(self.repo_link))
            return False
