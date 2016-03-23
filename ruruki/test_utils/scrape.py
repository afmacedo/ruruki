#pylint: skip-file

import logging
import inspect
import ruruki

from ruruki.graphs import Graph


GRAPH = Graph()
GRAPH.add_vertex_constraint("class", "name")
GRAPH.add_vertex_constraint("method", "name")
GRAPH.add_vertex_constraint("file", "name")
GRAPH.add_vertex_constraint("function", "name")
GRAPH.add_vertex_constraint("module", "name")


SEEN = set()

def build_dep(lib, parent):
    previous = parent

    for name, module in inspect.getmembers(lib, inspect.ismodule):
        if module in SEEN:
            continue
        SEEN.add(module)
        parent = GRAPH.get_or_create_vertex("module", name=name)

        # link to the previous parent
        GRAPH.get_or_create_edge(parent, "comes-form", previous)

        try:
            filename = inspect.getfile(module)
            if filename:
                parent_file = GRAPH.get_or_create_vertex("file", name=filename)
                GRAPH.get_or_create_edge(parent, "found-in", parent_file)
        except TypeError:
            logging.warn("Failed to get the file for %s", name)


        # get all the functions in the module
        for fname, func in inspect.getmembers(module, inspect.isfunction):
            fnode = GRAPH.get_or_create_vertex("function", name=fname)
            GRAPH.get_or_create_edge(parent, "has-function", fnode)

        # get all the classes in the module
        for cname, cls in inspect.getmembers(module, inspect.isclass):
            cnode = GRAPH.get_or_create_vertex("class", name=cname)
            GRAPH.get_or_create_edge(parent, "has-class", cnode)

            # get all the class methods in the class
            for mname, meth in inspect.getmembers(cls, inspect.ismethod):
                mnode = GRAPH.get_or_create_vertex("method", name=mname)
                GRAPH.get_or_create_edge(cnode, "has-method", mnode)

        build_dep(module, parent)


def scrape():
    build_dep(ruruki, GRAPH.get_or_create_vertex("package", name="ruruki"))
    return GRAPH


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)

    from ruruki_eye.server import run

    scrape()
    run("0.0.0.0", 8000, False, GRAPH)
