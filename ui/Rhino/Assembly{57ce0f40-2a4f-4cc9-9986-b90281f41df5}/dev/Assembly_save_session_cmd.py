from __future__ import print_function
from __future__ import absolute_import
from __future__ import division


import rhinoscriptsyntax as rs
import scriptcontext as sc

import os
import json
import traceback

import compas_rhino


HERE = os.path.abspath(os.path.dirname(__file__))
SESSIONS = os.path.join(HERE, '../sessions')


__commandname__ = "Assembly_save_session"


def RunCommand(is_interactive):
    try:
        if 'compas_assembly' not in sc.sticky:
            raise Exception('Initialise the Assembly plugin first!')

        assembly = sc.sticky['compas_assembly']['assembly']
        settings = sc.sticky['compas_assembly']['settings']

        session_dir = compas_rhino.select_folder('Save where?', SESSIONS)
        if not session_dir:
            return

        session_name = rs.GetString('Session name', 'session.compas_assembly')
        if not session_name:
            return

        session_path = os.path.join(session_dir, session_name)

        Blocks = {key: assembly.blocks[key].to_data() for key in assembly.vertices()}

        data = {
            'settings' : settings,
            'assembly' : assembly.to_data(),
            'blocks'   : Blocks,
        }

        with open(session_path, 'w+') as fo:
            json.dump(data, fo)

    except Exception as error:
        print(error)
        print(traceback.format_exc())


if __name__ == '__main__':

    RunCommand(True)
