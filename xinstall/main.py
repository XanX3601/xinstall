import logging

import click
import rich
import rich.logging

import xinstall.installer as xinstaller
import xinstall.package as xpackage
import xinstall.resources.logger as xlogger


@click.group()
def cli():
    pass


@cli.command()
@click.argument("package")
@click.option("--dependencies/--no-dependencies", "-d/-nd", default=False)
def install(package, dependencies):
    """Installs a package."""
    package = xpackage.LazyPackage(package)
    installer = xinstaller.Installer(package, with_dependencies=dependencies)
    try:
        installer.install()
    except xinstaller.InstallationIncomplete as e:
        xlogger.get_xinstall_logger().exception(str(e))


@cli.command()
@click.argument("package")
def config(package):
    """Configures a package."""
    package = xpackage.LazyPackage(package)
    configurator = xinstaller.Configurator(package)
    try:
        configurator.config()
    except xinstaller.ConfigurationIncomplete as e:
        xlogger.get_xinstall_logger().exception(str(e))


def main():
    cli()
