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
from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

from .blockartist import *
from .assemblyartist import *


__all__ = [name for name in dir() if not name.startswith('_')]
