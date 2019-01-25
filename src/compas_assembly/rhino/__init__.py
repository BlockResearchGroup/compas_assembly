"""
********************************************************************************
compas_assembly.rhino
********************************************************************************

.. currentmodule:: compas_assembly.rhino

This package defines various classes and functions for working with assemblies
in Rhino.


Classes
=======

.. autosummary::
    :toctree: generated/
    :nosignatures:

    AssemblyArtist
    AssemblyHelper
    BlockArtist
    BlockHelper

"""
from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

from .helpers import *
from .artists import *


__all__ = [name for name in dir() if not name.startswith('_')]
