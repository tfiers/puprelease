import click

from . import __version__
from .check import check_package
from .release import new_release
from .util import ExitSignal, echo


@click.command()
def cli():
    try:
        echo(f"This is puprelease version {__version__}")
        echo()
        echo(
            "This program can be safely stopped and restarted at any time: "
            "the release steps are idempotent."
        )
        check_package()
        new_release()
    except click.Abort:
        # Do not print click's ugly "Aborted!"
        pass
    except ExitSignal as sig:
        if sig.message:
            echo()
            echo(sig.message)
    echo("Exiting")
