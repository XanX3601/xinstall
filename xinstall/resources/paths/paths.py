import pathlib

home_dir_path = pathlib.Path.home()
"""Path to the current user home directory."""

repositories_dir_path = home_dir_path.joinpath("Repositories")
"""Path to the git repositories directory."""

tarballs_dir_path = home_dir_path.joinpath("Tarballs")
"""Path to the tarballs directory."""
