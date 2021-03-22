import git

import xinstall.task as xtask


class GitRemoveChanges(xtask.Task):
    """Remove local changes in a repository."""

    def __init__(self, repo_path):
        """See Task.__init__"""
        super().__init__()
        self.repo_path = xtask.parse_path(repo_path)

    def run(self):
        """See Task.run"""
        if not self.repo_path.exists():
            self._error("Location {} does not exists".format(self.repo_path))

        try:
            self._info("Opening repo {}".format(self.repo_path))
            repo = git.Repo(self.repo_path)
        except Exception:
            self._exception("An error occured while opening the repo")
            return False

        try:
            self._info("Removing local changes for repo {}".format(self.repo_path))
            repo.git.reset("--hard")
        except Exception:
            self._exception("An error occured during the removal")
            return False

        return True
