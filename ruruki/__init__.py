"""
Helpers and convenience functions for quering all the graph plugins and
for creating graph instances based on a particular graph plugin.
"""
from pkg_resources import (  # pylint: disable=no-name-in-module
    iter_entry_points,
    load_entry_point,
)

# id tracking
_EID = 0
_VID = 0


def generate_edge_id():
    """
    Generate a edge id.

    :returns: Edge id number.
    :rtype: :class:`int`
    """
    global _EID  # pylint: disable=global-statement
    ident = _EID
    _EID += 1
    return ident


def generate_vertex_id():
    """
    Generate a vertex id.

    :returns: Vertex id number.
    :rtype: :class:`int`
    """
    global _VID  # pylint: disable=global-statement
    ident = _VID
    _VID += 1
    return ident


def get_graph_plugins():
    """
    Return all the registered graph plugins available.

    :returns: All the names of the registered and available graph
        plugins.
    :rtype: Iterable of :class:`str`
    """
    return [
        each.name
        for each in iter_entry_points("ruruki.graphs")
    ]


def create_graph(graph_plugin="graph", data=None):
    """
    Create a graph based on the graph_plugin name.

    :param graph_plugin: Name of the graph plugin entry point used when
        creating the database.
    :type graph_plugin: :class:`str`
    :param data: If provided, the graph will be populated with data read
        from this file (as with graph.load()).
        Otherwise, the graph will be empty.
    :type data: :class:`file`
    :returns: A new graph instance using the implementation named in
        graph_plugin
    :rtype: :class:`~.interfaces.IGraph`
    """
    graph = load_entry_point("ruruki", "ruruki.graphs", graph_plugin)()

    if data:
        graph.load(data)

    return graph
