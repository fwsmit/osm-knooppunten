import os
import sys
import argparse as arg
from PySide6 import QtWidgets
from _version import __version__
from gui import MainWindow

def main():
    rootpath = os.path.dirname(os.path.abspath(__file__))
    os.chdir(rootpath)
    print("Working directory:", os.getcwd())
    parser = arg.ArgumentParser()
    parser.add_argument('--version', action='version', version='%(prog)s {version}'.format(version=__version__))
    parser.parse_args()
    app = QtWidgets.QApplication([])

    widget = MainWindow()
    widget.resize(800, 600)
    widget.show()

    sys.exit(app.exec())

if __name__ == "__main__":
    main()
