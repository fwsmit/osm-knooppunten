from import_osm import import_osm
from import_geojson import import_geojson, export_geojson
from compare import find_matching_point, dist_complicated
import math

def main():
    nodes_osm = import_osm("data/groningen.osm")
    #  nodes_ext = import_geojson("data/groningen.geojson")
    nodes_ext = import_geojson("data/Wandelknooppunten (wgs84).json", rwn_name="knooppuntnummer")

    #  print("OSM nodes")
    #  for n in nodes_osm:
        #  print(n.__geo_interface__)

    #  print("Geojson nodes")
    #  for n in nodes_ext:
        #  print(n.__geo_interface__)

    great_matches = 0
    good_matches = 0
    poor_matches = 0
    non_matches = []

    for node in nodes_ext:
        best_match = find_matching_point(node, nodes_osm)
        if best_match:
            dist = dist_complicated(best_match.lat, best_match.lon, node.lat, node.lon)
        else:
            dist = math.inf

        if dist < 1:
            great_matches += 1
        elif dist < 10:
            good_matches += 1
        elif dist < 100:
            poor_matches += 1
            #  print("Poor match. Distance:", dist)
        else:
            non_matches.append(node)
            #  print("Non match. Distance:", dist)

    print("Statistics:")
    print("Nodes analyzed (external):", len(nodes_ext))
    print("Nodes analyzed (OSM):", len(nodes_ext))
    print("Great matches (<1m):", great_matches)
    print("Good matches: (1-10m)", good_matches)
    print("Poor matches: (10-100m)", poor_matches)
    print("Non matches: (>100m))", len(non_matches))

    export_geojson(non_matches, "non_matches.geojson")

if __name__ == "__main__":
    main()


