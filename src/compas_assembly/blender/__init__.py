"""
********************************************************************************
compas_assembly.blender
********************************************************************************

.. currentmodule:: compas_assembly.blender

This package defines various classes and functions for working with assemblies
in blender.


Classes
=======

.. autosummary::
    :toctree: generated/
    :nosignatures:

    BlockArtist
    AssemblyArtist

"""

# from .blockartist import *
from .assemblyartist import *


__all__ = [name for name in dir() if not name.startswith('_')]
