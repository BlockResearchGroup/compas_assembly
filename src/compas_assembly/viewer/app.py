from __future__ import print_function
from __future__ import absolute_import
from __future__ import division

from compas_viewers.core import App

from compas_assembly.viewer.view import View
from compas_assembly.viewer.controller import Controller

from compas_assembly.viewer import CONFIG
from compas_assembly.viewer import STYLE


__all__ = ['AssemblyViewer']


class AssemblyViewer(App):
    """"""

    def __init__(self):
        super(AssemblyViewer, self).__init__(CONFIG, STYLE)
        self.controller = Controller(self)
        self.view = View(self.controller)
        self.setup()
        self.init()
        self.view.glInit()
        self.view.setup_grid()

    @property
    def assembly(self):
        return self.controller.assembly

    @assembly.setter
    def assembly(self, assembly):
        self.controller.assembly = assembly
        self.controller.center_assembly()
        self.view.glInit()
        self.view.make_buffers()
        self.view.updateGL()


# ==============================================================================
# Main
# ==============================================================================

if __name__ == '__main__':

    import os
    import compas_assembly
    from compas_assembly.datastructures import Assembly

    assembly = Assembly.from_json(os.path.join(compas_assembly.DATA, 'stack.json'))

    viewer = AssemblyViewer()
    viewer.assembly = assembly
    viewer.show()

