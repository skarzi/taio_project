from .graph import (
    create_graph,
    edmonds_karp,
    GraphDrawer,
)
from .data_loader import DataLoader


def associate_worker_with_project(flow_graph):
    labels_modifier = flow_graph.graph['labels_modifier']
    task_info = flow_graph.graph['task_info']
    for worker_id in range(task_info.workers_number):
        worker_label = labels_modifier.modify_worker(worker_id)
        for feature, edge_data in flow_graph.adj[worker_label].items():
            if edge_data['flow'] > 0:
                for project, edge_data in flow_graph.adj[feature].items():
                    if edge_data['flow'] > 0:
                        yield (
                            worker_id,
                            labels_modifier.unmodify_project(project),
                        )
                        flow_graph[feature][project]['flow'] -= 1
                        break
                break


def dev_solution(test_data_path, debug=False):
    task = DataLoader().load(test_data_path)
    g = create_graph(task)
    flow_graph = edmonds_karp(g, g.graph['source'], g.graph['target'])
    if debug:
        graph_drawer = GraphDrawer()
        graph_drawer.draw(
            flow_graph,
            label_edge=lambda x: (
                x[:2],
                f"{x[-1]['flow']}/{x[-1]['capacity']}",
            ),
            edge_list=g.edges,
        )
        return g, flow_graph, list(associate_worker_with_project(flow_graph))
    return list(associate_worker_with_project(flow_graph))
