from __future__ import absolute_import

from compas.plugins import plugin
from compas.artists import Artist

from compas_assembly.datastructures import Assembly
from .assemblyartist import RhinoAssemblyArtist


@plugin(category="factories", requires=["Rhino"])
def register_artists():
    Artist.register(Assembly, RhinoAssemblyArtist, context="Rhino")
