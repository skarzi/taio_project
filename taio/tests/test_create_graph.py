import os

from taio.data_loader import DataLoader
from taio.graph import create_graph

TEST_DATA_DIRECTORY = os.path.join(
    os.path.dirname(__file__),
    '..', '..', 'data',
)


def test_create_graph():
    task = DataLoader().load(
        os.path.join(TEST_DATA_DIRECTORY, "test_data_0.txt"),
    )
    g = create_graph(task)

    assert len(list(g)) == 11
    assert len(g.edges) == 12

    assert len(g[g.graph['source']].outgoing_edges) == 3
    assert len(g[g.graph['target']].outgoing_edges) == 0
