from __future__ import print_function
from __future__ import absolute_import
from __future__ import division

import os

__author__ = ["Tom Van Mele"]
__copyright__ = "ETH Zurich - Block Research Group"
__license__ = "MIT License"
__email__ = "tom.v.mele@gmail.com"
__version__ = "0.7.0"


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
