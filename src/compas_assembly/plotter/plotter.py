from compas_plotters import Plotter
from compas_plotters import NetworkPlotter
from compas_plotters import MeshPlotter


def valuedict(keys, value, default):
    value = value or default
    if isinstance(value, dict):
        valuedict = {key: default for key in keys}
        valuedict.update(value)
    else:
        valuedict = {key: value for key in keys}
    return valuedict


class AssemblyPlotter(Plotter):
    """An ``AssemblyPlotter`` combines the functionality of a ``NetworkPlotter``
    and a ``MeshPlotter`` and uses the same set of axes for all drawing output.

    Parameters
    ----------
    assembly : Assembly
        The assembly data structure.

    Notes
    -----
    For all other relevant parameters, see ``Plotter``.

    Examples
    --------
    >>>
    """

    def __init__(self, assembly, **kwargs):
        super(AssemblyPlotter, self).__init__(**kwargs)
        self.assembly = assembly
        self.assembly_plotter = NetworkPlotter(self.assembly, axes=self.axes)
        self.block_plotter = MeshPlotter(None, axes=self.axes)
        self.blockcollection = None

    def draw_nodes(self, *args, **kwargs):
        """Draw the nodes of an assembly.

        Parameters
        ----------

        Examples
        --------
        >>>
        """
        return self.assembly_plotter.draw_nodes(*args, **kwargs)

    def draw_edges(self, *args, **kwargs):
        """Draw the edges of an assembly.
        """
        self.assembly_plotter.draw_edges(*args, **kwargs)

    def clear_blocks(self):
        if self.blockcollection:
            self.blockcollection.remove()

    def draw_blocks(self,
                    nodes=None,
                    facecolor=None,
                    edgecolor=None,
                    edgewidth=None,
                    textcolor=None,
                    fontsize=None):
        """Draw the blocks of an assembly.

        Notes
        -----
        The blocks are drawn as the boundaing boxes of their vertices.

        """
        nodes = nodes or list(self.assembly.nodes())

        node_facecolor = valuedict(nodes, facecolor, self.block_plotter.defaults['face.facecolor'])
        node_edgecolor = valuedict(nodes, edgecolor, self.block_plotter.defaults['face.edgecolor'])
        node_edgewidth = valuedict(nodes, edgewidth, self.block_plotter.defaults['face.edgewidth'])

        polygons = []
        for node in nodes:
            block = self.assembly.node_attribute(node, 'block')
            for face in block.faces():
                polygons.append({
                    'points': block.face_coordinates(face),
                    'edgecolor': node_edgecolor[node],
                    'edgewidth': node_edgewidth[node],
                    'facecolor': node_facecolor[node]
                })
        collection = self.draw_polygons(polygons)
        self.blockcollection = collection
        return collection
