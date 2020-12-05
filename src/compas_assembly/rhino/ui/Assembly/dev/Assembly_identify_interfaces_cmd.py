from __future__ import print_function
from __future__ import absolute_import
from __future__ import division

import scriptcontext as sc
import traceback

from compas.rpc import Proxy


proxy = Proxy('compas_assembly.datastructures')
assembly_interfaces_xfunc = proxy.assembly_interfaces_xfunc


def assembly_interfaces(assembly, nmax=10, tmax=0.05, amin=0.01, lmin=0.01):
    data = {
        'assembly': assembly.to_data(),
        'blocks': {str(key): assembly.blocks[key].to_data() for key in assembly.blocks}
    }
    result = assembly_interfaces_xfunc(data, nmax=nmax, tmax=tmax, amin=amin, lmin=lmin)
    assembly.data = result['assembly']
    for key in assembly.blocks:
        assembly.blocks[key].data = result['blocks'][str(key)]


__commandname__ = "Assembly_assembly_interfaces"


def RunCommand(is_interactive):
    try:
        if 'compas_assembly' not in sc.sticky:
            raise Exception('Initialise the Assembly plugin first!')

        assembly = sc.sticky['compas_assembly']['assembly']
        settings = sc.sticky['compas_assembly']['settings']

        assembly_interfaces(assembly, nmax=100)

        assembly.draw(settings)

    except Exception as error:
        print(error)
        print(traceback.format_exc())


if __name__ == '__main__':

    RunCommand(True)
