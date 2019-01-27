from __future__ import print_function
from __future__ import absolute_import
from __future__ import division


import scriptcontext as sc

import os
import json
import traceback

import compas_rhino

from compas_rbe.datastructures import Assembly
from compas_rbe.datastructures import Block


HERE = os.path.abspath(os.path.dirname(__file__))
SESSIONS = os.path.join(HERE, '../sessions')


__commandname__ = "Assembly_load_session"


def RunCommand(is_interactive):
    try:
        if 'compas_assembly' not in sc.sticky:
            raise Exception('Initialise the Assembly plugin first!')

        path = compas_rhino.select_file(folder=SESSIONS, filter='JSON files (*.json)|*.json||')
        if not path:
            return

        with open(path, 'r') as fo:
            session = json.load(fo)

        if 'blocks' not in session:
            raise Exception('Session data is incomplete.')
        if 'assembly' not in session:
            raise Exception('Session data is incomplete.')
        if 'settings' not in session:
            raise Exception('Session data is incomplete.')

        sc.sticky['compas_assembly']['settings'].update(session['settings'])
        settings = sc.sticky['compas_assembly']['settings']

        assembly = Assembly.from_data(session['assembly'])
        assembly.blocks = {key: Block.from_data(data) for key, data in session['blocks'].items()}
        assembly.draw(settings)

        sc.sticky['compas_assembly']['assembly'] = assembly

    except Exception as error:
        print(error)
        print(traceback.format_exc())


if __name__ == '__main__':

    RunCommand(True)
