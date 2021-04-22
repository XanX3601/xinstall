import tempfile
import datetime

import xinstall.resources.paths as xpaths

task_variables = {
    "REPOS": str(xpaths.repositories_dir_path),
    "TEMP": str(tempfile.gettempdir()),
    "TARS": str(xpaths.tarballs_dir_path),
    "HOME": str(xpaths.home_dir_path),
    "YYYY": "{:0>4d}".format(datetime.datetime.now().year),
    "MM": "{:0>2d}".format(datetime.datetime.now().month),
    "DD": "{:0>2d}".format(datetime.datetime.now().day),
}
