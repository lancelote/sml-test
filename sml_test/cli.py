import click

from sml_test.main import main


@click.command(help="Recursively execute all SML tests")
@click.version_option()
def cli() -> int:
    return main()


if __name__ == "__main__":
    cli()
