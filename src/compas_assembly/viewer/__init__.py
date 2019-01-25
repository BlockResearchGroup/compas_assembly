"""
********************************************************************************
compas_assembly.viewer
********************************************************************************

.. currentmodule:: compas_assembly.viewer


.. autosummary::
    :toctree: generated/


"""

from __future__ import print_function
from __future__ import absolute_import
from __future__ import division

from .view import View
from .controller import Controller


CONFIG = {
    'menubar': [
        {
            'type'  : 'menu',
            'text'  : 'View',
            'items' : []
        },
        {
            'type'  : 'menu',
            'text'  : 'Tools',
            'items' : []
        },
        {
            'type'  : 'menu',
            'text'  : 'Window',
            'items' : []
        },
        {
            'type'  : 'menu',
            'text'  : 'Help',
            'items' : []
        }
    ],
    'toolbar': [],
    'sidebar': [
        {
            'type'  : 'group',
            'text'  : None,
            'items' : [
                {
                    'type'  : 'group',
                    'text'  : None,
                    'items' : [
                        {'type' : 'checkbox', 'text' : 'vertices',    'action' : 'toggle_vertices',   'state' : Controller.settings['vertices.on'], },
                        {'type' : 'checkbox', 'text' : 'edges',       'action' : 'toggle_edges',      'state' : Controller.settings['edges.on'], },
                        {'type' : 'checkbox', 'text' : 'faces',       'action' : 'toggle_faces',      'state' : Controller.settings['faces.on'], },
                        {'type' : 'checkbox', 'text' : 'interfaces',  'action' : 'toggle_interfaces', 'state' : Controller.settings['interfaces.on'], },
                    ]
                },
            ]
        },
        {
            'type' : 'group',
            'text' : None,
            'items': [
                {
                    'type' : 'group',
                    'text' : None,
                    'items': [
                        {
                            'type'  : 'colorbutton',
                            'text'  : 'color vertices',
                            'value' : Controller.settings['vertices.color'],
                            'action': 'change_vertices_color',
                        },
                        {
                            'type'  : 'colorbutton',
                            'text'  : 'color edges',
                            'value' : Controller.settings['edges.color'],
                            'action': 'change_edges_color',
                        },
                        {
                            'type'  : 'colorbutton',
                            'text'  : 'color faces (front)',
                            'value' : Controller.settings['faces.color:front'],
                            'action': 'change_faces_color_front',
                        },
                        {
                            'type'  : 'colorbutton',
                            'text'  : 'color faces (back)',
                            'value' : Controller.settings['faces.color:back'],
                            'action': 'change_faces_color_back',
                        },
                    ]
                },
                {
                    'type' : 'group',
                    'text' : None,
                    'items': [
                        {
                            'type'   : 'slider',
                            'text'   : 'size vertices',
                            'value'  : Controller.settings['vertices.size:value'],
                            'minval' : Controller.settings['vertices.size:minval'],
                            'maxval' : Controller.settings['vertices.size:maxval'],
                            'step'   : Controller.settings['vertices.size:step'],
                            'scale'  : Controller.settings['vertices.size:scale'],
                            'slide'  : 'slide_size_vertices',
                            'edit'   : 'edit_size_vertices',
                        },
                        {
                            'type'   : 'slider',
                            'text'   : 'width edges',
                            'value'  : Controller.settings['edges.width:value'],
                            'minval' : Controller.settings['edges.width:minval'],
                            'maxval' : Controller.settings['edges.width:maxval'],
                            'step'   : Controller.settings['edges.width:step'],
                            'scale'  : Controller.settings['edges.width:scale'],
                            'slide'  : 'slide_width_edges',
                            'edit'   : 'edit_width_edges',
                        }
                    ]
                },
                {
                    'type'   : 'stretch',
                }
            ]
        },
    ]
}

STYLE = """
QMainWindow {}

QMenuBar {}

QToolBar#Tools {
padding: 4px;
}

QDockWidget#Sidebar {}

QDockWidget#Console {}

QDockWidget#Console QPlainTextEdit {
background-color: #222222;
color: #eeeeee;
border-top: 8px solid #cccccc;
border-left: 1px solid #cccccc;
border-right: 1px solid #cccccc;
border-bottom: 1px solid #cccccc;
padding-left: 4px;
}
"""

from .app import AssemblyViewer


__all__ = ['AssemblyViewer']

