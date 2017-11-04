class GraphException(Exception):
    pass


class EdgeDoesNotExist(GraphException):
    pass


class VertexDoesNotExist(GraphException):
    pass


class GraphNodeLabelError(GraphException):
    pass
