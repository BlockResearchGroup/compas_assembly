from __future__ import print_function
from __future__ import absolute_import
from __future__ import division

from compas.utilities import color_to_colordict
from compas.utilities import i_to_blue
from compas.utilities import i_to_red
from compas.utilities import pairwise

from compas.geometry import Box
from compas.geometry import Translation
from compas.geometry import Rotation
from compas.geometry import subtract_vectors
from compas.geometry import midpoint_point_point
from compas.geometry import transform_points
from compas.geometry import add_vectors
from compas.geometry import scale_vector
from compas.geometry import length_vector
from compas.geometry import sum_vectors

import compas_blender

from compas_blender.artists import Artist
from compas_blender.artists import MeshArtist
from compas_blender.artists import NetworkArtist

from compas_assembly.blender.blockartist import BlockArtist


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

    def __init__(self, assembly, layer=None):
        super(AssemblyArtist, self).__init__(assembly, layer=layer)
        # self.settings.update({
        #     'color.vertex'            : (0, 0, 0),
        #     'color.vertex:is_support' : (0, 0, 0),
        #     'color.edge'              : (0, 0, 0),
        #     'color.interface'         : (255, 255, 255),
        #     'color.force:compression' : (0, 0, 255),
        #     'color.force:tension'     : (255, 0, 0),
        #     'color.selfweight'        : (0, 255, 0),
        #     'scale.force'             : 0.1,
        #     'scale.selfweight'        : 0.1,
        #     'eps.selfweight'          : 1e-3,
        #     'eps.force'               : 1e-3,
        # })
        layer = layer or "Assembly"
        self.assembly_collection = compas_blender.create_collection(layer)
        self.node_collection = compas_blender.create_collection("Nodes", parent=self.assembly_collection)
        self.link_collection = compas_blender.create_collection("Links", parent=self.assembly_collection)
        self.block_collection = compas_blender.create_collection("Blocks", parent=self.assembly_collection)
        self.interface_collection = compas_blender.create_collection("Interfaces", parent=self.assembly_collection)

    @property
    def assembly(self):
        """Assembly : the assembly data structure."""
        return self.network

    @assembly.setter
    def assembly(self, assembly):
        self.network = assembly

    def draw_nodes(self, keys=None):
        add_point = compas_blender.bpy.ops.surface.primitive_nurbs_surface_sphere_add
        points = []
        for key in self.assembly.nodes():
            xyz = self.assembly.node_attributes(key, 'xyz')
            add_point(radius=0.03, location=xyz)
            obj = compas_blender.bpy.context.active_object
            obj.name = "Assembly.node.{}".format(key)
            if self.assembly.node_attribute(key, 'is_support'):
                compas_blender.drawing.set_object_color(obj, [1.0, 0.0, 0.0])
            else:
                compas_blender.drawing.set_object_color(obj, [1.0, 1.0, 1.0])
            points.append(obj)
        for obj in points:
            for col in obj.users_collection:
                col.objects.unlink(obj)
            self.node_collection.objects.link(obj)

    def draw_blocks(self, keys=None, show_faces=False, show_vertices=False, show_edges=True):
        """Draw the blocks of the assembly.

        Parameters
        ----------
        show_faces : bool, optional
            Draw the faces of the blocks.
            Default is ``False``.
        show_vertices : bool, optional
            Draw the vertices of the blocks.
            Default is ``False``.
        show_edges : bool, optional
            Draw the edges of the blocks.
            Default is ``True``.

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
        blocks = []
        # compas_blender.clear_collection()
        for key in self.assembly.nodes():
            block = self.assembly.blocks[key]
            centroid = block.centroid()
            T = Translation(subtract_vectors([0, 0, 0], centroid))
            name = "Assembly.block.{}".format(key)
            vertices = transform_points(block.vertices_attributes('xyz'), T)
            edges = list(block.edges())
            faces = [block.face_vertices(fkey) for fkey in block.faces()]
            mesh = compas_blender.bpy.data.meshes.new(name)
            mesh.from_pydata(vertices, edges, faces)
            obj = compas_blender.bpy.data.objects.new(name, mesh)
            obj.show_wire = True
            obj.location = centroid
            if self.assembly.node_attribute(key, 'is_support'):
                compas_blender.drawing.set_object_color(obj, [1.0, 0.0, 0.0])
            else:
                compas_blender.drawing.set_object_color(obj, [1.0, 1.0, 1.0])
            blocks.append(obj)
        for obj in blocks:
            for col in obj.users_collection:
                col.objects.unlink(obj)
            self.block_collection.objects.link(obj)

    def draw_edges(self, keys=None):
        #lines = []
        #for key in assembly.edges():
        #    u, v = key
        #    name = "Assembly.edge.{}-{}".format(u, v)
        #    a = assembly.node_attributes(u, 'xyz')
        #    b = assembly.node_attributes(v, 'xyz')
        #    m = midpoint_point_point(a, b)
        #    mesh = bpy.data.meshes.new(name)
        #    mesh.from_pydata([subtract_vectors(a, m), subtract_vectors(b, m)], [[0, 1]], [])
        #    obj = bpy.data.objects.new(name, mesh)
        #    obj.show_wire = True
        #    obj.location = m
        #    set_object_color(obj, [0.0, 0.0, 0.0])
        #    lines.append(obj)
        lines = []
        for key in self.assembly.edges():
            u, v = key
            name = "Assembly.edge.{}-{}".format(u, v)
            a = self.assembly.node_attributes(u, 'xyz')
            b = self.assembly.node_attributes(v, 'xyz')
            m = midpoint_point_point(a, b)
            curve = compas_blender.bpy.data.curves.new(name, type='CURVE')
            curve.dimensions = '3D'
            curve.fill_mode = 'FULL'
            curve.bevel_depth = 0.01
            curve.bevel_resolution = 8
            curve.use_fill_caps = True
            spline = curve.splines.new('POLY')
            spline.points.add(2)
            spline.points[0].co = subtract_vectors(a, m) + [1.0]
            spline.points[1].co = subtract_vectors(b, m) + [1.0]
            spline.order_u = 2
            obj = compas_blender.bpy.data.objects.new(name, curve)
            obj.location = m
            compas_blender.drawing.set_object_color(obj, [0.0, 0.0, 0.0])
            lines.append(obj)
        for obj in lines:
            for col in obj.users_collection:
                col.objects.unlink(obj)
            self.link_collection.objects.link(obj)

    def draw_interfaces(self, keys=None, color=None):
        """Draw the interfaces between the blocks.

        Parameters
        ----------
        keys : list
            A list of interface identifiers (i.e. assembly edge (u, v) tuples).
            Default is ``None``, in which case all interfaces are drawn.
        color : str, tuple, dict
            The color specififcation for the interfaces.
            Colors should be specified in the form of a string (hex colors) or
            as a tuple of RGB components.
            To apply the same color to all interfaces, provide a single color
            specification. Individual colors can be assigned using a dictionary
            of key-color pairs. Missing keys will be assigned the default interface
            color (``self.settings['color.interface']``).
            The default is ``None``, in which case all interfaces are assigned the
            default interface color.

        Notes
        -----
        * Interfaces are drawn as mesh faces.
        * Interfaces are drawn on a sub-layer *Interfaces* of the base layer, if a base layer was provided.
        * Interface names have the following pattern: ``"{assembly_name}.interface.{from block_id}-{to block_id}"``
        * Interfaces have a direction, as suggested by the naming convention.
        """
        interfaces = []
        for key, attr in self.assembly.edges(True):
            u, v = key
            name = "Assembly.interface.{}-{}".format(u, v)
            points = attr['interface_points']
            base = attr['interface_origin']
            T = Translation(subtract_vectors([0, 0, 0], base))
            vertices = transform_points(points, T)
            faces = [list(range(len(vertices)))]
            edges = list(pairwise(faces[0] + [0]))
            mesh = compas_blender.bpy.data.meshes.new(name)
            mesh.from_pydata(vertices, edges, faces)
            obj = compas_blender.bpy.data.objects.new(name, mesh)
            obj.location = base
            compas_blender.drawing.set_object_color(obj, [0, 0, 1.0])
            interfaces.append(obj)
        for obj in interfaces:
            for col in obj.users_collection:
                col.objects.unlink(obj)
            self.interface_collection.objects.link(obj)

    # def draw_interface_frames(self):
    #     """Draw the frames of the interfaces.
    #     """
    #     layer = "{}::Interfaces::Frames".format(self.layer) if self.layer else None
    #     lines = []
    #     for (a, b), attr in self.assembly.edges(True):
    #         o = attr['interface_origin']
    #         u, v, w = attr['interface_uvw']
    #         lines.append({
    #             'start' : o,
    #             'end'   : add_vectors(o, u),
    #             'name'  : "{}.iframe.{}-{}.u".format(self.assembly.name, a, b),
    #             'color' : (255, 0, 0),
    #             'arrow' : 'end'
    #         })
    #         lines.append({
    #             'start' : o,
    #             'end'   : add_vectors(o, v),
    #             'name'  : "{}.iframe.{}-{}.v".format(self.assembly.name, a, b),
    #             'color' : (0, 255, 0),
    #             'arrow' : 'end'
    #         })
    #         lines.append({
    #             'start' : o,
    #             'end'   : add_vectors(o, w),
    #             'name'  : "{}.iframe.{}-{}.w".format(self.assembly.name, a, b),
    #             'color' : (0, 0, 255),
    #             'arrow' : 'end'
    #         })
    #     self.draw_lines(lines, layer=layer, clear=True, redraw=True)

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

    # def draw_resultants(self, scale=1.0, eps=1e-3):
    #     """
    #     """
    #     layer = "{}::Resultants".format(self.layer) if self.layer else None
    #     scale = scale or self.settings['scale.force']
    #     eps = eps or self.settings['eps.force']
    #     color_compression = self.settings['color.force:compression']
    #     color_tension = self.settings['color.force:tension']
    #     eps2 = eps**2
    #     lines = []
    #     points = []
    #     for key in self.assembly.edges():
    #         u, v = key
    #         corners = self.assembly.edge_attribute(key, 'interface_points')
    #         forces = self.assembly.edge_attribute(key, 'interface_forces')
    #         if not forces:
    #             continue
    #         n = self.assembly.edge_attribute(key, 'interface_uvw')[2]
    #         cx, cy, cz = 0, 0, 0
    #         p = len(corners)
    #         R = 0
    #         for point, force in zip(corners, forces):
    #             c = force['c_np']
    #             t = force['c_nn']
    #             f = c - t
    #             cx += point[0] * f
    #             cy += point[1] * f
    #             cz += point[2] * f
    #             R += f
    #         if R**2 < eps2:
    #             continue
    #         cx = cx / R
    #         cy = cy / R
    #         cz = cz / R
    #         c = [cx, cy, cz]
    #         sp = add_vectors(c, scale_vector(n, R * scale))
    #         ep = add_vectors(c, scale_vector(n, -R * scale))
    #         if R < 0:
    #             color = color_tension
    #         else:
    #             color = color_compression
    #         lines.append({'start': sp, 'end': ep, 'color': color, 'name': "{0}.resultant.{1}-{2}".format(self.assembly.name, u, v)})
    #         points.append({'pos': c, 'color': color, 'name': "{0}.resultant.{1}-{2}".format(self.assembly.name, u, v)})
    #     compas_blender.draw_lines(lines, layer=layer, clear=False, redraw=False)
    #     compas_blender.draw_points(points, layer=layer, clear=False, redraw=False)

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
