import argparse as arg
import sys
from import_osm import import_osm
from import_geojson import import_geojson, export_geojson
from compare import find_matching_point, dist_complicated, find_closest_node
import math

def main():
    parser = arg.ArgumentParser()
    parser.add_argument("--osmfile", type=open, required=True, help="File with OSM data")
    parser.add_argument("--importfile", type=str, required=True, help="File with import data")
    parser.add_argument("--region", type=str, help="Compare the OSM data only to the import data from this region")

    try:
        args = parser.parse_args()
    except IOError as er:
        print(er)
        sys.exit(1)

    nodes_osm = import_osm(args.osmfile)
    nodes_ext, nodes_ext_invalid = import_geojson(args.importfile, rwn_name="knooppuntnummer", filter_regio=args.region)

    great_matches = []
    great_matches_osm = []
    good_matches = []
    good_matches_osm = []
    poor_matches = []
    poor_matches_osm = []
    non_matches = []

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
        else:
            dist = math.inf

        if dist < 1:
            great_matches.append(node)
            great_matches_osm.append(best_match)
        elif dist < 10:
            good_matches.append(node)
            good_matches_osm.append(best_match)
        elif dist < 100:
            poor_matches.append(node)
            poor_matches_osm.append(best_match)
        else:
            non_matches.append(node)


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

    print("Statistics:")
    print("Nodes analyzed (external):", len(nodes_ext))
    print("Nodes analyzed (OSM):", len(nodes_osm))
    print("Great matches (<1m):", len(great_matches))
    print("Good matches: (1-10m):", len(good_matches))
    print("Poor matches: (10-100m):", len(poor_matches))
    print("Non matches: (>100m)):", len(non_matches))
    print("")
    print("Dataset routedatabank:")
    print("Nodes with 0 matches: ", len(ext_match_0))
    print("Nodes with 1 matches: ", len(ext_match_1))
    print("Invalid nodes: ", len(nodes_ext_invalid))
    print("")
    print("Dataset OSM:")
    print("Nodes with 0 matches: ", len(osm_match_0))
    print("Nodes with 1 matches: ", len(osm_match_1))
    print("Nodes with 2 matches: ", len(osm_match_2))
    print("Nodes with >2 matches: ", len(osm_match_gt_2))
    print("Analysis concludes:")
    print("New nodes: ", len(new_nodes_ext))
    print("Renamed nodes: ", len(renamed_nodes_ext))
    print("Unsure nodes: ", len(unsure_nodes_ext))

    export_geojson(great_matches, "great_matches.geojson")
    export_geojson(great_matches_osm, "great_matches_osm.geojson")
    export_geojson(non_matches, "non_matches.geojson")
    export_geojson(poor_matches, "poor_matches.geojson")
    export_geojson(poor_matches_osm, "poor_matches_osm.geojson")
    export_geojson(good_matches, "good_matches.geojson")
    export_geojson(good_matches_osm, "good_matches_osm.geojson")
    export_geojson(osm_match_0, "osm_match_0.geojson")
    export_geojson(osm_match_2, "osm_match_2.geojson")
    export_geojson(osm_match_gt_2, "osm_match_gt_2.geojson")
    export_geojson(nodes_ext_invalid, "invalid_nodes_ext.geojson")
    export_geojson(new_nodes_ext, "new_nodes_ext.geojson")
    export_geojson(renamed_nodes_ext, "renamed_nodes_ext.geojson")
    export_geojson(unsure_nodes_ext, "unsure_nodes_ext.geojson")

if __name__ == "__main__":
    main()
