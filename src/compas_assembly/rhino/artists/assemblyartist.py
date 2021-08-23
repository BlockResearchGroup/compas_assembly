from __future__ import print_function
from __future__ import absolute_import
from __future__ import division

from functools import partial

from compas.utilities import color_to_colordict
from compas.utilities import i_to_blue
from compas.geometry import add_vectors
from compas.geometry import scale_vector

import compas_rhino
from compas_rhino.artists import NetworkArtist
from compas_rhino.artists import FrameArtist

from .blockartist import BlockArtist


__all__ = ['AssemblyArtist']


colordict = partial(color_to_colordict, colorformat='rgb', normalize=False)


class AssemblyArtist(NetworkArtist):
    """An artist for visualisation of assemblies in Rhino.

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
        self.settings = {
            'color.vertex': (0, 0, 0),
            'color.vertex:is_support': (0, 0, 0),
            'color.edge': (0, 0, 0),
            'color.interface': (255, 255, 255),
            'color.force:compression': (0, 0, 255),
            'color.force:tension': (255, 0, 0),
            'color.selfweight': (0, 255, 0),
            'scale.force': 0.1,
            'scale.selfweight': 0.1,
            'eps.selfweight': 1e-3,
            'eps.force': 1e-3,
        }

    @property
    def assembly(self):
        """Assembly : the assembly data structure."""
        return self.network

    @assembly.setter
    def assembly(self, assembly):
        self.network = assembly

    def draw_blocks(self, nodes=None, show_faces=False, show_vertices=False, show_edges=True):
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
        nodes = nodes or list(self.assembly.nodes())
        layer = "{}::Blocks".format(self.layer) if self.layer else None
        guids = []
        for node in nodes:
            block = self.assembly.node_attribute(node, 'block')
            block.name = "{}.block.{}".format(self.assembly.name, node)
            artist = BlockArtist(block, layer=layer)
            if show_edges:
                guids += artist.draw_edges()
            if show_faces:
                guids += artist.draw_faces()
            if show_vertices:
                guids += artist.draw_vertices()
        return guids

    def draw_interfaces(self, edges=None, color=None):
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
        layer = "{}::Interfaces".format(self.layer) if self.layer else None
        faces = []
        edges = edges or list(self.assembly.edges())
        edge_color = colordict(color, edges, default=self.settings.get('color.interface'))
        for edge in self.assembly.edges():
            interface = self.assembly.edge_attribute(edge, 'interface')
            faces.append({
                'points': interface.points,
                'name': "{}.interface.{}-{}".format(self.assembly.name, *edge),
                'color': edge_color[edge]
            })
        return compas_rhino.draw_faces(faces, layer=layer, clear=False, redraw=False)

    def draw_interface_frames(self):
        """Draw the frames of the interfaces.
        """
        layer = "{}::Interfaces::Frames".format(self.layer) if self.layer else None
        compas_rhino.clear_layer(layer)
        guids = []
        for edge in self.assembly.edges():
            interface = self.assembly.edge_attribute(edge, 'interface')
            artist = FrameArtist(interface.frame, layer=layer)
            guids += artist.draw()
        return guids

    def draw_selfweight(self, scale=None, eps=None):
        """Draw vectors indicating the magnitude of the selfweight of the blocks.

        Parameters
        ----------
        scale : float, optional
            The scale at which the selfweight vectors should be drawn.
            Default is `0.1`.
        eps : float, optional
            A tolerance for drawing small vectors.
            Selfweight vectors with a scaled length smaller than this tolerance are not drawn.
            Default is `1e-3`.

        Notes
        -----
        * Selfweight vectors are drawn as Rhino lines with arrow heads.
        * The default color is *green*: `'#00ff00'` or `(0, 255, 0)`.
        * Selfweight vectors are drawn in a sub-layer *Selfweight* of the base layer, if a base layer was specified.
        * Selfweight vectors are named according to the following pattern: `"{assembly name}.selfweight.{block id}"`.

        """
        layer = "{}::Selfweight".format(self.layer) if self.layer else None
        scale = scale or self.settings['scale.selfweight']
        eps = eps or self.settings['eps.selfweight']
        color = self.settings['color.selfweight']
        lines = []
        for node in self.assembly.nodes():
            block = self.assembly.node_attribute(node, 'block')
            volume = block.volume()
            if volume * scale < eps:
                continue
            vector = [0.0, 0.0, -1.0 * volume * scale]
            sp = block.centroid()
            ep = sp[:]
            ep[2] += vector[2]
            lines.append({
                'start': sp,
                'end': ep,
                'name': "{}.selfweight.{}".format(self.assembly.name, node),
                'color': color,
                'arrow': 'end'
            })
        return compas_rhino.draw_lines(lines, layer=layer, clear=False, redraw=False)

    def draw_forces(self, scale=None, eps=None, mode=0):
        """Draw the contact forces at the interfaces.

        Parameters
        ----------
        scale : float, optional
            The scale at which the forces should be drawn.
            Default is `0.1`.
        eps : float, optional
            A tolerance for drawing small force vectors.
            Force vectors with a scaled length smaller than this tolerance are not drawn.
            Default is `1e-3`.
        mode : int, optional
            Display mode: 0 normal, 1 resultant forces
            Default is 0

        Notes
        -----
        * Forces are drawn as lines with arrow heads.
        * Forces are drawn on a sub-layer *Forces* of the base layer, if a base layer was specified.
        * At every interface point there can be a *compression* force (blue) and a *tension* force (red).
        * Forces are named according to the following pattern:
          ``"{assembly_name}.force.{from block}-{to block}.{interface point}"``

        """
        layer = "{}::Forces".format(self.layer) if self.layer else None
        scale = scale or self.settings['scale.force']
        eps = eps or self.settings['eps.force']
        color_compression = self.settings['color.force:compression']
        color_tension = self.settings['color.force:tension']
        lines = []
        for edge in self.assembly.edges():
            interface = self.assembly.edge_attribute(edge, 'interface')
            if not interface.forces:
                continue
            w = interface.frame.zaxis
            for i in range(len(interface.points)):
                sp = interface.points[i]
                c = interface.forces[i]['c_np']
                t = interface.forces[i]['c_nn']
                f = c - t
                if f > 0.0:
                    if scale * f < eps:
                        continue
                    color = color_compression
                elif f < 0.0:
                    if -scale * f < eps:
                        continue
                    color = color_tension
                else:
                    continue
                lines.append({
                    'start': sp,
                    'end': [sp[axis] + scale * f * w[axis] for axis in range(3)],
                    'color': color,
                    'name': "{0}.force.{1}-{2}.{3}".format(self.assembly.name, edge[0], edge[1], i),
                    'arrow': 'end'
                })
        return compas_rhino.draw_lines(lines, layer=layer, clear=False, redraw=False)

    def draw_resultants(self, scale=1.0, eps=1e-3):
        """
        """
        layer = "{}::Resultants".format(self.layer) if self.layer else None
        scale = scale or self.settings['scale.force']
        eps = eps or self.settings['eps.force']
        color_compression = self.settings['color.force:compression']
        color_tension = self.settings['color.force:tension']
        eps2 = eps**2
        lines = []
        points = []
        for edge in self.assembly.edges():
            u, v = edge
            interface = self.assembly.edge_attribute(edge, 'interface')
            corners = interface.points
            forces = interface.forces
            if not forces:
                continue
            n = interface.frame.zaxis
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
            sp = add_vectors(c, scale_vector(n, R * scale))
            ep = add_vectors(c, scale_vector(n, -R * scale))
            if R < 0:
                color = color_tension
            else:
                color = color_compression
            lines.append({'start': sp, 'end': ep, 'color': color, 'name': "{0}.resultant.{1}-{2}".format(self.assembly.name, u, v)})
            points.append({'pos': c, 'color': color, 'name': "{0}.resultant.{1}-{2}".format(self.assembly.name, u, v)})
        guids = compas_rhino.draw_lines(lines, layer=layer, clear=False, redraw=False)
        guids += compas_rhino.draw_points(points, layer=layer, clear=False, redraw=False)
        return guids

    def color_interfaces(self, mode=0):
        """"""
        if mode == 0:
            return
        if mode == 1:
            resultants = []
            for edge in self.assembly.edges():
                interface = self.assembly.edge_attribute(edge, 'interface')
                forces = interface.forces
                if not forces:
                    resultants.append(0)
                    continue
                R = 0
                for force in forces:
                    c = force['c_np']
                    t = force['c_nn']
                    f = c - t
                    R += f
                resultants.append(R)
            Rmax = max(resultants)
            Rmin = min(resultants)
            print(Rmax)
            print(Rmin)
            for index, edge in enumerate(self.assembly.edges()):
                u, v = edge
                name = "{}.interface.{}-{}".format(self.assembly.name, u, v)
                guids = compas_rhino.get_objects(name=name)
                if not guids:
                    continue
                guid = guids[0]
                R = resultants[index]
                color = i_to_blue((R - Rmin) / (Rmax - Rmin))
                compas_rhino.rs.ObjectColor(guid, color)
