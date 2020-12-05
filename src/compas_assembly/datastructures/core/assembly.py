from __future__ import print_function
from __future__ import absolute_import
from __future__ import division

# import json
from compas.datastructures import Network
from .block import Block
# from .interface import Interface


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

    def __init__(self):
        super(Assembly, self).__init__()
        self.default_node_attributes.update({
            'block': None
        })
        # self.default_edge_attributes.update({
        #     'interface_points': None,
        #     'interface_type': None,
        #     'interface_size': None,
        #     'interface_uvw': None,
        #     'interface_origin': None,
        #     'interface_forces': None
        # })
        self.default_edge_attributes.update({
            'interface': None
        })
        # self.blocks = {}
        # self.interfaces = {}

    # @classmethod
    # def from_json(cls, filepath):
    #     """Construct an assembly from the data contained in a JSON file.

    #     Parameters
    #     ----------
    #     filepath : str
    #         Path to the file containing the data.

    #     Returns
    #     -------
    #     Assembly
    #         An assembly data structure.

    #     Examples
    #     --------
    #     >>>
    #     """
    #     with open(filepath, 'r') as f:
    #         data = json.load(f)
    #         assembly = cls.from_data(data['assembly'])
    #         assembly.blocks = {int(key): Block.from_data(data['blocks'][key]) for key in data['blocks']}
    #     return assembly

    # def to_json(self, filepath):
    #     """Serialise the data dictionary representing an assembly to JSON and store in a file.

    #     Parameters
    #     ----------
    #     filepath : str
    #         Path to the file.

    #     Examples
    #     --------
    #     >>>
    #     """
    #     data = {
    #         'assembly': self.to_data(),
    #         'blocks': {str(key): self.blocks[key].to_data() for key in self.blocks}}
    #     with open(filepath, 'w') as fo:
    #         json.dump(data, fo, indent=4, sort_keys=True)

    # def copy(self):
    #     """Make an independent copy of an assembly.

    #     Examples
    #     --------
    #     >>>
    #     """
    #     assembly = super(Assembly, self).copy()
    #     assembly.blocks = {key: self.blocks[key].copy() for key in self.nodes()}
    #     return assembly

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
        return self.add_node(key, block=block)

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

    # def subset(self, keys):
    #     """Create an assembly that is a subset of the urrent assembly.

    #     Parameters
    #     ----------
    #     keys : list
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
    #     for key, attr in self.nodes(True):
    #         if key in keys:
    #             block = self.blocks[key].copy()
    #             sub.add_node(key=key, **attr)
    #             sub.blocks[key] = block
    #     for u, v, attr in self.edges(True):
    #         if u in keys and v in keys:
    #             sub.add_edge(u, v, **attr)
    #     return sub


# ==============================================================================
# Main
# ==============================================================================

if __name__ == "__main__":
    pass
