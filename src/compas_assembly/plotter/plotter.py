from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

from compas_plotters import Plotter
from compas_plotters import NetworkPlotter
from compas_plotters import MeshPlotter

from compas.utilities import color_to_rgb
from compas.geometry import oriented_bounding_box_xy_numpy


__all__ = ['AssemblyPlotter']


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
                    keys=None,
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
        keys = keys or list(self.assembly.nodes())

        facecolordict = valuedict(keys, facecolor, self.block_plotter.defaults['face.facecolor'])
        edgecolordict = valuedict(keys, edgecolor, self.block_plotter.defaults['face.edgecolor'])
        edgewidthdict = valuedict(keys, edgewidth, self.block_plotter.defaults['face.edgewidth'])
        textcolordict = valuedict(keys, textcolor, self.block_plotter.defaults['face.textcolor'])
        fontsizedict  = valuedict(keys, fontsize,  self.block_plotter.defaults['face.fontsize'])

        polygons = []
        for key in self.assembly.nodes():
            block = self.assembly.blocks[key]
            for fkey in block.faces():
                polygons.append({
                    'points': block.face_coordinates(fkey),
                    'edgecolor': edgecolordict[key],
                    'edgewidth': edgewidthdict[key],
                    'facecolor': facecolordict[key]
                })
        collection = self.draw_polygons(polygons)
        self.blockcollection = collection
        return collection


# ==============================================================================
# Main
# ==============================================================================

if __name__ == '__main__':
    pass
