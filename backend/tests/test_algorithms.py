from app.graph import Graph
from app.algorithms import dijkstra_dest_apq, a_star_dest_apq


def create_test_graph():
    graph = Graph()

    a = graph.add_vertex((0, 0))
    b = graph.add_vertex((1, 0))
    c = graph.add_vertex((2, 0))
    d = graph.add_vertex((1, 1))

    graph.add_edge(a, b, 2)
    graph.add_edge(b, c, 3)
    graph.add_edge(a, d, 5)
    graph.add_edge(d, c, 1)

    return graph, a, c


def test_dijkstra():
    graph, start, destination = create_test_graph()

    result = dijkstra_dest_apq(graph, start, destination)

    assert destination in result
    assert result[destination][0] == 5


def test_a_star():
    graph, start, destination = create_test_graph()

    result = a_star_dest_apq(graph, start, destination)

    assert destination in result
    assert result[destination][0] == 5