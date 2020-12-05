"""
********************************************************************************
compas_assembly.blender
********************************************************************************

.. currentmodule:: compas_assembly.blender

Artists
=======

.. autosummary::
    :toctree: generated/
    :nosignatures:

    BlockArtist
    AssemblyArtist

"""

from .assemblyartist import *  # noqa: F401 F403


__all__ = [name for name in dir() if not name.startswith('_')]
