import os, sys
from PyQt5 import QtWidgets as QtW
from PyQt5.QtCore import Qt, pyqtSignal
import NodeGraphQt as NGQt


disease_stages = [
    "recovered",
    "healthy",
    "exposed",
    "asymptomatic",
    "mild",
    "severe",
    "hospitalised",
    "intensive_care",
    "dead_home",
    "dead_hospital",
    "dead_icu",
]


class StartNode(NGQt.BaseNode):
    __identifier__ = "stages"
    NODE_NAME = "Start State"

    def __init__(self):
        super(StartNode, self).__init__()
        self.set_color(40, 150, 40)
        self.add_output("Next Stage")


class TransitionNode(NGQt.BaseNode):
    __identifier__ = "stages"
    NODE_NAME = "Transition"

    def __init__(self):
        super(TransitionNode, self).__init__()
        self.set_color(220, 160, 20)
        self.add_input("From Stage")
        self.add_output("To Stage")

        self.add_text_input("Prob", "Probability", text="0.1")


class EndNode(NGQt.BaseNode):
    __identifier__ = "stages"
    NODE_NAME = "End State"

    def __init__(self):
        super(EndNode, self).__init__()
        self.set_color(180, 40, 40)
        self.add_input("From Stage")


class DiseaseConfigWidget(QtW.QWidget):
    config_saved = pyqtSignal(dict)

    def __init__(self):
        super().__init__()
        self.setObjectName("configPanel")
        layout = QtW.QVBoxLayout(self)

        layout.setContentsMargins(20, 20, 20, 10)

        title_label = QtW.QLabel("Disease Config")
        title_label.setObjectName("title_label")
        layout.addWidget(title_label)

        layout.addWidget(QtW.QLabel("Name:"))
        self.name_entry = QtW.QLineEdit()
        self.name_entry.setPlaceholderText("e.g., COVID-19 / Measles / Black Death")
        layout.addWidget(self.name_entry)

        layout.addWidget(QtW.QLabel("Default Lowest Stage:"))
        self.dls_combo = QtW.QComboBox()
        self.dls_combo.addItems(disease_stages)
        self.dls_combo.setCurrentText(disease_stages[0])
        layout.addWidget(self.dls_combo)

        layout.addWidget(QtW.QLabel("Max Mild Symptom Tag:"))
        self.mmst_combo = QtW.QComboBox()
        self.mmst_combo.addItems(disease_stages)
        self.mmst_combo.setCurrentText(disease_stages[0])
        layout.addWidget(self.mmst_combo)

        self.save_button = QtW.QPushButton("Save Configuration")
        self.save_button.clicked.connect(self.getConfigData)
        layout.addWidget(self.save_button)

        layout.addStretch(1)

    def getConfigData(self):
        config_data = {
            "name": self.name_entry.text(),
            "default_lowest_stage": self.dls_combo.currentText(),
            "max_mild_symptom_tag": self.mmst_combo.currentText(),
        }

        print("--- Configuration Data Retrieved ---")
        print(f"Name: {config_data['name']}")
        print(f"Default Lowest Stage: {config_data['default_lowest_stage']}")
        print(f"Max Mild Symptom Tag: {config_data['max_mild_symptom_tag']}")
        print("------------------------------------")

        self.config_saved.emit(config_data)


class NodeGraphWidget(QtW.QWidget):
    def __init__(self):
        super().__init__()

        layout = QtW.QVBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)

        self.graph = NGQt.NodeGraph()

        layout.addWidget(self.graph.viewer())

        self.graph.register_nodes([StartNode, TransitionNode, EndNode])
        self.graph.set_background_color(38, 50, 56)
        self.graph.set_grid_color(55, 71, 79)

        self._setup_context_menu()

    def _setup_context_menu(self):
        graph_menu = self.graph.get_context_menu("graph")
        stage_menu = graph_menu.add_menu("stages")

        func_start = lambda: self.graph.create_node(
            StartNode.__identifier__ + "." + StartNode.__name__
        )

        func_transition = lambda: self.graph.create_node(
            TransitionNode.__identifier__ + "." + TransitionNode.__name__
        )

        func_end = lambda: self.graph.create_node(
            EndNode.__identifier__ + "." + EndNode.__name__
        )

        stage_menu.add_command(StartNode.NODE_NAME, func_start)
        stage_menu.add_command(TransitionNode.NODE_NAME, func_transition)
        stage_menu.add_command(EndNode.NODE_NAME, func_end)


class MainWindow(QtW.QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("pandemic-config-gui")
        self.resize(1280, 720)

        self.splitter = QtW.QSplitter(Qt.Horizontal)

        left_panel = DiseaseConfigWidget()
        self.right_panel = NodeGraphWidget()

        left_panel.config_saved.connect(self.handle_config_save)

        self.splitter.addWidget(left_panel)
        self.splitter.addWidget(self.right_panel)

        self.splitter.setSizes([300, 980])

        self.setCentralWidget(self.splitter)

    def handle_config_save(self, config_data):
        print("MainWindow received saved config.")

        graph_data = self.right_panel.graph.serialize_session()
        print("Current Graph Data:", graph_data)
        pass


def run_app():
    app = QtW.QApplication(sys.argv)
    window = MainWindow()

    script_dir = os.path.dirname(os.path.abspath(__file__))

    qss_path = os.path.join(script_dir, "style", "theme.qss")

    if os.path.exists(qss_path):
        try:
            with open(qss_path, "r") as f:
                _style = f.read()
                app.setStyleSheet(_style)
        except Exception as e:
            print(f"Error loading stylesheet: {e}")
    else:
        print(
            f"Warning: Stylesheet not found at {qss_path}. Running with default theme."
        )

    window.show()
    sys.exit(app.exec_())
