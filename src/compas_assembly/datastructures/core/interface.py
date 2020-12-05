from __future__ import print_function
from __future__ import absolute_import
from __future__ import division

from compas.base import Base


__all__ = ['Interface']


class Interface(Base):
    """"""

    def __init__(self):
        super(Interface, self).__init__()
        self.points = None
        self.type = None
        self.size = None
        self.frame = None
        self.forces = None


# ==============================================================================
# Main
# ==============================================================================

if __name__ == '__main__':
    pass
