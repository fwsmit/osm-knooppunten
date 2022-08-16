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

    print("Analyzing differences between datasets")

    nodes_osm = import_osm(args.osmfile)
    nodes_ext, nodes_ext_invalid = import_geojson(args.importfile, rwn_name="knooppuntnummer", filter_regio=args.region)

    print("OSM dataset:", args.osmfile.name, "({} nodes)".format(len(nodes_osm)))

    if (args.region):
        print("External dataset: {}, filtered by region '{}' ({} nodes)".format(args.importfile, args.region, len(nodes_ext)))
    else:
        print("External dataset:", args.importfile, "({} nodes)".format(len(nodes_ext)))
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

    print("#### Analysis results ####")
    print()
    print("## Fault analysis ##")
    print("Invalid nodes (external): ", len(nodes_ext_invalid))
    print()
    print("## Node changes ##")
    print("New nodes: ", len(new_nodes_ext))
    print("Renamed nodes: ", len(renamed_nodes_ext))
    print("Unsure nodes: ", len(unsure_nodes_ext))

    export_geojson(nodes_ext_invalid, "invalid_nodes_ext.geojson")
    export_geojson(new_nodes_ext, "new_nodes_ext.geojson")
    export_geojson(renamed_nodes_ext, "renamed_nodes_ext.geojson")
    export_geojson(unsure_nodes_ext, "unsure_nodes_ext.geojson")

if __name__ == "__main__":
    main()
