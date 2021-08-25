"""
********************************************************************************
compas_assembly.geometry
********************************************************************************

.. currentmodule:: compas_assembly.geometry

Generate assemblies from geometry for well-known typologies.


Base Classes
============

.. autosummary::
    :toctree: generated/
    :nosignatures:

    Geometry


Classes
=======

.. autosummary::
    :toctree: generated/
    :nosignatures:

    Arch
    Dome
    Wall

"""
from __future__ import print_function
from __future__ import absolute_import
from __future__ import division

from ._geometry import Geometry  # noqa: F401

from .arch import Arch  # noqa: F401
from .dome import Dome  # noqa: F401
from .wall import Wall  # noqa: F401

__all__ = [
    'Geometry',
    'Arch',
    'Dome',
    'Wall'
]
