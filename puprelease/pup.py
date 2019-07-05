import click
from puprelease.check import check_package
from puprelease.release import new_release
from puprelease.util import echo, print_own_version, ExitSignal


@click.command()
def pup():
    """
    Note: this program can be safely stopped at any time. The release steps are
    idempotent.
    """
    try:
        print_own_version()
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


if __name__ == "__main__":
    pup()
