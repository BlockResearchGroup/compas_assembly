from __future__ import print_function
from __future__ import absolute_import
from __future__ import division

import ast
import json

import compas_rhino
from compas.datastructures import Network


__all__ = ['Assembly']


class Assembly(Network):
    """A data structure for discrete element assemblies.

    An assembly is essentially a network of assembly elements.
    Each node of the network represents an element of the assembly.
    Each edge of the network represents an interface between two assembly elements.

    Parameters
    ----------

    Attributes
    ----------

    Examples
    --------
    >>>
    """

    __module__ = 'compas_assembly.datastructures'

    def __init__(self):
        super(Assembly, self).__init__()
        self.blocks = {}
        self.attributes.update({'name': 'Assembly'})
        self.default_node_attributes.update({
            'is_support': False,
            'course': None})
        self.default_edge_attributes.update({
            'interface_points': None,
            'interface_type': None,
            'interface_size': None,
            'interface_uvw': None,
            'interface_origin': None,
            'interface_forces': None})

    @classmethod
    def from_json(cls, filepath):
        """Construct an assembly from the data contained in a JSON file.

        Parameters
        ----------
        filepath : str
            Path to the file containing the data.

        Returns
        -------
        Assembly
            An assembly data structure.

        Examples
        --------
        >>>
        """
        from compas_assembly.datastructures import Block
        with open(filepath, 'r') as fo:
            data = json.load(fo)
            assembly = cls.from_data(data['assembly'])
            assembly.blocks = {int(key): Block.from_data(data['blocks'][key]) for key in data['blocks']}
        return assembly

    def to_json(self, filepath):
        """Serialise the data dictionary representing an assembly to JSON and store in a file.

        Parameters
        ----------
        filepath : str
            Path to the file.

        Examples
        --------
        >>>
        """
        data = {
            'assembly': self.to_data(),
            'blocks': {str(key): self.blocks[key].to_data() for key in self.blocks}}
        with open(filepath, 'w') as fo:
            json.dump(data, fo, indent=4, sort_keys=True)

    def copy(self):
        """Make an independent copy of an assembly.

        Examples
        --------
        >>>
        """
        assembly = super(Assembly, self).copy()
        assembly.blocks = {key: self.blocks[key].copy() for key in self.nodes()}
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
        attr = attr_dict or {}
        attr.update(kwattr)
        x, y, z = block.centroid()
        key = self.add_node(key=key, attr_dict=attr, x=x, y=y, z=z)
        self.blocks[key] = block
        return key

    # def add_blocks_from_polysurfaces(self, guids):
    #     """Add multiple blocks from their representation as Rhino poly surfaces.

    #     Parameters
    #     ----------
    #     guids : list of str
    #         A list of GUIDs identifying the poly-surfaces representing the blocks of the assembly.

    #     Returns
    #     -------
    #     list
    #         The keys of the added blocks.

    #     Warning
    #     -------
    #     This method only works in Rhino.

    #     Examples
    #     --------
    #     >>>
    #     """
    #     from compas_assembly.datastructures import Block
    #     onames = compas_rhino.get_object_names(guids)
    #     keys = []
    #     for i, (guid, oname) in enumerate(zip(guids, onames)):
    #         try:
    #             attr = ast.literal_eval(oname)
    #         except (TypeError, ValueError):
    #             attr = {}
    #         name = attr.get('name', 'B{0}'.format(i))
    #         block = Block.from_polysurface(guid)
    #         block.attributes['name'] = name
    #         key = self.add_block(block, attr_dict=attr)
    #         keys.append(key)
    #     return keys

    # def add_blocks_from_rhinomeshes(self, guids):
    #     """Add multiple blocks from their representation as as Rhino meshes.

    #     Parameters
    #     ----------
    #     guids : list of str
    #         A list of GUIDs identifying the meshes representing the blocks of the assembly.

    #     Returns
    #     -------
    #     list
    #         The keys of the added blocks.

    #     Warning
    #     -------
    #     This method only works in Rhino.

    #     Examples
    #     --------
    #     .. code-block:: python

    #         assembly = Assembly()

    #         guids = compas_rhino.select_meshes()

    #         assembly.add_blocks_from_rhinomeshes(guids)

    #     """
    #     from compas_assembly.datastructures import Block

    #     onames = compas_rhino.get_object_names(guids)
    #     keys = []
    #     for i, (guid, oname) in enumerate(zip(guids, onames)):
    #         try:
    #             attr = ast.literal_eval(oname)
    #         except (TypeError, ValueError):
    #             attr = {}
    #         name = attr.get('name', 'B{0}'.format(i))
    #         block = Block.from_rhinomesh(guid)
    #         block.attributes['name'] = name
    #         key = self.add_block(block, attr_dict=attr)
    #         keys.append(key)
    #     return keys

    def number_of_interface_nodes(self):
        """Compute the total number of interface nodes.

        Returns
        -------
        int
            The number of nodes.

        """
        return sum(len(attr['interface_points']) for u, v, attr in self.edges(True))

    def subset(self, keys):
        """Create an assembly that is a subset of the urrent assembly.

        Parameters
        ----------
        keys : list
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
        for key, attr in self.nodes(True):
            if key in keys:
                block = self.blocks[key].copy()
                sub.add_node(key=key, **attr)
                sub.blocks[key] = block
        for u, v, attr in self.edges(True):
            if u in keys and v in keys:
                sub.add_edge(u, v, **attr)
        return sub


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
