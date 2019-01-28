from __future__ import print_function
from __future__ import absolute_import
from __future__ import division

from ast import literal_eval

import compas

try:
    import clr
    clr.AddReference('Rhino.UI')
    import Rhino.UI

except ImportError:
    compas.raise_if_ironpython()

from compas_rhino.selectors import VertexSelector
from compas_rhino.selectors import EdgeSelector
from compas_rhino.selectors import FaceSelector
from compas_rhino.modifiers import VertexModifier
from compas_rhino.modifiers import EdgeModifier
from compas_rhino.modifiers import FaceModifier

from compas_rhino.etoforms import PropertyListForm


__all__ = ['AssemblyHelper', 'BlockHelper']


class AssemblyHelper(VertexSelector,
                     EdgeSelector,
                     VertexModifier,
                     EdgeModifier):

    @staticmethod
    def update_vertex_attributes(assembly, keys, names=None):
        if not names:
            names = assembly.default_vertex_attributes.keys()
        names = sorted(names)
        values = [assembly.vertex[keys[0]][name] for name in names]
        if len(keys) > 1:
            for i, name in enumerate(names):
                for key in keys[1:]:
                    if values[i] != assembly.vertex[key][name]:
                        values[i] = '-'
                        break

        values = map(str, values)

        dialog = PropertyListForm(names, values)
        if dialog.ShowModal(Rhino.UI.RhinoEtoApp.MainWindow):
            values = dialog.values
        else:
            values = None

        if values:
            for name, value in zip(names, values):
                if value != '-':
                    for key in keys:
                        try:
                            value = literal_eval(value)
                        except (SyntaxError, ValueError, TypeError):
                            pass
                        assembly.set_vertex_attribute(key, name, value)

            return True
        return False

    @staticmethod
    def update_edge_attributes(assembly, keys, names=None):
        if not names:
            names = assembly.default_edge_attributes.keys()
        names = sorted(names)

        key = keys[0]
        values = assembly.get_edge_attributes(key, names)

        if len(keys) > 1:
            for i, name in enumerate(names):
                for key in keys[1:]:
                    if values[i] != assembly.get_edge_attribute(key, name):
                        values[i] = '-'
                        break

        dialog = PropertyListForm(names, values)
        if dialog.ShowModal(Rhino.UI.RhinoEtoApp.MainWindow):
            values = dialog.values
        else:
            values = None

        if values:
            for name, value in zip(names, values):
                if value != '-':
                    for key in keys:
                        try:
                            value = literal_eval(value)
                        except (SyntaxError, ValueError, TypeError):
                            pass
                        assembly.set_edge_attribute(key, name, value)

            return True
        return False

    @staticmethod
    def select_block(assembly):
        key = AssemblyHelper.select_vertex(assembly)
        if key is not None:
            block = assembly.blocks[key]
            return block
        return None


class BlockHelper(VertexSelector,
                  EdgeSelector,
                  FaceSelector,
                  VertexModifier,
                  EdgeModifier,
                  FaceModifier):

    pass


# ==============================================================================
# Debugging
# ==============================================================================

if __name__ == "__main__":
    pass
