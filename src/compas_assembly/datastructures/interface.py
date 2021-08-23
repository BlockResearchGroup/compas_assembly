from __future__ import print_function
from __future__ import absolute_import
from __future__ import division

import json
from copy import deepcopy
from compas.utilities import DataDecoder
from compas.utilities import DataEncoder
from compas.base import Base


class Interface(Base):
    """"""

    def __init__(self, itype=None, isize=None, ipoints=None, iframe=None, iforces=None):
        super(Interface, self).__init__()
        self.points = ipoints
        self.type = itype
        self.size = isize
        self.frame = iframe
        self.forces = iforces

    @property
    def data(self):
        return {
            'points': self.points,
            'type': self.type,
            'size': self.size,
            'frame': self.frame,
            'forces': self.forces}

    @data.setter
    def data(self, data):
        self.points = data['points']
        self.type = data['type']
        self.size = data['size']
        self.frame = data['frame']
        self.forces = data['forces']

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
            The constructed interface.

        Examples
        --------
        >>>
        """
        return cls(itype=data['type'], isize=data['size'], ipoints=data['points'], iframe=data['frame'], iforces=data['forces'])

    @classmethod
    def from_json(cls, filepath):
        """Construct an interface from structured data contained in a json file.

        Parameters
        ----------
        filepath : str
            The path to the json file.

        Returns
        -------
        object
            An object of the type of ``cls``.

        Notes
        -----
        This constructor method is meant to be used in conjunction with the
        corresponding *to_json* method.
        """
        with open(filepath, 'r') as fp:
            data = json.load(fp, cls=DataDecoder)
        return cls.from_data(data)

    def to_data(self):
        """Returns the data dictionary that represents the interface.

        Returns
        -------
        dict
            The object's data.
        """
        return self.data

    def to_json(self, filepath):
        """Serialise the structured data representing the interface to json.

        Parameters
        ----------
        filepath : str
            The path to the json file.
        """
        with open(filepath, 'w+') as f:
            json.dump(self.data, f, cls=DataEncoder)

    def copy(self):
        """Makes a copy of this interface.

        Returns
        -------
        Primitive
            The copy.
        """
        cls = type(self)
        return cls.from_data(deepcopy(self.data))
