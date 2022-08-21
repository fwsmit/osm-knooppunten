import sys
import random
from PySide6 import QtCore, QtWidgets, QtGui
from pathlib import Path

class MainWindow(QtWidgets.QWidget):
    def addFileSlot(self, fileSelectFunc, label):
        button = QtWidgets.QPushButton(label)
        text = QtWidgets.QLineEdit()

        hlayout = QtWidgets.QHBoxLayout(self)
        hlayout.addWidget(text)
        hlayout.addWidget(button)

        button.clicked.connect(self.selectOSM)

        return text, button


    def __init__(self):
        super().__init__()

        self.hello = ["Hallo Welt", "Hei maailma", "Hola Mundo", "Привет мир"]

        self.text1, button1 = self.addFileSlot(self.selectOSM, "Select OSM file")



    @QtCore.Slot()
    def selectOSM(self):
        self.osmFile, selectedFilter = QtWidgets.QFileDialog.getOpenFileName(self,
                "Select OSM file",
                filter="All Files (*);;OSM Files (*.osm)",
                selectedFilter="OSM Files (*.osm)")

        self.text1.setText(self.osmFile)

if __name__ == "__main__":
    app = QtWidgets.QApplication([])

    widget = MainWindow()
    widget.resize(800, 600)
    widget.show()

    sys.exit(app.exec())
