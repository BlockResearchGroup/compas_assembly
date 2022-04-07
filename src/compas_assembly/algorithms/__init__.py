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
    assembly_interfaces_numpy

"""
from __future__ import absolute_import

import compas

from .hull import assembly_hull

__all__ = ["assembly_hull"]

if not compas.IPY:
    from .hull_numpy import assembly_hull_numpy
    from .interfaces_numpy import assembly_interfaces_numpy

    __all__ += ["assembly_hull_numpy", "assembly_interfaces_numpy"]
