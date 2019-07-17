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

    assembly_construct_wall
    assembly_courses
    assembly_interfaces_numpy
    assembly_interfaces_xfunc
    assembly_hull
    assembly_hull_numpy
    assembly_hull_xfunc


"""

from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

import compas

from ._assembly import *
from ._block import *

from .transformations import *

from .constructors import *

from .collision import *
from .courses import *
from .hull import *

if not compas.IPY:
    from .hull_numpy import *

if not compas.IPY:
    from .interfaces_numpy import *

from .paths import *
from .planarization import *

from .sequencing import *


def assembly_interfaces_xfunc(data, **kwargs):
    """Convenience wrapper for ``assembly_interfaces_numpy`` that can be used with ``XFunc`` or ``RPC``.

    Parameters
    ----------
    data : dict
        The data dictionary representing an assembly data structure.
        The dict has the following items:

        * assembly: the assembly data
        * blocks: the data per block

    Returns
    -------
    dict
        A data dict with the same structure as the input dict.

    Notes
    -----
    For additional named parameters that can be passed to this function,
    see ``assembly_interfaces_numpy``.

    Examples
    --------
    .. code-block:: python

        assembly_interfaces_xfunc = XFunc('compas_assembly.datastructures.assembly_interfaces_xfunc')

        data = {'assembly': assembly.to_data(),
                'blocks': {str(key): assembly.blocks[key].to_data() for key in assembly.vertices()}}

        result = assembly_interfaces_xfunc(data)

        assembly.data = result['assembly']
        assembly.blocks = {int(key): Block.from_data(data) for key, data in result['blocks']}

    """
    from compas_assembly.datastructures import Assembly
    from compas_assembly.datastructures import Block
    assembly = Assembly.from_data(data['assembly'])
    assembly.blocks = {int(key): Block.from_data(data['blocks'][key]) for key in data['blocks']}
    assembly_interfaces_numpy(assembly, **kwargs)
    return {'assembly': assembly.to_data(),
            'blocks': {str(key): assembly.blocks[key].to_data() for key in assembly.blocks}}


def assembly_hull_xfunc(data, **kwargs):
    """Convenience wrapper for ``assembly_hull_numpy`` that can be used with ``XFunc`` or ``RPC``.

    Parameters
    ----------
    data : dict
        The data dictionary representing an assembly data structure.
        The dict has the following items:

        * assembly: the assembly data
        * blocks: the data per block

    Returns
    -------
    tuple
        Vertices and faces of the hull.

    Notes
    -----
    For additional named parameters that can be passed to this function,
    see ``assembly_hull_numpy``.

    Examples
    --------
    .. code-block:: python

        assembly_hull_xfunc = XFunc('compas_assembly.datastructures.assembly_hull_xfunc')

        data = {'assembly': assembly.to_data(),
                'blocks': {str(key): assembly.blocks[key].to_data() for key in assembly.vertices()}}

        vertices, faces = assembly_hull_xfunc(data)

    """
    from compas_assembly.datastructures import Assembly
    from compas_assembly.datastructures import Block
    assembly = Assembly.from_data(data['assembly'])
    assembly.blocks = {int(key): Block.from_data(data['blocks'][key]) for key in data['blocks']}
    return assembly_hull_numpy(assembly, **kwargs)


__all__ = [name for name in dir() if not name.startswith('_')]
