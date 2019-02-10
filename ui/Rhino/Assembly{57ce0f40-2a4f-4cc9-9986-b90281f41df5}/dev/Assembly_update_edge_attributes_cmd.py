from __future__ import print_function
from __future__ import absolute_import
from __future__ import division

import scriptcontext as sc
import traceback

from compas_rbe.rhino import AssemblyHelper


__commandname__ = "Assembly_update_edge_attributes"


def RunCommand(is_interactive):
    try:
        if 'compas_assembly' not in sc.sticky:
            raise Exception('Initialise the Assembly plugin first!')

        assembly = sc.sticky['compas_assembly']['assembly']
        settings = sc.sticky['compas_assembly']['settings']

        keys = AssemblyHelper.select_edges(assembly)
        if not keys:
            return

        if AssemblyHelper.update_edge_attributes(assembly, keys):
            assembly.draw(settings)

    except Exception as error:
        print(error)
        print(traceback.format_exc())


if __name__ == '__main__':

    RunCommand(True)
