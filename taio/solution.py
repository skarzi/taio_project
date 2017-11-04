from .data_loader import DataLoader
from .graph import (
    create_graph,
    edmonds_karp,
)


def associate_worker_with_project(flow_graph):
    labels_modifier = flow_graph.graph['labels_modifier']
    task_info = flow_graph.graph['task_info']
    for worker_id in range(task_info.workers_number):
        worker_label = labels_modifier.modify_worker(worker_id)
        for f_edge in flow_graph[worker_label].outgoing_edges:
            if f_edge['flow'] > 0:
                feature = f_edge.to_vertex
                for p_edge in flow_graph[feature].outgoing_edges:
                    if p_edge['flow'] > 0:
                        project = p_edge.to_vertex
                        yield (
                            worker_id,
                            labels_modifier.unmodify_project(project),
                        )
                        flow_graph[feature][project]['flow'] -= 1
                        break
                break


def solution(test_data_path):
    task = DataLoader().load(test_data_path)
    g = create_graph(task)
    flow_graph = edmonds_karp(g, g.graph['source'], g.graph['target'])
    max_flow = flow_graph.graph['max_flow']
    assignments = list(associate_worker_with_project(flow_graph))
    return max_flow, assignments
