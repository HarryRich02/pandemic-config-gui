import os, sys
from PyQt5 import QtWidgets as QtW
from PyQt5.QtCore import Qt

import graph
import configPanel


class MainWindow(QtW.QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("pandemic-config-gui")
        self.resize(1280, 720)

        self.splitter = QtW.QSplitter(Qt.Horizontal)

        left_panel = configPanel.DiseaseConfigWidget()

        self.right_panel = graph.NodeGraphWidget()

        left_panel.config_saved.connect(self.handle_config_save)

        self.splitter.addWidget(left_panel)
        self.splitter.addWidget(self.right_panel)
        self.splitter.setSizes([350, 930])

        self.setCentralWidget(self.splitter)

    def handle_config_save(self, config_data):
        print("MainWindow received saved config.")
        graph_data = self.right_panel.graph.serialize_session()


def run_app():
    app = QtW.QApplication(sys.argv)

    script_dir = os.path.dirname(os.path.abspath(__file__))
    qss_path = os.path.join(script_dir, "style", "theme.qss")

    if os.path.exists(qss_path):
        try:
            with open(qss_path, "r") as f:
                app.setStyleSheet(f.read())
        except Exception as e:
            print(f"Error loading stylesheet: {e}")

    window = MainWindow()
    window.show()
    sys.exit(app.exec_())


if __name__ == "__main__":
    run_app()
