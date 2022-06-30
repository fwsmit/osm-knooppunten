from import_osm import import_osm
from import_geojson import import_geojson, export_geojson
from compare import find_matching_point, dist_complicated
import math

def main():
    nodes_osm = import_osm("data/groningen.osm")
    nodes_ext = import_geojson("data/Wandelknooppunten (wgs84).geojson", rwn_name="knooppuntnummer", filter_regio="Groningen")

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
                node.matching_nodes.append(node)
            else:
                best_match.bad_matching_nodes.append(node)
                node.bad_matching_nodes.append(node)

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

    print("Statistics:")
    print("Nodes analyzed (external):", len(nodes_ext))
    print("Nodes analyzed (OSM):", len(nodes_ext))
    print("Great matches (<1m):", len(great_matches))
    print("Good matches: (1-10m):", len(good_matches))
    print("Poor matches: (10-100m):", len(poor_matches))
    print("Non matches: (>100m)):", len(non_matches))
    print("")
    print("Dataset routedatabank:")
    print("Nodes with 0 matches: ", len(ext_match_0))
    print("Nodes with 1 matches: ", len(ext_match_1))
    print("")
    print("Dataset OSM:")
    print("Nodes with 0 matches: ", len(osm_match_0))
    print("Nodes with 1 matches: ", len(osm_match_1))
    print("Nodes with 2 matches: ", len(osm_match_2))
    print("Nodes with >2 matches: ", len(osm_match_gt_2))

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

if __name__ == "__main__":
    main()
