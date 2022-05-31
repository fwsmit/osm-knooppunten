class Node():
    def __init__(self, x, y, rwn_ref, rcn_ref):
        self.x = x
        self.y = y
        self.rwn_ref = rwn_ref
        self.rcn_ref = rcn_ref

    @property
    def __geo_interface__(self):
        return {"geometry": {"coordinates": (self.x, self.y), "type": "Point"},
                "properties": {"rwn_ref": self.rwn_ref, "rcn_ref": self.rcn_ref}, "type": "Feature"}
