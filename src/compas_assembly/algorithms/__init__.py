"""
********************************************************************************
compas_assembly.algorithms
********************************************************************************

.. currentmodule:: compas_assembly.algorithms


Functions
=========

.. autosummary::
    :toctree: generated/
    :nosignatures:

    assembly_hull
    assembly_hull_numpy
    assembly_interfaces
    assembly_interfaces_numpy
    mesh_mesh_interfaces
    merge_coplanar_interfaces

"""
from __future__ import absolute_import

import compas

from .hull import assembly_hull

__all__ = ["assembly_hull"]

if not compas.IPY:
    from .hull_numpy import assembly_hull_numpy
    from .interfaces import assembly_interfaces
    from .interfaces import mesh_mesh_interfaces
    from .interfaces import merge_coplanar_interfaces
    from .interfaces_numpy import assembly_interfaces_numpy

    __all__ += [
        "assembly_hull_numpy",
        "assembly_interfaces",
        "mesh_mesh_interfaces",
        "merge_coplanar_interfaces",
        "assembly_interfaces_numpy",
    ]
