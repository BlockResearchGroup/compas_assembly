from __future__ import print_function
from __future__ import absolute_import
from __future__ import division

from functools import partial

from compas.utilities import color_to_colordict
# from compas.utilities import i_to_blue
# from compas.utilities import i_to_red
# from compas.utilities import pairwise

# from compas.geometry import Box
# from compas.geometry import Translation
# from compas.geometry import Rotation
# from compas.geometry import subtract_vectors
# from compas.geometry import midpoint_point_point
# from compas.geometry import transform_points
# from compas.geometry import add_vectors
# from compas.geometry import scale_vector
# from compas.geometry import length_vector
# from compas.geometry import sum_vectors

import compas_blender
# from compas_blender.artists import BaseArtist
# from compas_blender.artists import MeshArtist
from compas_blender.artists import NetworkArtist

# from .blockartist import BlockArtist

colordict = partial(color_to_colordict, colorformat='rgb', normalize=True)


__all__ = ['AssemblyArtist']


class AssemblyArtist(NetworkArtist):
    """An artist for visualisation of assemblies in compas_blender.

    Parameters
    ----------
    assembly : compas_assembly.datastructures.Assembly
        The assembly data structure.
    layer : str, optional
        The base layer for drawing.
        Default is ``None``, which means drawing in the current layer.

    Examples
    --------
    >>>
    """

    def __init__(self, assembly):
        super().__init__(assembly)
        self._blockcollection = None
        self._interfacecollection = None
        self._resultantcollection = None
        self._object_block = {}
        self._object_interface = {}
        self._object_resultant = {}
        self.color_blocks = (1.0, 1.0, 1.0)
        self.color_interfaces = (1.0, 1.0, 1.0)
        self.color_compression = (0.0, 0.0, 1.0)
        self.color_tension = (1.0, 0.0, 0.0)
        self.color_selfweight = (0.0, 1.0, 0.0)
        self.scale_forces = 0.1
        self.scale_selfweight = 0.1
        self.eps_selfweight = 1e-3
        self.eps_forces = 1e-3

    @property
    def assembly(self):
        """Assembly : the assembly data structure."""
        return self.network

    @assembly.setter
    def assembly(self, assembly):
        self.network = assembly

    @property
    def blockcollection(self):
        path = f"{self.assembly.name}::Blocks"
        if not self._blockcollection:
            self._blockcollection = compas_blender.create_collections_from_path(path)[1]
        return self._blockcollection

    @property
    def interfacecollection(self):
        path = f"{self.assembly.name}::Interfaces"
        if not self._interfacecollection:
            self._interfacecollection = compas_blender.create_collections_from_path(path)[1]
        return self._interfacecollection

    @property
    def resultantcollection(self):
        path = f"{self.assembly.name}::Resultants"
        if not self._resultantcollection:
            self._resultantcollection = compas_blender.create_collections_from_path(path)[1]
        return self._resultantcollection

    @property
    def object_block(self):
        if not self._object_block:
            self._object_block = {}
        return self._object_block

    @object_block.setter
    def object_block(self, values):
        self._object_block = dict(values)

    @property
    def object_interface(self):
        if not self._object_interface:
            self._object_interface = {}
        return self._object_interface

    @object_interface.setter
    def object_interface(self, values):
        self._object_interface = dict(values)

    @property
    def object_resultant(self):
        if not self._object_resultant:
            self._object_resultant = {}
        return self._object_resultant

    @object_resultant.setter
    def object_resultant(self, values):
        self._object_resultant = dict(values)

    def clear(self):
        super().clear()
        objects = list(self.object_block)
        compas_blender.delete_objects(objects, purge_data=True)
        self._object_block = {}

    def draw(self):
        self.draw_nodes()
        self.draw_edges()
        self.draw_blocks()

    def draw_nodes(self, nodes=None, color=None):
        """Draw the blocks of the assembly.
        """
        nodes = nodes or list(self.assembly.nodes())
        node_color = colordict(color, nodes, default=self.color_nodes)
        points = []
        for node in nodes:
            block = self.assembly.node_attribute(node, 'block')
            points.append({
                'pos': block.centroid(),
                'name': f"{self.assembly.name}.node.{node}",
                'color': node_color[node],
                'radius': 0.05})
        objects = compas_blender.draw_points(points, self.nodecollection)
        self.object_node = zip(objects, nodes)
        return objects

    def draw_blocks(self, nodes=None):
        """Draw the blocks of the assembly.
        """
        nodes = nodes or list(self.assembly.nodes())
        objects = []
        for node in nodes:
            # block = self.assembly.blocks[node]
            block = self.assembly.node_attribute(node, 'block')
            vertices, faces = block.to_vertices_and_faces()
            obj = compas_blender.draw_mesh(vertices, faces, name=block.name, collection=self.blockcollection)
            objects.append(obj)
        self.object_block = zip(objects, nodes)
        return objects

    def draw_interfaces(self, edges=None):
        """Draw the interfaces between the blocks.
        """
        edges = edges or list(self.assembly.edges())
        objects = []
        for edge in edges:
            name = f"Interface.{edge[0]}-{edge[1]}"
            vertices = self.assembly.edge_attribute(edge, 'interface_points')
            faces = [list(range(len(vertices)))]
            obj = compas_blender.draw_mesh(vertices, faces, name=name, collection=self.interfacecollection)
            objects.append(obj)
        self.object_interface = zip(objects, edges)
        return objects

    def draw_resultants(self, scale=1.0, eps=1e-3):
        """
        """
        edges = list(self.assembly.edges())
        scale = scale or self.scale_forces
        eps = eps or self.eps_forces
        eps2 = eps**2
        points = []
        # lines = []
        for edge in edges:
            u, v = edge
            corners = self.assembly.edge_attribute(edge, 'interface_points')
            forces = self.assembly.edge_attribute(edge, 'interface_forces')
            if not forces:
                continue
            # n = self.assembly.edge_attribute(edge, 'interface_uvw')[2]
            cx, cy, cz = 0, 0, 0
            # p = len(corners)
            R = 0
            for point, force in zip(corners, forces):
                c = force['c_np']
                t = force['c_nn']
                f = c - t
                cx += point[0] * f
                cy += point[1] * f
                cz += point[2] * f
                R += f
            if R**2 < eps2:
                continue
            cx = cx / R
            cy = cy / R
            cz = cz / R
            c = [cx, cy, cz]
            # sp = add_vectors(c, scale_vector(n, R * scale))
            # ep = add_vectors(c, scale_vector(n, -R * scale))
            if R < 0:
                color = self.color_tension
                radius = -R * scale
            else:
                color = self.color_compression
                radius = +R * scale
            points.append({'pos': c, 'radius': radius, 'color': color, 'name': f"POA.{u}-{v}"})
            # lines.append({'start': sp, 'end': ep, 'color': color, 'name': f"Force.{u}-{v}"})
        objects = compas_blender.draw_points(points, self.resultantcollection)
        # objects = compas_blender.draw_lines(lines, self.resultantcollection)
        self.object_resultant = zip(objects, edges)

    # def draw_selfweight(self, scale=None, eps=None):
    #     """Draw vectors indicating the magnitude of the selfweight of the blocks.

    #     Parameters
    #     ----------
    #     scale : float, optional
    #         The scale at which the selfweight vectors should be drawn.
    #         Default is `0.1`.
    #     eps : float, optional
    #         A tolerance for drawing small vectors.
    #         Selfweight vectors with a scaled length smaller than this tolerance are not drawn.
    #         Default is `1e-3`.

    #     Notes
    #     -----
    #     * Selfweight vectors are drawn as Blender lines with arrow heads.
    #     * The default color is *green*: `'#00ff00'` or `(0, 255, 0)`.
    #     * Selfweight vectors are drawn in a sub-layer *Selfweight* of the base layer, if a base layer was specified.
    #     * Selfweight vectors are named according to the following pattern: `"{assembly name}.selfweight.{block id}"`.

    #     """
    #     layer = "{}::Selfweight".format(self.layer) if self.layer else None
    #     scale = scale or self.settings['scale.selfweight']
    #     eps = eps or self.settings['eps.selfweight']
    #     color = self.settings['color.selfweight']
    #     lines = []
    #     for key, attr in self.assembly.vertices(True):
    #         block = self.assembly.blocks[key]
    #         volume = block.volume()
    #         if volume * scale < eps:
    #             continue
    #         vector = [0.0, 0.0, -1.0 * volume * scale]
    #         sp = block.centroid()
    #         ep = sp[:]
    #         ep[2] += vector[2]
    #         lines.append({
    #             'start' : sp,
    #             'end'   : ep,
    #             'name'  : "{}.selfweight.{}".format(self.assembly.name, key),
    #             'color' : color,
    #             'arrow' : 'end'
    #         })
    #     compas_blender.draw_lines(lines, layer=layer, clear=False, redraw=False)

    # def draw_forces(self, scale=None, eps=None, mode=0):
    #     """Draw the contact forces at the interfaces.

    #     Parameters
    #     ----------
    #     scale : float, optional
    #         The scale at which the forces should be drawn.
    #         Default is `0.1`.
    #     eps : float, optional
    #         A tolerance for drawing small force vectors.
    #         Force vectors with a scaled length smaller than this tolerance are not drawn.
    #         Default is `1e-3`.
    #     mode : int, optional
    #         Display mode: 0 normal, 1 resultant forces
    #         Default is 0

    #     Notes
    #     -----
    #     * Forces are drawn as lines with arrow heads.
    #     * Forces are drawn on a sub-layer *Forces* of the base layer, if a base layer was specified.
    #     * At every interface point there can be a *compression* force (blue) and a *tension* force (red).
    #     * Forces are named according to the following pattern:
    #       ``"{assembly_name}.force.{from block}-{to block}.{interface point}"``

    #     """
    #     layer = "{}::Forces".format(self.layer) if self.layer else None
    #     scale = scale or self.settings['scale.force']
    #     eps = eps or self.settings['eps.force']
    #     color_compression = self.settings['color.force:compression']
    #     color_tension = self.settings['color.force:tension']
    #     lines = []
    #     for (a, b), attr in self.assembly.edges(True):
    #         if attr['interface_forces'] is None:
    #             continue
    #         w = attr['interface_uvw'][2]
    #         for i in range(len(attr['interface_points'])):
    #             sp = attr['interface_points'][i]
    #             c = attr['interface_forces'][i]['c_np']
    #             t = attr['interface_forces'][i]['c_nn']
    #             f = c - t
    #             if f > 0.0:
    #                 if scale * f < eps:
    #                     continue
    #                 color = color_compression
    #             elif f < 0.0:
    #                 if -scale * f < eps:
    #                     continue
    #                 color = color_tension
    #             else:
    #                 continue
    #             lines.append({
    #                 'start' : sp,
    #                 'end'   : [sp[axis] + scale * f * w[axis] for axis in range(3)],
    #                 'color' : color,
    #                 'name'  : "{0}.force.{1}-{2}.{3}".format(self.assembly.name, a, b, i),
    #                 'arrow' : 'end'
    #             })
    #     compas_blender.draw_lines(lines, layer=layer, clear=False, redraw=False)

    # def color_interfaces(self, mode=0):
    #     """"""
    #     if mode == 0:
    #         return
    #     if mode == 1:
    #         color_compression = self.settings['color.force:compression']
    #         color_tension = self.settings['color.force:tension']
    #         resultants = []
    #         for key in self.assembly.edges():
    #             forces = self.assembly.edge_attribute(key, 'interface_forces')
    #             if not forces:
    #                 resultants.append(0)
    #                 continue
    #             R = 0
    #             for force in forces:
    #                 c = force['c_np']
    #                 t = force['c_nn']
    #                 f = c - t
    #                 R += f
    #             resultants.append(R)
    #         Rmax = max(resultants)
    #         Rmin = min(resultants)
    #         print(Rmax)
    #         print(Rmin)
    #         for index, key in enumerate(self.assembly.edges()):
    #             u, v = key
    #             name = "{}.interface.{}-{}".format(self.assembly.name, u, v)
    #             guids = compas_blender.get_objects(name=name)
    #             if not guids:
    #                 continue
    #             guid = guids[0]
    #             R = resultants[index]
    #             color = i_to_blue((R - Rmin) / (Rmax - Rmin))
    #             compas_blender.rs.ObjectColor(guid, color)


# ==============================================================================
# Debugging
# ==============================================================================

if __name__ == "__main__":
    pass
