import os, sys
from PyQt5 import QtWidgets as QtW
from PyQt5.QtCore import Qt

# Import the separated graph logic
import graph

# --- Constants ---
DISEASE_STAGES = [
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


class DiseaseConfigWidget(QtW.QWidget):
    def __init__(self):
        super().__init__()
        self.setObjectName("configPanel")
        layout = QtW.QVBoxLayout(self)
        layout.setContentsMargins(20, 20, 20, 10)

        title_label = QtW.QLabel("Disease Config")
        title_label.setObjectName("title_label")
        layout.addWidget(title_label)

        layout.addWidget(QtW.QLabel("Disease Model Name:"))
        self.name_entry = QtW.QLineEdit()
        self.name_entry.setPlaceholderText("e.g. covid19")
        layout.addWidget(self.name_entry)

        layout.addWidget(QtW.QLabel("Default Lowest Stage:"))
        self.dls_combo = QtW.QComboBox()
        self.dls_combo.addItems(DISEASE_STAGES)
        layout.addWidget(self.dls_combo)

        # Example save button
        self.save_btn = QtW.QPushButton("Export YAML (Console)")
        layout.addWidget(self.save_btn)

        layout.addStretch(1)


class MainWindow(QtW.QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("JUNEbug Configurator")
        self.resize(1280, 720)

        # 1. Create Components
        self.config_panel = DiseaseConfigWidget()
        self.graph_widget = graph.NodeGraphWidget()
        self.prop_editor = graph.PropertyEditorWidget()

        # 2. Setup Layout
        splitter = QtW.QSplitter(Qt.Horizontal)

        # Left container (Config + Properties)
        left_widget = QtW.QWidget()
        left_layout = QtW.QVBoxLayout(left_widget)
        left_layout.setContentsMargins(0, 0, 0, 0)
        left_layout.addWidget(self.config_panel)
        left_layout.addWidget(self.prop_editor)

        splitter.addWidget(left_widget)
        splitter.addWidget(self.graph_widget)
        splitter.setSizes([300, 980])

        self.setCentralWidget(splitter)

        # 3. Wire up Signals & Slots
        # Pass graph selection events to the Property Editor
        self.graph_widget.graph.scene().selectionChanged.connect(
            lambda: self.prop_editor.on_selection_changed(self.graph_widget.graph)
        )

        # Pass connection events to Property Editor (to init/delete data)
        self.graph_widget.graph.port_connected.connect(
            self.prop_editor.on_port_connected
        )
        self.graph_widget.graph.port_disconnected.connect(
            self.prop_editor.on_port_disconnected
        )

        # Export Button Logic
        self.config_panel.save_btn.clicked.connect(self.export_data)

    def export_data(self):
        print("--- Exporting Data ---")
        print(f"Disease Name: {self.config_panel.name_entry.text()}")

        # Retrieve graph data
        all_nodes = self.graph_widget.graph.all_nodes()
        print(f"Stages ({len(all_nodes)}):")
        for n in all_nodes:
            print(f" - {n.name()} (Stage: {n.get_property('stage_name')})")

        print("Transitions (Edges):")
        for key, data in self.prop_editor.transition_data.items():
            # key is (from_id, to_id)
            print(f" - {key}: {data}")
        print("----------------------")


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
