import sys
from PyQt5.QtWidgets import (
    QApplication,
    QMainWindow,
    QWidget,
    QHBoxLayout,
    QSplitter,
    QLabel,
)
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QColor, QPalette


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("pandemic-config-gui")
        self.resize(1280, 720)

        self.splitter = QSplitter(Qt.Horizontal)

        left_panel = QWidget()
        left_panel.setStyleSheet("background-color: #f0f0f0")
        left_layout = QHBoxLayout(left_panel)
        left_layout.addWidget(QLabel("Config Panel"))

        right_panel = QWidget()
        right_panel.setStyleSheet("background-color: #d9d9d9")
        right_layout = QHBoxLayout(right_panel)
        right_layout.addWidget(QLabel("Trajectories"))

        self.splitter.addWidget(left_panel)
        self.splitter.addWidget(right_panel)
        self.setCentralWidget(self.splitter)


def run_app():
    app = QApplication(sys.argv)
    window = MainWindow()

    window.show()
    sys.exit(app.exec_())
