import math
from .apq import APQBinaryHeap

def heuristic(vertex, destination):
    """Estimate the distance between two vertices in metres."""
    lat1 = math.radians(vertex.latitude())
    lon1 = math.radians(vertex.longitude())
    lat2 = math.radians(destination.latitude())
    lon2 = math.radians(destination.longitude())

    earth_radius = 6371000  # metres

    dlat = lat2 - lat1
    dlon = lon2 - lon1

    a = (
        math.sin(dlat / 2) ** 2
        + math.cos(lat1)
        * math.cos(lat2)
        * math.sin(dlon / 2) ** 2
    )

    return 2 * earth_radius * math.asin(math.sqrt(a))

def dijkstra_dest_apq(graph, s, f):
        open = APQBinaryHeap()
        closed = {}
        preds = {s: None}

        open.add(0,s)

        while open._size > 0:
            v_cost, v = open.remove_min()
            predecessor = preds.pop(v)
            closed[v] = (v_cost, predecessor)
            if v == f: #if have found the destination no need to keep searching
                break
            for e in graph.get_edges(v):
                w = e.opposite(v)
                if not w in closed:
                    newcost = v_cost + e.element() + w.cost() #element label of the edge = cost of traversing
                    if not w in preds:
                        preds[w] = v
                        open.add(newcost, w)
                    elif newcost < open.get_key(w):
                        preds[w] = v
                        open.update_key(w, newcost)
        print(f"Items removed from dijkstras open apq: {open._items_removed}")
        return closed

def a_star_dest_apq(graph, s, f):
        open = APQBinaryHeap()
        closed = {}
        preds = {s: None}

        open.add((0,0),s)#storing this time as (total cost, incurred cost)
        while open._size > 0:
            (v_total_cost, v_incurred_cost),v = open.remove_min()
            predecessor = preds.pop(v)
            closed[v] = (v_incurred_cost, predecessor)
            if v == f: #if have found the destination no need to keep searching
                break
            for e in graph.get_edges(v):
                w = e.opposite(v)
                estimated_cost = estimated_cost = heuristic(w, f)
                if not w in closed:
                    new_incurred_cost = v_incurred_cost + e.element() + w.cost()#element label of the edge = cost of traversing
                    if not w in preds:
                        preds[w] = v
                        open.add((estimated_cost + new_incurred_cost, new_incurred_cost), w)
                    else:
                        old_total_cost, old_incurred_cost = open.get_key(w) # changed to a tuple for a* so we need to unpack to do a comparison for the if
                        if new_incurred_cost < old_incurred_cost:
                            preds[w] = v
                            open.update_key(w, (estimated_cost + new_incurred_cost, new_incurred_cost))
        print(f"Items removed from a*'s open apq: {open._items_removed}")
        return closed