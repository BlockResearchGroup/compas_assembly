from compas.colors import Color
from compas.artists.colordict import ColorDict
from compas.artists import Artist

from abc import abstractmethod


class AssemblyArtist(Artist):
    """
    Base artist for assembly data structures.
    """

    default_nodecolor = Color.from_hex("#0092D2")
    default_edgecolor = Color.white()

    default_selfweightcolor = Color.magenta()

    node_color = ColorDict()
    edge_color = ColorDict()

    def __init__(self, assembly, **kwargs):
        super(AssemblyArtist, self).__init__()
        self._default_nodecolor = None
        self._default_edgecolor = None
        self._default_selfweightcolor = None
        self._assembly = None
        self._nodes = None
        self._edges = None
        self._node_xyz = None
        self._node_color = None
        self._edge_color = None
        self._node_text = None
        self._edge_text = None
        self._nodecollection = None
        self._edgecollection = None
        self._nodelabelcollection = None
        self._edgelabelcollection = None

        self.assembly = assembly

    @property
    def assembly(self):
        return self._assembly

    @assembly.setter
    def assembly(self, assembly):
        self._assembly = assembly
        self._node_xyz = None

    @property
    def nodes(self):
        if self._nodes is None:
            self._nodes = list(self.assembly.nodes())
        return self._nodes

    @nodes.setter
    def nodes(self, nodes):
        self._nodes = nodes

    @property
    def edges(self):
        if self._edges is None:
            self._edges = list(self.assembly.edges())
        return self._edges

    @edges.setter
    def edges(self, edges):
        self._edges = edges

    @property
    def node_xyz(self):
        if not self._node_xyz:
            return {
                node: self.assembly.node_point(node) for node in self.assembly.nodes()
            }
        return self._node_xyz

    @node_xyz.setter
    def node_xyz(self, node_xyz):
        self._node_xyz = node_xyz

    @property
    def node_text(self):
        if not self._node_text:
            self._node_text = {node: str(node) for node in self.assembly.nodes()}
        return self._node_text

    @node_text.setter
    def node_text(self, text):
        if text == "key":
            self._node_text = {node: str(node) for node in self.assembly.nodes()}
        elif text == "index":
            self._node_text = {
                node: str(index) for index, node in enumerate(self.assembly.nodes())
            }
        elif isinstance(text, dict):
            self._node_text = text

    @property
    def edge_text(self):
        if not self._edge_text:
            self._edge_text = {
                edge: "{}-{}".format(*edge) for edge in self.assembly.edges()
            }
        return self._edge_text

    @edge_text.setter
    def edge_text(self, text):
        if text == "key":
            self._edge_text = {
                edge: "{}-{}".format(*edge) for edge in self.assembly.edges()
            }
        elif text == "index":
            self._edge_text = {
                edge: str(index) for index, edge in enumerate(self.assembly.edges())
            }
        elif isinstance(text, dict):
            self._edge_text = text

    def draw(self):
        self.draw_blocks()

    @abstractmethod
    def draw_nodes(self):
        pass

    @abstractmethod
    def draw_edges(self):
        pass

    @abstractmethod
    def draw_blocks(self):
        pass

    @abstractmethod
    def draw_interfaces(self):
        pass

    @abstractmethod
    def draw_selfweight(self):
        pass

    @abstractmethod
    def draw_forces(self):
        pass

    @abstractmethod
    def draw_resultants(self):
        pass

    @abstractmethod
    def draw_reactions(self):
        pass
