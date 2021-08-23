"""
********************************************************************************
compas_assembly.templates
********************************************************************************

.. currentmodule:: compas_assembly.templates

Generate assemblies from templates for well-known typologies.


Classes
=======

.. autosummary::
    :toctree: generated/
    :nosignatures:

    Geometry
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
