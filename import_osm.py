import xml.sax
from xml import sax
from node import Node

class OSMContentHandler(xml.sax.ContentHandler):
    def __init__(self, nodes):
        xml.sax.ContentHandler.__init__(self)
        self.rwn_ref = None
        self.rcn_ref = None
        self.lat = None
        self.lon = None
        self.nodes = nodes

    def startElement(self, name, attrs):
        if name == "node":
            self.lat = attrs["lat"]
            self.lon = attrs["lon"]

        if name == "tag":
            key = attrs["k"]
            value = attrs["v"]
            if key == "rwn_ref":
                self.rwn_ref = value.lstrip("0")
            if key == "rcn_ref":
                self.rcn_ref = value.lstrip("0")

    def endElement(self, name):
        if name == "node":
            self.nodes.append(Node(lat=self.lat, lon=self.lon, rwn_ref=self.rwn_ref, rcn_ref=self.rcn_ref))

def import_osm(filename):
    nodes = []
    xml.sax.parse(filename, OSMContentHandler(nodes))
    return nodes
