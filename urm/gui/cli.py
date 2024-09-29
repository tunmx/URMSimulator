import click
from .aliased_group import AliasedGroup
from .server import gui

__all__ = ['cli']

CONTEXT_SETTINGS = dict(help_option_names=['-h', '--help'])


@click.command(cls=AliasedGroup, context_settings=CONTEXT_SETTINGS)
def cli():
    pass


cli.add_command(gui)

if __name__ == '__main__':
    cli()