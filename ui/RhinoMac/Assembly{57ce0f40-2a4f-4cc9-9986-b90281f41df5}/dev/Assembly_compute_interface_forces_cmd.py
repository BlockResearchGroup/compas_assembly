from __future__ import print_function
from __future__ import absolute_import
from __future__ import division

import scriptcontext as sc
import traceback

import compas_rbe

from compas_rhino.utilities import XFunc


compute_interface_forces_xfunc = XFunc('compas_rbe.equilibrium.compute_interface_forces_xfunc', tmpdir=compas_rbe.TEMP)


def compute_interface_forces(assembly, solver):
    data = {
        'assembly': assembly.to_data(),
        'blocks': {str(key): assembly.blocks[key].to_data() for key in assembly.blocks},
    }
    result = compute_interface_forces_xfunc(data, solver=solver)
    assembly.data = result['assembly']
    for key in assembly.blocks:
        assembly.blocks[key].data = result['blocks'][str(key)]


__commandname__ = "Assembly_compute_interface_forces"


def RunCommand(is_interactive):
    try:
        if 'compas_assembly' not in sc.sticky:
            raise Exception('Initialise the Assembly plugin first!')

        assembly = sc.sticky['compas_assembly']['assembly']
        settings = sc.sticky['compas_assembly']['settings']

        python = settings['python']
        solver = settings['solver']

        compute_interface_forces_xfunc.python = python
        compute_interface_forces(assembly, solver)

        assembly.draw(settings)

    except Exception as error:
        print(error)
        print(traceback.format_exc())


if __name__ == '__main__':

    RunCommand(True)
