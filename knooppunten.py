import xml.sax
from xml import sax

class MyContentHandler(xml.sax.ContentHandler):
    def __init__(self):
        xml.sax.ContentHandler.__init__(self)
        self.rwn_ref = None
        self.rcn_ref = None

    def startElement(self, name, attrs):
        print('start:', name)
        #  self.current_data = name
        print('attributes:')
        for attr in attrs.getNames():
            print("    " + attr + ": " + attrs[attr]);

        if name == "tag":
            print("name is tag")
            key = attrs["k"]
            value = attrs["v"]
            if key == "rwn_ref":
                self.rwn_ref = value
            if key == "rcn_ref":
                self.rcn_ref = value

    def endElement(self, name):
        print('end:', name)

        if name == "node":
            print('rwn_ref:', self.rwn_ref)
            print('rcn_ref:', self.rcn_ref)

def main():
    xml.sax.parse('data/best.osm', MyContentHandler())


if __name__ == "__main__":
    main()


