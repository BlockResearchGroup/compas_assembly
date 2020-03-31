from __future__ import print_function
from __future__ import absolute_import
from __future__ import division


from compas.utilities import pairwise
from compas.geometry import centroid_points


__all__ = ['BlockView', 'InterfaceView']


class BlockView(object):

    def __init__(self, block):
        self._block = None
        self._xyz = None
        self._vertices = None
        self._faces = None
        self.block = block

    @property
    def xyz(self):
        return self._xyz

    @property
    def vertices(self):
        return self.block.vertices()

    @property
    def faces(self):
        return self._faces

    @property
    def edges(self):
        key_index = self.block.key_index()
        for u, v in self.block.edges():
            yield key_index[u], key_index[v]

    @property
    def block(self):
        return self._block

    @block.setter
    def block(self, block):
        self._block = block

        key_index = block.key_index()
        xyz = block.vertices_attributes('xyz')
        faces = []

        for fkey in block.faces():
            fvertices = [key_index[key] for key in block.face_vertices(fkey)]

            f = len(fvertices)
            if f < 3:
                pass
            elif f == 3:
                faces.append(fvertices)
            elif f == 4:
                a, b, c, d = fvertices
                faces.append([a, b, c])
                faces.append([c, d, a])
            else:
                o = block.face_centroid(fkey)
                v = len(xyz)
                xyz.append(o)
                for a, b in pairwise(fvertices + fvertices[0:1]):
                    faces.append([a, b, v])

        self._xyz = xyz
        self._faces = faces


class InterfaceView(object):

    def __init__(self, interface):
        self._interface = None
        self._xyz = None
        self._faces = None
        self.interface = interface

    @property
    def xyz(self):
        return self._xyz

    @property
    def faces(self):
        return self._faces

    @property
    def interface(self):
        return self._interface

    @interface.setter
    def interface(self, interface):
        self._interface = interface

        faces = []
        xyz = interface['interface_points']

        f = len(xyz)

        if f < 3:
            pass

        elif f == 3:
            faces.append([0, 1, 2])

        elif f == 4:
            faces.append([0, 1, 2])
            faces.append([2, 3, 0])
        else:
            c = centroid_points(xyz)
            xyz.append(c)
            for a, b in pairwise(list(range(0, f))):
                faces.append([a, b, f])
            faces.append([b, 0, f])

        self._xyz = xyz
        self._faces = faces


# ==============================================================================
# Main
# ==============================================================================

if __name__ == "__main__":
    pass
