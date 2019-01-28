"""Compute the convex hull of an assembly.

The convex hull is a quick and dirty approximation of a collision mesh.

Note that the function ``assembly_hull_numpy`` can fail when the assembly is much
larger in one direction than in all others.

This is because the function postprocess the obtained hull faces by unifying their
cicle directions to create a consistent, watertight mesh.
The ``unify_cycles`` function uses a nearest neighbors search to speed up the
calculation. However, this will exclude some of the faces from being processed
in the situation described above if the number of neighbors taken into account is
too small.

Note
----
Swith to tree based search only if number of faces exceeds 100?

"""
from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

import compas_assembly

from compas.datastructures import Mesh
from compas.viewers import MeshViewer

from compas_assembly.datastructures import Assembly
from compas_assembly.datastructures import assembly_hull_numpy


assembly = Assembly.from_json(compas_assembly.get('assembly.json'))

vertices, faces = assembly_hull_numpy(assembly)

hull = Mesh.from_vertices_and_faces(vertices, faces)

viewer = MeshViewer()
viewer.mesh = hull
viewer.show()
