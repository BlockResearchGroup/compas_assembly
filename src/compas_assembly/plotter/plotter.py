from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

from compas_plotters import Plotter
from compas_plotters import NetworkPlotter
from compas_plotters import MeshPlotter

from compas.utilities import valuedict
from compas.utilities import color_to_rgb

from compas.geometry import bounding_box_xy


__all__ = ['AssemblyPlotter']


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
    .. code-block:: python

        plotter = AssemblyPlotter(assembly, tight=True, figsize=(12, 8))

        plotter.draw_vertices()
        plotter.draw_blocks()

        plotter.show()

    """

    def __init__(self, assembly, **kwargs):
        super(AssemblyPlotter, self).__init__(**kwargs)
        self.assembly = assembly
        self.assembly_plotter = NetworkPlotter(self.assembly, axes=self.axes)
        self.block_plotter = MeshPlotter(None, axes=self.axes)
        self.blockcollection = None

    def draw_vertices(self, *args, **kwargs):
        """Draw the vertices of an assembly.

        Parameters
        ----------
        keys
        text
        radius
        edgecolor
        facecolor
        edgewidth
        picker

        Examples
        --------
        .. code-block:: python



        """
        return self.assembly_plotter.draw_vertices(*args, **kwargs)

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
        keys = keys or list(self.assembly.vertices())

        facecolordict = valuedict(keys, facecolor, self.block_plotter.defaults['face.facecolor'])
        edgecolordict = valuedict(keys, edgecolor, self.block_plotter.defaults['face.edgecolor'])
        edgewidthdict = valuedict(keys, edgewidth, self.block_plotter.defaults['face.edgewidth'])
        textcolordict = valuedict(keys, textcolor, self.block_plotter.defaults['face.textcolor'])
        fontsizedict  = valuedict(keys, fontsize,  self.block_plotter.defaults['face.fontsize'])

        polygons = []
        for key, attr in self.assembly.vertices(True):
            block = self.assembly.blocks[key]
            xyz = block.get_vertices_attributes('xyz')
            box = bounding_box_xy(xyz)
            polygons.append({
                'points': box,
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
