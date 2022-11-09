import compas_rhino

from compas.geometry import Vector
from compas.geometry import Polygon
from compas.colors import Color
from compas.artists import Artist
from compas_rhino.artists import RhinoArtist
from compas_assembly.artists import AssemblyArtist


class RhinoAssemblyArtist(RhinoArtist, AssemblyArtist):
    def __init__(self, assembly, layer=None, **kwargs):
        super(RhinoAssemblyArtist, self).__init__(
            assembly=assembly, layer=layer, **kwargs
        )

    def draw_nodes(self, nodes=None, color=None, text=None):
        """Draw a selection of nodes.

        Parameters
        ----------
        nodes : list[hashable], optional
            A list of nodes to draw.
            Default is None, in which case all nodes are drawn.
        color : :class:`~compas.colors.Color` | dict[hashable, :class:`~compas.colors.Color`], optional
            Color of the nodes.
            The default color is :attr:`AssemblyArtist.default_nodecolor`.
        text : str | dict[hashable, str], optional
            Text labels for the nodes.

        Returns
        -------
        list[System.Guid]
            The GUIDs of the created Rhino objects.

        """
        layer = "{}::Nodes".format(self.layer or self.assembly.name)
        self.node_color = color
        self.node_text = text
        nodes = nodes or self.nodes
        points = []
        for node in nodes:
            pos = self.node_xyz[node]
            color = self.node_color[node].rgb255
            points.append(
                {
                    "pos": list(pos),
                    "name": "{}.node.{}".format(self.assembly.name, node),
                    "color": color,
                    "text": self.node_text[node],
                }
            )
        guids = compas_rhino.draw_points(points, layer=layer, clear=False, redraw=False)
        if text:
            guids += compas_rhino.draw_labels(
                points, layer=layer, clear=False, redraw=False
            )
        return guids

    def draw_edges(self, edges=None, color=None, text=None):
        """Draw a selection of edges.

        Parameters
        ----------
        edges : list[tuple[hashable, hashable]], optional
            A list of edges to draw.
            The default is None, in which case all edges are drawn.
        color : :class:`~compas.colors.Color` | dict[tuple[hashable, hashable], :class:`~compas.colors.Color`], optional
            Color of the edges.
            The default color is :attr:`AssemblyArtist.default_edgecolor`.
        text : str | dict[hashable, str], optional
            Text labels for the edges.

        Returns
        -------
        list[System.Guid]
            The GUIDs of the created Rhino objects.

        """
        layer = "{}::Edges".format(self.layer or self.assembly.name)
        self.edge_color = color
        self.edge_text = text
        edges = edges or self.edges
        lines = []
        for edge in edges:
            u, v = edge
            a = self.node_xyz[u]
            b = self.node_xyz[v]
            color = self.edge_color[edge].rgb255
            name = "{}.edge.{}-{}".format(self.assembly.name, u, v)
            lines.append(
                {
                    "start": list(a),
                    "end": list(b),
                    "color": color,
                    "name": name,
                }
            )
        guids = compas_rhino.draw_lines(lines, layer=layer, clear=False, redraw=False)
        if text:
            pass
        return guids

    def draw_blocks(
        self,
        color=None,
        show_faces=True,
        show_edges=False,
        show_vertices=False,
    ):
        """Draw the blocks of the assembly.

        Parameters
        ----------
        color : :class:`~compas.colors.Color` | dict[hashable, :class:`~compas.colors.Color`], optional
            Color of the blocks.
            The default color is :attr:`AssemblyArtist.default_nodecolor`.
        show_faces : bool, optional
            If True, draw the faces of the blocks.
        show_edges : bool, optional
            If True, draw the edges of the blocks.
        show_vertices : bool, optional
            If True, draw the vertices of the blocks.

        Returns
        -------
        list[System.Guid]

        """
        layer = "{}::Blocks".format(self.layer or self.assembly.name)
        self.node_color = color
        guids = []
        for node in self.nodes:
            block = self.assembly.node_block(node)
            artist = Artist(block)
            artist.layer = layer
            color = self.node_color[node].rgb255
            if show_faces:
                guids += artist.draw_faces(color=color, join_faces=True)
            if show_edges:
                guids += artist.draw_edges(color=color)
            if show_vertices:
                guids += artist.draw_vertices(color=color)
        return guids

    def draw_interfaces(self, color=None, show_frames=False):
        """Draw the interfaces of the assembly.

        Parameters
        ----------
        color : :class:`~compas.colors.Color` | dict[hashable, :class:`~compas.colors.Color`], optional
            Color of the interfaces.
            The default color is :attr:`AssemblyArtist.default_edgecolor`.
        show_frames : bool, optional
            If True, draw the local interface frames.

        Returns
        -------
        list[System.Guid]

        """
        layer = "{}::Interfaces".format(self.layer or self.assembly.name)
        self.edge_color = color
        guids = []
        for edge in self.edges:
            interfaces = self.assembly.edge_interfaces(edge)
            for interface in interfaces:
                artist = Artist(Polygon(interface.points))
                artist.layer = layer
                color = self.edge_color[edge].rgb255
                guids += artist.draw(color=color)
                if show_frames:
                    artist = Artist(interface.frame, scale=0.1)
                    artist.layer = layer
                    guids += artist.draw()
        return guids

    def draw_selfweight(self, color=None, scale=1.0, tol=1e-3):
        """Draw the vectors representing the selfweight of the blocks of the assembly.

        Parameters
        ----------
        scale : float, optional
            Scale factor for the length of the vectors.
        tol : float, optional
            Minimum length requirement for displaying vectors.

        Returns
        -------
        list[Sysyem.Guid]

        """
        layer = "{}::Selfweight".format(self.layer or self.assembly.name)
        guids = []
        color = color or self.default_selfweightcolor
        color = color.rgb255
        for node in self.nodes:
            block = self.assembly.node_block(node)
            volume = block.volume()
            if volume * scale < tol:
                continue
            point = block.centroid()
            vector = Vector(0, 0, -volume * scale)
            artist = Artist(vector)
            artist.layer = layer
            guids += artist.draw(color=color, point=point)
        return guids

    def draw_forces(self, scale=1.0, tol=1e-3):
        """Draw the contact (normal) forces at the interfaces between the blocks of the assembly.

        Parameters
        ----------
        scale : float, optional
            Scale factor for the length of the vectors.
        tol : float, optional
            Minimum length requirement for displaying vectors.

        Returns
        -------
        list[System.Guid]

        """
        layer = "{}::Forces".format(self.layer or self.assembly.name)
        guids = []
        tension = Color.red().rgb255
        compression = Color.blue().rgb255
        friction = Color.cyan().rgb255
        for edge in self.edges:
            interfaces = self.assembly.edge_interfaces(edge)
            for interface in interfaces:
                for force in interface.compressionforces:
                    vector = force.vector * scale
                    if vector.length > tol:
                        artist = Artist(vector)
                        artist.layer = layer
                        guids += artist.draw(color=compression, point=force.start)
                for force in interface.tensionforces:
                    vector = force.vector * scale
                    if vector.length > tol:
                        artist = Artist(vector)
                        artist.layer = layer
                        guids += artist.draw(color=tension, point=force.start)
                for force in interface.frictionforces:
                    vector = force.vector * scale
                    if vector.length > tol:
                        artist = Artist(vector)
                        artist.layer = layer
                        guids += artist.draw(color=friction, point=force.start)
        return guids

    def draw_resultants(self, scale=1.0, tol=1e-3):
        guids = []
        return guids

    def draw_reactions(self, scale=1.0, tol=1e-3):
        guids = []
        return guids
