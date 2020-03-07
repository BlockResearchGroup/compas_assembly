from __future__ import print_function
from __future__ import absolute_import
from __future__ import division

from compas.utilities import color_to_colordict
from compas.utilities import i_to_blue
from compas.utilities import i_to_red
from compas.geometry import add_vectors
from compas.geometry import scale_vector
from compas.geometry import length_vector
from compas.geometry import sum_vectors

import compas_rhino
from compas_rhino.artists import NetworkArtist
from compas_assembly.rhino.blockartist import BlockArtist


__all__ = ['AssemblyArtist']


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
        self.settings.update({
            'color.vertex'            : (0, 0, 0),
            'color.vertex:is_support' : (0, 0, 0),
            'color.edge'              : (0, 0, 0),
            'color.interface'         : (255, 255, 255),
            'color.force:compression' : (0, 0, 255),
            'color.force:tension'     : (255, 0, 0),
            'color.selfweight'        : (0, 255, 0),
            'scale.force'             : 0.1,
            'scale.selfweight'        : 0.1,
            'eps.selfweight'          : 1e-3,
            'eps.force'               : 1e-3,
        })

    @property
    def assembly(self):
        """Assembly : the assembly data structure."""
        return self.network

    @assembly.setter
    def assembly(self, assembly):
        self.network = assembly

    # def _clear(self, name):
    #     name = "{}.{}.*".format(self.assembly.name, name)
    #     guids = compas_rhino.get_objects(name=name)
    #     compas_rhino.delete_objects(guids)

    # def clear_blocks(self):
    #     """Delete all previously drawn blocks."""
    #     self._clear('block')

    # def clear_interfaces(self):
    #     """Delete all previously drawn interfaces."""
    #     self._clear('interface')

    # def clear_selfweight(self):
    #     """Delete all previously drawn self-weight vectors."""
    #     self._clear('selfweight')

    # def clear_forces(self):
    #     """Delete all previously drawn force vectors."""
    #     self._clear('force')

    # def clear_resultants(self):
    #     """Delete all previously drawn resultant vectors."""
    #     self._clear('resultant')

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
        keys = keys or list(self.assembly.nodes())
        layer = "{}::Blocks".format(self.layer) if self.layer else None
        artist = BlockArtist(None, layer=layer)
        for key in keys:
            block = self.assembly.blocks[key]
            block.name = "{}.block.{}".format(self.assembly.name, key)
            artist.block = block
            if show_edges:
                artist.draw_edges()
            if show_faces:
                artist.draw_faces()
            if show_vertices:
                artist.draw_vertices()
        artist.redraw()

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
        layer = "{}::Interfaces".format(self.layer) if self.layer else None
        faces = []
        keys = keys or list(self.assembly.edges())
        colordict = color_to_colordict(
            color,
            keys,
            default=self.settings.get('color.interface'),
            colorformat='rgb',
            normalize=False
        )
        for (u, v), attr in self.assembly.edges(True):
            faces.append({
                'points' : attr['interface_points'],
                'name'   : "{}.interface.{}-{}".format(self.assembly.name, u, v),
                'color'  : colordict[(u, v)]
            })
        compas_rhino.draw_faces(faces, layer=layer, clear=False, redraw=False)

    def draw_interface_frames(self):
        """Draw the frames of the interfaces.
        """
        layer = "{}::Interfaces::Frames".format(self.layer) if self.layer else None
        lines = []
        for (a, b), attr in self.assembly.edges(True):
            o = attr['interface_origin']
            u, v, w = attr['interface_uvw']
            lines.append({
                'start' : o,
                'end'   : add_vectors(o, u),
                'name'  : "{}.iframe.{}-{}.u".format(self.assembly.name, a, b),
                'color' : (255, 0, 0),
                'arrow' : 'end'
            })
            lines.append({
                'start' : o,
                'end'   : add_vectors(o, v),
                'name'  : "{}.iframe.{}-{}.v".format(self.assembly.name, a, b),
                'color' : (0, 255, 0),
                'arrow' : 'end'
            })
            lines.append({
                'start' : o,
                'end'   : add_vectors(o, w),
                'name'  : "{}.iframe.{}-{}.w".format(self.assembly.name, a, b),
                'color' : (0, 0, 255),
                'arrow' : 'end'
            })
        self.draw_lines(lines, layer=layer, clear=True, redraw=True)

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
        for key, attr in self.assembly.vertices(True):
            block = self.assembly.blocks[key]
            volume = block.volume()
            if volume * scale < eps:
                continue
            vector = [0.0, 0.0, -1.0 * volume * scale]
            sp = block.centroid()
            ep = sp[:]
            ep[2] += vector[2]
            lines.append({
                'start' : sp,
                'end'   : ep,
                'name'  : "{}.selfweight.{}".format(self.assembly.name, key),
                'color' : color,
                'arrow' : 'end'
            })
        compas_rhino.draw_lines(lines, layer=layer, clear=False, redraw=False)

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
        for (a, b), attr in self.assembly.edges(True):
            if attr['interface_forces'] is None:
                continue
            w = attr['interface_uvw'][2]
            for i in range(len(attr['interface_points'])):
                sp = attr['interface_points'][i]
                c = attr['interface_forces'][i]['c_np']
                t = attr['interface_forces'][i]['c_nn']
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
                    'start' : sp,
                    'end'   : [sp[axis] + scale * f * w[axis] for axis in range(3)],
                    'color' : color,
                    'name'  : "{0}.force.{1}-{2}.{3}".format(self.assembly.name, a, b, i),
                    'arrow' : 'end'
                })
        compas_rhino.draw_lines(lines, layer=layer, clear=False, redraw=False)

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
        for key in self.assembly.edges():
            u, v = key
            corners = self.assembly.edge_attribute(key, 'interface_points')
            forces = self.assembly.edge_attribute(key, 'interface_forces')
            if not forces:
                continue
            n = self.assembly.edge_attribute(key, 'interface_uvw')[2]
            cx, cy, cz = 0, 0, 0
            p = len(corners)
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
        compas_rhino.draw_lines(lines, layer=layer, clear=False, redraw=False)
        compas_rhino.draw_points(points, layer=layer, clear=False, redraw=False)

    def color_interfaces(self, mode=0):
        """"""
        if mode == 0:
            return
        if mode == 1:
            color_compression = self.settings['color.force:compression']
            color_tension = self.settings['color.force:tension']
            resultants = []
            for key in self.assembly.edges():
                forces = self.assembly.edge_attribute(key, 'interface_forces')
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
            for index, key in enumerate(self.assembly.edges()):
                u, v = key
                name = "{}.interface.{}-{}".format(self.assembly.name, u, v)
                guids = compas_rhino.get_objects(name=name)
                if not guids:
                    continue
                guid = guids[0]
                R = resultants[index]
                color = i_to_blue((R - Rmin) / (Rmax - Rmin))
                compas_rhino.rs.ObjectColor(guid, color)


# ==============================================================================
# Debugging
# ==============================================================================

if __name__ == "__main__":
    pass
