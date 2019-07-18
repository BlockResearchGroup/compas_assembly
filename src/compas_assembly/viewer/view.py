from __future__ import print_function
from __future__ import absolute_import
from __future__ import division

from functools import partial

from OpenGL.GL import *
from OpenGL.GLU import *
from OpenGL.GLUT import *

import compas

from compas.utilities import hex_to_rgb
from compas.utilities import flatten

from compas_viewers.core import GLWidget
from compas_viewers.core import Grid
from compas_viewers.core import Axes


__all__ = ['View']


hex_to_rgb = partial(hex_to_rgb, normalize=True)


def flist(items):
    return list(flatten(items))


class View(GLWidget):
    """"""

    def __init__(self, controller):
        super(View, self).__init__()
        self.controller = controller
        self.v = 0
        self.e = 0
        self.b = 0
        self.i = 0

    @property
    def assembly(self):
        return self.controller.assembly

    @property
    def blocks(self):
        return self.controller.blocks

    @property
    def interfaces(self):
        return self.controller.interfaces

    @property
    def settings(self):
        return self.controller.settings

    # ==========================================================================
    # arrays
    # ==========================================================================

    def block_array_xyz(self, block):
        return flist(block.xyz)

    def block_array_vertices(self, block):
        return list(block.vertices)

    def block_array_edges(self, block):
        return flist(block.edges)

    def block_array_faces_front(self, block):
        return flist(block.faces)

    def block_array_faces_back(self, block):
        return flist(face[::-1] for face in block.faces)

    def block_array_vertices_color(self, block):
        return flist(hex_to_rgb(self.settings['vertices.color']) for key in block.vertices)

    def block_array_edges_color(self, block):
        return flist(hex_to_rgb(self.settings['edges.color']) for key in block.vertices)

    def block_array_faces_color_front(self, block):
        return flist(hex_to_rgb(self.settings['faces.color:front']) for key in block.xyz)

    def block_array_faces_color_back(self, block):
        return flist(hex_to_rgb(self.settings['faces.color:back']) for key in block.xyz)

    def interface_array_xyz(self, interface):
        return flist(interface.xyz)

    def interface_array_faces_front(self, interface):
        return flist(interface.faces)

    def interface_array_faces_back(self, interface):
        return flist(face[::-1] for face in interface.faces)

    def interface_array_faces_color_front(self, interface):
        return flist(hex_to_rgb(self.settings['interfaces.color:front']) for key in interface.xyz)

    def interface_array_faces_color_back(self, interface):
        return flist(hex_to_rgb(self.settings['interfaces.color:back']) for key in interface.xyz)

    # ==========================================================================
    # CAD
    # ==========================================================================

    def setup_grid(self):
        grid = Grid()
        index = glGenLists(1)
        glNewList(index, GL_COMPILE)
        grid.draw()
        glEndList()
        self.display_lists.append(index)

    def setup_axes(self):
        axes = Axes()
        index = glGenLists(1)
        glNewList(index, GL_COMPILE)
        axes.draw()
        glEndList()
        self.display_lists.append(index)

    # ==========================================================================
    # painting
    # ==========================================================================

    def paint(self):
        glDisable(GL_DEPTH_TEST)
        for dl in self.display_lists:
            glCallList(dl)

        glEnable(GL_DEPTH_TEST)
        self.draw_buffers()

    def make_buffers(self):
        self.buffers = {
            "blocks" : [],
            "interfaces" : [],
            "forces" : [],
        }
        for block in self.blocks:
            # combine all block vertex coordinates in one buffer
            # use a map to find the vertex coordinates of a specific block
            self.buffers["blocks"].append({
                'xyz'              : self.make_vertex_buffer(self.block_array_xyz(block)),
                'vertices'         : self.make_index_buffer(self.block_array_vertices(block)),
                'edges'            : self.make_index_buffer(self.block_array_edges(block)),
                'faces:front'      : self.make_index_buffer(self.block_array_faces_front(block)),
                'faces:back'       : self.make_index_buffer(self.block_array_faces_back(block)),
                'vertices.color'   : self.make_vertex_buffer(self.block_array_vertices_color(block), dynamic=True),
                'edges.color'      : self.make_vertex_buffer(self.block_array_edges_color(block), dynamic=True),
                'faces.color:front': self.make_vertex_buffer(self.block_array_faces_color_front(block), dynamic=True),
                'faces.color:back' : self.make_vertex_buffer(self.block_array_faces_color_back(block), dynamic=True),
                'n'                : len(self.block_array_xyz(block)),
                'v'                : len(self.block_array_vertices(block)),
                'e'                : len(self.block_array_edges(block)),
                'f'                : len(self.block_array_faces_front(block)),
            })
        for interface in self.interfaces:
            # combine all interface vertices in a single
            self.buffers["interfaces"].append({
                'xyz'                   : self.make_vertex_buffer(self.interface_array_xyz(interface)),
                'interfaces:front'      : self.make_index_buffer(self.interface_array_faces_front(interface)),
                'interfaces:back'       : self.make_index_buffer(self.interface_array_faces_back(interface)),
                'interfaces.color:front': self.make_vertex_buffer(self.interface_array_faces_color_front(interface), dynamic=True),
                'interfaces.color:back' : self.make_vertex_buffer(self.interface_array_faces_color_back(interface), dynamic=True),
                'f'                     : len(self.interface_array_faces_front(interface)),
            })

    def draw_buffers(self):
        if not self.buffers:
            return

        glEnableClientState(GL_VERTEX_ARRAY)
        glEnableClientState(GL_COLOR_ARRAY)

        for b in self.buffers["blocks"]:

            glBindBuffer(GL_ARRAY_BUFFER, b['xyz'])
            glVertexPointer(3, GL_FLOAT, 0, None)

            if self.settings['faces.on']:
                glBindBuffer(GL_ARRAY_BUFFER, b['faces.color:front'])
                glColorPointer(3, GL_FLOAT, 0, None)
                glBindBuffer(GL_ELEMENT_ARRAY_BUFFER, b['faces:front'])
                glDrawElements(GL_TRIANGLES, b['f'], GL_UNSIGNED_INT, None)

                glBindBuffer(GL_ARRAY_BUFFER, b['faces.color:back'])
                glColorPointer(3, GL_FLOAT, 0, None)
                glBindBuffer(GL_ELEMENT_ARRAY_BUFFER, b['faces:back'])
                glDrawElements(GL_TRIANGLES, b['f'], GL_UNSIGNED_INT, None)

            if self.settings['edges.on']:
                glLineWidth(self.settings['edges.width:value'])
                glBindBuffer(GL_ARRAY_BUFFER, b['edges.color'])
                glColorPointer(3, GL_FLOAT, 0, None)
                glBindBuffer(GL_ELEMENT_ARRAY_BUFFER, b['edges'])
                glDrawElements(GL_LINES, b['e'], GL_UNSIGNED_INT, None)

            if self.settings['vertices.on']:
                glPointSize(self.settings['vertices.size:value'])
                glBindBuffer(GL_ARRAY_BUFFER, b['vertices.color'])
                glColorPointer(3, GL_FLOAT, 0, None)
                glBindBuffer(GL_ELEMENT_ARRAY_BUFFER, b['vertices'])
                glDrawElements(GL_POINTS, b['v'], GL_UNSIGNED_INT, None)

        for b in self.buffers["interfaces"]:

            glBindBuffer(GL_ARRAY_BUFFER, b['xyz'])
            glVertexPointer(3, GL_FLOAT, 0, None)

            if self.settings['interfaces.on']:
                glBindBuffer(GL_ARRAY_BUFFER, b['interfaces.color:front'])
                glColorPointer(3, GL_FLOAT, 0, None)
                glBindBuffer(GL_ELEMENT_ARRAY_BUFFER, b['interfaces:front'])
                glDrawElements(GL_TRIANGLES, b['f'], GL_UNSIGNED_INT, None)

                glBindBuffer(GL_ARRAY_BUFFER, b['interfaces.color:back'])
                glColorPointer(3, GL_FLOAT, 0, None)
                glBindBuffer(GL_ELEMENT_ARRAY_BUFFER, b['interfaces:back'])
                glDrawElements(GL_TRIANGLES, b['f'], GL_UNSIGNED_INT, None)

        for b in self.buffers['forces']:

            glBindBuffer(GL_ARRAY_BUFFER, b['xyz'])
            glVertexPointer(3, GL_FLOAT, 0, None)

            glLineWidth(self.settings['forces.width:value'])
            glBindBuffer(GL_ARRAY_BUFFER, b['forces.color'])
            glColorPointer(3, GL_FLOAT, 0, None)
            glBindBuffer(GL_ELEMENT_ARRAY_BUFFER, b['forces'])
            glDrawElements(GL_LINES, b['f'], GL_UNSIGNED_INT, None)

        glDisableClientState(GL_COLOR_ARRAY)
        glDisableClientState(GL_VERTEX_ARRAY)


# ==============================================================================
# Main
# ==============================================================================

if __name__ == '__main__':

    pass
