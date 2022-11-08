from __future__ import print_function
from __future__ import absolute_import
from __future__ import division

from compas.geometry import Point
from compas.geometry import Line
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

        self._blocks = {}
        self.attributes = {"name": name or "Assembly"}
        self.attributes.update(kwargs)
        self.graph = Graph()
        self.graph.update_default_node_attributes(
            {
                "block": None,
                "is_support": False,
                "section": None,
                "mesh_size": None,
                "displacement": [0, 0, 0, 0, 0, 0],
            }
        )
        self.graph.update_default_edge_attributes(
            {
                "interfaces": None,
            }
        )

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
        return {
            "attributes": self.attributes,
            "graph": self.graph.data,
        }

    @data.setter
    def data(self, data):
        self.attributes.update(data["attributes"] or {})
        self.graph.data = data["graph"]
        self._blocks = {}
        for node in self.graph.nodes():
            block = self.graph.node_attribute(node, "block")
            if block:
                self._blocks[block.guid] = node

    # ==========================================================================
    # properties
    # ==========================================================================

    # ==========================================================================
    # customization
    # ==========================================================================

    def __str__(self):
        tpl = "<Assembly with {} blocks and {} interfaces>"
        return tpl.format(self.graph.number_of_nodes(), self.graph.number_of_edges())

    # ==========================================================================
    # constructors
    # ==========================================================================

    @classmethod
    def from_template(cls, template, identify_interfaces=False, **kwargs):
        """Construct an assembly from a parameteric template.

        Returns
        -------
        :class:`Assembly`

        """
        assembly = cls()
        for mesh in template.blocks():
            block = mesh.copy(cls=Block)
            x, y, z = block.centroid()
            assembly.add_block(block, x=x, y=y, z=z)

        if identify_interfaces:
            from compas_assembly.algorithms import assembly_interfaces

            assembly_interfaces(assembly)
        return assembly

    @classmethod
    def from_polysurfaces(cls, guids, identify_interfaces=False, **kwargs):
        """Construct an assembly from Rhino polysurfaces.

        Parameters
        ----------
        guids : list[str]
            A list of GUIDs identifying the poly-surfaces representing the blocks of the assembly.

        Returns
        -------
        :class:`Assembly`

        Examples
        --------
        >>> assembly = Assembly()
        >>> guids = compas_rhino.select_surfaces()
        >>> assembly.add_blocks_from_polysurfaces(guids)

        """
        assembly = cls()
        for guid in guids:
            block = Block.from_polysurface(guid)
            assembly.add_block(block)

        if identify_interfaces:
            from compas_assembly.algorithms import assembly_interfaces

            assembly_interfaces(assembly)
        return assembly

    def from_rhinomeshes(cls, guids, identify_interfaces=False):
        """Construct an assembly from Rhino meshes.

        Parameters
        ----------
        guids : list[str]
            A list of GUIDs identifying the meshes representing the blocks of the assembly.

        Returns
        -------
        :class:`Assembly`

        Examples
        --------
        >>> assembly = Assembly()
        >>> guids = compas_rhino.select_meshes()
        >>> assembly.add_blocks_from_rhinomeshes(guids)

        """
        assembly = cls()
        for guid in guids:
            block = Block.from_rhinomesh(guid)
            assembly.add_block(block)

        if identify_interfaces:
            from compas_assembly.algorithms import assembly_interfaces

            assembly_interfaces(assembly)
        return assembly

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
        if self.has_block(block):
            raise Exception("Block already exists in this assembly.")
        node = self.graph.add_node(node, block=block, attr_dict=attr_dict, **kwattr)
        self._blocks[block.guid] = node
        return node

    def add_block_from_mesh(self, mesh, node=None, attr_dict=None, **kwattr):
        """Add a block to the assembly from a normal mesh.

        Parameters
        ----------
        mesh : :class:`compas.datastructures.Mesh`
            The mesh to add.
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
        block = mesh.copy(cls=Block)
        return self.add_block(block, node=node, attr_dict=attr_dict, **kwattr)

    def add_block_block_interfaces(self, a, b, interfaces):
        """Add an interface between two blocks.

        Parameters
        ----------
        a : :class:`compas_assembly.datastructures.Block`
            The "from" block.
        b : :class:`compas_assembly.datastructures.Block`
            The "to" block.
        interfaces : List[:class:`compas_assembly.datastructures.Interface`]
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
        if not self.has_block(a):
            raise AssemblyError("Block A is not part of the assembly.")
        if not self.has_block(b):
            raise AssemblyError("Block B is not part of the assembly.")

        u = self.block_node(a)
        v = self.block_node(b)

        edge = self.graph.add_edge(u, v, interfaces=interfaces)
        return edge

    # ==========================================================================
    # verification
    # ==========================================================================

    def has_block(self, block):
        """Verify that the assembly contains a given block.

        Parameters
        ----------
        block : :class:`compas_assembly.datastructures.Block`

        Returns
        -------
        bool

        """
        if block.guid not in self._blocks:
            return False
        node = self._blocks[block.guid]
        if not self.graph.has_node(node):
            return False
        return True

    def has_interface(self, interface):
        """Verify that the assembly contains a given interface.

        Parameters
        ----------
        interface : :class:`compas_assembly.datastructures.Interface`

        Returns
        -------
        bool

        """
        raise NotImplementedError

    # ==========================================================================
    # accessors
    # ==========================================================================

    def number_of_nodes(self):
        """Return the number of nodes in the assembly graph.

        Returns
        -------
        int

        """
        return len(list(self.graph.nodes()))

    def nodes(self):
        """Iterate over the nodes of the graph of the assembly.

        Returns
        -------
        Generator[hashable, None, None]

        """
        return self.graph.nodes()

    def number_of_edges(self):
        """Return the number of edges in the assembly graph.

        Returns
        -------
        int

        """
        return len(list(self.graph.edges()))

    def edges(self):
        """Iterate over the edges of the graph of the assembly.

        Returns
        -------
        Generator[tuple[hashable, hashable], None, None]

        """
        return self.graph.edges()

    def number_of_blocks(self):
        """Return the number of blocks in the assembly.

        Returns
        -------
        int

        """
        return self.number_of_nodes()

    def blocks(self):
        """Iterate over the blocks of the assembly.

        Yields
        ------
        :class:`compas_assembly.datastructures.Block`

        """
        for node in self.graph.nodes():
            yield self.node_block(node)

    def number_of_interfaces(self):
        """Return the number of interfaces in the assembly.

        Returns
        -------
        int

        """
        return self.number_of_edges()

    def interfaces(self):
        """Yield the interfaces of the assembly.

        Yields
        ------
        :class:`compas_assembly.datastructures.Interface`

        """
        for edge in self.graph.edges():
            interfaces = self.edge_interfaces(edge)
            for interface in interfaces:
                yield interface

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

    def block_node(self, block):
        """Retrieve the graph node corresponding to a block.

        Parameters
        ----------
        block : :class:`compas_assembly.datastructures.Block`

        Returns
        -------
        hashable

        """
        return self._blocks[block.guid]

    def edge_interfaces(self, edge):
        """Retrieve the interface corresponding to a graph edge.

        Parameters
        ----------
        edge : tuple[hashable, hashable]
            The identifier of the edge.

        Returns
        -------
        List[:class:`compas_assembly.datastructures.Interface`]

        """
        return self.graph.edge_attribute(edge, "interfaces") or []

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
    # geometry
    # ==========================================================================

    def node_point(self, node):
        """Retrieve a point representing the location of the node.

        Parameters
        ----------
        node : hashable
            The identifier of the node.

        Returns
        -------
        :class:`compas.geometry.Point`

        """
        block = self.node_block(node)
        return Point(*block.centroid())

    def edge_line(self, edge):
        """Retrieve the line segment between the nodes of the edge.

        Parameters
        ----------
        edge : tuple[hashable, hashable]
            The identifier of the edge.

        Returns
        -------
        :class:`compas.geometry.Line`

        """
        u, v = edge
        a = self.node_point(u)
        b = self.node_point(v)
        return Line(a, b)

    # ==========================================================================
    # boundary conditions
    # ==========================================================================

    def unset_boundary_conditions(self):
        """Unset all boundary conditions.

        Returns
        -------
        None

        """
        for node in self.graph.nodes():
            self.graph.unset_node_attribute(node, "is_support")

    def set_boundary_condition(self, node):
        """Set the boundary condition for a single node.

        Parameters
        ----------
        node : hashable
            The identifier of the node.

        Returns
        -------
        None

        """
        self.graph.node_attribute(node, "is_support", True)

    def set_boundary_conditions(self, nodes):
        """Set the boundary condition for multiple nodes.

        Parameters
        ----------
        nodes : list[hashable]
            The identifiers of the node.

        Returns
        -------
        None

        """
        for node in nodes:
            self.graph.node_attribute(node, "is_support", True)

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
