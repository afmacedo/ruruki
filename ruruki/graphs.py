"""
Graph implementations
"""
from collections import defaultdict
import json
from ruruki import interfaces
from ruruki.entities import Vertex, Edge
from ruruki.entities import EntitySet


class Graph(interfaces.IGraph):
    """
    Graph database.

    .. note::

        See :class:`~.IGraph` for doco.
    """
    def __init__(self):
        self._vconstraints = defaultdict(dict)
        self._econstraints = defaultdict()
        self.vertices = EntitySet()
        self.edges = EntitySet()

    def load(self, file_handler):
        vertex_id_mapping = {}
        data = json.load(file_handler)

        constraints = data.get("constraints", [])
        for constraint_dict in constraints:
            self.add_vertex_constraint(
                constraint_dict["label"],
                constraint_dict["key"],
            )

        vertices = sorted(data.get("vertices", []), key=lambda x: x["id"])
        for vertex_dict in vertices:
            vertex = self.get_or_create_vertex(
                vertex_dict["label"],
                **vertex_dict["properties"]
            )
            vertex_id_mapping[vertex_dict["id"]] = vertex

        edges = sorted(data.get("edges", []), key=lambda x: x["id"])
        for edge_dict in edges:
            head = vertex_id_mapping[edge_dict["head_id"]]
            tail = vertex_id_mapping[edge_dict["tail_id"]]
            self.get_or_create_edge(
                head,
                edge_dict["label"],
                tail,
                **edge_dict["properties"]
            )

    def dump(self, file_handler):
        data = {
            "vertices": [],
            "edges": [],
            "constraints": [],
        }

        for vertex in self.vertices:
            data["vertices"].append(vertex.as_dict())

        for edge in self.edges:
            data["edges"].append(edge.as_dict())

        for label, key in self.get_vertex_constraints():
            data["constraints"].append(
                {
                    "label": label,
                    "key": key
                }
            )

        json.dump(data, file_handler, indent=4, sort_keys=True)

    def add_vertex_constraint(self, label, key):
        self._vconstraints[label][key] = set()

    def get_vertex_constraints(self):
        constraints = []
        for label in self._vconstraints:
            for key in self._vconstraints[label]:
                constraints.append((label, key))
        return constraints

    def bind_to_graph(self, entity):
        entity.graph = self

    def get_or_create_vertex(self, label=None, **kwargs):
        if not label or not kwargs:
            return None

        # first check constraints.
        if label in self._vconstraints:
            for key, collection in self._vconstraints[label].items():
                if key not in kwargs:
                    continue

                for vertex in collection:
                    if vertex.properties[key] == kwargs[key]:
                        return vertex

        # no matches in constraints, so do a EntitySet filter
        vertices = self.vertices.filter(label, **kwargs).all()
        if len(vertices) > 1:
            raise interfaces.MultipleFoundExpectedOne(
                "Multiple vertices found when one expected."
            )
        elif len(vertices) == 1:
            return vertices[0]

        return self.add_vertex(label, **kwargs)

    def get_or_create_edge(self, head, label, tail, **kwargs):
        if isinstance(head, tuple):
            head = self.get_or_create_vertex(head[0], **head[1])

        if isinstance(tail, tuple):
            tail = self.get_or_create_vertex(tail[0], **tail[1])

        # There can only a single edge between head and tail with a
        # particular label. So there is not point filtering for
        # properties.
        indexed_edge = self._econstraints.get((head, label, tail))
        if indexed_edge:
            return indexed_edge
        return self.add_edge(head, label, tail, **kwargs)

    def add_edge(self, head, label, tail, **kwargs):
        if (head, label, tail) in self._econstraints:
            raise interfaces.ConstraintViolation(
                "Duplicate {0!r} edges between head {1!r} and tail {2!r} "
                "is not allowed".format(
                    label,
                    head,
                    tail
                )
            )
        edge = Edge(head, label, tail, **kwargs)
        self._econstraints[(head, label, tail)] = edge
        self.bind_to_graph(edge)
        self.edges.add(edge)
        head.out_edges.add(edge)
        tail.in_edges.add(edge)
        return edge

    def add_vertex(self, label=None, **kwargs):
        vertex = Vertex(label=label, **kwargs)

        if label in self._vconstraints:
            for key in self._vconstraints[label]:
                if key in kwargs:
                    self._vconstraints[label][key].add(vertex)

        self.bind_to_graph(vertex)
        self.vertices.add(vertex)
        return vertex

    def set_property(self, entity, **kwargs):
        if entity not in self:
            raise interfaces.UnknownEntityError(
                "Unknown entity {0!r}".format(entity)
            )

        if isinstance(entity, interfaces.IVertex):
            key_index = self._vconstraints.get(entity.label, {})
            for key, value in kwargs.items():
                if key not in key_index:
                    continue
                for indexed_entity in key_index[key]:
                    if indexed_entity != entity:
                        if indexed_entity.properties[key] == value:
                            raise interfaces.ConstraintViolation(
                                "Constraint violation with {0}".format(
                                    entity
                                )
                            )
            self.vertices.update_index(entity, **kwargs)

        if isinstance(entity, interfaces.IEdge):
            self.edges.update_index(entity, **kwargs)

        entity._update_properties(kwargs)  # pylint: disable=protected-access

    def get_edge(self, id_num):
        return self.edges.get(id_num)

    def get_vertex(self, id_num):
        return self.vertices.get(id_num)

    def get_edges(self, head=None, label=None, tail=None, **kwargs):
        if head is None and tail is None:
            return self.edges.filter(label, **kwargs)

        container = EntitySet()
        for edge in self.edges.filter(label, **kwargs):
            if head and tail is None:
                if edge.head == head:
                    container.add(edge)
            elif tail and head is None:
                if edge.tail == tail:
                    container.add(edge)
            else:
                if edge.head == head and edge.tail == tail:
                    container.add(edge)
        return container

    def get_vertices(self, label=None, **kwargs):
        return self.vertices.filter(label, **kwargs)

    def remove_edge(self, edge):
        edge.head.remove_edge(edge)
        edge.tail.remove_edge(edge)
        self.edges.remove(edge)

    def remove_vertex(self, vertex):
        if len(vertex.get_both_edges()) > 0:
            raise interfaces.VertexBoundByEdges(
                "Vertex {0!r} is still bound to another vertex "
                "by an edge. First remove all the edges on the vertex and "
                "then remove it again.".format(vertex)
            )
        self.vertices.remove(vertex)

    def close(self):  # pragma: no cover
        # Nothing to do for the close at this stage.
        return

    def __contains__(self, entity):
        is_vertex = isinstance(entity, interfaces.IVertex)
        is_edge = isinstance(entity, interfaces.IEdge)

        if not is_vertex and not is_edge:
            raise TypeError(
                "Unsupported entity type {0}".format(type(entity))
            )

        return entity in self.vertices or entity in self.edges
