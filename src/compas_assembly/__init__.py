"""
********************************************************************************
compas_assembly
********************************************************************************

.. currentmodule:: compas_assembly


.. toctree::
    :maxdepth: 1

    compas_assembly.datastructures
    compas_assembly.interfaces
    compas_assembly.rhino
    compas_assembly.utilities


"""

from __future__ import print_function

import os


__author__    = ["Tom Van Mele <van.mele@arch.ethz.ch>"]
__copyright__ = "Block Research Group - ETH Zurich"
__license__   = "MIT License"
__email__     = "van.mele@arch.ethz.ch"

__version__ = "0.1.0"


HERE = os.path.dirname(__file__)
HOME = os.path.abspath(os.path.join(HERE, '../../'))
DATA = os.path.abspath(os.path.join(HOME, 'data'))
TEMP = os.path.abspath(os.path.join(HOME, 'temp'))


__all__ = ['DATA', 'TEMP']
