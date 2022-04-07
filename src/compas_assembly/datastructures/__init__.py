"""
********************************************************************************
compas_assembly.datastructures
********************************************************************************

.. currentmodule:: compas_assembly.datastructures

Classes
=======

.. autosummary::
    :toctree: generated/
    :nosignatures:

    Assembly
    Block
    Interface

"""
from __future__ import absolute_import

from .block import Block
from .interface import Interface
from .assembly import Assembly

__all__ = ["Block", "Interface", "Assembly"]
