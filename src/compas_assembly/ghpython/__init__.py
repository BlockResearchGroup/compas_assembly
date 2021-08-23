"""
********************************************************************************
compas_assembly.ghpython
********************************************************************************

.. currentmodule:: compas_assembly.ghpython

This package defines various classes and functions for working with assemblies
in Rhino.


Classes
=======

.. autosummary::
    :toctree: generated/
    :nosignatures:

    AssemblyArtist
    BlockArtist

"""
from __future__ import absolute_import

from .artists import BlockArtist
from .artists import AssemblyArtist


__all__ = [
    'BlockArtist',
    'AssemblyArtist'
]
