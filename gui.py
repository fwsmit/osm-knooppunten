import traceback, sys
from PySide6 import QtCore, QtWidgets
from PySide6.QtCore import QRunnable, Signal, QObject
from analyze import do_analysis
# from resultsView import StringListModel

def gui_do_analysis(osmFileName, importFile, filterRegion, progress):
        with open(str(osmFileName), 'r') as osmFile:
            return do_analysis(osmFile, importFile, filterRegion, progress=progress)


class WorkerSignals(QObject):
    '''
    Defines the signals available from a running worker thread.

    Supported signals are:

    finished
        No data

    error
        tuple (exctype, value, traceback.format_exc() )

    result
        object data returned from processing, anything

    '''
    finished = Signal()  # QtCore.Signal
    progress = Signal(object)
    error = Signal(tuple)
    result = Signal(object)

class Worker(QRunnable):
    '''
    Worker thread

    Inherits from QRunnable to handler worker thread setup, signals and wrap-up.

    :param callback: The function callback to run on this worker thread. Supplied args and
                     kwargs will be passed through to the runner.
    :type callback: function
    :param args: Arguments to pass to the callback function
    :param kwargs: Keywords to pass to the callback function

    '''

    def __init__(self, fn, *args, **kwargs):
        super(Worker, self).__init__()
        # Store constructor arguments (re-used for processing)
        self.fn = fn
        self.args = args
        self.kwargs = kwargs
        self.signals = WorkerSignals()

    @QtCore.Slot()
    def run(self):
        '''
        Initialise the runner function with passed args, kwargs.
        '''
        # Retrieve args/kwargs here; and fire processing using them
        try:
            result = self.fn(
                *self.args, **self.kwargs,
                progress=self.signals.progress
            )
        except:
            traceback.print_exc()
            exctype, value = sys.exc_info()[:2]
            self.signals.error.emit((exctype, value, traceback.format_exc()))
        else:
            self.signals.result.emit(result)  # Return the result of the processing
        finally:
            self.signals.finished.emit()  # Done


class RunWindow(QtWidgets.QWidget):
    def __init__(self, osmFileName, importFile, filterRegion):
        super().__init__()
        print("started run window")
        self.osmFileName = osmFileName
        self.importFile = importFile
        self.filterRegion = filterRegion
        self.setWindowTitle("Running analysis...")
        self.vlayout = QtWidgets.QVBoxLayout(self)
        self.progressLabel = QtWidgets.QLabel("")
        self.progressLabel.setAlignment(QtCore.Qt.AlignCenter)
        self.vlayout.addWidget(self.progressLabel)

        self.threadpool = QtCore.QThreadPool()

        worker = Worker(gui_do_analysis, osmFileName, importFile, filterRegion)
        worker.signals.result.connect(self.thread_results)
        worker.signals.finished.connect(self.thread_complete)
        worker.signals.progress.connect(self.thread_progress)
        self.threadpool.start(worker)

    def thread_results(self, results):
        self.results = results

    def thread_progress(self, progress):
        print(progress)
        self.progressLabel.setText(progress)
    
    def thread_complete(self):
        print("Thread complete")
        self.setWindowTitle("Done with analysis")
        self.progressLabel.setText("Results")
        model = QtCore.QStringListModel()
        self.table = QtWidgets.QTableWidget(len(self.results), 2, self)
        self.table.setHorizontalHeaderLabels(["Filename", "Node count"])
        for j in range(len(self.results)):
            filenameItem = QtWidgets.QTableWidgetItem(self.results[j].filename)
            filenameItem.setFlags(QtCore.Qt.ItemIsSelectable)
            nodeCountItem = QtWidgets.QTableWidgetItem(str(self.results[j].n_nodes))
            nodeCountItem.setFlags(QtCore.Qt.ItemIsSelectable)
            self.table.setItem(j, 0, filenameItem)
            self.table.setItem(j, 1, nodeCountItem)

        self.table.verticalHeader().hide()
        self.table.setSelectionMode(QtWidgets.QAbstractItemView.SingleSelection)
        self.table.setSortingEnabled(True)

        self.vlayout.addWidget(self.table)


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

        return text, hlayout

    def addFilterRegionWidgets(self, label, layout):
        label = QtWidgets.QLabel(label)
        text = QtWidgets.QLineEdit()

        hlayout = QtWidgets.QHBoxLayout()
        hlayout.addWidget(label)
        hlayout.addWidget(text)

        groupbox = QtWidgets.QGroupBox()
        groupbox.setLayout(hlayout)

        layout.addWidget(groupbox)
        return text

    def __init__(self):
        super().__init__()
        self.osmFile = None
        self.importFile = None
        vlayout = QtWidgets.QVBoxLayout(self)

        self.setWindowTitle("OSM Knooppunten import analyzer")


        self.text1, groupbox1 = self.addFileSlot(self.selectOSM, "OSM file:", vlayout)

        # Add import file and filter region in the same layout
        vlayout2 = QtWidgets.QVBoxLayout()
        self.text2, groupbox2 = self.addFileSlot(self.selectImportFile, "Import file:", vlayout2)
        self.filterRegion = self.addFilterRegionWidgets("Filter region:", vlayout2)
        groupbox = QtWidgets.QGroupBox()
        groupbox.setLayout(vlayout2)
        vlayout.addWidget(groupbox)

        startButton = QtWidgets.QPushButton("Run")
        vlayout.addWidget(startButton)
        startButton.clicked.connect(self.startAnalysis)

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

    @QtCore.Slot()
    def startAnalysis(self):
        print(self.osmFile)
        print(self.importFile)
        filterRegion = self.filterRegion.text()
        if len(filterRegion) == 0:
            filterRegion = None

        if self.osmFile is None:
            return -1

        if self.importFile is None:
            return -1

        self.runWindow = RunWindow(self.osmFile, self.importFile, self.filterRegion)
        self.runWindow.resize(600, 400)
        self.runWindow.show()

