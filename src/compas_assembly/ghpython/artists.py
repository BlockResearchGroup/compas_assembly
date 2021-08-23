from __future__ import print_function
from __future__ import absolute_import
from __future__ import division

from compas_ghpython.artists import MeshArtist
from compas_ghpython.artists import NetworkArtist


class AssemblyArtist(NetworkArtist):
    """An artist for visualisation of assemblies in GHPython.

    Parameters
    ----------
    assembly : compas_assembly.datastructures.Assembly
        The assembly data structure.
    layer : str, optional
        The base layer for drawing.
        Default is ``None``, which means drawing in the current layer.

    Examples
    --------
    .. code-block:: python

        pass

    """

    def __init__(self, assembly):
        super(AssemblyArtist, self).__init__(assembly)
        self.defaults.update({
            'color.vertex': (0, 0, 0),
            'color.vertex:is_support': (255, 0, 0),
            'color.edge': (0, 0, 0),
            'color.interface': (255, 255, 255),
            'color.force:compression': (0, 0, 255),
            'color.force:tension': (255, 0, 0),
            'color.force:friction': (255, 165, 0),
            'color.selfweight': (0, 255, 0),
            'scale.force': 0.1,
            'scale.selfweight': 0.1,
            'scale.friction': 0.1,
            'eps.selfweight': 1e-3,
            'eps.force': 1e-3,
            'eps.friction': 1e-3,
            'range.friction': 5,
        })

    @property
    def assembly(self):
        """Assembly : the assembly data structure."""
        return self.datastructure

    @assembly.setter
    def assembly(self, assembly):
        self.datastructure = assembly

    def draw_blocks(self, keys=None, show_faces=False, show_edges=True, show_vertices=False):
        """Draw the blocks of the assembly.

        Parameters
        ----------
        show_faces : bool, optional
            Draw the faces of the block.
            Default is ``False``.
        show_vertices : bool, optional
            Draw the vertices of the block.
            Default is ``False``.

        Notes
        -----
        * By default, blocks are drawn as wireframes.
        * By default, blocks are drawn on a sublayer of the base layer, if a base layer was specified.
        * Block names have the following pattern: ``"{assembly_name}.block.{block_id}"``
        * Faces and vertices can be drawn using the corresponding flags.
        * Block components have the following pattern:

          * face: ``"{assembly_name}.block.{block_id}.face.{face_id}"``
          * edge: ``"{assembly_name}.block.{block_id}.edge.{edge_id}"``
          * vertex: ``"{assembly_name}.block.{block_id}.vertex.{vertex_id}"``


        Examples
        --------
        >>>
        """
        keys = keys or list(self.assembly.vertices())
        artist = BlockArtist(None)
        meshes = []
        for key in keys:
            block = self.assembly.blocks[key]
            block.name = "{}.block.{}".format(self.assembly.name, key)
            artist.block = block
            # if not show_faces and not show_vertices:
            #     show_edges = True
            # if show_edges:
            #    edges = artist.draw_edges()
            # if show_faces:
            #    faces = artist.draw_faces()
            # if show_vertices:
            #    vertices = artist.draw_vertices()
            meshes.append(artist.draw())
        return meshes


class BlockArtist(MeshArtist):
    """An artist for painting blocks."""

    def __init__(self, *args, **kwargs):
        super(BlockArtist, self).__init__(*args, **kwargs)
        self.defaults.update({
            'color.vertex': (0, 0, 0),
            'color.edge': (0, 0, 0),
            'color.face': (255, 255, 255),
        })

    @property
    def block(self):
        return self.datastructure

    @block.setter
    def block(self, block):
        self.datastructure = block
