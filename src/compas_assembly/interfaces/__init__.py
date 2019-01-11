"""
********************************************************************************
compas_assembly.interfaces
********************************************************************************

.. currentmodule:: compas_assembly.interfaces


This package defines basic functionality for handling the interfaces between
the individual elements of an assembly.


Functions
=========

.. autosummary::
    :toctree: generated/
    :nosignatures:

    identify_interfaces
    identify_interfaces_bestfit
    identify_interfaces_offset

"""
from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

from .identify import *
from .planarize import *


def identify_interfaces_xfunc(data, **kwargs):
    from compas_assembly.datastructures import Assembly
    from compas_assembly.datastructures import Block

    assembly = Assembly.from_data(data['assembly'])
    assembly.blocks = {
        int(key): Block.from_data(data['blocks'][key])
        for key in data['blocks']
    }

    identify_interfaces(assembly, **kwargs)

    return {
        'assembly': assembly.to_data(),
        'blocks':
        {str(key): assembly.blocks[key].to_data()
         for key in assembly.blocks}
    }


def identify_interfaces_offset_xfunc(data, **kwargs):
    from compas_assembly.datastructures import Assembly
    from compas_assembly.datastructures import Block

    assembly = Assembly.from_data(data['assembly'])
    assembly.blocks = {
        int(key): Block.from_data(data['blocks'][key])
        for key in data['blocks']
    }

    identify_interfaces_offset(assembly, **kwargs)

    return {
        'assembly': assembly.to_data(),
        'blocks':
        {str(key): assembly.blocks[key].to_data()
         for key in assembly.blocks}
    }


__all__ = [name for name in dir() if not name.startswith('_')]
