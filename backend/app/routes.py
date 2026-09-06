from flask import Blueprint, request
from .graph import Graph
from .algorithms import dijkstra_dest_apq, a_star_dest_apq

"""
Learning for self - 
the Blueprint creates a container that groups the APIs
endpoints with similar characteristcs together
first parameter is the name the second is the 
python module it belongs to
"""
routes = Blueprint("routes", __name__)
graph = Graph()
graph.create_from_json("app/data/map.json")

@routes.get("/api/health")
def health():
    return {"status": "healthy"}

@routes.post("/api/routes/calculate")
def calculate_route():
    """ A JSON file is sent with the start,
    destination and the selectedalgorithm 
    used to calculate the path
    """
    data = request.get_json()

    start_id = data["start"]
    destination_id = data["destination"]
    algorithm = data["algorithm"]

    start = graph.get_vertex_by_label(start_id)
    destination = graph.get_vertex_by_label(destination_id)

    if algorithm == "dijkstra":
        result = dijkstra_dest_apq(graph, start, destination)
    elif algorithm == "astar":
        result = a_star_dest_apq(graph, start, destination)
    else:
        return {"error": "Invalid algorithm"}, 400 # bad request

    path, distance = graph.extract_path(result, destination_id)
    
    return {
        "path": path,
        "distance": distance,
        "nodes_explored": len(result)
    }