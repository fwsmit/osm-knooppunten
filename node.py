class Node():
    def __init__(self, lat, lon, rwn_ref, rcn_ref):
        self.lat = float(lat)
        self.lon = float(lon)
        self.rwn_ref = rwn_ref
        self.rcn_ref = rcn_ref
        self.matching_nodes = []
        self.bad_matching_nodes = [] # matching nodes with a distance >100m

    @property
    def __geo_interface__(self):
        return {"geometry": {"coordinates": (self.lat, self.lon), "type": "Point"},
                "properties": {"rwn_ref": self.rwn_ref, "rcn_ref": self.rcn_ref}, "type": "Feature"}
