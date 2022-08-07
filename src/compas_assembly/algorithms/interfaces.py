from typing import List

from math import fabs

from shapely.geometry import Polygon as ShapelyPolygon

from compas.geometry import Frame, Transformation
from compas.geometry import centroid_polygon
from compas.geometry import bestfit_frame_numpy, transform_points
from compas.datastructures import Mesh

from compas_assembly.datastructures import Assembly
from compas_assembly.datastructures import Block
from compas_assembly.datastructures import Interface
from compas_assembly.algorithms.nnbrs import find_nearest_neighbours


def assembly_interfaces(
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

    """
    node_index = {node: index for index, node in enumerate(assembly.nodes())}
    index_node = {index: node for index, node in enumerate(assembly.nodes())}

    blocks: List[Block] = list(assembly.blocks())

    nmax = min(nmax, len(blocks))

    block_cloud = [block.centroid() for block in blocks]
    block_nnbrs = find_nearest_neighbours(block_cloud, nmax)

    for node in assembly.nodes():
        i = node_index[node]

        block = blocks[i]
        nbrs = block_nnbrs[i][1]

        for j in nbrs:
            n = index_node[j]

            if n == node:
                # a block has no interfaces with itself
                continue

            if assembly.graph.has_edge(n, node, directed=False):
                # the interfaces between these two blocks have already been identified
                continue

            nbr = blocks[j]

            interfaces = mesh_mesh_interfaces(block, nbr, tmax, amin)

            if interfaces:
                assembly.add_block_block_interfaces(block, nbr, interfaces)


def mesh_mesh_interfaces(
    a: Mesh,
    b: Mesh,
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
    world = Frame.worldXY()
    interfaces = []

    for face in a.faces():
        points = a.face_coordinates(face)
        result = bestfit_frame_numpy(points)
        frame = Frame(*result)
        matrix = Transformation.from_change_of_basis(world, frame)
        projected = transform_points(points, matrix)
        p0 = ShapelyPolygon(projected)

        for test in b.faces():
            points = b.face_coordinates(test)
            projected = transform_points(points, matrix)
            p1 = ShapelyPolygon(projected)

            if not all(fabs(point[2]) < tmax for point in projected):
                continue

            if p1.area < amin:
                continue

            if not p0.intersects(p1):
                continue

            intersection = p0.intersection(p1)
            area = intersection.area

            if area < amin:
                continue

            coords = [[x, y, 0.0] for x, y, _ in intersection.exterior.coords]
            coords = transform_points(coords, matrix.inverted())

            interface = Interface(
                type="face_face",
                size=area,
                points=coords,
                frame=Frame(
                    centroid_polygon(coords[:-1]),
                    frame.xaxis,
                    frame.yaxis,
                ),
            )

            interfaces.append(interface)

    return interfaces
