import geojson
from node import Node

def import_geojson(filename):
    with open("data/groningen.geojson", 'r') as file:
        data = geojson.load(file)
        print("Geojson data imported")

    nodes = []

    print(len(data['features']))

    for node_data in data['features']:
        ref_id = node_data['properties']['KNOOPP_NR']
        if node_data['geometry']:
            coords = node_data['geometry']['coordinates']
            coord_x = coords[0]
            coord_y = coords[1]
        else:
            coord_x = None
            coord_y = None

        nodes.append(Node(x=coord_x, y=coord_y, rwn_ref=ref_id, rcn_ref=-1))

    return nodes

    #  for node in nodes:
        #  print(node.__geo_interface__)
