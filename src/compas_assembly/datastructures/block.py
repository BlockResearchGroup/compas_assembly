from __future__ import print_function
from __future__ import absolute_import
from __future__ import division

from compas.geometry import centroid_points
from compas.geometry import cross_vectors
from compas.geometry import dot_vectors
from compas.geometry import normalize_vector
from compas.geometry import centroid_polyhedron
from compas.geometry import volume_polyhedron

from compas.datastructures import Mesh


class Block(Mesh):
    """A data structure for the individual blocks of a discrete element assembly.

    Examples
    --------
    >>>
    """

    def __init__(self):
        super(Block, self).__init__()

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
        from compas_rhino.geometry import RhinoSurface
        surface = RhinoSurface.from_guid(guid)
        return surface.to_compas(cls)

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
        from compas_rhino.geometry import RhinoMesh
        mesh = RhinoMesh.from_guid(guid)
        return mesh.to_compas(cls)

    def centroid(self):
        """Compute the centroid of the block.

        Returns
        -------
        point
            The XYZ location of the centroid.
        """
        return centroid_points(
            [self.vertex_coordinates(key) for key in self.vertices()])

    def frames(self):
        """Compute the local frame of each face of the block.

        Returns
        -------
        dict
            A dictionary mapping face identifiers to face frames.
        """
        return {fkey: self.frame(fkey) for fkey in self.faces()}

    def frame(self, fkey):
        """Compute the frame of a specific face.

        Parameters
        ----------
        fkey : hashable
            The identifier of the frame.

        Returns
        -------
        frame
            The frame of the specified face.
        """
        xyz = self.face_coordinates(fkey)
        o = self.face_center(fkey)
        w = self.face_normal(fkey)
        u = [xyz[1][i] - xyz[0][i] for i in range(3)]  # align with longest edge instead?
        v = cross_vectors(w, u)
        uvw = normalize_vector(u), normalize_vector(v), normalize_vector(w)
        return o, uvw

    def top(self):
        """Identify the *top* face of the block.

        Returns
        -------
        int
            The identifier of the face.
        """
        z = [0, 0, 1]
        faces = list(self.faces())
        normals = [self.face_norma(face) for face in faces]
        return sorted(zip(faces, normals), key=lambda x: dot_vectors(x[1], z))[-1][0]

    def center(self):
        """Compute the center of mass of the block.

        Returns
        -------
        point
            The center of mass of the block.
        """
        vertices = [self.vertex_coordinates(key) for key in self.vertices()]
        faces = [self.face_vertices(fkey) for fkey in self.faces()]
        return centroid_polyhedron((vertices, faces))

    def volume(self):
        """Compute the volume of the block.

        Returns
        -------
        float
            The volume of the block.
        """
        vertices = [self.vertex_coordinates(key) for key in self.vertices()]
        faces = [self.face_vertices(fkey) for fkey in self.faces()]
        v = volume_polyhedron((vertices, faces))
        return v
