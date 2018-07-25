# -*- coding: utf-8 -*-
###########################################################################
# Copyright (c), The AiiDA team. All rights reserved.                     #
# This file is part of the AiiDA code.                                    #
#                                                                         #
# The code is hosted on GitHub at https://github.com/aiidateam/aiida_core #
# For further information on the license, see the LICENSE.txt file        #
# For further information please visit http://www.aiida.net               #
###########################################################################
"""The `verdi data` command line interface."""
import click

from aiida.cmdline.commands import verdi
from aiida.cmdline.utils import decorators, echo
from aiida.cmdline.utils.pluginable import Pluginable


@verdi.group('data', entry_point_group='aiida.cmdline.data', cls=Pluginable)
def verdi_data():
    """Inspect, create and manage data nodes."""
    pass


@verdi_data.command('plugins')
@click.argument('entry_point', type=click.STRING, required=False)
@decorators.with_dbenv()
def data_plugins(entry_point):
    """Print a list of registered data plugins or details of a specific data plugin."""
    from aiida.common.exceptions import LoadingPluginFailed, MissingPluginError
    from aiida.plugins.entry_point import get_entry_point_names, load_entry_point

    if entry_point:
        try:
            plugin = load_entry_point('aiida.data', entry_point)
        except (LoadingPluginFailed, MissingPluginError) as exception:
            echo.echo_critical(exception)
        else:
            echo.echo_info(entry_point)
            echo.echo(plugin.get_description())
    else:
        entry_points = get_entry_point_names('aiida.data')
        if entry_points:
            echo.echo('Registered data entry points:')
            for registered_entry_point in entry_points:
                echo.echo("* {}".format(registered_entry_point))

            echo.echo('')
            echo.echo_info('Pass the entry point as an argument to display detailed information')
        else:
            echo.echo_error('No data plugins found')


# Import to populate the `verdi data` sub commands
# pylint: disable=wrong-import-position
from aiida.cmdline.commands.cmd_data import (
    cmd_array,
    cmd_bands,
    cmd_cif,
    cmd_parameter,
    cmd_remote,
    cmd_structure,
    cmd_trajectory,
    cmd_upf,
)
