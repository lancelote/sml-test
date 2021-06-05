import sys

import click

from sml_test.main import main


@click.command(help="Recursively execute all SML tests")
@click.version_option()
@click.option("-v", "--verbose", is_flag=True, help="Print raw SML output.")
def cli(verbose: bool) -> None:
    sys.exit(main(verbose))


if __name__ == "__main__":
    cli()
