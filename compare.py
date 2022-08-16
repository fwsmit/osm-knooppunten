import math

def dist_complicated(lat1, lon1, lat2, lon2):
    lat1, lon1, lat2, lon2 = map(math.radians, [lat1, lon1, lat2, lon2])

    dlon = lon2 - lon1
    dlat = lat2 - lat1
    a = math.sin(dlat/2)**2 + math.cos(lat1) * math.cos(lat2) * math.sin(dlon/2)**2
    c = 2 * math.asin(math.sqrt(a))
    # Radius of earth in kilometers is 6371
    km = 6371* c
    return 1000 * km

def dist_simple_sq(lat1, lon1, lat2, lon2):
    dlon = lon2 - lon1
    dlat = lat2 - lat1
    return dlon**2 + dlat**2


def find_matching_point(node_ext, nodes_osm):
    closest_node = None
    best_dist_sq = math.inf
    for node in nodes_osm:
        if node.rwn_ref == node_ext.rwn_ref or node.rcn_ref == node_ext.rcn_ref:
            dist_sq = dist_simple_sq(node.lat, node.lon, node_ext.lat, node_ext.lon)
            if dist_sq < best_dist_sq:
                best_dist_sq = dist_sq
                closest_node = node

    if closest_node:
        actual_dist = dist_complicated(closest_node.lat, closest_node.lon, node_ext.lat, node_ext.lon)

    return closest_node

# Returns the closest node from the given node
def find_closest_node(node, comparison_nodes):
    closest_node = None
    best_dist_sq = math.inf
    for n in comparison_nodes:
        dist_sq = dist_simple_sq(node.lat, node.lon, n.lat, n.lon)
        if dist_sq < best_dist_sq:
            best_dist_sq = dist_sq
            closest_node = n

    return closest_node

