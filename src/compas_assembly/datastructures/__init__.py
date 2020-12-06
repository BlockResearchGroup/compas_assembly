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
    Interface


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
from __future__ import division
from __future__ import print_function

import compas

from .block import Block  # noqa: F401
from .interface import Interface  # noqa: F401
from .assembly import Assembly  # noqa: F401

from .hull import *  # noqa: F401 F403

if not compas.IPY:
    from .hull_numpy import *  # noqa: F401 F403
    from .interfaces_numpy import *  # noqa: F401 F403


__all__ = [name for name in dir() if not name.startswith('_')]
