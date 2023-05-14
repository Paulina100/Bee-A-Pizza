from PyQt5.QtCore import QObject, pyqtSignal
import time


class SolutionWorker(QObject):
    def __init__(self, parameters):
        super().__init__()
        self.progress = pyqtSignal(int)
        self.finished = pyqtSignal()

    def run(self):
        for i in range(100):
            time.sleep(0.1)
            self.progress.emit(i)
        self.finished.emit()