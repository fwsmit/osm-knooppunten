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

    print("Statistics:")
    print("Nodes analyzed (external):", len(nodes_ext))
    print("Nodes analyzed (OSM):", len(nodes_ext))
    print("Great matches (<1m):", len(great_matches))
    print("Good matches: (1-10m)", len(good_matches))
    print("Poor matches: (10-100m)", len(poor_matches))
    print("Non matches: (>100m))", len(non_matches))

    export_geojson(non_matches, "non_matches.geojson")
    export_geojson(poor_matches, "poor_matches.geojson")
    export_geojson(poor_matches_osm, "poor_matches_osm.geojson")
    export_geojson(good_matches, "good_matches.geojson")
    export_geojson(good_matches_osm, "good_matches_osm.geojson")

if __name__ == "__main__":
    main()
