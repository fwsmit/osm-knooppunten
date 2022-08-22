import sys
import random
from PySide6 import QtCore, QtWidgets, QtGui
from pathlib import Path

class MainWindow(QtWidgets.QWidget):
    def addFileSlot(self, fileSelectFunc, label, layout):
        label = QtWidgets.QLabel(label)
        button = QtWidgets.QPushButton("Select")
        text = QtWidgets.QLineEdit()

        hlayout = QtWidgets.QHBoxLayout()
        hlayout.addWidget(label)
        hlayout.addWidget(text)
        hlayout.addWidget(button)

        groupbox = QtWidgets.QGroupBox()
        groupbox.setLayout(hlayout)

        layout.addWidget(groupbox)

        button.clicked.connect(fileSelectFunc)

        return text

    def __init__(self):
        super().__init__()
        vlayout = QtWidgets.QVBoxLayout(self)

        self.setWindowTitle("OSM Knooppunten import analyzer")

        self.text1 = self.addFileSlot(self.selectOSM, "OSM file:", vlayout)
        self.text2 = self.addFileSlot(self.selectImportFile, "Import file:", vlayout)

    @QtCore.Slot()
    def selectOSM(self):
        self.osmFile, selectedFilter = QtWidgets.QFileDialog.getOpenFileName(self,
                "Select OSM file",
                filter="All Files (*);;OSM Files (*.osm)",
                selectedFilter="OSM Files (*.osm)")

        self.text1.setText(self.osmFile)

    @QtCore.Slot()
    def selectImportFile(self):
        self.importFile, selectedFilter = QtWidgets.QFileDialog.getOpenFileName(self,
                "Select import file",
                filter="All Files (*);;GeoJSOSN Files (*.json, *.geojson)",
                selectedFilter="GeoJSOSN Files (*.json, *.geojson)")

        self.text2.setText(self.importFile)

if __name__ == "__main__":
    app = QtWidgets.QApplication([])

    widget = MainWindow()
    widget.resize(800, 600)
    widget.show()

    sys.exit(app.exec())
