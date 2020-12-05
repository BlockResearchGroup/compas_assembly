from __future__ import print_function
from __future__ import absolute_import
from __future__ import division

import rhinoscriptsyntax as rs
import scriptcontext as sc
import traceback
import os

import compas_rhino
import compas_rbe


__commandname__ = "Assembly_to_json"


def RunCommand(is_interactive):
    try:
        if 'compas_assembly' not in sc.sticky:
            raise Exception('Initialise the Assembly plugin first!')

        assembly = sc.sticky['compas_assembly']['assembly']

        folder = compas_rhino.select_folder(default=compas_rbe.DATA)
        print(folder)
        if not folder:
            return

        filename = rs.GetString('Name of the json file?')
        print(filename)
        if not filename:
            return

        name, ext = os.path.splitext(filename)
        if ext != '.json':
            filename = name + ext + '.json'

        assembly.to_json(os.path.join(folder, filename))

    except Exception as error:
        print(error)
        print(traceback.format_exc())


if __name__ == '__main__':

    RunCommand(True)
