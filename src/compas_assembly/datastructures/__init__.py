"""
********************************************************************************
compas_assembly.datastructures
********************************************************************************

.. currentmodule:: compas_assembly.datastructures


This package defines various data structures for the representation
of discrete/distinct-element assemblies.
The individual elements of an assembly are represented by customised versions of the COMPAS
mesh data structure (:class:`compas.datastructures.Mesh`).
The relationships between the elements in the assembly are represented by
customised versions of the COMPAS network data structure (:class:`compas.datastructures.Network`).


Classes
=======

.. autosummary::
    :toctree: generated/
    :nosignatures:

    Assembly
    Block


Functions
=========

.. autosummary::
    :toctree: generated/
    :nosignatures:

    assembly_courses
    assembly_interfaces_numpy
    assembly_hull
    assembly_hull_numpy


"""

from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

from ._assembly import *
from ._block import *

from .transformations import *

from .constructors import *

from .collision import *
from .courses import *
from .hull import *
from .hull_numpy import *
from .interfaces_numpy import *
from .paths import *
from .planarization import *

from .sequencing import *


def assembly_interfaces_xfunc(data, **kwargs):
    from compas_rbe.datastructures import Assembly
    from compas_rbe.datastructures import Block

    assembly = Assembly.from_data(data['assembly'])
    assembly.blocks = {int(key): Block.from_data(data['blocks'][key]) for key in data['blocks']}

    assembly_interfaces(assembly, **kwargs)

    return {
        'assembly': assembly.to_data(),
        'blocks': {str(key): assembly.blocks[key].to_data() for key in assembly.blocks}
    }


__all__ = [name for name in dir() if not name.startswith('_')]
