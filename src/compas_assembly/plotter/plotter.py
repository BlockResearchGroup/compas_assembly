from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

from compas.plotters import Plotter
from compas.plotters import NetworkPlotter
from compas.plotters import MeshPlotter

from compas.geometry import bounding_box_xy


__all__ = ['AssemblyPlotter']


class AssemblyPlotter(Plotter):
    """"""

    def __init__(self, assembly, **kwargs):
        super(AssemblyPlotter, self).__init__(**kwargs)
        self.assembly = assembly
        self.assembly_plotter = NetworkPlotter(self.assembly, axes=self.axes)
        self.block_plotter = MeshPlotter(None, axes=self.axes)

    def draw_vertices(self, *args, **kwargs):
        self.assembly_plotter.draw_vertices(*args, **kwargs)

    def draw_edges(self, *args, **kwargs):
        self.assembly_plotter.draw_edges(*args, **kwargs)

    def draw_blocks(self):
        polylines = []
        for key, attr in self.assembly.vertices(True):
            block = self.assembly.blocks[key]
            xyz = block.get_vertices_attributes('xyz')
            box = bounding_box_xy(xyz)
            polylines.append({
                'points': box + box[:1],
                'color': '#ff0000' if attr['is_support'] else '#cccccc',
            })
        self.draw_polylines(polylines)
