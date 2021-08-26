from __future__ import print_function
from __future__ import absolute_import
from __future__ import division

from compas.datastructures import Network

from .block import Block


class Assembly(Network):
    """A data structure for discrete element assemblies.

    An assembly is essentially a network of assembly elements.
    Each node of the network represents an element of the assembly.
    Each edge of the network represents an interface between two assembly elements.

    Examples
    --------
    >>>
    """

    def __init__(self):
        super(Assembly, self).__init__()
        self.default_node_attributes.update({
            'block': None
        })
        self.default_edge_attributes.update({
            'interface': None
        })

    @classmethod
    def from_geometry(cls, geometry):
        """Construct an assembly of blocks from a particular type of assembly geometry.

        Parameters
        ----------
        geometry : compas_assembly.geometry.Geometry
            A geometry object.

        Returns
        -------
        assembly : compas_assembly.datastructures.Assembly
            The resulting assembly data structure.

        """
        assembly = cls()
        for mesh in geometry.blocks():
            assembly.add_block(mesh.copy(cls=Block))
        return assembly

    def add_block(self, block, key=None, attr_dict=None, **kwattr):
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
        The block is added as a node in the assembly data structure.
        The XYZ coordinates of the node are the coordinates of the centroid of the block.
        """
        x, y, z = block.centroid()
        return self.add_node(key, x=x, y=y, z=z, block=block, attr_dict=attr_dict, **kwattr)

    def add_interface(self, edge, interface):
        """"""
        u, v = edge
        return self.add_edge(u, v, interface=interface)

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

        Examples
        --------
        >>> assembly = Assembly()
        >>> guids = compas_rhino.select_surfaces()
        >>> assembly.add_blocks_from_polysurfaces(guids)

        """
        keys = []
        for guid in guids:
            block = Block.from_polysurface(guid)
            key = self.add_block(block)
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

        Examples
        --------
        >>> assembly = Assembly()
        >>> guids = compas_rhino.select_meshes()
        >>> assembly.add_blocks_from_rhinomeshes(guids)

        """
        keys = []
        for guid in guids:
            block = Block.from_rhinomesh(guid)
            key = self.add_block(block)
            keys.append(key)
        return keys

    def number_of_interface_nodes(self):
        """Compute the total number of interface nodes.

        Returns
        -------
        int
            The number of nodes.

        """
        return sum(len(attr['interface_points']) for u, v, attr in self.edges(True))

    def subset(self, nodes):
        """Create an assembly that is a subset of the current assembly.

        Parameters
        ----------
        nodes : list
            Identifiers of the blocks that should be included in the subset.

        Returns
        -------
        Assembly
            The sub-assembly.

        Examples
        --------
        >>>
        """
        cls = type(self)
        sub = cls()
        for node in self.nodes():
            if node in nodes:
                attr = self.node_attributes()
                sub.add_node(key=node, **attr)
        for u, v in self.edges():
            if u in nodes and v in nodes:
                sub.add_edge(u, v, **attr)
        return sub

    def transform(self, T):
        """Transform this assembly by the given transformation matrix.

        Parameters
        ----------
        T : Transformation
            The transformation matrix.

        Notes
        -----
        The assembly is transformed in place. No copy is made.

        Examples
        --------
        >>> assembly = Assembly.from_json('assembly.json')
        >>> R = Rotation.from_axis_and_angle([1.0, 0, 0], -pi / 2)
        >>> assembly_transform(assembly, R)

        """
        for node in self.nodes():
            block = self.node_attribute(node, 'block')
            block.transform(T)
            self.node_attributes(node, 'xyz', block.centroid())

    def transformed(self, T):
        """Transform a copy of this assembly by the given transformation matrix.

        Parameters
        ----------
        T : Transformation
            The transformation matrix.

        Returns
        -------
        Assembly
            The transformed copy.

        Examples
        --------
        >>> assembly = Assembly.from_json('assembly.json')
        >>> R = Rotation.from_axis_and_angle([1.0, 0, 0], -pi / 2)
        >>> transformed = assembly_transformed(assembly, R)

        """
        assembly = self.copy()
        assembly.transform(T)
        return assembly
