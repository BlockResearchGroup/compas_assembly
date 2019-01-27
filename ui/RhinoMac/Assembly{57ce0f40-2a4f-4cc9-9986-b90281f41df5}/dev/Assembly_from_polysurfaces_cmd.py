from __future__ import print_function
from __future__ import absolute_import
from __future__ import division


import scriptcontext as sc

import traceback

import compas_rhino
from compas_assembly.datastructures import Assembly


__commandname__ = "Assembly_from_polysurfaces"


def RunCommand(is_interactive):
    try:
        if 'compas_assembly' not in sc.sticky:
            raise Exception('Initialise the Assembly plugin first!')

        settings = sc.sticky['compas_assembly']['settings']

        guids = compas_rhino.select_surfaces()

        assembly = Assembly()
        assembly.add_blocks_from_polysurfaces(guids)
        assembly.draw(settings)

        sc.sticky['compas_assembly']['assembly'] = assembly

    except Exception as error:
        print(error)
        print(traceback.format_exc())


if __name__ == '__main__':

    RunCommand(True)
