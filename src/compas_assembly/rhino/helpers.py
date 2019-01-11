from __future__ import print_function
from __future__ import absolute_import
from __future__ import division

import compas_rhino

from compas_rhino.selectors import VertexSelector
from compas_rhino.selectors import EdgeSelector
from compas_rhino.selectors import FaceSelector
from compas_rhino.modifiers import VertexModifier
from compas_rhino.modifiers import EdgeModifier
from compas_rhino.modifiers import FaceModifier


__all__ = ['AssemblyHelper', 'BlockHelper']


class AssemblyHelper(VertexSelector,
                     EdgeSelector,
                     VertexModifier,
                     EdgeModifier):
    """Helper class for selecting and modifying vertices and edges of an Assembly
    through the Rhino interface."""
    pass


class BlockHelper(VertexSelector,
                  EdgeSelector,
                  FaceSelector,
                  VertexModifier,
                  EdgeModifier,
                  FaceModifier):
    """Helper class for selecting and modifying vertices, edges, and faces of an
    assembly Block through the Rhino interface."""
    pass


# ==============================================================================
# Debugging
# ==============================================================================

if __name__ == "__main__":
    pass
