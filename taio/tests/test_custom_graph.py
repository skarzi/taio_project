import pytest

from taio.graph.custom_graph import Vertex, DirectedEdge, DirectedGraph
from taio.graph.exceptions import EdgeDoesNotExist, VertexDoesNotExist


def get_sample_vertices(n):
    return [Vertex(i) for i in range(n)]


def get_sample_graph(n=0):
    g = DirectedGraph()
    for i in range(n):
        g.add_vertex(i)
    return g


class TestVertex:
    @pytest.mark.parametrize('key', [1, 'a', (True, False)])
    def test_creating_vertex_with_different_keys(self, key):
        vertex = Vertex(key)
        assert vertex.key == key

    def test_adding_edges(self):
        v1, v2 = get_sample_vertices(2)
        v1.add_outgoing_edge(v2.key)

        assert v1.has_edge_to(v2.key)
        assert not v2.has_edge_to(v1.key)

    def test_getting_edge_to_vertex(self):
        v1, v2 = get_sample_vertices(2)
        weight = 5
        v1.add_outgoing_edge(v2.key, weight=weight)

        edge = v1[v2.key]
        assert edge.from_vertex == v1.key
        assert edge.to_vertex == v2.key
        assert edge['weight'] == weight

        with pytest.raises(EdgeDoesNotExist):
            edge = v2[v1.key]

    def test_getting_edges_list(self):
        v1, v2, v3 = get_sample_vertices(3)
        v1.add_outgoing_edge(v2.key)
        v1.add_outgoing_edge(v3.key)

        assert len(v1.outgoing_edges) == 2
        assert len(v2.outgoing_edges) == 0
        assert v1[v2.key] in v1.outgoing_edges
        assert v1[v3.key] in v1.outgoing_edges

    def test_iterating_over_vertex(self):
        v1, v2, v3 = get_sample_vertices(3)
        v1.add_outgoing_edge(v2.key)
        v1.add_outgoing_edge(v3.key)

        key2, key3 = v1
        assert key2 == v2.key
        assert key3 == v3.key


class TestDirectedEdge:
    @pytest.mark.parametrize('data', [
        {},
        {'weight': 1},
        {'name': 'test_edge'},
        {'param_a': 1, 'param_b': 2}
    ])
    def test_creating_edge_with_different_data(self, data):
        v1, v2 = get_sample_vertices(2)
        edge = DirectedEdge(v1.key, v2.key, **data)
        assert edge.from_vertex == v1.key
        assert edge.to_vertex == v2.key
        for key, value in data.items():
            assert edge[key] == value

    def test_unpacking_edge(self):
        v1, v2 = get_sample_vertices(2)
        edge = DirectedEdge(v1.key, v2.key)
        from_key, to_key = edge
        assert from_key == v1.key
        assert to_key == v2.key


class TestDirectedGraph:
    def test_adding_vertex(self):
        g = DirectedGraph()
        key = "vertex"
        assert not g.has_vertex(key)
        g.add_vertex(key)
        assert g.has_vertex(key)

    def test_getting_vertex(self):
        g = DirectedGraph()
        key = "vertex"
        g.add_vertex(key)
        v = g[key]
        assert v.key == key
        with pytest.raises(VertexDoesNotExist):
            v = g["invalid_key"]

    def test_adding_edge(self):
        g = get_sample_graph(2)

        assert not g.has_edge(0, 1)
        g.add_edge(0, 1)
        assert g.has_edge(0, 1)
        assert not g.has_edge(1, 0)
        with pytest.raises(VertexDoesNotExist):
            g.has_edge(1, 10)

    def test_getting_edges_list(self):
        g = get_sample_graph(3)
        assert len(g.edges) == 0
        g.add_edge(0, 1)
        g.add_edge(1, 2)
        assert len(g.edges) == 2

    def test_copying(self):
        g1 = DirectedGraph()
        g1.add_vertex(1)
        g1.add_vertex(2)
        g2 = g1.copy()
        assert g2.has_vertex(1)
        assert g2.has_vertex(2)

        g2.add_edge(1, 2)
        assert g2.has_edge(1, 2)
        assert not g1.has_edge(1, 2)

        g1.add_vertex(3)
        assert g1.has_vertex(3)
        assert not g2.has_vertex(3)

    def test_iterating_over_graph(self):
        g = DirectedGraph()
        g.add_vertex(1)
        g.add_vertex(2)
        key1, key2 = g
        assert key1 == 1
        assert key2 == 2
