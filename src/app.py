import sys
from PyQt5.QtWidgets import (
    QApplication,
    QMainWindow,
    QWidget,
    QHBoxLayout,
    QVBoxLayout,
    QSplitter,
    QLabel,
)
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QColor, QPalette


class DiseaseConfigWidget(QWidget):
    def __init__(self):
        super().__init__()
        layout = QVBoxLayout(self)

        label = QLabel("Disease Config")
        layout.addWidget(label)


class NodeGraphWidget(QWidget):
    def __init__(self):
        super().__init__()
        self.setStyleSheet("background-color:#d9d9d9")

        layout = QVBoxLayout(self)
        label = QLabel("placeholder")
        layout.addWidget(label)


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("pandemic-config-gui")
        self.resize(1280, 720)

        self.splitter = QSplitter(Qt.Horizontal)

        left_panel = DiseaseConfigWidget()
        right_panel = NodeGraphWidget()

        self.splitter.addWidget(left_panel)
        self.splitter.addWidget(right_panel)
        self.setCentralWidget(self.splitter)


def run_app():
    app = QApplication(sys.argv)
    window = MainWindow()

    window.show()
    sys.exit(app.exec_())
