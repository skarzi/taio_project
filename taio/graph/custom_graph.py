import networkx

from .labels_modifier import LabelsModifier


def create_graph(task, labels_modifier=None):
    # TODO: need refactor. It if is probably useful only for debugging.
    labels_modifier = labels_modifier or LabelsModifier(task.info)

    graph = networkx.DiGraph()  # directed graph
    # to easily draw graph
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
