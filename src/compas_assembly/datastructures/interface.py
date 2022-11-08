from __future__ import print_function
from __future__ import absolute_import
from __future__ import division

from compas.data import Data
from compas.geometry import Point
from compas.geometry import Line
from compas.geometry import Polygon
from compas.geometry import centroid_points_weighted


class Interface(Data):
    """
    A data structure for representing interfaces between blocks
    and managing their geometrical and structural properties.

    Parameters
    ----------
    type
    size
    points
    frame
    forces
    mesh
    viewmesh
    interaction

    Attributes
    ----------
    polygon
    contactforces
    compressionforces
    tensionforces
    frictionforces
    resultantforce

    """

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

    @property
    def polygon(self):
        return Polygon(self.points)

    @property
    def contactforces(self):
        lines = []
        if not self.forces:
            return lines
        frame = self.frame
        w = frame.zaxis
        for point, force in zip(self.points, self.forces):
            point = Point(*point)
            force = force["c_np"] - force["c_nn"]
            p1 = point + w * force * 0.5
            p2 = point - w * force * 0.5
            lines.append(Line(p1, p2))
        return lines

    @property
    def compressionforces(self):
        lines = []
        if not self.forces:
            return lines
        frame = self.frame
        w = frame.zaxis
        for point, force in zip(self.points, self.forces):
            point = Point(*point)
            force = force["c_np"] - force["c_nn"]
            if force > 0:
                p1 = point + w * force * 0.5
                p2 = point - w * force * 0.5
                lines.append(Line(p1, p2))
        return lines

    @property
    def tensionforces(self):
        lines = []
        if not self.forces:
            return lines
        frame = self.frame
        w = frame.zaxis
        for point, force in zip(self.points, self.forces):
            point = Point(*point)
            force = force["c_np"] - force["c_nn"]
            if force < 0:
                p1 = point + w * force * 0.5
                p2 = point - w * force * 0.5
                lines.append(Line(p1, p2))
        return lines

    @property
    def frictionforces(self):
        lines = []
        if not self.forces:
            return lines
        frame = self.frame
        u, v = frame.xaxis, frame.yaxis
        for point, force in zip(self.points, self.forces):
            point = Point(*point)
            ft_uv = (u * force["c_u"] + v * force["c_v"]) * 0.5
            p1 = point + ft_uv
            p2 = point - ft_uv
            lines.append(Line(p1, p2))
        return lines

    @property
    def resultantforce(self):
        if not self.forces:
            return []
        frame = self.frame
        w, u, v = frame.zaxis, frame.xaxis, frame.yaxis
        normalcomponents = [f["c_np"] - f["c_nn"] for f in self.forces]
        sum_n = sum(normalcomponents)
        sum_u = sum(f["c_u"] for f in self.forces)
        sum_v = sum(f["c_v"] for f in self.forces)
        position = Point(*centroid_points_weighted(self.points, normalcomponents))
        forcevector = (w * sum_n + u * sum_u + v * sum_v) * 0.5
        p1 = position + forcevector
        p2 = position - forcevector
        return [Line(p1, p2)]
