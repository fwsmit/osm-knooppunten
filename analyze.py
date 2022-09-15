from enum import Enum
from compare import find_closest_node, dist_complicated
from import_osm import import_osm
from import_geojson import import_geojson, export_geojson
from compare import find_matching_point, dist_complicated, find_closest_node
from _version import __version__

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

def do_analysis(osmfile, importfilename, filter_region, progress):
    nodes_osm = import_osm(osmfile)
    nodes_ext, nodes_ext_invalid = import_geojson(importfilename, rwn_name="knooppuntnummer", filter_regio=filter_region)

    print("OSM dataset:", osmfile.name, "({} nodes)".format(len(nodes_osm)))

    if (filter_region):
        print("External dataset: {}, filtered by region '{}' ({} nodes)".format(importfilename, filter_region, len(nodes_ext)))
    else:
        print("External dataset:", importfilename, "({} nodes)".format(len(nodes_ext)))
    print()

    for node in nodes_ext:
        best_match = find_matching_point(node, nodes_osm)
        if best_match:
            dist = dist_complicated(best_match.lat, best_match.lon, node.lat, node.lon)
            if dist < 100:
                best_match.matching_nodes.append(node)
                node.matching_nodes.append(best_match)
            else:
                best_match.bad_matching_nodes.append(node)
                node.bad_matching_nodes.append(best_match)

    ext_match_0 = []
    ext_match_1 = []
    for node in nodes_ext:
        n_matches = len(node.matching_nodes)

        if n_matches == 0:
            ext_match_0.append(node)
        elif n_matches == 1:
            ext_match_1.append(node)
        else:
            print("Error: external node is matched with multiple OSM nodes")

    osm_match_0 = []
    osm_match_1 = []
    osm_match_2 = []
    osm_match_gt_2 = []
    for node in nodes_osm:
        n_matches = len(node.matching_nodes)

        if n_matches == 0:
            osm_match_0.append(node)
        elif n_matches == 1:
            osm_match_1.append(node)
        elif n_matches == 2:
            osm_match_2.append(node)
        else:
            osm_match_gt_2.append(node)

    new_nodes_ext = []
    renamed_nodes_ext = []
    unsure_nodes_ext = []
    # Try to find new nodes
    for node in ext_match_0:
        closest_node = find_closest_node(node, nodes_osm)
        dist = dist_complicated(closest_node.lat, closest_node.lon, node.lat, node.lon)
        if dist > 100:
            # Not near any node, so it must be new
            new_nodes_ext.append(node)
        elif dist < 10:
            renamed_nodes_ext.append(node)
        else:
            unsure_nodes_ext.append(node)
    
    node_changes_dict = dict()
    for key in ChangeType:
        node_changes_dict[key] = []

    for node in nodes_ext:
        change_type = get_node_change_type_ext(node, nodes_osm, nodes_ext)
        node_changes_dict[change_type].append(node)

    print("#### Analysis results ####")
    print()
    print("## Fault analysis ##")
    print("Invalid nodes (external): ", len(nodes_ext_invalid))
    print()
    print("## Node changes ##")
    for key in node_changes_dict:
        print("{}: {}".format(key, len(node_changes_dict[key])))

    print("## Exporting changes ##")
    export_geojson(nodes_ext_invalid, "invalid_nodes_ext.geojson")
    for key in ChangeType:
        export_geojson(node_changes_dict[key], "{}_ext.geojson".format(key))
