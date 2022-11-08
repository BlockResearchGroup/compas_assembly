"""
********************************************************************************
compas_assembly
********************************************************************************

.. currentmodule:: compas_assembly


.. toctree::
    :maxdepth: 1

    compas_assembly.algorithms
    compas_assembly.artists
    compas_assembly.datastructures
    compas_assembly.geometry
    compas_assembly.rhino
    compas_assembly.viewer

"""
from __future__ import print_function
from __future__ import absolute_import
from __future__ import division

import os

__author__ = ["Tom Van Mele <van.mele@arch.ethz.ch>"]
__copyright__ = "Block Research Group - ETH Zurich"
__license__ = "MIT License"
__email__ = "van.mele@arch.ethz.ch"

__version__ = "0.6.0"


HERE = os.path.dirname(__file__)
HOME = os.path.abspath(os.path.join(HERE, "../../"))
DATA = os.path.abspath(os.path.join(HOME, "data"))
TEMP = os.path.abspath(os.path.join(HERE, "__temp"))
SAMPLES = os.path.abspath(os.path.join(HERE, "data/samples"))


__all__ = ["DATA", "TEMP", "SAMPLES"]
__all_plugins__ = ["compas_assembly.install", "compas_assembly.rhino"]


def get(filename):
    filename = filename.strip("/")
    return os.path.abspath(os.path.join(SAMPLES, filename))
