from __future__ import print_function
from __future__ import absolute_import
from __future__ import division

import compas_rhino
from compas_rhino.artists import MeshArtist


__all__ = ['BlockArtist']


class BlockArtist(MeshArtist):
    """An artist for painting blocks."""

    def __init__(self, *args, **kwargs):
        super(BlockArtist, self).__init__(*args, **kwargs)
        self.settings.update({
            'color.vertex': (0, 0, 0),
            'color.edge': (0, 0, 0),
            'color.face': (255, 255, 255),
        })

    @property
    def block(self):
        return self.mesh

    @block.setter
    def block(self, block):
        self.mesh = block


# ==============================================================================
# Debugging
# ==============================================================================

if __name__ == "__main__":
    pass
