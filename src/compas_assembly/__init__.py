"""
********************************************************************************
compas_assembly
********************************************************************************

.. currentmodule:: compas_assembly


.. toctree::
    :maxdepth: 1

    compas_assembly.blender
    compas_assembly.datastructures
    compas_assembly.geometry
    compas_assembly.ghpython
    compas_assembly.plotter
    compas_assembly.rhino

"""
from __future__ import print_function
from __future__ import absolute_import
from __future__ import division

import os

__author__ = ['Tom Van Mele <van.mele@arch.ethz.ch>']
__copyright__ = 'Block Research Group - ETH Zurich'
__license__ = 'MIT License'
__email__ = 'van.mele@arch.ethz.ch'

__version__ = '0.4.1'


HERE = os.path.dirname(__file__)
HOME = os.path.abspath(os.path.join(HERE, '../../'))
DATA = os.path.abspath(os.path.join(HOME, 'data'))

TEMP = os.path.abspath(os.path.join(HERE, '__temp'))


__all__ = ['DATA', 'TEMP']


def get(filename):
    filename = filename.strip('/')
    return os.path.abspath(os.path.join(DATA, filename))
