from .apq import APQBinaryHeap

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
        fx, fy = f.element()
        while open._size > 0:
            (v_total_cost, v_incurred_cost),v = open.remove_min()
            predecessor = preds.pop(v)
            closed[v] = (v_incurred_cost, predecessor)
            if v == f: #if have found the destination no need to keep searching
                break
            for e in graph.get_edges(v):
                w = e.opposite(v)
                wx, wy = w.element()
                estimated_cost = abs(wx - fx) + abs(wy - fy) #manhatten formula to estimate how far in a 2d space we are from 2 points
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