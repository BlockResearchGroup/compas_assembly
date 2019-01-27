from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

from compas.plotters import Plotter
from compas.plotters import NetworkPlotter
from compas.plotters import MeshPlotter


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
