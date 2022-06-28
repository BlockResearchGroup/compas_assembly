from __future__ import print_function
from __future__ import absolute_import
from __future__ import division

from compas.data import Data


class Interface(Data):
    def __init__(
        self, type=None, size=None, points=None, frame=None, forces=None, viewmesh=None
    ):
        super(Interface, self).__init__()
        self.points = points
        self.type = type
        self.size = size
        self.frame = frame
        self.forces = forces
        self.viewmesh = viewmesh

    @property
    def data(self):
        return {
            "points": self.points,
            "type": self.type,
            "size": self.size,
            "frame": self.frame,
            "forces": self.forces,
            "viewmesh": self.viewmesh,
        }

    @data.setter
    def data(self, data):
        self.points = data["points"]
        self.type = data["type"]
        self.size = data["size"]
        self.frame = data["frame"]
        self.forces = data["forces"]
        self.viewmesh = data["viewmesh"]

    @classmethod
    def from_data(cls, data):
        """Construct an interface from a data dict.

        Parameters
        ----------
        data : dict
            The data dictionary.

        Returns
        -------
        :class:`compas_assembly.datastructures.Interface`

        """
        return cls(
            type=data["type"],
            size=data["size"],
            points=data["points"],
            frame=data["frame"],
            forces=data["forces"],
            viewmesh=data["viewmesh"],
        )
