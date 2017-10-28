import networkx
import numpy as np

from matplotlib import pylab as plt


class GraphDrawer:
    # TODO: refactor
    DEFAULT_LABEL_EDGE_FUNC = lambda x: (x[:2], x[-1]['capacity'])

    def draw(
        self,
        graph,
        label_edge=DEFAULT_LABEL_EDGE_FUNC,
        draw_options=None,
    ):
        # TODO: refactor
        graph.graph.update(draw_options or {})

        nodes_positions = self._calculate_node_positions(graph)
        networkx.draw_networkx_labels(graph, nodes_positions)
        networkx.draw_networkx_nodes(graph, nodes_positions)
        networkx.draw_networkx_edges(graph, nodes_positions, arrow=True)
        networkx.draw_networkx_edge_labels(
            graph,
            nodes_positions,
            edge_labels=dict(label_edge(x) for x in graph.edges.data()),
        )
        plt.show()

    def _calculate_node_positions(self, graph):
        task_info = graph.graph['task_info']
        labels_modifier = graph.graph['labels_modifier']
        # source -> workers -> features -> projects -> target
        X = np.linspace(0, 1, 5)
        positions = {
            graph.graph['source']: [X[0], 0.5],
            graph.graph['target']: [X[-1], 0.5],
        }
        for i, key in enumerate(('workers', 'features', 'projects')):
            for j, y in enumerate(np.linspace(0, 1, task_info[i])):
                positions[labels_modifier.modify(key, j)] = [X[i + 1], y]
        return positions
