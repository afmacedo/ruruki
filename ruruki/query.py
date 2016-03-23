import time

from ruruki.graphs import EntitySet

from ruruki.interfaces import IVertex
from ruruki.interfaces import IEdge


class QuerySyntaxError(object):
    def __init__(self, partial_query):
        super(QuerySyntaxError, self).__init__(
            'Invalid query synxtax near: {0}'.format(partial_query)
        )


class ResultSet(object):
    def __init__(self):
        self.vertices = EntitySet()
        self.edges = EntitySet()


def _filter(graph, query):
    if isinstance(query, ResultSet):
        return query

    result = ResultSet()

    result.edges = graph.get_edges(**query) if query else graph.get_edges()
    result.vertices = graph.get_vertices(**query) if query else graph.get_vertices()

    return result


def _edges(graph, query):
    if isinstance(query, ResultSet):
        return query

    result = ResultSet()

    result.edges = graph.get_edges(**query)

    return result


def _vertices(graph, query):
    if isinstance(query, ResultSet):
        return query

    result = ResultSet()

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


def _in_edges(graph, query):
    result = ResultSet()

    for vertex in rs.vertices:
        for edge in vertex.in_edges:
            result.edges.add(edge)

    return result


def _and(graph, items):
    if len(items) < 1:
        return ResultSet()

    rs = items[0]

    for part in items[1:]:
        rs.vertices = rs.vertices & part.vertices
        rs.edges = rs.edges & part.edges

    return rs


def _or(graph, items):
    if len(items) < 1:
        return ResultSet()

    rs = items[0]

    for part in items[1:]:
        rs.vertices = rs.vertices | part.vertices
        rs.edges = rs.edges | part.edges

    return rs


def _return(graph, items):
    if len(items) < 1:
        return ResultSet()

    for part in items:
        print 'PART: %s' % part

    return rs


def find(graph, query, rvars={}):
#    if isinstance(query, list):
#        for part in query:
#            return find(graph, part, rvars)

    for rawkey, value in query.iteritems():
        keyvar = rawkey.split('|')
        key = keyvar[0]
        varname = ''.join(keyvar[1:]) if len(keyvar) > 1 else None

        if key not in query_functions.keys():
            return _filter(graph, query)

        pvalue = value

        if isinstance(value, list):
            pvalue = []
            for sub in value:
                pvalue.append(find(graph, sub, rvars))

        elif isinstance(value, str) or isinstance(value, unicode):
            # throw for non-existing variable
            if not value in rvars:
                print 'KABOOM!'
            return rvars[value]

        elif not isinstance(value, ResultSet):
            pvalue = find(graph, value, rvars)

        result = query_functions[key](graph, pvalue)

        if varname:
            rvars[varname] = result

        return result


query_functions = {
    '$filter': _filter,
    '$edges': _edges,
    '$vertices': _vertices,
    '$heads': _heads,
    '$tails': _tails,
    '$out_edges': _out_edges,
    '$in_edges': _in_edges,
    '$and': _and,
    '$or': _or,
    '$return': _return,
}
