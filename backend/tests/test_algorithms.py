from app.graph import Graph
from app.algorithms import dijkstra_dest_apq, a_star_dest_apq


def create_test_graph():
    graph = Graph()

    a = graph.add_vertex("A", lat=51.8985, lon=-8.4756)
    b = graph.add_vertex("B", lat=51.8995, lon=-8.4770)
    c = graph.add_vertex("C", lat=51.9010, lon=-8.4780)
    d = graph.add_vertex("D", lat=51.9000, lon=-8.4735)

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