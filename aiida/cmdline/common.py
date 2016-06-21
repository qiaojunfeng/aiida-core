# -*- coding: utf-8 -*-
import os
import sys

from aiida.backends.utils import load_dbenv, is_dbenv_loaded
from aiida.cmdline import delayed_load_node as load_node
from aiida.cmdline.baseclass import VerdiCommandWithSubcommands

__copyright__ = u"Copyright (c), This file is part of the AiiDA platform. For further information please visit http://www.aiida.net/.. All rights reserved."
__license__ = "MIT license, see LICENSE.txt file"
__version__ = "0.6.0"
__authors__ = "The AiiDA team."


def print_node_summary(node):
    from tabulate import tabulate

    table = []
    table.append(["type", node.__class__.__name__])
    table.append(["pk", str(node.pk)])
    table.append(["uuid", str(node.uuid)])
    table.append(["label", node.label])
    table.append(["description", node.description])
    table.append(["ctime", node.ctime])
    table.append(["mtime", node.mtime])
    if node.get_computer() is not None:
        table.append(["computer",
                      "[{}] {}".format(node.get_computer().pk,
                                       node.get_computer().name)])
    print(tabulate(table))


def print_node_info(node, print_summary=True):
    from aiida.backends.utils import get_log_messages
    from tabulate import tabulate

    if print_summary:
        print_node_summary(node)

    table_headers = ['Link label', 'PK', 'Type']

    code = node.get_code()
    if code is not None:
        print "Using code: {}".format(code.label)

    table = []
    print "##### INPUTS:"
    for k, v in node.get_inputs_dict().iteritems():
        if k == 'code': continue
        table.append([k, v.pk, v.__class__.__name__])
    print(tabulate(table, headers=table_headers))

    table = []
    print "##### OUTPUTS:"
    for k, v in node.get_outputs(also_labels=True):
        table.append([k, v.pk, v.__class__.__name__])
    print(tabulate(table, headers=table_headers))

    log_messages = get_log_messages(node)
    if log_messages:
        print ("##### NOTE! There are {} log messages for this "
               "calculation.".format(len(log_messages)))
        print "      Use the 'calculation logshow' command to see them."
