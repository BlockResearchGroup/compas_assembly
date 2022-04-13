from __future__ import print_function
from __future__ import absolute_import
from __future__ import division

from compas.datastructures import Datastructure
from compas.datastructures import Graph

from compas_assembly.datastructures import Block


class AssemblyError(Exception):
    pass


class Assembly(Datastructure):
    """A data structure for managing the connections between different parts of an assembly.

    Parameters
    ----------
    name : str, optional
        The name of the assembly.

    Attributes
    ----------
    attributes : dict[str, Any]
        General attributes of the data structure that will be included in the data dict and serialization.
    graph : :class:`compas.datastructures.Graph`
        The graph that is used under the hood to store the parts and their connections.

    Examples
    --------
    >>>

    """

    def __init__(self, name=None, **kwargs):
        super(Assembly, self).__init__()

        self.attributes = {"name": name or "Assembly"}
        self.attributes.update(kwargs)
        self.graph = Graph()
        self.graph.update_default_node_attributes({"block": None, "is_support": False})
        self.graph.update_default_edge_attributes({"interface": None})

    # ==========================================================================
    # data
    # ==========================================================================

    @property
    def DATASCHEMA(self):
        import schema

        return schema.Schema(
            {
                "attributes": dict,
                "graph": Graph,
            }
        )

    @property
    def JSONSCHEMANAME(self):
        return "assembly"

    @property
    def data(self):
        data = {
            "attributes": self.attributes,
            "graph": self.graph.data,
        }
        return data

    @data.setter
    def data(self, data):
        self.attributes.update(data["attributes"] or {})
        self.graph.data = data["graph"]

    # ==========================================================================
    # properties
    # ==========================================================================

    # ==========================================================================
    # customization
    # ==========================================================================

    def __str__(self):
        tpl = "<Assembly with {} blocks and {} interfaces>"
        return tpl.format(self.graph.number_of_nodes(), self.graph.number_of_edges())

    # @classmethod
    # def from_geometry(cls, geometry):
    #     """Construct an assembly of blocks from a particular type of assembly geometry.

    #     Parameters
    #     ----------
    #     geometry : compas_assembly.geometry.Geometry
    #         A geometry object.

    #     Returns
    #     -------
    #     assembly : compas_assembly.datastructures.Assembly
    #         The resulting assembly data structure.

    #     """
    #     assembly = cls()
    #     for mesh in geometry.blocks():
    #         assembly.add_block(mesh.copy(cls=Block))
    #     return assembly

    # ==========================================================================
    # builders
    # ==========================================================================

    def add_block(self, block, node=None, attr_dict=None, **kwattr):
        """Add a block to the assembly.

        Parameters
        ----------
        block : :class:`compas_assembly.datastructures.Block`
            The block to add.
        node : hashable, optional
            The identifier of the corresponding node in the connectivity graph.
            If no value is provided, the identifier will be generated automatically by the graph.
        attr_dict : dict, optional
            A dictionary of block attributes.
        **kwatr : dict, optional
            Additional attributes in the form of named function parameters.

        Returns
        -------
        hashable
            The identifier of the node in the graph corresponding to the block.

        """
        node = self.graph.add_node(node, block=block, attr_dict=attr_dict, **kwattr)
        block.node = node
        return node

    def add_interface(self, a, b, interface):
        """Add an interface between two blocks.

        Parameters
        ----------
        a : :class:`compas_assembly.datastructures.Block`
            The "from" block.
        b : :class:`compas_assembly.datastructures.Block`
            The "to" block.
        interface : :class:`compas_assembly.datastructures.Interface`
            The interface.

        Returns
        -------
        tuple[hashable, hashable]
            the identifier of the edge in the graph corresponding to the interface.

        Raises
        ------
        AssemblyError
            If at least one of the blocks is not part of the assembly.

        """
        if a.node is None or b.node is None:
            raise AssemblyError("Both blocks have to be part of the assembly.")
        if not self.graph.has_node(a.node) or not self.graph.has_node(b.node):
            raise AssemblyError("Both blocks have to be part of the assembly.")

        edge = self.graph.add_edge(a.node, b.node, interface=interface)
        interface.edge = edge
        return edge

    def add_blocks_from_polysurfaces(self, guids):
        """Add multiple blocks from their representation as Rhino poly surfaces.

        Parameters
        ----------
        guids : list[str]
            A list of GUIDs identifying the poly-surfaces representing the blocks of the assembly.

        Returns
        -------
        list[hashable]
            The identifiers of the nodes in the graph corresponding to the added blocks.

        Examples
        --------
        >>> assembly = Assembly()
        >>> guids = compas_rhino.select_surfaces()
        >>> assembly.add_blocks_from_polysurfaces(guids)

        """
        nodes = []
        for guid in guids:
            block = Block.from_polysurface(guid)
            node = self.add_block(block)
            nodes.append(node)
        return nodes

    def add_blocks_from_rhinomeshes(self, guids):
        """Add multiple blocks from their representation as as Rhino meshes.

        Parameters
        ----------
        guids : list[str]
            A list of GUIDs identifying the meshes representing the blocks of the assembly.

        Returns
        -------
        list[hashable]
            The identifiers of the nodes in the graph corresponding to the added blocks.

        Examples
        --------
        >>> assembly = Assembly()
        >>> guids = compas_rhino.select_meshes()
        >>> assembly.add_blocks_from_rhinomeshes(guids)

        """
        nodes = []
        for guid in guids:
            block = Block.from_rhinomesh(guid)
            node = self.add_block(block)
            nodes.append(node)
        return nodes

    # ==========================================================================
    # accessors
    # ==========================================================================

    def nodes(self):
        """Iterate over the nodes of the graph of the assembly.

        Yields
        ------
        hashable

        """
        for node in self.graph.nodes():
            yield node

    def edges(self):
        """Iterate over the edges of the graph of the assembly.

        Yields
        ------
        tuple[hashable, hashable]

        """
        for edge in self.graph.edges():
            yield edge

    def blocks(self):
        """Iterate over the blocks of the assembly.

        Yields
        ------
        :class:`compas_assembly.datastructures.Block`

        """
        for node in self.graph.nodes():
            yield self.node_block(node)

    def interfaces(self):
        """Yield the interfaces of the assembly.

        Yields
        ------
        :class:`compas_assembly.datastructures.Interface`

        """
        for edge in self.graph.edges():
            yield self.edge_interface(edge)

    def node_block(self, node):
        """Retrieve the block corresponding to a graph node.

        Parameters
        ----------
        node : hashable
            The identifier of the node.

        Returns
        -------
        :class:`compas_assembly.datastructures.Block`

        """
        return self.graph.node_attribute(node, "block")

    def node_point(self, node):
        """Retrieve a point representing the location of the node.

        Parameters
        ----------
        node : hashable
            the identifier of the node.

        Returns
        -------
        :class:`compas.geometry.Point`

        """
        block = self.node_block(node)
        return block.centroid()

    def edge_interface(self, edge):
        """Retrieve the interface corresponding to a graph edge.

        Parameters
        ----------
        edge : tuple[hashable, hashable]
            The identifier of the edge.

        Returns
        -------
        :class:`compas_assembly.datastructures.Interface`

        """
        return self.graph.edge_attribute(edge, "interface")

    def edge_blocks(self, edge):
        """Retrieve the two blocks corresponding to a graph edge.

        Parameters
        ----------
        edge : tuple[hashable, hashable]
            The identifier of the edge.

        Returns
        -------
        tuple[:class:`compas_assembly.datastructures.Block`, :class:`compas_assembly.datastructures.Block`]

        """
        u, v = edge
        return self.node_block(u), self.node_block(v)

    # ==========================================================================
    # methods
    # ==========================================================================

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
        for node in self.graph.nodes():
            block = self.graph.node_attribute(node, "block")
            block.transform(T)

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

    # def number_of_interface_nodes(self):
    #     """Compute the total number of interface nodes.

    #     Returns
    #     -------
    #     int
    #         The number of nodes.

    #     """
    #     return sum(len(attr["interface_points"]) for u, v, attr in self.edges(True))

    # def subset(self, nodes):
    #     """Create an assembly that is a subset of the current assembly.

    #     Parameters
    #     ----------
    #     nodes : list
    #         Identifiers of the blocks that should be included in the subset.

    #     Returns
    #     -------
    #     Assembly
    #         The sub-assembly.

    #     Examples
    #     --------
    #     >>>
    #     """
    #     cls = type(self)
    #     sub = cls()
    #     for node in self.nodes():
    #         if node in nodes:
    #             attr = self.node_attributes()
    #             sub.add_node(key=node, **attr)
    #     for u, v in self.edges():
    #         if u in nodes and v in nodes:
    #             sub.add_edge(u, v, **attr)
    #     return sub
