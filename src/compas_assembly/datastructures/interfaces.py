from __future__ import print_function
from __future__ import absolute_import
from __future__ import division

from math import fabs

import compas

try:
    from numpy import array

    from scipy.linalg import solve
    from scipy.spatial import cKDTree
except ImportError:
    compas.raise_if_not_ironpython()

try:
    from shapely.geometry import Polygon
except ImportError:
    compas.raise_if_not_ironpython()

from compas.geometry import global_coords_numpy
# from compas.geometry import project_points_plane
# from compas.geometry import centroid_points


__all__ = [
    'assembly_interfaces',
]


def _find_nearest_neighbours(cloud, nmax):
    tree = cKDTree(cloud)
    nnbrs = [tree.query(root, nmax) for root in cloud]
    nnbrs = [(d.flatten().tolist(), n.flatten().tolist()) for d, n in nnbrs]
    return nnbrs


def identify_interface(assembly, a, b):
    pass


def assembly_interfaces(assembly,
                        nmax=10,
                        tmax=1e-6,
                        amin=1e-1,
                        lmin=1e-3,
                        face_face=True,
                        face_edge=False,
                        face_vertex=False):
    """Identify the interfaces between the blocks of an assembly.

    Parameters
    ----------
    assembly : compas_assembly.datastructures.Assembly
        An assembly of discrete blocks.
    nmax : int, optional
        Maximum number of neighbours per block.
        Default is ``10``.
    tmax : float, optional
        Maximum deviation from the perfectly flat interface plane.
        Default is ``1e-6``.
    amin : float, optional
        Minimum area of a "face-face" interface.
        Default is ``1e-1``.
    lmin : float, optional
        Minimum length of a "face-edge" interface.
        Default is ``1e-3``.
    face_face : bool, optional
        Test for "face-face" interfaces.
        Default is ``True``.
    face_edge : bool, optional
        Test for "face-edge" interfaces.
        Default is ``False``.
    face_vertex : bool, optional
        Test for "face-vertex" interfaces.
        Default is ``False``.

    References
    ----------
    The identification of interfaces is discussed in detail here [Frick2016]_.

    Examples
    --------
    .. code-block:: python

        pass

    """
    # replace by something proper
    assembly.edge = {}
    assembly.halfedge = {}
    for key in assembly.vertices():
        assembly.edge[key] = {}
        assembly.halfedge[key] = {}

    key_index = assembly.key_index()
    index_key = assembly.index_key()

    blocks = [assembly.blocks[key] for key in assembly.vertices()]
    nmax = min(nmax, len(blocks))
    block_cloud = assembly.get_vertices_attributes('xyz')
    block_nnbrs = _find_nearest_neighbours(block_cloud, nmax)

    # k:      key of the base block
    # i:      index of the base block
    # block:  base block
    # nbrs:   list of indices of the neighbouring blocks
    # frames: list of frames for each of the faces of the base block

    # f0:   key of the current base face
    # A:    uvw base frame of f0
    # o:    origin of the base frame of f0
    # xyz0: xyz coordinates of the vertices of f0
    # rst0: local coordinates of the vertices of f0, with respect to the frame of f0
    # p0:   2D polygon of f0 in local coordinates

    # j:   index of the current neighbour
    # n:   key of the current neighbour
    # nbr: neighbour block
    # k_i: key index map for the vertices of the nbr block
    # xyz: xyz coorindates of all vertices of nbr
    # rst: local coordinates of all vertices of nbr, with respect to the frame of f0

    # f1:   key of the current neighbour face
    # rst1: local coordinates of the vertices of f1, with respect to the frame of f0
    # p1:   2D polygon of f1 in local coordinates

    for k in assembly.vertices():

        i = key_index[k]

        block = assembly.blocks[k]
        nbrs = block_nnbrs[i][1]

        frames = block.frames()

        if face_face:

            # parallelise?
            # exclude faces with parallel normals
            # e.g. exclude overlapping top faces of two neighbouring blocks in same row

            for f0, (origin, uvw) in frames.items():
                A = array(uvw, dtype=float)
                o = array(origin, dtype=float).reshape((-1, 1))
                xyz0 = array(block.face_coordinates(f0), dtype=float).reshape((-1, 3)).T
                rst0 = solve(A.T, xyz0 - o).T.tolist()
                p0 = Polygon(rst0)

                for j in nbrs:
                    n = index_key[j]

                    if n == k:
                        continue

                    if k in assembly.edge and n in assembly.edge[k]:
                        continue

                    if n in assembly.edge and k in assembly.edge[n]:
                        continue

                    nbr = assembly.blocks[n]
                    k_i = {key: index for index, key in enumerate(nbr.vertices())}
                    xyz = array(nbr.get_vertices_attributes('xyz'), dtype=float).reshape((-1, 3)).T
                    rst = solve(A.T, xyz - o).T.tolist()
                    rst = {key: rst[k_i[key]] for key in nbr.vertices()}

                    for f1 in nbr.faces():

                        rst1 = [rst[key] for key in nbr.face_vertices(f1)]

                        if any(fabs(t) > tmax for r, s, t in rst1):
                            continue

                        p1 = Polygon(rst1)

                        if p1.area == 0.0:
                            continue

                        if p0.intersects(p1):
                            intersection = p0.intersection(p1)

                            area = intersection.area

                            if area >= amin:
                                coords = [[x, y, 0.0] for x, y, z in intersection.exterior.coords]
                                coords = global_coords_numpy(o, A, coords)

                                attr = {
                                    'interface_type': 'face_face',
                                    'interface_size': area,
                                    'interface_points': coords.tolist()[:-1],
                                    'interface_origin': origin,
                                    'interface_uvw': uvw,
                                }

                                assembly.add_edge(k, n, attr_dict=attr)


# def assembly_interfaces_bestfit(assembly,
#                                 nmax=10,
#                                 tmax=1e-6,
#                                 amin=1e-1,
#                                 lmin=1e-3,
#                                 face_face=True,
#                                 face_edge=False,
#                                 face_vertex=False):
#     """Identify the bestfit planar interfaces between the blocks of an assembly.

#     Parameters
#     ----------
#     assembly : compas_assembly.datastructures.Assembly
#         An assembly of discrete blocks.
#     nmax : int, optional
#         Maximum number of neighbours per block.
#         Default is ``10``.
#     tmax : float, optional
#         Maximum deviation from the perfectly flat interface plane.
#         Default is ``1e-6``.
#     amin : float, optional
#         Minimum area of a "face-face" interface.
#         Default is ``1e-1``.
#     lmin : float, optional
#         Minimum length of a "face-edge" interface.
#         Default is ``1e-3``.
#     face_face : bool, optional
#         Test for "face-face" interfaces.
#         Default is ``True``.
#     face_edge : bool, optional
#         Test for "face-edge" interfaces.
#         Default is ``False``.
#     face_vertex : bool, optional
#         Test for "face-vertex" interfaces.
#         Default is ``False``.

#     References
#     ----------
#     The identification of interfaces is discussed in detail here [Frick2016]_.

#     Examples
#     --------
#     .. code-block:: python

#         pass

#     """

#     key_index = {key: index for index, key in enumerate(assembly.vertices())}
#     index_key = {index: key for index, key in enumerate(assembly.vertices())}

#     blocks = [assembly.blocks[key] for key in assembly.vertices()]
#     nmax = min(nmax, len(blocks))
#     block_cloud = [
#         assembly.vertex_coordinates(key) for key in assembly.vertices()
#     ]
#     block_nnbrs = _find_nearest_neighbours(block_cloud, nmax)

#     # k:      key of the base block
#     # i:      index of the base block
#     # block:  base block
#     # nbrs:   list of indices of the neighbouring blocks
#     # frames: list of frames for each of the faces of the base block

#     # f0:   key of the current base face
#     # A:    uvw base frame of f0
#     # o:    origin of the base frame of f0
#     # xyz0: xyz coordinates of the vertices of f0
#     # rst0: local coordinates of the vertices of f0, with respect to the frame of f0
#     # p0:   2D polygon of f0 in local coordinates

#     # j:   index of the current neighbour
#     # n:   key of the current neighbour
#     # nbr: neighbour block
#     # k_i: key index map for the vertices of the nbr block
#     # xyz: xyz coorindates of all vertices of nbr
#     # rst: local coordinates of all vertices of nbr, with respect to the frame of f0

#     # f1:   key of the current neighbour face
#     # rst1: local coordinates of the vertices of f1, with respect to the frame of f0
#     # p1:   2D polygon of f1 in local coordinates

#     for k in assembly.vertices():

#         i = key_index[k]

#         block = assembly.blocks[k]
#         nbrs = block_nnbrs[i][1]

#         frames = block.frames()

#         if face_face:

#             # parallelise?
#             # exclude faces with parallel normals
#             # e.g. exclude overlapping top faces of two neighbouring blocks in same row

#             for f0, (origin, uvw) in frames.items():

#                 A = array(uvw)
#                 o = array(origin).reshape((-1, 1))
#                 xyz0 = array(block.face_coordinates(f0)).reshape((-1, 3)).T
#                 rst0 = solve(A.T, xyz0 - o).T.tolist()
#                 p0 = Polygon(rst0)

#                 for j in nbrs:
#                     n = index_key[j]

#                     if n == k:
#                         continue

#                     if k in assembly.edge and n in assembly.edge[k]:
#                         continue

#                     if n in assembly.edge and k in assembly.edge[n]:
#                         continue

#                     nbr = assembly.blocks[n]
#                     k_i = {
#                         key: index
#                         for index, key in enumerate(nbr.vertices())
#                     }
#                     xyz = array([
#                         nbr.vertex_coordinates(key) for key in nbr.vertices()
#                     ]).reshape((-1, 3)).T
#                     rst = solve(A.T, xyz - o).T.tolist()
#                     rst = {key: rst[k_i[key]] for key in nbr.vertices()}

#                     for f1 in nbr.faces():

#                         rst1 = [rst[key] for key in nbr.face_vertices(f1)]

#                         if any(fabs(t) > tmax for r, s, t in rst1):
#                             continue

#                         p1 = Polygon(rst1)

#                         if p1.area == 0.0:
#                             continue

#                         if p0.intersects(p1):

#                             # recalculate the planar frames.
#                             p_origin, p_uvw, p_xyz, p = block.frame_planar(f0)

#                             intersection = p0.intersection(p1)

#                             # try:
#                             #     intersection = p0.intersection(p1)
#                             # except Exception:
#                             #     print(p0, p1)
#                             #     continue
#                             # else:
#                             area = intersection.area

#                             if area >= amin:

#                                 coords = [[
#                                     x, y, 0.0
#                                 ] for x, y, z in intersection.exterior.coords]

#                                 coords = global_coords_numpy(o, A, coords)
#                                 coords = coords.tolist()[:-1]

#                                 coords = project_points_plane(coords, p)

#                                 attr = {
#                                     'interface_type': 'face_face',
#                                     'interface_size': area,
#                                     'interface_points': coords,
#                                     'interface_origin': p_origin,
#                                     'interface_uvw': p_uvw,
#                                 }

#                                 assembly.add_edge(k, n, attr_dict=attr)


# def assembly_interfaces_offset(assembly,
#                                nmax=10,
#                                tmax=1e-6,
#                                amin=1e-1,
#                                lmin=1e-3,
#                                face_face=True,
#                                face_edge=False,
#                                face_vertex=False):
#     """Identify the offset interfaces between the blocks of an assembly.

#     Parameters
#     ----------
#     assembly : compas_assembly.datastructures.Assembly
#         An assembly of discrete blocks.
#     nmax : int, optional
#         Maximum number of neighbours per block.
#         Default is ``10``.
#     tmax : float, optional
#         Maximum deviation from the perfectly flat interface plane.
#         Default is ``1e-6``.
#     amin : float, optional
#         Minimum area of a "face-face" interface.
#         Default is ``1e-1``.
#     lmin : float, optional
#         Minimum length of a "face-edge" interface.
#         Default is ``1e-3``.
#     face_face : bool, optional
#         Test for "face-face" interfaces.
#         Default is ``True``.
#     face_edge : bool, optional
#         Test for "face-edge" interfaces.
#         Default is ``False``.
#     face_vertex : bool, optional
#         Test for "face-vertex" interfaces.
#         Default is ``False``.

#     References
#     ----------
#     The identification of interfaces is discussed in detail here [Frick2016]_.

#     Examples
#     --------
#     .. code-block:: python

#         pass

#     """

#     # TODO this function need to be properly re-write this is just a quick hack

#     # replace by something proper
#     assembly.edge = {}
#     assembly.halfedge = {}
#     for key in assembly.vertices():
#         assembly.edge[key] = {}
#         assembly.halfedge[key] = {}
#     # replace

#     key_index = {key: index for index, key in enumerate(assembly.vertices())}
#     index_key = {index: key for index, key in enumerate(assembly.vertices())}

#     blocks = [assembly.blocks[key] for key in assembly.vertices()]
#     nmax = min(nmax, len(blocks))
#     block_cloud = [
#         assembly.vertex_coordinates(key) for key in assembly.vertices()
#     ]
#     block_nnbrs = _find_nearest_neighbours(block_cloud, nmax)

#     # k:      key of the base block
#     # i:      index of the base block
#     # block:  base block
#     # nbrs:   list of indices of the neighbouring blocks
#     # frames: list of frames for each of the faces of the base block

#     # f0:   key of the current base face
#     # A:    uvw base frame of f0
#     # o:    origin of the base frame of f0
#     # xyz0: xyz coordinates of the vertices of f0
#     # rst0: local coordinates of the vertices of f0, with respect to the frame of f0
#     # p0:   2D polygon of f0 in local coordinates

#     # j:   index of the current neighbour
#     # n:   key of the current neighbour
#     # nbr: neighbour block
#     # k_i: key index map for the vertices of the nbr block
#     # xyz: xyz coorindates of all vertices of nbr
#     # rst: local coordinates of all vertices of nbr, with respect to the frame of f0

#     # f1:   key of the current neighbour face
#     # rst1: local coordinates of the vertices of f1, with respect to the frame of f0
#     # p1:   2D polygon of f1 in local coordinates

#     for k in assembly.vertices():

#         i = key_index[k]

#         block = assembly.blocks[k]
#         nbrs = block_nnbrs[i][1]

#         frames = block.frames_offset()
#         print('hello--------- right function')

#         if face_face:

#             # parallelise?
#             # exclude faces with parallel normals
#             # e.g. exclude overlapping top faces of two neighbouring blocks in same row

#             for f0, (origin, uvw) in frames.items():
#                 A = array(uvw)
#                 o = array(origin).reshape((-1, 1))
#                 xyz0 = array(block.face_coordinates(f0)).reshape((-1, 3)).T
#                 rst0 = solve(A.T, xyz0 - o).T.tolist()
#                 p0 = Polygon(rst0)

#                 for j in nbrs:
#                     n = index_key[j]

#                     if n == k:
#                         continue

#                     if k in assembly.edge and n in assembly.edge[k]:
#                         continue

#                     if n in assembly.edge and k in assembly.edge[n]:
#                         continue

#                     nbr = assembly.blocks[n]
#                     k_i = {
#                         key: index
#                         for index, key in enumerate(nbr.vertices())
#                     }
#                     xyz = array([
#                         nbr.vertex_coordinates(key) for key in nbr.vertices()
#                     ]).reshape((-1, 3)).T
#                     rst = solve(A.T, xyz - o).T.tolist()
#                     rst = {key: rst[k_i[key]] for key in nbr.vertices()}

#                     for f1 in nbr.faces():

#                         rst1 = [rst[key] for key in nbr.face_vertices(f1)]

#                         if any(fabs(t) > tmax for r, s, t in rst1):
#                             continue

#                         p1 = Polygon(rst1)

#                         if p1.area == 0.0:
#                             continue

#                         if p0.intersects(p1):
#                             intersection = p0.intersection(p1)

#                             area = intersection.area

#                             if area >= amin:

#                                 coords = [[
#                                     x, y, 0.0
#                                 ] for x, y, z in intersection.exterior.coords]
#                                 coords = global_coords_numpy(o, A, coords)

#                                 coords = coords.tolist()[:-1]
#                                 centroid = centroid_points(coords)

#                                 new_coords = []

#                                 for c in coords:
#                                     new_coords.append([
#                                         c[i] * 0.9 + centroid[i] * 0.1
#                                         for i in range(3)
#                                     ])

#                                 attr = {
#                                     'interface_type': 'face_face',
#                                     'interface_size': area,
#                                     'interface_points': new_coords,
#                                     'interface_origin': origin,
#                                     'interface_uvw': uvw,
#                                 }

#                                 assembly.add_edge(k, n, attr_dict=attr)


# ==============================================================================
# Debugging
# ==============================================================================

if __name__ == "__main__":
    pass
