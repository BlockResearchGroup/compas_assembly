from __future__ import absolute_import

from compas.plugins import plugin
from compas.artists import Artist

from compas_assembly.datastructures import Assembly
from .assemblyartist import AssemblyArtist


@plugin(category="factories", pluggable_name="register_artists", requires=["Rhino"])
def register_artists_rhino():
    Artist.register(Assembly, AssemblyArtist, context="Rhino")


@plugin(category="factories", pluggable_name="register_artists", requires=["bpy"])
def register_artists_blender():
    Artist.register(Assembly, AssemblyArtist, context="Blender")
