from __future__ import print_function
from __future__ import absolute_import
from __future__ import division

import scriptcontext as sc
import traceback

import compas_assembly

from compas_rhino.utilities import XFunc


identify_interfaces_xfunc = XFunc('compas_assembly.datastructures.identify_interfaces_xfunc')
identify_interfaces_xfunc.tmpdir = compas_assembly.TEMP


def identify_interfaces(assembly, nmax=10, tmax=0.05, amin=0.01, lmin=0.01):
    data = {
        'assembly': assembly.to_data(),
        'blocks': {str(key): assembly.blocks[key].to_data() for key in assembly.blocks}
    }
    result = identify_interfaces_xfunc(data, nmax=nmax, tmax=tmax, amin=amin, lmin=lmin)
    assembly.data = result['assembly']
    for key in assembly.blocks:
        assembly.blocks[key].data = result['blocks'][str(key)]


__commandname__ = "Assembly_identify_interfaces"


def RunCommand(is_interactive):
    try:
        if 'compas_assembly' not in sc.sticky:
            raise Exception('Initialise the Assembly plugin first!')

        assembly = sc.sticky['compas_assembly']['assembly']
        settings = sc.sticky['compas_assembly']['settings']

        python = settings['python']

        identify_interfaces_xfunc.python = python
        identify_interfaces(assembly)

        assembly.draw(settings)

    except Exception as error:
        print(error)
        print(traceback.format_exc())


if __name__ == '__main__':

    RunCommand(True)
