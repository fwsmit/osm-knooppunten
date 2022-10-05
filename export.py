class ExportFile():
    # Abstract class that represents an exported file
    def __init__(self, filename, n_nodes):
        self.filename = filename
        self.n_nodes = n_nodes

