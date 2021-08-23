from functools import partial

from compas.utilities import color_to_colordict

import compas_blender
from compas_blender.artists import NetworkArtist

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
            interface = self.assembly.edge_attribute(edge, 'interface')
            vertices = interface.points
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
        for edge in edges:
            u, v = edge
            interface = self.assembly.edge_attribute(edge, 'interface')
            corners = interface.points
            forces = interface.forces
            if not forces:
                continue
            cx, cy, cz = 0, 0, 0
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
            if R < 0:
                color = self.color_tension
                radius = -R * scale
            else:
                color = self.color_compression
                radius = +R * scale
            points.append({'pos': c, 'radius': radius, 'color': color, 'name': f"POA.{u}-{v}"})
        objects = compas_blender.draw_points(points, self.resultantcollection)
        self.object_resultant = zip(objects, edges)
