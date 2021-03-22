import tempfile

import xinstall.resources.paths as xpaths

task_variables = {
    "REPOS": str(xpaths.repositories_dir_path),
    "TEMP": str(tempfile.gettempdir()),
    "TARS": str(xpaths.tarballs_dir_path),
    "HOME": str(xpaths.home_dir_path),
}
