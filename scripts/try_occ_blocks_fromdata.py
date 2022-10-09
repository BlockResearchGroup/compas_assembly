import os
import compas
from compas.colors import Color
from compas_view2.app import App
from compas_view2.objects import Collection

HERE = os.path.dirname(__file__)
FILE_I = os.path.join(HERE, "armadillo_breps.json")

blocks = compas.json_load(FILE_I)

viewer = App()
viewer.view.show_grid = False

blue = Color.from_hex("#0092d2")
lightblue = blue.lightened(90)

for i, block in enumerate(blocks):
    try:
        viewer.add(
            block.to_tesselation(),
            show_faces=True,
            show_edges=False,
            color=lightblue,
        )
    except Exception as e:
        print(e)
        print(i)

    edges = []
    for edge in block.edges:
        if edge.is_line:
            edges.append(edges.to_line())
        elif edge.is_bspline:
            edges.append(edge.curve.to_polyline())

    viewer.add(Collection(edges), linewidth=3, color=blue)

viewer.show()
