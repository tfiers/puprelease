from os import getcwd
from os.path import exists

from requests import get

from .util import (
    ExitSignal,
    KeyValueTable,
    get_stripped_output,
    step_title_printer,
)


package_info_table = KeyValueTable(key_column_width=42)


def check_package():
    """ Display existing package versions, inter alia. """
    step_title_printer.step(f"Inspecting Python package")
    package_name = check_setup_py()
    check_pip_installed(package_name)
    check_pypi(package_name)
    check_git_worktree()


def check_setup_py():
    package_info_table.print_row("Working directory", getcwd())
    if not exists("setup.py"):
        raise ExitSignal('Working directory does not contain a "setup.py" file')
    package_name = get_stripped_output(["python", "setup.py", "--name"])
    package_info_table.print_row("Package name", package_name)
    version = get_stripped_output(["python", "setup.py", "--version"])
    package_info_table.print_row('Version in working dir (via "setup.py")', version)
    return package_name


def check_pip_installed(package_name):
    # Note: using pip's internal API to get this info is (too) convoluted.
    lines = get_stripped_output(("pip", "list")).splitlines()
    try:
        line = next(line for line in lines if line.startswith(package_name))
        _, version, *_ = line.split()
    except StopIteration:
        version = "[not pip-installed]"
    package_info_table.print_row("System-wide version, installed with pip", version)


def check_pypi(package_name):
    response = get(f"https://pypi.org/pypi/{package_name}/json")
    if response.ok:
        version = response.json()["info"]["version"]
    elif response.status_code == 404:
        version = "[not yet published on pypi.org]"
    else:
        response.raise_for_status()
    package_info_table.print_row("Latest version on pypi.org", version)


def check_git_worktree():
    clean = git_worktree_is_clean()
    if clean:
        status = "Clean (no uncommited changes)"
    else:
        status = "Dirty (uncommited changes)"
    package_info_table.print_row("Git working tree status", status)
    if not clean:
        raise ExitSignal(
            """Please commit or stash working tree changes before making a new
            release."""
        )


def git_worktree_is_clean():
    # The output of this command (which is the same command as in
    # "setuptools_scm.git.GitWorkdir.is_dirty") is empty when no uncommited
    # files are present in the git working tree.
    cmd = ("git", "status", "--porcelain", "--untracked-files=no")
    output = get_stripped_output(cmd)
    return not output
