"""
********************************************************************************
compas_assembly.datastructures
********************************************************************************

.. currentmodule:: compas_assembly.datastructures

.. rst-class:: lead

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

import compas

from .block import Block
from .interface import Interface
from .assembly import Assembly

from .hull import assembly_hull

__all__ = [
    'Block',
    'Interface',
    'Assembly',
    'assembly_hull'
]

if not compas.IPY:
    from .hull_numpy import assembly_hull_numpy
    from .interfaces_numpy import assembly_interfaces_numpy

    __all__ += [
        'assembly_hull_numpy',
        'assembly_interfaces_numpy'
    ]
