from compas_blender.artists import MeshArtist


__all__ = ['BlockArtist']


class BlockArtist(MeshArtist):
    """An artist for painting blocks."""

    def __init__(self, block):
        super().__init__(block)

    @property
    def block(self):
        return self.mesh

    @block.setter
    def block(self, block):
        self.mesh = block
