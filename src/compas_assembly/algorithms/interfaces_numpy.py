from math import fabs

from numpy import array
from numpy import float64
from scipy.linalg import solve
from shapely.geometry import Polygon

from compas.geometry import Frame
from compas.geometry import local_to_world_coordinates_numpy
from compas.geometry import centroid_points

from compas_assembly.datastructures import Assembly
from compas_assembly.datastructures import Block
from compas_assembly.datastructures import Interface
from compas_assembly.algorithms.nnbrs import find_nearest_neighbours


def assembly_interfaces_numpy(
    assembly: Assembly,
    nmax: int = 10,
    tmax: float = 1e-6,
    amin: float = 1e-1,
):
    """Identify the interfaces between the blocks of an assembly.

    Parameters
    ----------
    assembly : compas_assembly.datastructures.Assembly
        An assembly of discrete blocks.
    nmax : int, optional
        Maximum number of neighbours per block.
    tmax : float, optional
        Maximum deviation from the perfectly flat interface plane.
    amin : float, optional
        Minimum area of a "face-face" interface.

    Returns
    -------
    :class:`Assembly`

    References
    ----------
    The identification of interfaces is discussed in detail here [Frick2016]_.

    """
    node_index = {node: index for index, node in enumerate(assembly.nodes())}
    index_node = {index: node for index, node in enumerate(assembly.nodes())}

    blocks = list(assembly.blocks())

    nmax = min(nmax, len(blocks))

    block_cloud = [block.centroid() for block in blocks]
    block_nnbrs = find_nearest_neighbours(block_cloud, nmax)

    assembly.graph.edge = {node: {} for node in assembly.graph.nodes()}

    for node in assembly.graph.nodes():
        i = node_index[node]

        block = blocks[i]
        nbrs = block_nnbrs[i][1]

        for j in nbrs:
            n = index_node[j]

            if n == node:
                # a block has no interfaces with itself
                continue

            if assembly.graph.has_edge(n, node):
                # the interfaces between these two blocks have already been identified
                continue

            nbr = blocks[j]

            interfaces = mesh_mesh_interfaces(block, nbr, tmax, amin)

            if interfaces:
                assembly.add_block_block_interfaces(block, nbr, interfaces)

    return assembly


def mesh_mesh_interfaces(
    a: Block,
    b: Block,
    tmax: float = 1e-6,
    amin: float = 1e-1,
):
    """Compute all face-face contact interfaces between two meshes.

    Parameters
    ----------
    a : :class:`compas.datastructures.Mesh`
    b : :class:`compas.datastructures.Mesh`
    tmax : float, optional
        Maximum deviation from the perfectly flat interface plane.
    amin : float, optional
        Minimum area of a "face-face" interface.

    Returns
    -------
    List[:class:`Interface`]

    """
    k_i = {key: index for index, key in enumerate(b.vertices())}
    frames: dict[int, Frame] = a.frames()

    interfaces = []

    for f0, frame in frames.items():
        origin = frame.point
        uvw = [frame.xaxis, frame.yaxis, frame.zaxis]

        A = array(uvw, dtype=float64)
        o = array(origin, dtype=float64).reshape((-1, 1))

        xyz0 = array(a.face_coordinates(f0), dtype=float64).reshape((-1, 3)).T
        rst0 = solve(A.T, xyz0 - o).T.tolist()
        p0 = Polygon(rst0)

        xyz = array(b.vertices_attributes("xyz"), dtype=float64).reshape((-1, 3)).T
        rst = solve(A.T, xyz - o).T.tolist()
        rst = {key: rst[k_i[key]] for key in b.vertices()}

        for f1 in b.faces():

            rst1 = [rst[key] for key in b.face_vertices(f1)]

            if any(fabs(t) > tmax for r, s, t in rst1):
                continue

            p1 = Polygon(rst1)

            if p1.area < amin:
                continue

            if not p0.intersects(p1):
                continue

            intersection = p0.intersection(p1)
            area = intersection.area

            if area < amin:
                continue

            coords = [[x, y, 0.0] for x, y, z in intersection.exterior.coords]
            coords = local_to_world_coordinates_numpy(
                Frame(o, A[0], A[1]), coords[:-1]
            ).tolist()
            interface = Interface(
                type="face_face",
                size=area,
                points=coords,
                frame=Frame(
                    centroid_points(coords),
                    frame.xaxis,
                    frame.yaxis,
                ),
            )

            interfaces.append(interface)

    return interfaces
