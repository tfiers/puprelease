from ast import keyword, parse, walk
from dataclasses import dataclass
from os import getenv
from subprocess import check_output, list2cmdline, run
from typing import Optional, Sequence

from click import confirm, prompt
from puprelease.util import (
    ExitSignal,
    KeyValueTable,
    MAX_LINEWIDTH,
    echo,
    print_header,
)


table = KeyValueTable(key_column_width=13, total_width=MAX_LINEWIDTH)
PyPI_user = getenv("TWINE_USERNAME")


def new_release():
    print_header("Preparing new release")
    confirm("Did you run testsuite locally?", default=True, abort=True)
    if is_versioned_with_git_tags():
        desired_new_version = prompt("Please enter the new version number")
        git_tag_command(desired_new_version).check_and_run()
        worktree_version = get_worktree_version()
        echo()
        echo(f'Version of package in worktree is now: "{worktree_version}"')
        if worktree_version != desired_new_version:
            echo("This does not match the desired new version")
            echo("Removing added tag and quitting")
            revert_tag_command(desired_new_version).run()
            raise ExitSignal
        push_tag_command.check_and_run()
    create_dists_command.check_and_run()
    publish_command.check_and_run()
    echo("Congrats on the new release")


def is_versioned_with_git_tags() -> bool:
    """
    Is the package versioned using git-tags (i.e. using setuptools_scm), or is
    the version set in "setup.py"?
    """
    # Check whether a function call keyword argument of the type
    # "use_scm_version=" appears somewhere in setup.py. Method is not
    # foolproof; But more than good enough.
    with open("setup.py") as f:
        src = f.read()
    tree = parse(src)
    kwargs = [node.arg for node in walk(tree) if type(node) == keyword]
    return "use_scm_version" in kwargs


def get_worktree_version():
    output: bytes = check_output(("python", "setup.py", "--version"))
    return output.decode().strip()


@dataclass
class Command:
    title: str
    args: Sequence[str]
    description: Optional[str] = None

    def check_and_run(self):
        print_header(self.title)
        table.print_row("Command", list2cmdline(self.args))
        if self.description:
            table.print_row("Description", self.description)
        confirm("Execute?", default=True, abort=True)
        self.run()

    def run(self):
        echo(list2cmdline(self.args))
        completed_process = run(self.args)
        retcode = completed_process.returncode
        if retcode == 0:
            echo("Command completed succesfully")
        else:
            echo(f"Command completed with return code {retcode}")


def git_tag_command(new_version):
    msg = f"Version {new_version}"
    return Command(
        title="Create tag",
        args=("git", "tag", "-a", new_version, "--message", msg),
        description=(
            """Create a git tag on the current commit. (Option "-a" makes an
            "annotated" tag, which includes tagger name, email, date, a custom
            message, etc)."""
        ),
    )


def revert_tag_command(new_version):
    return Command(
        title="Remove newly created tag", args=("git", "tag", "-d", new_version)
    )


push_tag_command = Command(
    title="Push tag",
    args=("git", "push", "--tags"),
    description="Push tag to public source code repository.",
)

create_dists_command = Command(
    title="Create distributions",
    args=("python", "setup.py", "bdist_wheel", "sdist"),
    description=(
        """Create two package distributions in "dist/": a built
            distribution and a source distribution. (The source distribution
            includes the project's top-level directory, and requires running
            "setup.py" on each "pip install" -- i.e. requires a full build. The
            built distribution on the other hand only requires moving files on
            "pip install", and includes only source files from the package
            directory.)"""
    ),
)

publish_command = Command(
    title="Publish release",
    args=("twine", "upload", "dist/*"),
    description=(
        f'Upload new release to PyPI, using account "{PyPI_user}".'
        if PyPI_user
        else """Upload new release to PyPI. Login details will be prompted
            for. (Note: these can also be set via the TWINE_USERNAME and
            TWINE_PASSWORD environment variables)."""
    ),
)
