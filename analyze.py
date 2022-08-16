from enum import Enum
from compare import find_closest_node, dist_complicated

class ChangeType(Enum):
    # No significant change
    NO = 1

    # Exists in OSM dataset, but does not exist in import dataset and is not renamed
    REMOVED = 2

    # Does not exist in OSM dataset, but does exist in import dataset and is not renamed
    ADDED = 3

    # Close to node in other dataset with a different name. The other node
    # doesn't have a matching node either.
    RENAMED = 4

    # Matches with a node in the other dataset with distance 1-100m
    MOVED_SHORT = 5

    # Matches with a node in the other dataset with distance 100-1000m
    MOVED_LONG = 6

    # None of the others
    OTHER = 7

    def __str__(self):
        if self == ChangeType.NO:
            return "No change"

        if self == ChangeType.REMOVED:
            return "Removed"

        if self == ChangeType.ADDED:
            return "Added"

        if self == ChangeType.RENAMED:
            return "Renamed"

        if self == ChangeType.MOVED_SHORT:
            return "Moved short distance"

        if self == ChangeType.MOVED_LONG:
            return "Moved long distance"

        if self == ChangeType.OTHER:
            return "Other"

        return "Unknown enum value: {}".format(self.value)

def get_node_change_type_ext(node_ext, nodes_osm, nodes_ext):
    all_matching_nodes = node_ext.matching_nodes
    all_matching_nodes.extend(node_ext.bad_matching_nodes)

    if not all_matching_nodes or len(all_matching_nodes) == 0:
        print("No matching nodes")
        return ChangeType.ADDED
    
    closest_match = find_closest_node(node_ext, all_matching_nodes)
    closest_match_dist = dist_complicated(closest_match.lat, closest_match.lon, node_ext.lat, node_ext.lon)

    closest_node = find_closest_node(node_ext, nodes_osm)
    closest_node_dist = dist_complicated(closest_node.lat, closest_node.lon, node_ext.lat, node_ext.lon)

    # TODO: Should find next closest node if closest node has a match
    if closest_match_dist > 1000 and closest_node_dist < 10 and len(closest_node.matching_nodes) == 0:
        return ChangeType.RENAMED

    if closest_match_dist > 1 and closest_match_dist < 100:
        return ChangeType.MOVED_SHORT

    if closest_match_dist > 100 and closest_match_dist < 1000:
        return ChangeType.MOVED_LONG

    if closest_match_dist < 1:
        return ChangeType.NO

    return ChangeType.OTHER
