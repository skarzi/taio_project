import networkx

from .labels_modifier import LabelsModifier


def create_graph(task, labels_modifiers=None):
    # TODO: need refactor. It if is probably useful only for debugging.
    if not labels_modifiers:
        labels_modifier = LabelsModifier(
            workers=lambda x: str(x + 1),
            features=lambda x: str(x + 1 + task.info.workers_number),
            projects=lambda x: str(x + 1 + task.info.workers_number +
                                   task.info.features_number),
        )
    else:
        labels_modifier = LabelsModifier(**labels_modifiers)

    graph = networkx.DiGraph()  # directed graph
    # to easily draw graph
    graph.graph['task_info'] = task.info
    graph.graph['labels_modifier'] = labels_modifier
    graph.graph['source'] = labels_modifier.modify('source', 0)
    graph.graph['target'] = labels_modifier.modify(
        'target',
        (1 + task.info.workers_number + task.info.features_number +
         task.info.projects_number),
    )
    # add edges from source to workers
    for i, worker in enumerate(task.workers):
        graph.add_edge(
            graph.graph['source'],
            labels_modifier.modify('workers', i),
            capacity=1,  # or weight=1
        )
    # add edges from workers to features
    for i, worker in enumerate(task.workers):
        for feature_no in range(task.info.features_number):
            if worker[feature_no]:
                graph.add_edge(
                    labels_modifier.modify('workers', i),
                    labels_modifier.modify('features', feature_no),
                    capacity=1,
                )
    # add edges from features to projects
    for i, project in enumerate(task.projects):
        features_sum = 0
        for feature_no in range(task.info.features_number):
            if project[feature_no] > 0:
                features_sum += project[feature_no]
                graph.add_edge(
                    labels_modifier.modify('features', feature_no),
                    labels_modifier.modify('projects', i),
                    capacity=project[feature_no],
                )
        graph.add_edge(
            labels_modifier.modify('projects', i),
            graph.graph['target'],
            capacity=features_sum,
        )
    return graph
