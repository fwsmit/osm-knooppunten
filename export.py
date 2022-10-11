class ExportFile():
    # Abstract class that represents an exported file
    def __init__(self, filename, filepath, n_nodes):
        self.filename = filename
        self.filepath = filepath
        self.n_nodes = n_nodes

