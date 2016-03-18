from ruruki.graphs import EntitySet


class ResultSet(object):
    def __init__(self):
        self.vertices = EntitySet()
        self.edges = EntitySet()


def _filter(graph, query):
    if isinstance(query, ResultSet):
        return query

    result = ResultSet()

    result.edges = graph.get_edges(**query)
    result.vertices = graph.get_vertices(**query)

    return result


def _heads(graph, rs):
    result = ResultSet()

    for edge in rs.edges:
        result.vertices.add(edge.head)

    return result


def _tails(graph, rs):
    result = ResultSet()

    for edge in rs.edges:
        result.vertices.add(edge.tail)

    return result


def _out_edges(graph, rs):
    result = ResultSet()

    for vertex in rs.vertices:
        for edge in vertex.out_edges:
            result.edges.add(edge)

    return result


def _in_edges(graph, rs):
    result = ResultSet()

    for vertex in rs.vertices:
        for edge in vertex.in_edges:
            result.edges.add(edge)

    return result


def _and(graph, items):
    if len(items) < 1:
        return items

    rs = items[0]

    for part in items[1:]:
        rs.vertices = rs.vertices & part.vertices
        rs.edges = rs.edges & part.edges

    return rs


def _or(graph, items):
    if len(items) < 1:
        return items

    rs = items[0]

    for part in items[1:]:
        rs.vertices = rs.vertices | part.vertices
        rs.edges = rs.edges | part.edges

    return rs


def find(graph, query):
    for key, value in query.iteritems():
        if key not in query_functions.keys():
            return _filter(graph, query)

        pvalue = value

        if isinstance(value, list):
            pvalue = []
            for sub in value:
                pvalue.append(find(graph, sub))

        elif not isinstance(value, ResultSet):
            pvalue = find(graph, value)

        return query_functions[key](graph, pvalue)


query_functions = {
    '$filter': _filter,
    '$heads': _heads,
    '$tails': _tails,
    '$out_edges': _out_edges,
    '$in_edges': _in_edges,
    '$and': _and,
    '$or': _or,
}
