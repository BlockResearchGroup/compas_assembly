"""
********************************************************************************
compas_assembly.plotter
********************************************************************************

.. currentmodule:: compas_assembly.plotter

This package defines various classes and functions for working with assemblies
in Rhino.


Classes
=======

.. autosummary::
    :toctree: generated/
    :nosignatures:

    AssemblyPlotter

"""
from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

from .plotter import *  # noqa: F401 F403

__all__ = [name for name in dir() if not name.startswith('_')]
