from __future__ import print_function
from __future__ import absolute_import
from __future__ import division

import os

import scriptcontext as sc
import traceback

import compas_rhino

from compas.rpc import Proxy

import clr

clr.AddReference("Eto")
clr.AddReference("Rhino.UI")


__commandname__ = "Assembly_init"


def RunCommand(is_interactive):
    try:
        proxy = Proxy()

        sc.sticky['compas_assembly'] = {
            'settings': {
                'layer': 'Assembly',
                'solver': 'ECOS',
                'scale.selfweight': 0.1,
                'scale.force': 0.1,
                'scale.friction': 0.1,
                'color.edge': (0, 0, 0),
                'color.vertex': (0, 0, 0),
                'color.vertex:is_support': (255, 0, 0),
                'eps.force': 1e-3,
                'eps.selfweight': 1e-3,
                'eps.friction': 1e-3,
                'show.vertices': True,
                'show.edges': False,
                'show.interfaces': True,
                'show.forces': True,
                'show.forces_as_vectors': False,
                'show.selfweight': True,
                'show.frictions': True,
                'range.friction': 5,
                'mode.interface': 0,
                'mode.friction': 0,
                'mode.force': 0,
            },
            'assembly': None,
        }

        compas_rhino.clear_layer(sc.sticky['compas_assembly']['settings']['layer'])

        print('success')

    except Exception as error:
        print(error)
        print(traceback.format_exc())


if __name__ == '__main__':

    RunCommand(True)
