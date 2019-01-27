from __future__ import print_function
from __future__ import absolute_import
from __future__ import division

import scriptcontext as sc
import traceback

import compas_rhino
import compas_assembly

from compas_assembly.datastructures import Assembly


__commandname__ = "Assembly_from_json"


def RunCommand(is_interactive):
    try:
        if 'compas_assembly' not in sc.sticky:
            raise Exception('Initialise the Assembly plugin first!')

        settings = sc.sticky['compas_assembly']['settings']

        # the default path points to the wrong location
        path = compas_rhino.select_file(folder=compas_assembly.DATA,
                                        filter='JSON files (*.json)|*.json||')
        if not path:
            return

        assembly = Assembly.from_json(path)
        sc.sticky['compas_assembly']['assembly'] = assembly

        assembly.draw(settings)

    except Exception as error:
        print(error)
        print(traceback.format_exc())


if __name__ == '__main__':

    RunCommand(True)
