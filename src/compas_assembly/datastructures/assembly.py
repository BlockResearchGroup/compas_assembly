from __future__ import print_function
from __future__ import absolute_import
from __future__ import division

import ast
import json

import compas_rhino
from compas.datastructures import Network


__all__ = ['Assembly']


# should an assembly be composed of a network attribute
# and a block collection
# rather than inherit from network
# and add inconsistent stuff to that interface?


class Assembly(Network):
    """A data structure for discrete element assemblies.

    An assembly is essentially a network of assembly elements.
    Each vertex of the network represents an element of the assembly.
    Each edge of the network represents an interface between two assembly elements.

    Parameters
    ----------
    blocks : list of :class:`compas_assembly.datastructures.Block`, optional
        A list of assembly blocks.
    attributes : dict, optional
        User-defined attributes of the assembly.
        Built-in attributes are:

        * name (str) : 'Assembly'

    default_vertex_attributes : dict, optional
        User-defined default attributes of the vertices of the network.
        Since the vertices of the assembly network represent the individual
        elements, the built-in attributes are:

        * is_support (bool) : False

    default_edge_attributes : dict, optional
        User-defined default attributes of the edges of the network.
        Since the edges of the assembly network represent the interfaces between
        the individual elements, the built-in attributes are:

        * interface_points (list) : None
        * interface_type ({'face_face', 'face_edge', 'face_vertex'}) : None
        * interface_size (float) : None
        * interface_uvw (list) : None
        * interface_origin (list) : None
        * interface_forces (list) : None

    Examples
    --------
    .. code-block:: python

        from compas_assembly.datastructures import Assembly
        from compas_assembly.datastructures import Block

        assembly = Assembly()

        for i in range(2):
            block = Block.from_polyhedron(6)
            assembly.add_block(block)

        print(assembly.summary())

    """

    __module__ = 'compas_assembly.datastructures'

    def __init__(self,
                 blocks=None,
                 attributes=None,
                 default_vertex_attributes=None,
                 default_edge_attributes=None):

        super(Assembly, self).__init__()

        self.blocks = {}
        self.attributes.update({'name': 'Assembly'})
        if attributes is not None:
            self.attributes.update(attributes)

        self.default_vertex_attributes.update({
            'is_support': False,
            'course': None,
        })
        if default_vertex_attributes is not None:
            self.default_vertex_attributes.update(default_vertex_attributes)

        self.default_edge_attributes.update({
            'interface_points': None,
            'interface_type': None,
            'niterface_size': None,
            'interface_uvw': None,
            'interface_origin': None,
            'interface_forces': None,
        })
        if default_edge_attributes is not None:
            self.default_edge_attributes.update(default_edge_attributes)

        if blocks:
            for block in blocks:
                self.add_block(block)

    @classmethod
    def from_json(cls, filepath):
        from compas_assembly.datastructures import Block

        with open(filepath, 'r') as fo:
            data = json.load(fo)

            # vertex keys in an assembly can be of any hashable type
            # keys in the blocks dict should be treated the same way!

            assembly = cls.from_data(data['assembly'])
            assembly.blocks = {
                int(key): Block.from_data(data['blocks'][key])
                for key in data['blocks']
            }

        return assembly

    def to_json(self, filepath):
        data = {
            'assembly': self.to_data(),
            'blocks':
            {str(key): self.blocks[key].to_data()
             for key in self.blocks}
        }
        with open(filepath, 'w') as fo:
            json.dump(data, fo)

    def copy(self):
        assembly = super(Assembly, self).copy()
        assembly.blocks = {key: self.blocks[key].copy() for key in self.vertices()}
        return assembly

    def add_block(self, block, attr_dict=None, **kwattr):
        """Add a block to the assembly.

        Parameters
        ----------
        block : compas_assembly.datastructures.Block
            The block to add.
        attr_dict : dict, optional
            A dictionary of block attributes.
            Default is ``None``.

        Returns
        -------
        hashable
            The identifier of the block.

        Notes
        -----
        The block is added as a vertex in the assembly data structure.
        The XYZ coordinates of the vertex are the coordinates of the centroid of the block.

        """
        attr = attr_dict or {}
        attr.update(kwattr)
        x, y, z = block.centroid()
        key = self.add_vertex(attr_dict=attr, x=x, y=y, z=z)
        self.blocks[key] = block
        return key

    def add_blocks_from_polysurfaces(self, guids):
        """Add multiple blocks from their representation as Rhino poly surfaces.

        Parameters
        ----------
        guids : list of str
            A list of GUIDs identifying the poly-surfaces representing the blocks of the assembly.

        Returns
        -------
        list
            The keys of the added blocks.

        Warning
        -------
        This method only works in Rhino.

        Examples
        --------
        .. code-block:: python

            pass

        """
        from compas_assembly.datastructures import Block

        onames = compas_rhino.get_object_names(guids)

        keys = []

        for i, (guid, oname) in enumerate(zip(guids, onames)):
            try:
                attr = ast.literal_eval(oname)
            except (TypeError, ValueError):
                attr = {}

            name = attr.get('name', 'B{0}'.format(i))

            block = Block.from_polysurface(guid)
            block.attributes['name'] = name

            key = self.add_block(block, attr_dict=attr)

            keys.append(key)

        return keys

    def add_blocks_from_rhinomeshes(self, guids):
        """Add multiple blocks from their representation as as Rhino meshes.

        Parameters
        ----------
        guids : list of str
            A list of GUIDs identifying the meshes representing the blocks of the assembly.

        Returns
        -------
        list
            The keys of the added blocks.

        Warning
        -------
        This method only works in Rhino.

        Examples
        --------
        .. code-block:: python

            pass

        """
        from compas_assembly.datastructures import Block

        onames = compas_rhino.get_object_names(guids)

        keys = []

        for i, (guid, oname) in enumerate(zip(guids, onames)):
            try:
                attr = ast.literal_eval(oname)
            except (TypeError, ValueError):
                attr = {}

            name = attr.get('name', 'B{0}'.format(i))

            block = Block.from_rhinomesh(guid)
            block.attributes['name'] = name

            key = self.add_block(block, attr_dict=attr)

            keys.append(key)

        return keys

    def number_of_interface_vertices(self):
        return sum(len(attr['interface_points']) for u, v, attr in self.edges(True))

    def draw(self, settings=None):
        """Convenience function for drawing the assembly in Rhino using common visualisation settings.

        Parameters
        ----------
        settings : dict, optional
            A dictionary with drawing options.

        """
        from compas_assembly.rhino import AssemblyArtist

        settings = settings or {}

        artist = AssemblyArtist(self, layer=settings.get('layer'))

        artist.defaults.update(settings)

        artist.clear_layer()
        artist.draw_blocks()

        vertexcolor = {key: artist.defaults['color.vertex:is_support'] for key in self.vertices_where({'is_support': True})}

        if settings.get('show.vertices'):
            artist.draw_vertices(color=vertexcolor)
        if settings.get('show.edges'):
            artist.draw_edges()
        if settings.get('show.interfaces'):
            artist.draw_interfaces()
        if settings.get('show.forces'):
            if settings.get('mode.interface') == 0:
                artist.color_interfaces(0)
            else:
                artist.color_interfaces(1)
            if settings.get('show.forces_as_vectors'):
                if settings.get('mode.force') == 0:
                    artist.draw_forces(mode=0)
                else:
                    artist.draw_forces(mode=1)
        if settings.get('show.selfweight'):
            artist.draw_selfweight()
        if settings.get('show.frictions'):
            if settings.get('mode.friction') == 0:
                artist.draw_frictions(mode=0)
            else:
                artist.draw_frictions(mode=1)

        artist.redraw()


# ==============================================================================
# Main
# ==============================================================================

if __name__ == "__main__":

    from compas_assembly.datastructures import Assembly
    from compas_assembly.datastructures import Block

    assembly = Assembly()

    for i in range(2):
        block = Block.from_polyhedron(6)
        assembly.add_block(block)

    print(assembly.summary())
