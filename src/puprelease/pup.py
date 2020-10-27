import click

from puprelease.check import check_package
from puprelease.release import new_release
from puprelease.util import ExitSignal, echo
from puprelease import __version__


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
