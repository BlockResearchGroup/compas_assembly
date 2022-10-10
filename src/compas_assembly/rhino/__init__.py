"""
********************************************************************************
compas_assembly.rhino
********************************************************************************

.. currentmodule:: compas_assembly.rhino

Classes
=======

.. autosummary::
    :toctree: generated/
    :nosignatures:

    RhinoAssemblyArtist

"""
from __future__ import absolute_import

from compas.plugins import plugin
from compas.artists import Artist

from compas_assembly.datastructures import Assembly
from .assemblyartist import RhinoAssemblyArtist


@plugin(category="factories", requires=["Rhino"])
def register_artists():
    Artist.register(Assembly, RhinoAssemblyArtist, context="Rhino")


__all__ = ["RhinoAssemblyArtist"]
