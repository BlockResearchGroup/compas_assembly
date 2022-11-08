from typing import List

import os
from compas.colors import Color
from compas.geometry import Line
from compas.utilities import remap_values
from compas_assembly.datastructures import Interface

from compas_view2.app import App
from compas_view2.app import Controller
from compas_view2.objects import Collection

from qt_material import apply_stylesheet

HERE = os.path.dirname(__file__)
CONFIG = os.path.join(HERE, "config.json")


class DEMController(Controller):
    def show_nodes(self, *args, **kwargs):
        state = args[0]
        self.app.nodes.is_visible = state
        self.app.view.update()

    def show_edges(self, *args, **kwargs):
        state = args[0]
        self.app.edges.is_visible = state
        self.app.view.update()

    def show_interfaces(self, *args, **kwargs):
        state = args[0]
        self.app.interfaces.is_visible = state
        self.app.view.update()

    def show_frictionforces(self, *args, **kwargs):
        state = args[0]
        self.app.friction.is_visible = state
        self.app.view.update()

    def show_normalforces(self, *args, **kwargs):
        state = args[0]
        self.app.compression.is_visible = state
        self.app.tension.is_visible = state
        self.app.view.update()

    def show_resultants(self, *args, **kwargs):
        state = args[0]
        self.app.resultants.is_visible = state
        self.app.view.update()

    def scale_contactforces(self, *args, **kwargs):
        value = args[0]
        if value <= 50:
            values = list(range(1, 51))
            values = remap_values(values, target_min=1, target_max=100)
            scale = values[value - 1] / 100
        else:
            value = value - 50
            values = list(range(0, 50))
            values = remap_values(values, target_min=1, target_max=100)
            scale = values[value - 1]

        if self.app._compression:
            for o, line in zip(self.app.compression._objects, self.app._compression):
                if line.length:
                    o._data.start = line.midpoint - line.vector * 0.5 * scale
                    o._data.end = line.midpoint + line.vector * 0.5 * scale
            self.app.compression.update()

        if self.app._tension:
            for o, line in zip(self.app.tension._objects, self.app._tension):
                if line.length:
                    o._data.start = line.midpoint - line.vector * 0.5 * scale
                    o._data.end = line.midpoint + line.vector * 0.5 * scale
            self.app.tension.update()

        if self.app._friction:
            for o, line in zip(self.app.friction._objects, self.app._friction):
                if line.length:
                    o._data.start = line.midpoint - line.vector * 0.5 * scale
                    o._data.end = line.midpoint + line.vector * 0.5 * scale
            self.app.friction.update()

        if self.app._resultants:
            for o, line in zip(self.app.resultants._objects, self.app._resultants):
                if line.length:
                    o._data.start = line.midpoint - line.vector * 0.5 * scale
                    o._data.end = line.midpoint + line.vector * 0.5 * scale
            self.app.resultants.update()

        self.app.view.update()


class DEMViewer(App):
    """
    Viewer for the interactive visualisation of discrete element models.
    """

    def __init__(self, *args, **kwargs):
        super().__init__(
            *args,
            config=CONFIG,
            controller_class=DEMController,
            enable_sidebar=True,
            **kwargs,
        )
        self.blocks = []
        self.interfaces = []
        self._compression = []
        self._tension = []
        self._friction = []
        self.compression = []
        self.tension = []
        self.friction = []

        extra = {"density_scale": "-1"}
        apply_stylesheet(self._app, theme="dark_blue.xml", extra=extra)

    def add_assembly(
        self,
        assembly,
        show_faces=True,
        show_lines=True,
        show_points=False,
        show_interfaces=True,
        opacity=0.5,
        linewidth=2,
        color_support=Color.red(),
        color_block=Color.grey(),
    ):
        node_point = {}
        nodes = []
        properties = []
        for node in assembly.graph.nodes():
            block = assembly.graph.node_attribute(node, "block")
            is_support = assembly.graph.node_attribute(node, "is_support")
            color = color_support if is_support else color_block
            point = block.center()
            nodes.append(point)
            node_point[node] = point
            properties.append(
                {
                    "pointcolor": color,
                    "pointsize": 10,
                }
            )
        self.nodes = self.add(Collection(nodes, properties))

        edges = []
        properties = []
        for u, v in assembly.graph.edges():
            a = node_point[u]
            b = node_point[v]
            color = Color.black()
            edges.append(Line(a, b))
            properties.append(
                {
                    "linecolor": color,
                    "linewidth": 3,
                }
            )
        self.edges = self.add(Collection(edges, properties))

        blocks = []
        properties = []
        for node in assembly.graph.nodes():
            block = assembly.graph.node_attribute(node, "block")
            is_support = assembly.graph.node_attribute(node, "is_support")
            color = color_support if is_support else color_block
            blocks.append(block)
            properties.append(
                {
                    "facecolor": color.lightened(50),
                    "linecolor": color,
                    "linewidth": linewidth,
                    "show_faces": show_faces,
                    "show_lines": show_lines,
                    "show_points": show_points,
                }
            )
        self.blocks = self.add(Collection(blocks, properties), opacity=opacity)

        blocks = []
        properties = []
        for node in assembly.graph.nodes():
            block = assembly.graph.node_attribute(node, "block")
            is_support = assembly.graph.node_attribute(node, "is_support")
            color = color_support if is_support else color_block
            blocks.append(block)
            properties.append(
                {
                    "facecolor": color.lightened(50),
                    "linecolor": color,
                    "linewidth": linewidth,
                    "show_faces": show_faces,
                    "show_lines": show_lines,
                    "show_points": show_points,
                }
            )
        self.blocks = self.add(Collection(blocks, properties), opacity=opacity)

        interfaces = []
        properties = []
        for edge in assembly.graph.edges():
            for interface in assembly.graph.edge_attribute(edge, "interfaces"):
                interfaces.append(interface.polygon)
                properties.append(
                    {"is_visible": show_interfaces, "linewidth": linewidth}
                )
        self.interfaces = self.add(Collection(interfaces, properties))

        compression = []
        tension = []
        friction = []
        resultants = []
        for edge in assembly.graph.edges():
            interfaces: List[Interface] = assembly.graph.edge_attribute(
                edge, "interfaces"
            )
            for interface in interfaces:
                compression += interface.compressionforces
                tension += interface.tensionforces
                friction += interface.frictionforces
                resultants += interface.resultantforce

        self._compression = [line.copy() for line in compression]
        self.compression = self.add(
            Collection(compression),
            linewidth=3,
            linecolor=Color.blue(),
        )

        self._tension = [line.copy() for line in tension]
        self.tension = self.add(
            Collection(tension),
            linewidth=3,
            linecolor=Color.red(),
        )

        self._friction = [line.copy() for line in friction]
        self.friction = self.add(
            Collection(friction),
            linewidth=3,
            linecolor=Color.cyan(),
        )

        self._resultants = [line.copy() for line in resultants]
        self.resultants = self.add(
            Collection(resultants),
            linewidth=3,
            linecolor=Color.green(),
        )

    def _add_sidebar_items(self, items, *args, **kwargs):
        for item in items:
            if item["type"] == "radio":
                action = item["action"]
                item["action"] = (
                    action if callable(action) else getattr(self.controller, action)
                )
            elif item["type"] == "checkbox":
                action = item["action"]
                item["action"] = (
                    action if callable(action) else getattr(self.controller, action)
                )
            elif item["type"] == "slider":
                action = item["action"]
                item["action"] = (
                    action if callable(action) else getattr(self.controller, action)
                )
            elif item["type"] == "button":
                action = item["action"]
                item["action"] = (
                    action if callable(action) else getattr(self.controller, action)
                )
        super()._add_sidebar_items(items, *args, **kwargs)
