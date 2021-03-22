import git

import xinstall.task as xtask


class GitUpdate(xtask.Task):
    """Pull a repository on its current branch."""

    def __init__(self, repo_path):
        """See Task.__init__"""
        super().__init__()
        self.repo_path = xtask.parse_path(repo_path)

    def run(self):
        """See Task.run"""
        if not self.repo_path.exists():
            self._error("Location {} does not exist".format(self.repo_path))

        try:
            self._info("Opening repo {}".format(self.repo_path))
            repo = git.Repo(self.repo_path)
        except Exception:
            self._exception("Something went wrong while opening the repo")
            return False

        try:
            self._info("Updating repo {}".format(self.repo_path))
            repo.remotes.origin.pull()
        except Exception:
            self._exception("Something went wrong during the update")
            return False

        return True
