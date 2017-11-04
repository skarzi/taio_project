import pytest

from taio.graph import edmonds_karp
from taio.graph.custom_graph import DirectedGraph


def create_test_graph(edges_list):
    g = DirectedGraph()
    for u, v, data in edges_list:
        g.add_edge(u, v, **data)
    return g


class TestEdmondsKarp:
    @pytest.mark.parametrize('edges_list, expected_max_flow', [
        (
                [
                    ('s', 'w1', {'capacity': 1}),
                    ('s', 'w2', {'capacity': 1}),
                    ('s', 'w3', {'capacity': 1}),
                    ('w1', 'p1', {'capacity': 1}),
                    ('w2', 'p2', {'capacity': 1}),
                    ('w3', 'p3', {'capacity': 1}),
                    ('p1', 't', {'capacity': 1}),
                    ('p2', 't', {'capacity': 1}),
                    ('p3', 't', {'capacity': 1}),
                ],
                3,
        ),
        (
                [
                    ('s', 'w1', {'capacity': 1}),
                    ('s', 'w2', {'capacity': 1}),
                    ('s', 'w3', {'capacity': 1}),
                    ('s', 'w4', {'capacity': 1}),
                    ('s', 'w5', {'capacity': 1}),
                    ('w1', 'f1', {'capacity': 1}),
                    ('w1', 'f2', {'capacity': 1}),
                    ('w2', 'f2', {'capacity': 1}),
                    ('w3', 'f2', {'capacity': 1}),
                    ('w4', 'f2', {'capacity': 1}),
                    ('w4', 'f3', {'capacity': 1}),
                    ('w5', 'f3', {'capacity': 1}),
                    ('f1', 'p1', {'capacity': 2}),
                    ('f2', 'p1', {'capacity': 2}),
                    ('f3', 'p2', {'capacity': 1}),
                    ('p1', 't', {'capacity': 4}),
                    ('p2', 't', {'capacity': 1}),
                ],
                4,
        ),
    ])
    def test_edmonds_karp_returns_correct_max_flow_value(
            self,
            edges_list,
            expected_max_flow,
    ):
        graph = create_test_graph(edges_list)
        max_flow = edmonds_karp(graph, 's', 't').graph['max_flow']
        assert max_flow == expected_max_flow
