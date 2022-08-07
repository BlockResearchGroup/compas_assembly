from __future__ import print_function
from __future__ import absolute_import
from __future__ import division

from compas.data import Data


class Interface(Data):
    def __init__(
        self,
        type=None,
        size=None,
        points=None,
        frame=None,
        forces=None,
        mesh=None,
        viewmesh=None,
        interaction=None,
    ):
        super(Interface, self).__init__()
        self.points = points
        self.type = type
        self.size = size
        self.frame = frame
        self.forces = forces
        self.mesh = mesh
        self.viewmesh = viewmesh
        self.interaction = interaction

    @property
    def data(self):
        return {
            "points": self.points,
            "type": self.type,
            "size": self.size,
            "frame": self.frame,
            "forces": self.forces,
            "mesh": self.mesh,
            "viewmesh": self.viewmesh,
            "interaction": self.interaction,
        }

    @data.setter
    def data(self, data):
        self.points = data["points"]
        self.type = data["type"]
        self.size = data["size"]
        self.frame = data["frame"]
        self.forces = data["forces"]
        self.mesh = data["mesh"]
        self.viewmesh = data["viewmesh"]
        self.interaction = data["interaction"]

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
        return cls(**data)
