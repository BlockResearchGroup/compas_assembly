"""Visualise an assembly.

1. Load an assembly from a JSON file.
2. Visualise with the viewer.

"""
import compas_assembly

from compas_assembly.datastructures import Assembly
from compas_assembly.viewer import AssemblyViewer

assembly = Assembly.from_json(compas_assembly.get('assembly.json'))

viewer = AssemblyViewer()
viewer.assembly = assembly
viewer.show()
