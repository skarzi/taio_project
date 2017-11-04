from copy import deepcopy

from .exceptions import VertexDoesNotExist, EdgeDoesNotExist
from .labels_modifier import LabelsModifier


class Vertex:
    def __init__(self, key):
        """ initialize new vertex and name it with given key """
        self.key = key
        self._outgoing_edges = {}

    @property
    def outgoing_edges(self):
        """ return list of outgoing edges """
        return self._outgoing_edges.values()

    def has_edge_to(self, key):
        """ check if this vertex has edge to another vertex with given key """
        return key in self._outgoing_edges

    def add_outgoing_edge(self, to_vertex, **kwargs):
        """ add edge from this vertex to another one with given key """
        edge = DirectedEdge(self.key, to_vertex, **kwargs)
        self._outgoing_edges[to_vertex] = edge

    def __getitem__(self, key):
        """ return edge to vertex named with given key (if it exists) """
        if self.has_edge_to(key):
            return self._outgoing_edges[key]
        else:
            raise EdgeDoesNotExist()

    def __iter__(self):
        """ iterate over outgoing edges yielding vertices """
        for vertex in self._outgoing_edges:
            yield vertex
        raise StopIteration()


class DirectedEdge:
    def __init__(self, from_vertex, to_vertex, **kwargs):
        """ initialize new edge from between two vertices and set it's data """
        self.from_vertex = from_vertex
        self.to_vertex = to_vertex
        self._data = kwargs

    def __getitem__(self, item):
        """ return item from edge data storage """
        return self._data[item]

    def __setitem__(self, key, value):
        """ set item in edge data storage """
        self._data[key] = value

    def __iter__(self):
        """ allow unpacking edge to get vertices it connects """
        yield self.from_vertex
        yield self.to_vertex


class DirectedGraph:
    def __init__(self):
        """ initialize new, empty graph """
        self._vertices = {}

        # storage container
        self.graph = {}

    @property
    def edges(self):
        """ return generator yielding existing edges """
        vertices = self._vertices.values()
        return [edge for vertex in vertices for edge in vertex.outgoing_edges]

    def add_vertex(self, key):
        """ add to graph new vertex named with given key """
        self._vertices[key] = Vertex(key)

    def add_edge(self, from_vertex, to_vertex, **kwargs):
        """ add to graph new edge between two vertices """
        if not self.has_vertex(from_vertex):
            self.add_vertex(from_vertex)

        if not self.has_vertex(to_vertex):
            self.add_vertex(to_vertex)

        self._vertices[from_vertex].add_outgoing_edge(to_vertex, **kwargs)

    def copy(self):
        """ return deep copy of itself """
        return deepcopy(self)

    def has_vertex(self, key):
        """ check if vertex named with given key exists in graph """
        return key in self._vertices

    def has_edge(self, v, u):
        """ check if edge between vertices v and u exists in graph """
        if not self.has_vertex(v) or not self.has_vertex(u):
            raise VertexDoesNotExist()
        v = self._vertices[v]
        return v.has_edge_to(u)

    def __getitem__(self, key):
        """ return vertex named with given key """
        if self.has_vertex(key):
            return self._vertices[key]
        else:
            raise VertexDoesNotExist()

    def __iter__(self):
        """ iterate over vertices in graph """
        for vertex in self._vertices:
            yield vertex
        raise StopIteration()


def create_graph(task, labels_modifier=None):
    labels_modifier = labels_modifier or LabelsModifier(task.info)
    graph = DirectedGraph()
    graph.graph['task_info'] = task.info
    graph.graph['labels_modifier'] = labels_modifier
    graph.graph['source'] = labels_modifier.modify_source(0)
    graph.graph['target'] = labels_modifier.modify_target(
        (1 + task.info.workers_number + task.info.features_number +
         task.info.projects_number),
    )
    # add edges from source to workers
    for i, worker in enumerate(task.workers):
        graph.add_edge(
            graph.graph['source'],
            labels_modifier.modify_worker(i),
            capacity=1,  # or weight=1
        )
    # add edges from workers to features
    for i, worker in enumerate(task.workers):
        for feature_no in range(task.info.features_number):
            if worker[feature_no]:
                graph.add_edge(
                    labels_modifier.modify_worker(i),
                    labels_modifier.modify_feature(feature_no),
                    capacity=1,
                )
    # add edges from features to projects
    for i, project in enumerate(task.projects):
        features_sum = 0
        for feature_no in range(task.info.features_number):
            if project[feature_no] > 0:
                features_sum += project[feature_no]
                graph.add_edge(
                    labels_modifier.modify_feature(feature_no),
                    labels_modifier.modify_project(i),
                    capacity=project[feature_no],
                )
        graph.add_edge(
            labels_modifier.modify_project(i),
            graph.graph['target'],
            capacity=features_sum,
        )
    return graph
