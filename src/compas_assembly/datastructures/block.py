from __future__ import print_function
from __future__ import absolute_import
from __future__ import division

from compas.geometry import centroid_points
from compas.geometry import cross_vectors
from compas.geometry import dot_vectors
from compas.geometry import centroid_polyhedron
from compas.geometry import volume_polyhedron

from compas.geometry import Point
from compas.geometry import Frame

from compas.datastructures import Mesh


class Block(Mesh):
    """A data structure for the individual blocks of a discrete element assembly."""

    def __init__(self, node=None):
        super(Block, self).__init__()
        self.attributes.update({"node": None})
        self.node = node

    @property
    def node(self):
        return self.attributes["node"]

    @node.setter
    def node(self, node):
        self.attributes["node"] = node

    # ==========================================================================
    # constructors
    # ==========================================================================

    @classmethod
    def from_polysurface(cls, guid):
        """Class method for constructing a block from a Rhino poly-surface.

        Parameters
        ----------
        guid : str
            The GUID of the poly-surface.

        Returns
        -------
        Block
            The block corresponding to the poly-surface.

        Notes
        -----
        In Rhino, poly-surfaces are organised such that the cycle directions of
        the individual sub-surfaces produce normal vectors that point out of the
        enclosed volume. The normal vectors of the faces of the mesh, therefore
        also point "out" of the enclosed volume.

        """
        from compas_rhino.conversions import RhinoSurface

        surface = RhinoSurface.from_guid(guid)
        return surface.to_compas_mesh(cls)

    @classmethod
    def from_rhinomesh(cls, guid):
        """Class method for constructing a block from a Rhino mesh.

        Parameters
        ----------
        guid : str
            The GUID of the mesh.

        Returns
        -------
        Block
            The block corresponding to the Rhino mesh.

        """
        from compas_rhino.conversions import RhinoMesh

        mesh = RhinoMesh.from_guid(guid)
        return mesh.to_compas(cls)

    def centroid(self):
        """Compute the centroid of the block.

        Returns
        -------
        :class:`compas.geometry.Point`

        """
        x, y, z = centroid_points(
            [self.vertex_coordinates(key) for key in self.vertices()]
        )
        return Point(x, y, z)

    def frames(self):
        """Compute the local frame of each face of the block.

        Returns
        -------
        dict
            A dictionary mapping face identifiers to face frames.

        """
        return {face: self.frame(face) for face in self.faces()}

    def frame(self, face):
        """Compute the frame of a specific face.

        Parameters
        ----------
        face : int
            The identifier of the frame.

        Returns
        -------
        :class:`compas.geometry.Frame`

        """
        xyz = self.face_coordinates(face)
        o = self.face_center(face)
        w = self.face_normal(face)
        u = [
            xyz[1][i] - xyz[0][i] for i in range(3)
        ]  # align with longest edge instead?
        v = cross_vectors(w, u)
        return Frame(o, u, v)

    def top(self):
        """Identify the *top* face of the block.

        Returns
        -------
        int
            The identifier of the face.

        """
        z = [0, 0, 1]
        faces = list(self.faces())
        normals = [self.face_normal(face) for face in faces]
        return sorted(zip(faces, normals), key=lambda x: dot_vectors(x[1], z))[-1][0]

    def center(self):
        """Compute the center of mass of the block.

        Returns
        -------
        :class:`compas.geometry.Point`

        """
        vertex_index = {vertex: index for index, vertex in enumerate(self.vertices())}
        vertices = [self.vertex_coordinates(vertex) for vertex in self.vertices()]
        faces = [
            [vertex_index[vertex] for vertex in self.face_vertices(face)]
            for face in self.faces()
        ]
        x, y, z = centroid_polyhedron((vertices, faces))
        return Point(x, y, z)

    def volume(self):
        """Compute the volume of the block.

        Returns
        -------
        float
            The volume of the block.

        """
        vertex_index = {vertex: index for index, vertex in enumerate(self.vertices())}
        vertices = [self.vertex_coordinates(vertex) for vertex in self.vertices()]
        faces = [
            [vertex_index[vertex] for vertex in self.face_vertices(face)]
            for face in self.faces()
        ]
        v = volume_polyhedron((vertices, faces))
        return v
