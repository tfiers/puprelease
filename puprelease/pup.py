import click
from puprelease.check import check_package
from puprelease.release import new_release
from puprelease.util import ExitSignal, echo, print_own_version


@click.command()
def pup():
    try:
        print_own_version()
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


if __name__ == "__main__":
    pup()
